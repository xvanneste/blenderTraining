"""Fit the CC0 MakeHuman head to the two character guides in image space."""
import math
import sys
from pathlib import Path

import bmesh
import bpy
import numpy as np
from mathutils import Vector

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_from_views import L, ROOT, UNIT, CENTER_FRONT, CENTER_SIDE, SOLE, crop_panel, guide_image, scan, FRONT, SIDE


def read_template():
    verts, faces = [], []
    group = None
    for line in (ROOT / "makehuman_base_cc0.obj").read_text(encoding="utf-8").splitlines():
        fields = line.split()
        if not fields:
            continue
        if fields[0] == "v":
            verts.append(tuple(float(v) for v in fields[1:4]))
        elif fields[0] == "g":
            group = fields[1]
        elif fields[0] == "f" and group == "body":
            faces.append(tuple(int(v.split("/")[0])-1 for v in fields[1:]))
    verts=np.asarray(verts)
    for line in (ROOT/"makehuman_adulte_cc0.target").read_text(encoding="utf-8").splitlines():
        fields=line.split()
        if len(fields)==4 and fields[0].isdigit():
            verts[int(fields[0])] += tuple(map(float,fields[1:]))
    return verts,faces


def filtered(x,sigma):
    n=math.ceil(sigma*3)
    k=np.exp(-.5*(np.arange(-n,n+1)/sigma)**2)
    return np.convolve(np.pad(x,n,mode="edge"),k/k.sum(),mode="valid")


def fit_template(verts,faces,pixels):
    # Each entry ties a recognizable anatomical level of the template to the
    # common vertical coordinates of the photographed guides.
    frame=np.interp(verts[:,1],
                   [5.7,6.2,6.5,6.85,7.02,7.26,7.51,7.83,8.2,8.44,8.70,9.30],
                   [242,218,199,174,152,142,128,115,93,82,69,42])
    fx=CENTER_FRONT+48*verts[:,0]
    dep=1187-49*verts[:,2]
    base=np.column_stack((fx,dep,frame))
    rows=np.arange(47,155)
    edges=np.asarray(list({tuple(sorted((a,b))) for face in faces if min(frame[list(face)])<190
                           for a,b in zip(face,face[1:]+face[:1])}))
    a=base[edges[:,0]]
    b=base[edges[:,1]]
    dif=b-a
    side_lo=[];side_hi=[];front_width=[]
    for y in rows:
        use=((a[:,2]<=y)&(b[:,2]>y))|((a[:,2]>y)&(b[:,2]<=y))
        sec=a[use]+dif[use]*((y-a[use,2])/dif[use,2])[:,None]
        f=scan(pixels,int(y),320,448)
        s=scan(pixels,int(y),1060,1230)
        target_w=max(abs(f[0][0]-CENTER_FRONT),abs(f[-1][1]-CENTER_FRONT)) if f else 35
        if len(sec)<2 or not s:
            side_lo.append(0);side_hi.append(0);front_width.append(1)
            continue
        lo,hi=float(sec[:,1].min()),float(sec[:,1].max())
        side_lo.append(np.clip(s[0][0]-lo,-17,17))
        side_hi.append(np.clip(s[-1][1]-hi,-15,15))
        front_width.append(np.clip(target_w/max(12,abs(sec[:,0]-CENTER_FRONT).max()),.86,1.24))
    lo=filtered(np.asarray(side_lo),2.2)
    hi=filtered(np.asarray(side_hi),2.8)
    ext=filtered(np.asarray(front_width),3.1)
    # Taper the fit to zero at the shoulder and on the very top ring.
    influence=np.clip((179-frame)/27,0,1)*np.clip((frame-40)/12,0,1)
    edge_mix=np.clip((dep-1106)/98,0,1)
    forward=np.interp(frame,rows,lo)
    rear=np.interp(frame,rows,hi)
    dep+=(forward*(1-edge_mix)+rear*edge_mix)*influence
    fx=CENTER_FRONT+(fx-CENTER_FRONT)*(1+(np.interp(frame,rows,ext)-1)*influence*.83)
    # Widen the orbital separation slightly, following the visible gabarit.
    dx=fx-CENTER_FRONT
    eye_weight=np.exp(-((frame-92)/10)**2)*np.exp(-((abs(dx)-14)/10)**2)*np.clip((1157-dep)/40,0,1)
    fx+=np.sign(dx)*1.7*eye_weight
    world=np.column_stack(((fx-CENTER_FRONT)*UNIT,(dep-CENTER_SIDE)*UNIT,(SOLE-frame)*UNIT))
    return world


def bust_geometry(world,faces):
    # Start with the continuous anatomical topology. Cut the bust below the
    # clavicles and close the section; no separate neck shell is used.
    cap=(SOLE-221)*UNIT
    used=sorted({i for f in faces if max(world[list(f),2]) >= cap-.03 for i in f})
    remap={old:i for i,old in enumerate(used)}
    chosen=[tuple(remap[i] for i in f) for f in faces if all(i in remap for i in f)]
    mesh=bpy.data.meshes.new("Anatomie continue · tête, nuque et épaules")
    mesh.from_pydata(world[used].tolist(),[],chosen)
    mesh.update()
    bm=bmesh.new()
    bm.from_mesh(mesh)
    bmesh.ops.bisect_plane(bm,geom=list(bm.verts)+list(bm.edges)+list(bm.faces),
                          dist=.00001,plane_co=(0,0,cap),plane_no=(0,0,1),clear_inner=True)
    boundary=[e for e in bm.edges if e.is_boundary and all(abs(v.co.z-cap)<.00003 for v in e.verts)]
    if boundary:
        bmesh.ops.holes_fill(bm,edges=boundary,sides=0)
    bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces))
    print("BUST",len(bm.verts),len(bm.faces),sum(not e.is_manifold for e in bm.edges))
    bm.to_mesh(mesh)
    bm.free()
    for p in mesh.polygons:
        p.use_smooth=True
    return mesh


def source_color(mesh,world_source):
    # Vertex colour is stored separately from the geometry. For shallow
    # grazing angles fall back to the most frontal reliable source.
    pixels=world_source
    layer=mesh.color_attributes.new(name="Teinte gabarits",type="FLOAT_COLOR",domain="POINT")
    mesh.update()
    for v in mesh.vertices:
        x,y,z=v.co
        fx=x/UNIT+CENTER_FRONT
        sx=y/UNIT+CENTER_SIDE
        py=SOLE-z/UNIT
        def sample(px):
            return pixels[int(np.clip(round(py),0,1023)),int(np.clip(round(px),0,1535)),:3]
        f,s=sample(fx),sample(sx)
        n=v.normal
        side=(abs(n.x)+max(0,n.y)*1.15)**2
        front=max(0,-n.y)**2
        if f.min()>.82:
            front=0
        if s.min()>.82:
            side=0
        if front+side<.015:
            c=np.array([.65,.43,.31])
        else:
            c=(f*front+s*side)/(front+side)
        c=np.where(c<.04045,c/12.92,((c+.055)/1.055)**2.4)
        layer.data[v.index].color=(*c,1.0)


def camera(studio,name,pos,target,scale):
    ob=L.camera(name,studio,location=pos,make_active=False)
    ob.rotation_euler=(Vector(target)-ob.location).to_track_quat("-Z","Y").to_euler()
    ob.data.type="ORTHO"
    ob.data.ortho_scale=scale
    return ob


def main():
    L.reset("Étude du visage · ajustement aux gabarits")
    model=L.collection("01 · Buste continu")
    refs=L.collection("02 · Gabarits d’origine")
    studio=L.collection("03 · Caméras et éclairage")
    src=bpy.data.images.load(str(ROOT/"planche_source.png"))
    raw=np.empty(1536*1024*4,dtype=np.float32)
    src.pixels.foreach_get(raw)
    px=raw.reshape((1024,1536,4))[::-1]
    for rect,is_side,name in ((FRONT,False,"reference_face"),(SIDE,True,"reference_profil")):
        image=bpy.data.images.load(str(ROOT/(name+".png")))
        image.pack()
        guide_image(image,rect,is_side,refs)
    v,f=read_template()
    world=fit_template(v,f,px)
    mesh=bust_geometry(world,f)
    source_color(mesh,px)
    ob=bpy.data.objects.new("GEO_Buste_Recalé",mesh)
    model.objects.link(ob)
    clay=L.material("Argile neutre",(.29,.34,.38),.54)
    color=L.material("Teinte projetée des deux vues",(.70,.48,.34),.52)
    nt=color.node_tree
    attr=nt.nodes.new("ShaderNodeVertexColor")
    attr.layer_name="Teinte gabarits"
    nt.links.new(attr.outputs["Color"],next(x for x in nt.nodes if x.type=="BSDF_PRINCIPLED").inputs["Base Color"])
    mesh.materials.append(clay)
    mesh.materials.append(color)
    mod=ob.modifiers.new("Subdivision de présentation","SUBSURF")
    mod.levels=1
    mod.render_levels=2
    # The iris and cornea sit separately inside the anatomical lid opening.
    sclera=L.material("Sclérotique",(.79,.76,.68),.24)
    iris=L.material("Iris brun",(.16,.07,.027),.27)
    pupil=L.material("Pupille",(.004,.006,.005),.25)
    for sign in (-1,1):
        x=sign*.0310
        z=(SOLE-93.8)*UNIT
        label="D" if sign<0 else "G"
        eye=L.sphere("Globe "+label,model,sclera,location=(x,-.055,z),segments=40,ring_count=20)
        eye.scale=(.0134,.0178,.0136)
        cornea=L.sphere("Iris "+label,model,iris,location=(x,-.0724,z),segments=32,ring_count=16)
        cornea.scale=(.0044,.0019,.0045)
        pu=L.sphere("Pupille "+label,model,pupil,location=(x,-.0739,z),segments=24,ring_count=12)
        pu.scale=(.0019,.0007,.0021)

    tgt=(0,-.008,(SOLE-110)*UNIT)
    cf=camera(studio,"CAM_Visage_Face",(0,-2.8,tgt[2]),tgt,.325)
    cp=camera(studio,"CAM_Visage_Profil",(2.8,tgt[1],tgt[2]),tgt,.325)
    c3=camera(studio,"CAM_Visage_3_4",(.95,-2.4,tgt[2]+.14),tgt,.325)
    L.world((.17,.20,.24),.54)
    for name,pos,power,size in (
        ("Key",(-.7,-1,2.7),55,1.2),
        ("Fill",(1,-.5,2.15),25,1.1),
        ("Rim",(.35,.85,2.45),38,.9)
    ):
        lamp=L.light(name,studio,location=pos,energy=power,size=size)
        lamp.rotation_euler=(Vector(tgt)-lamp.location).to_track_quat("-Z","Y").to_euler()
    scene=bpy.context.scene
    scene.camera=c3
    scene.render.engine="CYCLES"
    scene.cycles.samples=24
    scene.cycles.use_denoising=True
    scene.render.resolution_x=720
    scene.render.resolution_y=720
    scene.render.resolution_percentage=100
    scene.render.image_settings.file_format="PNG"
    scene.unit_settings.system="METRIC"
    bpy.ops.object.select_all(action="DESELECT")
    ob.select_set(True)
    bpy.context.view_layer.objects.active=ob
    for screen in bpy.data.screens:
        for area in screen.areas:
            if area.type=="VIEW_3D":
                space=area.spaces.active
                space.region_3d.view_perspective="CAMERA"
    note=bpy.data.texts.new("Sources et méthode")
    note.write("Maillage anatomique et morphotype MakeHuman, CC0, commit a8bc2d54ff0ac92e78ff71431b1023eda42bf482. Tête et cou continus. Les proportions sont ajustées en largeur et profondeur à partir des deux guides. La teinte projetée est un mode de comparaison séparé de la forme.")
    scene.render.filepath="//visage_recale_argile.png"
    L.save(str(ROOT/"visage_recale.blend"))
    for cam,path in ((c3,"visage_recale_argile"),(cp,"visage_recale_profil"),(cf,"visage_recale_face")):
        scene.camera=cam
        scene.render.filepath=f"//{path}.png"
        bpy.ops.render.render(write_still=True)
    ob.data.materials[0]=color
    scene.camera=c3
    scene.render.filepath="//visage_recale_projection.png"
    bpy.ops.render.render(write_still=True)


if __name__=="__main__":
    L.run(main)
