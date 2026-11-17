"""Low lace-up shoes for the finished character, saved as a sibling Blender scene."""
import math
import sys
from pathlib import Path

import bpy
from mathutils import Vector
from mathutils.bvhtree import BVHTree

ROOT=Path(__file__).resolve().parent
sys.path[:0]=[str(ROOT),str(ROOT.parents[1]/"SCRIPTS")]
import bcma_lib as L
from refit_boots import mask_values, verify_floor
from build_body_uv_rig import select_only


def smooth(t):
    t=max(0,min(1,t))
    return t*t*(3-2*t)


def fit_hems(body,pants):
    # Regularise the lower trouser leg around the ankle before masking away
    # the underlying anatomical foot.
    for v in pants.data.vertices:
        x,y,z=v.co
        if z<.207 and abs(x)>.04:
            strength=1-smooth((z-.086)/.121)
            c=math.copysign(.132,x)
            v.co.x+=(c+.045*math.tanh((x-c)/.043)-x)*strength
            v.co.y+=(.010+.059*math.tanh((y-.010)/.055)-y)*strength
    pants.data.update()
    mask_values(pants,"Coupe textile",lambda p:min(1.072-p.z,p.z-(.087-.018*smooth((p.y+.010)/.070)),.216-abs(p.x)),.022)
    mask_values(body,"Masquer le pied sous la botte",lambda p:p.z-.230,.029)


def mesh_object(name,col,v,f,mats):
    mesh=bpy.data.meshes.new(name)
    mesh.from_pydata(v,[],f)
    mesh.update()
    ob=bpy.data.objects.new(name,mesh)
    col.objects.link(ob)
    for m in mats:
        mesh.materials.append(m)
    for p in mesh.polygons:
        p.use_smooth=True
    return ob


def foot_bind(ob,rig,side):
    ob.parent=rig
    group=ob.vertex_groups.new(name="foot."+side)
    group.add(list(range(len(ob.data.vertices))),1.0,"REPLACE")
    mod=ob.modifiers.new("Suivi du pied","ARMATURE")
    mod.object=rig
    mod.use_deform_preserve_volume=True


def shoe_geometry(col,rig,sign,mats):
    # z, toe, heel, forefoot width, heel width, centre of the heel
    rings=[
        (0,-.171,.076,.047,.035,.128),
        (0,-.177,.082,.050,.037,.129),
        (.003,-.180,.084,.052,.038,.129),
        (.010,-.181,.085,.052,.038,.129),
        (.014,-.180,.085,.051,.038,.129),
        (.017,-.177,.084,.050,.037,.129),
        (.020,-.175,.083,.049,.037,.129),
        (.027,-.170,.082,.049,.037,.129),
        (.040,-.156,.080,.047,.036,.129),
        (.054,-.129,.078,.043,.037,.132),
        (.066,-.105,.075,.040,.037,.134),
        (.077,-.081,.074,.039,.037,.135),
        (.085,-.064,.073,.038,.037,.135),
        (.091,-.051,.069,.037,.036,.135),
        (.092,-.048,.067,.036,.035,.135),
        (.091,-.042,.063,.033,.032,.135),
        (.086,-.039,.060,.032,.031,.135),
        (.067,-.037,.057,.031,.030,.135),
        (.063,-.036,.056,.030,.029,.135),
    ]
    count=64
    verts=[]
    for z,toe,heel,ball,back,center in rings:
        for k in range(count):
            a=math.tau*k/count
            c,s=math.cos(a),math.sin(a)
            power=2/(2.8 if z<.056 else 2.34)
            y=(toe+heel)*.5+(heel-toe)*.5*math.copysign(abs(s)**power,s)
            fore=smooth((.051-y)/.183)
            width=back+(ball-back)*fore
            medial=-.007*smooth((-y-.058)/.11) if z<.067 else 0
            x=sign*(center+medial+width*math.copysign(abs(c)**power,c))
            tip_lift=.004*smooth((-y-.152)/.027)*(1-smooth(z/.045))
            # The tongue climbs over the front of the foot. The rear collar
            # is lower and the open mouth wraps under the trousers.
            front_raise=.012*smooth((-y-.018)/.036)*smooth((z-.05)/.04)
            verts.append((x,y,z+tip_lift+front_raise))
    f=[]
    for i in range(len(rings)-1):
        for j in range(count):
            k=(j+1)%count
            p=(i*count+j,i*count+k,(i+1)*count+k,(i+1)*count+j)
            f.append(p if sign>0 else tuple(reversed(p)))
    caps=(tuple(reversed(range(count))),tuple(range(len(verts)-count,len(verts))))
    f.extend(caps if sign>0 else tuple(tuple(reversed(c)) for c in caps))
    side="L" if sign>0 else "R"
    ob=mesh_object("Chaussure."+side,col,verts,f,mats)
    data=ob.data
    uv=data.uv_layers.new(name="UV_Chaussure")
    for poly in data.polygons:
        strip=poly.index//count
        if poly.index==len(data.polygons)-2 or strip<3:
            poly.material_index=1
        elif strip in (3,4,5):
            poly.material_index=2
        elif strip>=14:
            poly.material_index=3
        for li in poly.loop_indices:
            vi=data.loops[li].vertex_index
            ring,k=divmod(vi,count)
            if poly.index>=len(data.polygons)-2:
                x,y,z=verts[vi]
                u=.24+.35*(x-sign*.129)/.125
                v=(.16 if poly.index==len(data.polygons)-2 else .46)+.24*(y+.049)/.275
            else:
                u=(k if k or poly.index%count<count-1 else count)/count
                v=.62+.36*ring/(len(rings)-1)
            uv.data[li].uv=(u,v)
    foot_bind(ob,rig,side)
    mod=ob.modifiers.new("Arrondis de la chaussure","SUBSURF")
    mod.levels=mod.render_levels=2
    return ob


def laces_and_stitches(shoe,col,rig,sign,lace,thread):
    tree=BVHTree.FromObject(shoe,bpy.context.evaluated_depsgraph_get())
    side="L" if sign>0 else "R"
    c=sign*.130
    vertices=[]; faces=[]
    def surface(x,y):
        p,n,_,_=tree.ray_cast(Vector((x,y,.285)),Vector((0,0,-1)),.30)
        if p is None:
            raise RuntimeError(f"Lacet sans support à {(x,y)}")
        return p,n
    def pipe(path,r):
        start=len(vertices)
        for i,(p,normal) in enumerate(path):
            d=(path[min(i+1,len(path)-1)][0]-path[max(i-1,0)][0]).normalized()
            a=d.cross(normal).normalized()
            b=a.cross(d).normalized()
            for k in range(8):
                ang=math.tau*k/8
                vertices.append(tuple(p+r*(a*math.cos(ang)+b*math.sin(ang))))
        for i in range(len(path)-1):
            for k in range(8):
                n=(k+1)%8
                faces.append((start+i*8+k,start+i*8+n,start+(i+1)*8+n,start+(i+1)*8+k))
    for i in range(4):
        y=-.126+.015*i
        start=c-.014
        end=c+.014
        if i%2:
            start,end=end,start
        path=[]
        for k in range(13):
            t=k/12
            p,n=surface(start+(end-start)*t,y+.009*t)
            lift=.0015+.0018*math.sin(math.pi*t)
            path.append((p+n*lift,n))
        pipe(path,.00105)
    lace_obj=mesh_object("Lacets."+side,col,vertices,faces,[lace])
    foot_bind(lace_obj,rig,side)

    vertices.clear(); faces.clear()
    for s in (-1,1):
        path=[]
        for t in range(22):
            k=t/21
            y=-.142+.083*k
            x=c+s*(.027+.004*math.sin(math.pi*k))
            p,n=surface(x,y)
            path.append((p+n*.00034,n))
        pipe(path,.00048)
    stitch=mesh_object("Surpiqûres."+side,col,vertices,faces,[thread])
    foot_bind(stitch,rig,side)


def main():
    bpy.ops.wm.open_mainfile(filepath=str(ROOT/"personnage_final.blend"))
    scene=bpy.context.scene
    scene.frame_set(1)
    rig=bpy.data.objects["RIG_Personnage_FK"]
    pants=bpy.data.objects["Pantalon droit"]
    body=bpy.data.objects["GEO_Personnage"]
    rig["Pieds IK"]=0.0
    rig.update_tag()
    geo=pants.users_collection[0]
    for name in ("Botte.L","Botte.R","Finitions · Pantalon droit"):
        ob=bpy.data.objects.get(name)
        if ob:
            bpy.data.objects.remove(ob,do_unlink=True)
    fit_hems(body,pants)
    canvas=L.material("Chaussures · toile charbon",(.039,.047,.052),.65)
    tread=L.material("Chaussures · gomme",(.027,.029,.032),.81)
    stripe=L.material("Chaussures · tranche gris chaud",(.41,.365,.31),.74)
    inside=L.material("Chaussures · doublure textile",(.020,.023,.027),.82)
    lace=L.material("Chaussures · lacets tissés",(.30,.29,.26),.74)
    thread=L.material("Chaussures · fil ton sur ton",(.072,.079,.084),.72)
    shoes=[]
    for sign in (-1,1):
        sh=shoe_geometry(geo,rig,sign,(canvas,tread,stripe,inside))
        bpy.context.view_layer.update()
        laces_and_stitches(sh,geo,rig,sign,lace,thread)
        shoes.append(sh)
    print("CONTACT",verify_floor(scene,shoes))
    scene.camera=bpy.data.objects["CAM_Trois_Quarts"]
    cam=bpy.data.objects["CAM_Détail_Bottes"]
    cam.name="CAM_Détail_Chaussures"
    cam.location=(.83,-1.39,.407)
    cam.rotation_euler=(Vector((0,-.020,.112))-cam.location).to_track_quat("-Z","Y").to_euler()
    cam.data.ortho_scale=.62
    scene.render.filepath="//personnage_chaussures.png"
    select_only(rig)
    note=bpy.data.texts.new("LIRE · Chaussures basses")
    note.write("Chaussures basses à lacets, semelles plates et cartes UV propres. Les ourlets sont allongés et le corps est masqué sous le chaussant. Les chaussures, lacets et surpiqûres suivent les os des pieds. L’appui des pieds porteurs a été contrôlé aux clés FK d’origine.")
    L.save(str(ROOT/"personnage_final_chaussures.blend"))
    bpy.ops.render.render(write_still=True)
    scene.camera=cam
    scene.render.resolution_x=950
    scene.render.resolution_y=650
    scene.render.filepath="//chaussures_detail.png"
    bpy.ops.render.render(write_still=True)
    scene.frame_set(25)
    scene.render.filepath="//chaussures_appui.png"
    bpy.ops.render.render(write_still=True)


if __name__=="__main__":
    L.run(main)
