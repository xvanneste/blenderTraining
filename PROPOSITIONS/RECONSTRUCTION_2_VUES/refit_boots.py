"""Refit the boot geometry, trouser hems and ankle deformation in a sibling blend."""
import math
import sys
from pathlib import Path

import bpy
from mathutils import Vector

ROOT = Path(__file__).resolve().parent
sys.path[:0] = [str(ROOT), str(ROOT.parents[1] / "SCRIPTS")]
import bcma_lib as L


def mask_values(obj, name, value, span):
    group=obj.vertex_groups[name]
    group.remove(list(range(len(obj.data.vertices))))
    for v in obj.data.vertices:
        w=max(0,min(1,.5+value(v.co)/span))
        if w:
            group.add([v.index],w,"REPLACE")


def make_boot(rig, collection, sign, materials):
    # z, toe, heel, ball width, heel width, centre x
    sections=[
        (0.000,-.173,.083,.058,.042,.127),
        (0.000,-.178,.087,.060,.043,.128),
        (.005,-.182,.091,.062,.044,.129),
        (.014,-.182,.091,.062,.044,.129),
        (.020,-.180,.090,.061,.043,.129),
        (.024,-.177,.088,.060,.042,.129),
        (.030,-.174,.086,.058,.041,.129),
        (.042,-.166,.084,.056,.041,.129),
        (.062,-.146,.082,.055,.040,.130),
        (.082,-.113,.080,.053,.041,.133),
        (.106,-.092,.079,.049,.042,.133),
        (.130,-.085,.078,.046,.045,.135),
        (.151,-.078,.077,.046,.046,.135),
        (.180,-.073,.076,.045,.045,.135),
        (.202,-.070,.074,.045,.044,.135),
        (.206,-.069,.073,.044,.043,.135),
        (.206,-.066,.070,.042,.041,.135),
        (.205,-.060,.064,.038,.037,.135),
        (.200,-.057,.062,.036,.035,.135),
        (.184,-.056,.061,.036,.035,.135),
        (.177,-.054,.059,.035,.035,.135),
    ]
    around=48
    verts=[]
    for z,toe,heel,ball,back,center in sections:
        for k in range(around):
            a=math.tau*k/around
            c,s=math.cos(a),math.sin(a)
            power=2/(3.25 if z<.075 else 2.65)
            y=(toe+heel)*.5+(heel-toe)*.5*math.copysign(abs(s)**power,s)
            toe_bias=max(0,min(1,(.045-y)/.16))
            w=back+(ball-back)*toe_bias
            # Modest medial toe asymmetry and a rounded heel.
            camp=(-.006*max(0,min(1,(-y-.045)/.12))) if z<.09 else 0
            x=sign*(center+camp+w*math.copysign(abs(c)**power,c))
            verts.append((x,y,z))
    faces=[]
    for i in range(len(sections)-1):
        for k in range(around):
            j=(k+1)%around
            f=(i*around+k,i*around+j,(i+1)*around+j,(i+1)*around+k)
            faces.append(f if sign>0 else tuple(reversed(f)))
    bottom=tuple(reversed(range(around)))
    top=tuple(range(len(verts)-around,len(verts)))
    faces.extend((bottom,top) if sign>0 else (tuple(reversed(bottom)),tuple(reversed(top))))
    side="L" if sign>0 else "R"
    data=bpy.data.meshes.new("Botte · semelle plate et tige raccordée."+side)
    data.from_pydata(verts,[],faces)
    data.update()
    boot=bpy.data.objects.new("Botte."+side,data)
    collection.objects.link(boot)
    for material in materials:
        data.materials.append(material)
    uv=data.uv_layers.new(name="UV_Botte")
    for poly in data.polygons:
        poly.use_smooth=True
        strip=poly.index//around
        if poly.index==len(data.polygons)-2:
            poly.material_index=1
        elif strip>=len(sections)-5:
            poly.material_index=3
        elif strip<4:
            poly.material_index=1
        elif strip in (4,5):
            poly.material_index=2
        elif 10<=strip<=14 and (poly.index%around in range(2,7) or poly.index%around in range(22,27)):
            poly.material_index=3
        for loop in poly.loop_indices:
            i=data.loops[loop].vertex_index
            ring,k=divmod(i,around)
            if poly.index>=len(data.polygons)-2:
                x,y,z=verts[i]
                u=(x-sign*.13)/.145*.40+.24
                v=(y+.05)/.29*.23+(.19 if poly.index==len(data.polygons)-2 else .48)
            else:
                u=(k if k else (around if poly.index%around==around-1 else 0))/around
                v=.62+.365*ring/(len(sections)-1)
            uv.data[loop].uv=(u,v)
    boot.parent=rig
    foot=boot.vertex_groups.new(name="foot."+side)
    shin=boot.vertex_groups.new(name="lowerleg02."+side)
    for v in data.vertices:
        w=max(0,min(1,(v.co.z-.102)/.095))
        w=w*w*(3-2*w)*.88
        if w:
            shin.add([v.index],w,"REPLACE")
        foot.add([v.index],1-w,"REPLACE")
    arm=boot.modifiers.new("Déformation pied et cheville","ARMATURE")
    arm.object=rig
    arm.use_deform_preserve_volume=True
    sub=boot.modifiers.new("Arrondis du cuir et de la semelle","SUBSURF")
    sub.levels=sub.render_levels=2
    return boot


def verify_floor(scene,boots):
    # At the authored poses the rig was kept unchanged. The support boot
    # should keep a flat sole while the opposite leg is lifted.
    report={}
    for frame,planted in ((1,boots),(25,[boots[1]]),(49,[boots[0]]),(73,boots)):
        scene.frame_set(frame)
        dg=bpy.context.evaluated_depsgraph_get()
        for ob in planted:
            eo=ob.evaluated_get(dg)
            z=[(eo.matrix_world@v.co).z for v in eo.data.vertices]
            low=min(z)
            close=sum(abs(v)<.001 for v in z)
            assert abs(low)<.001 and close>30,(frame,ob.name,low,close)
            report[f"{frame} / {ob.name}"]={"minimum_z_mm":round(low*1000,3),"sommets_au_sol":close}
    scene.frame_set(1)
    return report


def main():
    bpy.ops.wm.open_mainfile(filepath=str(ROOT/"personnage_corps_uv_rig.blend"))
    scene=bpy.context.scene
    rig=bpy.data.objects["RIG_Personnage_FK"]
    pants=bpy.data.objects["Pantalon droit"]
    body=bpy.data.objects["GEO_Personnage"]
    collection=pants.users_collection[0]
    # Replace only the boot objects in the copied file.
    for name in ("Botte.L","Botte.R"):
        bpy.data.objects.remove(bpy.data.objects[name],do_unlink=True)
    mask_values(pants,"Coupe textile",lambda p:min(1.058-p.z,p.z-.178,.216-abs(p.x)),.022)
    mask_values(body,"Masquer le pied sous la botte",lambda p:p.z-.183,.035)
    leather=L.material("Cuir de la tige",(.052,.064,.080),.57)
    rubber=L.material("Semelle plate · gomme",(.021,.025,.030),.73)
    welt=L.material("Trépointe",(.090,.083,.072),.66)
    knit=L.material("Panneau souple de cheville",(.032,.043,.056),.82)
    boots=[make_boot(rig,collection,s,(leather,rubber,welt,knit)) for s in (-1,1)]
    report=verify_floor(scene,boots)
    print("APPUI",report)
    note=bpy.data.texts.new("LIRE · Bottes V2")
    note.write("Bottes refaites avec semelles plates, tiges et panneaux latéraux. Chaque botte a ses UV et partage ses poids entre pied et bas de jambe. Les ourlets remontent au-dessus de la tige. Appui contrôlé aux images 1, 25, 49 et 73 sur les pieds porteurs. L’armature reste FK.")
    studio=bpy.data.objects["CAM_Trois_Quarts"].users_collection[0]
    cam=L.camera("CAM_Détail_Bottes",studio,location=(.92,-1.55,.46),make_active=False)
    cam.rotation_euler=(Vector((0,-.026,.152))-cam.location).to_track_quat("-Z","Y").to_euler()
    cam.data.type="ORTHO"
    cam.data.ortho_scale=.65
    scene.camera=bpy.data.objects["CAM_Trois_Quarts"]
    scene.render.filepath="//personnage_pieds_v2.png"
    L.save(str(ROOT/"personnage_corps_uv_rig_pieds.blend"))
    bpy.ops.render.render(write_still=True)
    scene.camera=cam
    scene.render.resolution_x=950
    scene.render.resolution_y=670
    scene.render.filepath="//bottes_v2_detail.png"
    bpy.ops.render.render(write_still=True)
    scene.frame_set(25)
    scene.render.filepath="//bottes_v2_appui.png"
    bpy.ops.render.render(write_still=True)


if __name__=="__main__":
    L.run(main)
