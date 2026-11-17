"""Build a connected, deliberately simple human cage and a practice armature."""
import math
import sys
from pathlib import Path

import bmesh
import bpy
from mathutils import Vector

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_assets import HERE, L, mesh

def body():
    v, faces = [], []
    loop = [(1,-.55),(1,.55),(.57,1),(0,1),(-.57,1),
            (-1,.55),(-1,-.55),(-.57,-1),(0,-1),(.57,-1)]
    stages = ((.87,.162,.094,.012),(.97,.172,.098,.012),(1.08,.142,.080,.016),
              (1.24,.173,.101,.007),(1.35,.197,.096,.000),(1.44,.181,.083,.009),
              (1.48,.084,.066,.018),(1.52,.059,.053,.016),(1.60,.058,.053,.010),
              (1.63,.081,.075,-.006),(1.71,.098,.083,-.001),(1.79,.086,.080,.010),
              (1.83,.042,.051,.012))
    n=len(loop)
    for z,w,d,yc in stages:
        v.extend((w*x,yc+d*y,z) for x,y in loop)
    for i in range(len(stages)-1):
        for j in range(n):
            # The open shoulder faces are replaced by arm transitions.
            if i==4 and j in (0,5):
                continue
            p=(j+1)%n
            faces.append((i*n+j,i*n+p,(i+1)*n+p,(i+1)*n+j))
    faces.append(tuple(range((len(stages)-1)*n,len(v))))

    def extend(prev, positions):
        ring=list(range(len(v),len(v)+len(positions)))
        v.extend(positions)
        for i in range(len(ring)):
            j=(i+1)%len(ring)
            faces.append((prev[i],prev[j],ring[j],ring[i]))
        return ring

    for side in (-1,1):
        j=0 if side>0 else 5
        prev=[4*n+j,4*n+j+1,5*n+j+1,5*n+j]
        for x,z,w,depth,yc in ((.228,1.365,.071,.066,.001),(.303,1.298,.056,.054,-.002),
                               (.367,1.239,.043,.042,-.004),(.394,1.218,.041,.042,-.012),
                               (.416,1.199,.043,.042,-.019),(.471,1.142,.035,.036,-.026),
                               (.489,1.122,.029,.032,-.034),(.527,1.083,.035,.037,-.036),
                               (.553,1.058,.030,.030,-.039)):
            prev=extend(prev,[(side*(x+t*w*.46),yc+s*depth,z+t*w*.83)
                              for s,t in ((-side,-1),(side,-1),(side,1),(-side,1))])
        faces.append(tuple(prev))
        prev=[8,9,0,1,2,3] if side>0 else [3,4,5,6,7,8]
        for z,x,w,d,yc in ((.79,.105,.073,.087,.008),(.66,.109,.068,.078,.006),
                           (.54,.117,.053,.059,-.014),(.50,.119,.051,.053,-.019),
                           (.46,.120,.051,.053,-.014),(.34,.123,.057,.064,.004),
                           (.20,.128,.041,.044,.010),(.125,.128,.036,.035,.010),
                           (.086,.129,.043,.075,-.026),(.04,.129,.047,.103,-.048),
                           (.008,.130,.046,.107,-.051)):
            prev=extend(prev,[(side*(x+w*s),yc+side*d*t,z) for s,t in
                              ((-.72,-.88),(.45,-1),(1,-.38),(1,.50),(.48,1),(-.88,.53))])
        faces.append(tuple(prev))
    ob=mesh("GEO_Cage_Humaine",v,faces,L.material("Argile bleue",(.41,.58,.72)))
    bm=bmesh.new(); bm.from_mesh(ob.data)
    bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces))
    assert all(e.is_manifold for e in bm.edges)
    bm.to_mesh(ob.data);bm.free()
    for p in ob.data.polygons:
        p.use_smooth=True
    return ob


def armature(ob):
    data=bpy.data.armatures.new("Armature · atelier")
    rig=bpy.data.objects.new("RIG_Atelier",data)
    bpy.context.scene.collection.objects.link(rig)
    rig.show_in_front=True
    bpy.ops.object.select_all(action="DESELECT"); rig.select_set(True)
    bpy.context.view_layer.objects.active=rig
    chains=[
        ("bassin",(0,0,.87),(0,0,1.04),None),
        ("thorax",(0,0,1.04),(0,0,1.46),"bassin"),
        ("cou",(0,0,1.46),(0,0,1.61),"thorax"),
        ("tete",(0,0,1.61),(0,0,1.80),"cou"),
    ]
    for s,side in ((1,".L"),(-1,".R")):
        chains.extend([
            ("bras"+side,(s*.177,0,1.394),(s*.393,-.012,1.218),"thorax"),
            ("avantbras"+side,(s*.393,-.012,1.218),(s*.491,-.034,1.123),"bras"+side),
            ("main"+side,(s*.491,-.034,1.123),(s*.55,-.034,1.06),"avantbras"+side),
            ("cuisse"+side,(s*.105,0,.887),(s*.119,-.019,.50),"bassin"),
            ("tibia"+side,(s*.119,-.019,.50),(s*.129,.01,.126),"cuisse"+side),
            ("pied"+side,(s*.129,.01,.126),(s*.13,-.14,.032),"tibia"+side),
        ])
    bpy.ops.object.mode_set(mode="EDIT")
    for name,head,tail,parent in chains:
        b=data.edit_bones.new(name);b.head=head;b.tail=tail
        if parent:
            b.parent=data.edit_bones[parent]
            b.use_connect=(b.parent.tail-b.head).length<.001
    bpy.ops.object.mode_set(mode="OBJECT")
    groups={name:ob.vertex_groups.new(name=name) for name,*_ in chains}
    for v in ob.data.vertices:
        x,y,z=v.co
        side=".L" if x>0 else ".R"
        if abs(x)>.192 and 1.025<z<1.52:
            names=("thorax","bras"+side,"avantbras"+side,"main"+side)
        elif z<.92:
            names=("bassin","cuisse"+side,"tibia"+side,"pied"+side)
        else:
            names=("bassin","thorax","cou","tete")
        influences=[]
        for name,a,b,_ in chains:
            if name not in names:
                continue
            a,b=Vector(a),Vector(b);d=b-a
            t=max(.08,min(.92,(v.co-a).dot(d)/d.length_squared))
            influence=1/(.009+(v.co-(a+t*d)).length_squared)**2.7
            influences.append((name,influence))
        influences.sort(key=lambda item:item[1],reverse=True)
        adj=influences[:2]
        total=sum(w for _,w in adj)
        for name,w in adj:
            groups[name].add([v.index],w/total,"REPLACE")
    ob.parent=rig
    deform=ob.modifiers.new("Armature", "ARMATURE");deform.object=rig
    deform.use_deform_preserve_volume=True
    sub=ob.modifiers.new("Surface de comparaison", "SUBSURF");sub.levels=1
    for frame,degrees in ((1,0),(25,-82),(49,0)):
        for name,axis,angle in (("avantbras.L",(1,0,0),degrees),("tibia.R",(1,0,0),-degrees*.58)):
            pb=rig.pose.bones[name];pb.rotation_mode="QUATERNION"
            from mathutils import Quaternion
            pb.rotation_quaternion=Quaternion(pb.bone.matrix_local.to_3x3().inverted()@Vector(axis),math.radians(angle))
            pb.keyframe_insert("rotation_quaternion",frame=frame)
    return rig


def main():
    L.reset("Atelier · cage humaine")
    ob=body()
    rig=armature(ob)
    scene=bpy.context.scene
    studio=L.collection("Studio")
    cam=L.camera("Vue de contrôle",studio,location=(2.4,-4.8,2.3))
    cam.rotation_euler=(Vector((0,0,.91))-cam.location).to_track_quat("-Z","Y").to_euler()
    cam.data.type="ORTHO";cam.data.ortho_scale=2.22
    scene.frame_end=49
    scene.timeline_markers.new("Cage neutre",frame=1)
    scene.timeline_markers.new("Coude et genou fléchis",frame=25)
    scene.unit_settings.system="METRIC"
    scene.render.engine="BLENDER_WORKBENCH"
    scene.display.shading.color_type="MATERIAL"
    scene.display.shading.show_cavity=True
    scene.render.resolution_x=740
    scene.render.resolution_y=820
    scene.render.resolution_percentage=100
    scene.render.image_settings.file_format="PNG"
    scene.frame_set(1)
    note=bpy.data.texts.new("LIRE · Cage pédagogique")
    note.write("Les doigts et le visage sont simplifiés. Ce modèle est une cage de comparaison pour comprendre les extrusions, le raccord des bras et du cou, et la flexion. Tab sur le corps pour lire la cage. Le rig n’est pas un rig de production. Image 25 : pose de contrôle.")
    L.save(str(HERE/"assets"/"cage_humain.blend"))
    strip=ob.copy();strip.data=ob.data.copy();strip.name="Filaire de la cage pour le rendu"
    scene.collection.objects.link(strip)
    strip.data.materials.clear();strip.data.materials.append(L.material("Traits de cage",(.034,.059,.081)))
    strip.modifiers.remove(strip.modifiers[-1])
    wire=strip.modifiers.new("Arêtes de la cage","WIREFRAME")
    wire.thickness=.0030
    main_sub=ob.modifiers[-1]
    main_sub.show_render=False
    for frame,name in ((1,"cage_humain"),(25,"cage_humain_pose")):
        scene.frame_set(frame)
        scene.render.filepath=str(HERE/"assets"/(name+".png"))
        bpy.ops.render.render(write_still=True)
    scene.frame_set(1)
    scene.render.fps=24
    scene.render.image_settings.media_type="VIDEO"
    scene.render.ffmpeg.format="MPEG4"
    scene.render.ffmpeg.codec="H264"
    scene.render.ffmpeg.audio_codec="NONE"
    scene.render.filepath=str(HERE/"assets"/"cage_flexion_")
    bpy.ops.render.render(animation=True)


if __name__=="__main__":
    L.run(main)
