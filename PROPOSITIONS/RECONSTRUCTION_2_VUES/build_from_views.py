"""Build a connected quad surface from front and side image scanlines."""
import json
import math
import sys
from pathlib import Path
from collections import defaultdict

import bpy
import numpy as np
from mathutils import Vector

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT.parents[1] / "SCRIPTS"))
import bcma_lib as L

CENTER_FRONT = 383.5
CENTER_SIDE = 1151.0
CROWN = 42.0
SOLE = 962.5
UNIT = 1.82 / (SOLE - CROWN)
STEP = 4.5
FRONT = (10, 760, 26, 982)
SIDE = (778, 1526, 26, 982)


def crop_panel(image, pixels, name, rect):
    left, right, top, bottom = rect
    cropped = pixels[top:bottom, left:right, :]
    panel = bpy.data.images.new(name, width=right-left, height=bottom-top, alpha=False)
    panel.pixels.foreach_set(np.ascontiguousarray(cropped[::-1]).reshape(-1))
    panel.filepath_raw = str(ROOT / f"{name}.png")
    panel.file_format = "PNG"
    panel.save()
    panel.pack()
    return panel


def scan(pixels, px, left, right):
    y = int(round(px))
    row = pixels[y, left:right, :3]
    # Source has a light seamless backdrop and a dark, high-contrast figure.
    mask = row.min(axis=1) < .82
    changes = np.flatnonzero(np.diff(np.r_[False,mask,False]))
    return [(int(a+left),int(b+left-1)) for a,b in zip(changes[::2],changes[1::2]) if b-a>=5]


def interp(y, knots):
    return float(np.interp(y, [k[0] for k in knots], [k[1] for k in knots]))


def sampled_volume(pixels):
    xs=np.arange(173,595,STEP)
    ds=np.arange(1047,1241,STEP)
    zs=np.arange(975,30,-STEP)
    X,D=np.meshgrid(xs,ds,indexing="ij")
    field=np.full((len(xs),len(ds),len(zs)),-1.6,dtype=np.float32)
    torso_half=[(190,48),(222,80),(255,83),(286,83),(325,72),(370,58),(410,62),(441,70)]
    arm_depth=[(232,1176),(280,1178),(318,1176),(355,1174),(391,1165),
               (430,1164),(470,1152),(500,1142),(548,1141),(587,1144)]
    arm_radius=[(230,36),(275,34),(310,28),(356,22),(386,23),(423,19),
                (472,15),(500,21),(545,18),(585,11)]
    for i, row in enumerate(zs):
        front=scan(pixels,row,158,608)
        side=scan(pixels,row,1038,1251)
        if not front or not side:
            continue
        if row<193:
            front=[(front[0][0],front[-1][1])]
        low=min(x[0] for x in side)-1.5
        high=max(x[1] for x in side)+1.5
        if high-low<7:
            high=low+7
        cyc=(low+high)*.5
        broad=(high-low)*.5
        for min_x,max_x in front:
            mid=(min_x+max_x)*.5
            wide=max((max_x-min_x)*.5+1.8,3.2)
            if 215<row<320 and min_x<CENTER_FRONT<max_x:
                # A single connected silhouette row at the shoulder contains central
                # chest plus two upper arms. The side silhouette alone blends them.
                f_width=min(wide,interp(row,torso_half))
                xnorm=(X-CENTER_FRONT)/f_width
                region=1-np.sqrt(abs(xnorm)**2.25+abs((D-cyc)/broad)**2.0)
                outer=wide-f_width
                if outer>2:
                    arm_x=(f_width+wide)/2-5
                    aw=max(outer/2+13,16)
                    for sign in (-1,1):
                        ud=(X-(CENTER_FRONT+sign*arm_x))/aw
                        dd=(D-interp(row,arm_depth))/interp(row,arm_radius)
                        region=np.maximum(region,1-np.sqrt(ud*ud+dd*dd))
                    region=np.minimum(region,(wide-np.abs(X-CENTER_FRONT))/12)
            elif 290<row<592 and abs(mid-CENTER_FRONT)>87:
                rad=min(broad,interp(row,arm_radius))
                cd=interp(row,arm_depth)
                region=1-np.sqrt(((X-mid)/wide)**2+((D-cd)/rad)**2)
            else:
                ux=(X-mid)/wide
                if 78<row<149:
                    # The nose and lips determine the profile extreme on the
                    # mid-sagittal line; the cheeks curve back off that line.
                    tip=12*math.exp(-((row-111)/13)**2)+4*math.exp(-((row-128)/7)**2)
                    socket=8*math.exp(-((row-92)/8)**2)*np.exp(-((abs(ux)-.43)/.24)**2)
                    front_y=low+tip*(1-np.exp(-(ux/.32)**2))+socket
                    depth=((high-front_y)*.5)
                    middle=(high+front_y)*.5
                    region=1-np.sqrt(abs(ux)**2.1+abs((D-middle)/depth)**2)
                else:
                    power=3.3 if row>880 else 2.20
                    region=1-np.sqrt(abs(ux)**power+abs((D-cyc)/broad)**power)
            field[:,:,i]=np.maximum(field[:,:,i],np.clip(region,-1.6,1.0))

    # Soften scanline discontinuities conservatively around shoulders and crotch.
    for _ in range(5):
        f=field.copy()
        f[1:-1,1:-1,1:-1]=(
            .49*field[1:-1,1:-1,1:-1]+(.51/6)*(
                field[:-2,1:-1,1:-1]+field[2:,1:-1,1:-1]+
                field[1:-1,:-2,1:-1]+field[1:-1,2:,1:-1]+
                field[1:-1,1:-1,:-2]+field[1:-1,1:-1,2:]
            )
        )
        field=f
    return xs,ds,zs,field


def surface_net(xs,ds,zs,f):
    inside=f>0
    corners=[(a,b,c) for a in (0,1) for b in (0,1) for c in (0,1)]
    edges=[(p,q) for p in corners for q in corners if sum(x!=y for x,y in zip(p,q))==1 and p<q]
    sides=[inside[a:a+f.shape[0]-1,b:b+f.shape[1]-1,c:c+f.shape[2]-1] for a,b,c in corners]
    mixed=np.any(sides,axis=0)&~np.all(sides,axis=0)
    verts=[]
    index=np.full(mixed.shape,-1,dtype=np.int32)
    for i,j,k in np.argwhere(mixed):
        coord=np.array([i,j,k])
        cross=[]
        for p,q in edges:
            ip=tuple(coord+p); iq=tuple(coord+q)
            a=float(f[ip]); b=float(f[iq])
            if (a>0)==(b>0):
                continue
            cross.append(np.array(p)+(np.array(q)-p)*(a/(a-b)))
        x,y,z=coord+np.mean(cross,axis=0)
        index[i,j,k]=len(verts)
        verts.append(((xs[0]+x*STEP-CENTER_FRONT)*UNIT,
                      (ds[0]+y*STEP-CENTER_SIDE)*UNIT,
                      (SOLE-zs[0]+z*STEP)*UNIT))
    faces=[]
    for axis in range(3):
        aa=np.take(inside,range(inside.shape[axis]-1),axis=axis)
        bb=np.take(inside,range(1,inside.shape[axis]),axis=axis)
        other=[i for i in range(3) if i!=axis]
        a,b=other
        for p in np.argwhere(aa!=bb):
            adj=[]
            for u,v in ((0,0),(-1,0),(-1,-1),(0,-1)):
                q=p.copy()
                q[a]+=u; q[b]+=v
                if min(q)<0 or any(q[d]>=index.shape[d] for d in range(3)):
                    break
                adj.append(int(index[tuple(q)]))
            if len(adj)==4 and min(adj)>=0:
                # Axis 1 reverses the cyclic orientation of the other axes.
                if bool(aa[tuple(p)]) != (axis!=1):
                    adj.reverse()
                faces.append(adj)

    # Keep the largest shell if an anti-aliased pixel creates its own island.
    parent=list(range(len(verts)))
    def find(i):
        while parent[i]!=i:
            parent[i]=parent[parent[i]]
            i=parent[i]
        return i
    for face in faces:
        for v in face[1:]:
            parent[find(v)]=find(face[0])
    parts=defaultdict(list)
    for i in range(len(verts)):
        parts[find(i)].append(i)
    keep=max(parts.values(),key=len)
    indexes={j:i for i,j in enumerate(keep)}
    return [verts[i] for i in keep], [[indexes[v] for v in face] for face in faces if face[0] in indexes]


def guide_image(image, rect, is_side, collection):
    left,right,top,bottom=rect
    ob=bpy.data.objects.new("Référence profil" if is_side else "Référence face",None)
    collection.objects.link(ob)
    ob.empty_display_type="IMAGE"
    ob.data=image
    ob.empty_display_size=(bottom-top)*UNIT
    offset_x=((left+right)/2-(CENTER_SIDE if is_side else CENTER_FRONT))*UNIT
    ob.location=(.53,offset_x,(SOLE-(top+bottom)/2)*UNIT) if is_side else (offset_x,.46,(SOLE-(top+bottom)/2)*UNIT)
    ob.rotation_euler=(math.pi/2,0,math.pi/2 if is_side else 0)
    ob.empty_image_depth="BACK"
    ob.show_empty_image_perspective=False
    ob.show_empty_image_only_axis_aligned=True
    ob.use_empty_image_alpha=True
    ob.color[3]=.72
    ob.hide_render=True


LANDMARKS=[
    # name, front x, common scanline y, profile x
    ("Sommet du crâne",384,42,1161),("Arête du nez",383,104,1107),
    ("Pointe du nez",383,115,1095),("Milieu de la bouche",384,128,1104),
    ("Menton",383,152,1113),("Creux de gorge",383,172,1136),
    ("Oreille D",348,104,1173),("Oreille G",420,104,1173),
    ("Épaule D",278,216,1183),("Épaule G",488,216,1183),
    ("Coude D",249,350,1181),("Coude G",519,350,1181),
    ("Poignet D",211,476,1148),("Poignet G",556,476,1148),
    ("Bout du majeur D",201,583,1142),("Bout du majeur G",565,583,1142),
    ("Entrejambe",383,508,1149),("Genou D",329,685,1155),
    ("Genou G",439,685,1155),("Cheville D",321,884,1160),("Cheville G",447,884,1160),
    ("Pointe chaussure D",317,950,1066),("Pointe chaussure G",449,950,1066),
    ("Semelle D",318,961,1120),("Semelle G",448,961,1120),
]


def marker_data(ob, verts, collection):
    vv=np.asarray(verts)
    info=[]
    guide=[]
    for name,x,v,d in LANDMARKS:
        world=np.array([(x-CENTER_FRONT)*UNIT,(d-CENTER_SIDE)*UNIT,(SOLE-v)*UNIT])
        j=int(np.argmin(np.sum((vv-world)**2,axis=1)))
        vg=ob.vertex_groups.new(name=name)
        vg.add([j],1.0,"REPLACE")
        guide.append(tuple(world))
        vx,vd,vz=vv[j]
        info.append({
            "repere":name,"face_px":[x,v],"profil_px":[d,v],
            "position_m":[round(float(c),5) for c in world],
            "sommet":j,"ecart_mm":round(float(np.linalg.norm(vv[j]-world))*1000,1),
            "projection_face_px":[round(float(vx/UNIT+CENTER_FRONT),1),round(float(SOLE-vz/UNIT),1)],
            "projection_profil_px":[round(float(vd/UNIT+CENTER_SIDE),1),round(float(SOLE-vz/UNIT),1)]
        })
    m=bpy.data.meshes.new("25 points par correspondance")
    m.from_pydata(guide,[],[])
    g=bpy.data.objects.new("Cage · points tracés sur les deux images",m)
    collection.objects.link(g)
    g.show_in_front=True
    g.hide_set(True)
    for i,landmark in enumerate(LANDMARKS):
        g.vertex_groups.new(name=landmark[0]).add([i],1.0,"REPLACE")
    (ROOT/"correspondances.json").write_text(json.dumps({
        "image":"planche_source.png",
        "origine_px":{"face_x":CENTER_FRONT,"profil_x":CENTER_SIDE,"sol_y":SOLE},
        "metres_par_pixel":UNIT,"reperes":info
    },ensure_ascii=False,indent=2)+"\n",encoding="utf-8")


def main():
    L.reset("Reconstruction · face et profil")
    model=L.collection("01 · Surface reconstruite")
    refs=L.collection("02 · Références orthographiques")
    pts=L.collection("03 · Correspondances exactes")
    studio=L.collection("04 · Présentation")
    src=bpy.data.images.load(str(ROOT/"planche_source.png"))
    w,h=src.size
    assert (w,h)==(1536,1024),(w,h)
    raw=np.empty(w*h*4,dtype=np.float32)
    src.pixels.foreach_get(raw)
    pixels=raw.reshape((h,w,4))[::-1]
    f=crop_panel(src,pixels,"reference_face",FRONT)
    s=crop_panel(src,pixels,"reference_profil",SIDE)
    guide_image(f,FRONT,False,refs)
    guide_image(s,SIDE,True,refs)
    verts,faces=surface_net(*sampled_volume(pixels))
    data=bpy.data.meshes.new("Surface de silhouettes · quads")
    data.from_pydata(verts,[],faces)
    data.update()
    ob=bpy.data.objects.new("GEO_Personnage_Deux_Vues",data)
    model.objects.link(ob)
    neutral=L.material("Argile grise",(0.31,.355,.385),.57)
    data.materials.append(neutral)
    for p in data.polygons:
        p.use_smooth=True
    marker_data(ob,verts,pts)
    for name,pos in (("CAM_Face",(0,-4,.91)),("CAM_Profil",(4,0,.91)),("CAM_Revue",(2.9,-5.4,2.20))):
        cam=L.camera(name,studio,location=pos,make_active=name=="CAM_Revue")
        cam.rotation_euler=(Vector((0,0,.91))-cam.location).to_track_quat("-Z","Y").to_euler()
        cam.data.type="ORTHO"
        cam.data.ortho_scale=2.17
    L.world((.18,.22,.28),.42)
    for name,loc,power,size in (("Key",(-2.7,-3.2,4.6),515,3.0),
                                ("Fill",(2.5,-1.2,2.4),155,2.7),
                                ("Rim",(1.7,2.2,3.5),490,2.5)):
        lamp=L.light(name,studio,location=loc,energy=power,size=size)
        lamp.rotation_euler=(Vector((0,0,.95))-lamp.location).to_track_quat("-Z","Y").to_euler()
    floor=L.plane("Fond",studio,L.material("Fond ardoise",(.075,.115,.16),.7),size=200)
    floor.location.z=-.008
    scene=bpy.context.scene
    scene.unit_settings.system="METRIC"
    scene.render.engine="CYCLES"
    scene.cycles.samples=24
    scene.cycles.use_denoising=True
    scene.render.resolution_x=780
    scene.render.resolution_y=1050
    scene.render.resolution_percentage=100
    scene.render.image_settings.file_format="PNG"
    scene.render.filepath="//maillage_trois_quarts.png"
    bpy.ops.object.select_all(action="DESELECT")
    ob.select_set(True)
    bpy.context.view_layer.objects.active=ob
    for screen in bpy.data.screens:
        for area in screen.areas:
            if area.type=="VIEW_3D":
                space=area.spaces.active
                space.region_3d.view_perspective="ORTHO"
                space.region_3d.view_distance=2.65
                space.region_3d.view_location=(0,0,.91)
                space.region_3d.view_rotation=scene.camera.rotation_euler.to_quaternion()
    note=bpy.data.texts.new("LIRE · Correspondances")
    note.write("Num 1 : face. Num 3 : profil. Les références sont emballées. Masquer le studio dans la vue si le fond gêne. GEO contient 25 groupes, chacun repère le sommet le plus proche du point tracé. La cage de points exacte reste dans la collection 03 : activez-la dans l’Outliner, puis Tab. Le fichier JSON documente les coordonnées et les écarts.")
    L.save(str(ROOT/"personnage_deux_vues.blend"))
    print(f"RECONSTRUCTION {len(verts)} sommets / {len(faces)} faces / {len(LANDMARKS)} repères")
    bpy.ops.render.render(write_still=True)


if __name__=="__main__":
    L.run(main)
