"""Final presentation pass on the fitted character, without changing earlier files."""
import math
import sys
from pathlib import Path

import bpy
import numpy as np
from mathutils import Vector
from mathutils.bvhtree import BVHTree

ROOT=Path(__file__).resolve().parent
sys.path[:0]=[str(ROOT),str(ROOT.parents[1]/"SCRIPTS")]
import bcma_lib as L
from build_from_views import UNIT, SOLE
from build_body_uv_rig import select_only, bind_to_head
from fit_anatomy import camera


def skin_atlas(body,scene):
    mesh=body.data
    co=np.array([tuple(v.co) for v in mesh.vertices])
    x,y,z=co.T
    row=SOLE-z/UNIT
    # Authored neutral skin tone following landmarks, reprojected to the same UV atlas.
    facing=np.clip((-y-.018)/.060,0,1)
    cheek=np.exp(-((abs(x)-.043)/.026)**2-((row-110)/16)**2)*facing
    lips=np.exp(-(x/.023)**4-((row-128.6)/3.4)**2)*facing
    orbital=np.exp(-((abs(x)-.030)/.024)**2-((row-92)/9.4)**2)*facing
    beard=np.exp(-(x/.067)**4-((row-143)/12)**2)*facing
    warm=np.exp(-(x/.0145)**2-((row-114)/10)**2)*facing
    base=np.tile([.39,.196,.121],(len(co),1))
    base+=cheek[:,None]*[.080,.016,.007]
    base+=lips[:,None]*[-.045,-.072,-.051]
    base+=orbital[:,None]*[-.065,-.045,-.031]
    base+=beard[:,None]*[-.057,-.036,-.019]
    base+=warm[:,None]*[.053,.008,.003]
    color=mesh.color_attributes.new(name="Peau finale",type="FLOAT_COLOR",domain="POINT")
    color.data.foreach_set("color",np.column_stack((base,np.ones(len(co)))).astype(np.float32).ravel())
    work=body.copy()
    work.data=body.data.copy()
    work.name="TEMP · atlas"
    scene.collection.objects.link(work)
    work.parent=None
    work.modifiers.clear()
    work.data.materials.clear()
    mat=L.material("Peau · UV Peau finale 2048",(.46,.25,.164),.48)
    bsdf=next(n for n in mat.node_tree.nodes if n.type=="BSDF_PRINCIPLED")
    bsdf.inputs["Subsurface Weight"].default_value=.074
    bsdf.inputs["Subsurface Scale"].default_value=.010
    work.data.materials.append(mat)
    nt=mat.node_tree
    out=next(n for n in nt.nodes if n.type=="OUTPUT_MATERIAL")
    vc=nt.nodes.new("ShaderNodeVertexColor");vc.layer_name="Peau finale"
    emi=nt.nodes.new("ShaderNodeEmission")
    nt.links.new(vc.outputs["Color"],emi.inputs["Color"])
    nt.links.new(emi.outputs[0],out.inputs["Surface"])
    uv=nt.nodes.new("ShaderNodeUVMap");uv.uv_map="UV_Atlas"
    tex=nt.nodes.new("ShaderNodeTexImage")
    tex.image=bpy.data.images.new("Peau finale · 2048",width=2048,height=2048,alpha=False)
    nt.links.new(uv.outputs[0],tex.inputs["Vector"])
    nt.nodes.active=tex
    select_only(work)
    scene.render.bake.margin=12
    scene.cycles.samples=8
    bpy.ops.object.bake(type="EMIT")
    tex.image.filepath_raw=str(ROOT/"atlas_peau_finale_2048.png")
    tex.image.file_format="PNG"
    tex.image.save()
    tex.image.pack()
    nt.links.new(bsdf.outputs[0],out.inputs["Surface"])
    nt.links.new(tex.outputs[0],bsdf.inputs["Base Color"])
    nt.nodes.remove(emi);nt.nodes.remove(vc)
    temp_mesh=work.data
    bpy.data.objects.remove(work,do_unlink=True)
    bpy.data.meshes.remove(temp_mesh)
    old=body.data.materials[0]
    body.data.materials[0]=mat
    body.data.materials.append(old)
    return mat


def anatomy_tree(body):
    deps=bpy.context.evaluated_depsgraph_get()
    return BVHTree.FromObject(body,deps)


def make_mesh(name,col,verts,faces,mat):
    data=bpy.data.meshes.new(name)
    data.from_pydata(verts,[],faces)
    data.update()
    ob=bpy.data.objects.new(name,data)
    col.objects.link(ob)
    data.materials.append(mat)
    for p in data.polygons:
        p.use_smooth=True
    return ob


def hairline(a):
    a=abs((a+math.pi)%(2*math.pi)-math.pi)
    a=math.degrees(a)
    return float(np.interp(a,[0,16,34,47,57,68,79,87,96,108,119,135,156,180],
                             [59,57,55,56,63,75,101,98,91,90,104,121,130,132]))


def make_hair(body,rig,col):
    tree=anatomy_tree(body)
    n=100
    rings=25
    verts=[(0,-.003,1.825)]
    face=[]
    for row in range(1,rings+1):
        t=row/rings
        for k in range(n):
            a=math.tau*k/n
            base=hairline(a)
            py=42.4+(base-42.4)*(1-math.cos(t*math.pi/2))
            z=(SOLE-py)*UNIT
            d=Vector((math.sin(a),-math.cos(a),0))
            c=Vector((0,.002,z))
            point,normal,idx,dist=tree.ray_cast(c+d*.155,-d,.160)
            if point is None:
                # Very top of the reference skull can be just above the source surface.
                r=.006+.015*t
                point=c+d*r
                normal=Vector((d.x*.3,d.y*.3,1)).normalized()
            # Broad sweep that tapers into the cropped hairline.
            sweep=(.0036+.0015*math.cos(2*a+.5))*math.sin(math.pi*(t*.73+.15))
            grain=(.00027*math.sin(39*a+5*t)+.00020*math.sin(63*a-3*t))*math.sin(t*math.pi/2)
            verts.append(tuple(point+normal*(sweep+grain+.0009)))
    for k in range(n):
        face.append((0,1+k,1+(k+1)%n))
    for row in range(rings-1):
        for k in range(n):
            a=1+row*n+k
            b=1+row*n+(k+1)%n
            face.append((a,a+n,b+n,b))
    mat=L.material("Cheveux courts · brun chaud",(.038,.023,.014),.62)
    nt=mat.node_tree
    bsdf=next(node for node in nt.nodes if node.type=="BSDF_PRINCIPLED")
    noise=nt.nodes.new("ShaderNodeTexNoise")
    bsdf.inputs["Specular IOR Level"].default_value=.25
    noise.inputs["Scale"].default_value=158
    noise.inputs["Detail"].default_value=2.8
    ramp=nt.nodes.new("ShaderNodeValToRGB")
    ramp.color_ramp.elements[0].color=(.020,.011,.0065,1)
    ramp.color_ramp.elements[1].color=(.052,.028,.015,1)
    nt.links.new(noise.outputs["Fac"],ramp.inputs[0])
    nt.links.new(ramp.outputs["Color"],bsdf.inputs["Base Color"])
    tex=nt.nodes.new("ShaderNodeTexCoord")
    nt.links.new(tex.outputs["Generated"],noise.inputs["Vector"])
    bump=nt.nodes.new("ShaderNodeBump")
    bump.inputs["Strength"].default_value=.12
    bump.inputs["Distance"].default_value=.001
    nt.links.new(noise.outputs["Fac"],bump.inputs["Height"])
    nt.links.new(bump.outputs[0],bsdf.inputs["Normal"])
    ob=make_mesh("GEO_Coiffure · capuchon ajusté",col,verts,face,mat)
    # Recalculate the scalp normals before adding the inside surface.
    import bmesh
    bm=bmesh.new();bm.from_mesh(ob.data)
    bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces))
    bm.to_mesh(ob.data);bm.free()
    if ob.data.polygons[0].normal.z<0:
        bm=bmesh.new();bm.from_mesh(ob.data)
        bmesh.ops.reverse_faces(bm,faces=list(bm.faces))
        bm.to_mesh(ob.data);bm.free()
    bind_to_head(ob,rig)
    sub=ob.modifiers.new("Lisser le contour","SUBSURF");sub.levels=sub.render_levels=1
    solid=ob.modifiers.new("Épaisseur de la chevelure","SOLIDIFY");solid.thickness=.0012
    return ob


def make_brows(body,rig,col):
    tree=anatomy_tree(body)
    mat=L.material("Sourcils · brun chaud",(.058,.033,.020),.68)
    for s in (-1,1):
        vv=[];ff=[]
        for i in range(28):
            t=i/27
            x=s*(.014+t*.039)
            py=85.5-4.0*math.sin(math.pi*t)+4.2*t*t
            z=(SOLE-py)*UNIT
            width=(.0030+.0018*math.sin(math.pi*t))*(.35+.65*math.sin(math.pi*(.13+.83*t)))
            for j in range(5):
                c=(j-2)/2
                pos=Vector((x,-.28,z+width*c))
                pt,normal,idx,dist=tree.ray_cast(pos,Vector((0,1,0)),.38)
                if pt is None:
                    raise RuntimeError(f"Sourcil sans support : {s}/{i}/{j}")
                vv.append(tuple(pt+normal*(.00075+.00125*(1-c*c)*math.sin(math.pi*t))))
        for i in range(27):
            for j in range(4):
                p=i*5+j
                f=(p,p+5,p+6,p+1)
                ff.append(f if s>0 else tuple(reversed(f)))
        br=make_mesh("Sourcil."+("L" if s>0 else "R"),col,vv,ff,mat)
        bind_to_head(br,rig)


def cloth_pass():
    for name in ("Tee-shirt ajusté","Pantalon droit"):
        ob=bpy.data.objects[name]
        nt=ob.data.materials[0].node_tree
        bsdf=next(n for n in nt.nodes if n.type=="BSDF_PRINCIPLED")
        tc=nt.nodes.new("ShaderNodeTexCoord")
        noise=nt.nodes.new("ShaderNodeTexNoise")
        noise.inputs["Scale"].default_value=320 if name.startswith("Tee") else 230
        noise.inputs["Detail"].default_value=2
        nt.links.new(tc.outputs["UV"],noise.inputs["Vector"])
        bump=nt.nodes.new("ShaderNodeBump")
        bump.inputs["Strength"].default_value=.20
        bump.inputs["Distance"].default_value=.0015
        nt.links.new(noise.outputs["Fac"],bump.inputs["Height"])
        nt.links.new(bump.outputs[0],bsdf.inputs["Normal"])
    pants=bpy.data.objects["Pantalon droit"]
    # Move the shell away from the calf slightly, with a taper at knees and boot openings.
    for v in pants.data.vertices:
        x,y,z=v.co
        if .212<z<.72 and abs(x)<.22:
            w=math.sin(math.pi*(z-.212)/(.72-.212))**.72
            v.co.x+=.008*w*max(-.9,min(.9,(x-math.copysign(.129,x))/.037))
            v.co.y+=.005*w*max(-.9,min(.9,(y-.013)/.055))
    pants.data.update()
    # Tuck the top of the pants behind the shirt hem.
    g=pants.vertex_groups["Coupe textile"]
    g.remove(list(range(len(pants.data.vertices))))
    for v in pants.data.vertices:
        x,y,z=v.co
        distance=min(1.072-z,z-.178,.216-abs(x))
        w=max(0,min(1,.5+distance/.022))
        if w:
            g.add([v.index],w,"REPLACE")


def finish_trim(body,col):
    """Extract the real garment openings and bind their rounded narrow trims."""
    scene=bpy.context.scene
    deps=bpy.context.evaluated_depsgraph_get()
    from mathutils.kdtree import KDTree
    from collections import defaultdict
    kd=KDTree(len(body.data.vertices))
    for v in body.data.vertices:
        kd.insert(v.co,v.index)
    kd.balance()
    rig=body.parent
    no_deform={b.name for b in rig.data.bones if not b.use_deform}
    for name in ("Tee-shirt ajusté","Pantalon droit"):
        garment=bpy.data.objects[name]
        solid=garment.modifiers[-1]
        solid.show_viewport=False
        bpy.context.view_layer.update()
        ev=garment.evaluated_get(deps)
        src=ev.data
        edges=defaultdict(int)
        for poly in src.polygons:
            for k in poly.edge_keys:
                edges[k]+=1
        boundary=defaultdict(list)
        for (i,j),count in edges.items():
            if count==1:
                boundary[i].append(j);boundary[j].append(i)
        visited=set()
        loops=[]
        for i in boundary:
            if i in visited:
                continue
            loop=[i]
            prev=-1;cur=i
            while True:
                visited.add(cur)
                options=[j for j in boundary[cur] if j!=prev]
                if not options or options[0] in visited:
                    break
                nxt=options[0];loop.append(nxt)
                prev,cur=cur,nxt
            if len(loop)>12 and loop[0] in boundary[loop[-1]]:
                if name.startswith("Pantalon") and sum(src.vertices[h].co.z for h in loop)/len(loop)>.90:
                    continue
                loops.append(loop)
        verts=[];faces=[]
        for loop in loops:
            start=len(verts)
            for i,idx in enumerate(loop):
                p=src.vertices[idx].co.copy()
                normal=src.vertices[idx].normal.normalized()
                tangent=(src.vertices[loop[(i+1)%len(loop)]].co-src.vertices[loop[i-1]].co).normalized()
                bi=tangent.cross(normal).normalized()
                p=p+normal*.0005
                for j in range(8):
                    angle=math.tau*j/8
                    verts.append(tuple(p+normal*(.00115*math.cos(angle))+bi*(.00155*math.sin(angle))))
            for i in range(len(loop)):
                for j in range(8):
                    ni=(i+1)%len(loop);nj=(j+1)%8
                    faces.append((start+i*8+j,start+i*8+nj,start+ni*8+nj,start+ni*8+j))
        solid.show_viewport=True
        if not faces:
            continue
        rgb=(.036,.052,.091) if name.startswith("Tee") else (.029,.030,.035)
        trim=make_mesh("Finitions · "+name,col,verts,faces,L.material("Fil · "+name,rgb,.67))
        trim.parent=rig
        groups={}
        for v in trim.data.vertices:
            combined=defaultdict(float)
            for _pos,index,distance in kd.find_n(v.co,4):
                weight=1/(distance+.002)**2
                for w in body.data.vertices[index].groups:
                    n=body.vertex_groups[w.group].name
                    if n in rig.data.bones and n not in no_deform:
                        combined[n]+=w.weight*weight
            total=sum(combined.values())
            for gn,w in combined.items():
                if gn not in groups:
                    groups[gn]=trim.vertex_groups.new(name=gn)
                groups[gn].add([v.index],w/total,"REPLACE")
        m=trim.modifiers.new("Suivi de l’armature","ARMATURE");m.object=rig
        m.use_deform_preserve_volume=True
        print("FINITION",name,len(loops),len(verts))


def smile(body):
    body.shape_key_add(name="Basis",from_mix=False)
    smile=body.shape_key_add(name="Sourire léger",from_mix=False)
    mesh=body.data
    moved=0
    for v in mesh.vertices:
        x,y,z=v.co
        row=SOLE-z/UNIT
        influence=math.exp(-((abs(x)-.020)/.016)**2-((row-128.5)/7)**2)
        influence*=max(0,min(1,(-y-.022)/.044))
        if influence>.002:
            smile.data[v.index].co.z+=.0055*influence
            smile.data[v.index].co.x+=math.copysign(.002*influence,x)
            smile.data[v.index].co.y-=.0012*influence
            moved+=1
    print("SOURIRE",moved)


def make_ik(rig,scene):
    scene.frame_set(1)
    select_only(rig)
    bpy.ops.object.mode_set(mode="EDIT")
    for side in ("L","R"):
        foot=rig.data.edit_bones["foot."+side]
        control=rig.data.edit_bones.new("CTRL_Pied_IK."+side)
        control.head,control.tail,control.roll=foot.head.copy(),foot.tail.copy(),foot.roll
        control.use_deform=False
        control.hide_select=False
        pole=rig.data.edit_bones.new("CTRL_Genou."+side)
        k=rig.data.edit_bones["lowerleg01."+side].head
        pole.head=k+Vector((0,-.37,0))
        pole.tail=pole.head+Vector((0,0,.11))
        pole.use_deform=False
    bpy.ops.object.mode_set(mode="OBJECT")
    c=rig.data.collections.new("Pieds · IK")
    rig["Pieds IK"]=0.0
    rig.id_properties_ui("Pieds IK").update(min=0.0,max=1.0,description="0 : FK. 1 : déplacer les contrôles des pieds et des genoux.")
    for side in ("L","R"):
        for n in ("CTRL_Pied_IK.","CTRL_Genou."):
            bone=rig.data.bones[n+side]
            c.assign(bone)
            bone.color.palette="THEME04"
        for n in ("upperleg02.","lowerleg02."):
            pb=rig.pose.bones[n+side]
            pb.lock_ik_x=pb.lock_ik_y=pb.lock_ik_z=True
        pb=rig.pose.bones["lowerleg02."+side]
        ik=pb.constraints.new("IK")
        ik.name="Contrôler le pied"
        ik.target=rig
        ik.subtarget="CTRL_Pied_IK."+side
        ik.pole_target=rig
        ik.pole_subtarget="CTRL_Genou."+side
        ik.chain_count=4
        ik.use_stretch=False
        ik.iterations=180
        rot=rig.pose.bones["foot."+side].constraints.new("COPY_ROTATION")
        rot.name="Orientation du contrôle de pied"
        rot.target=rig
        rot.subtarget="CTRL_Pied_IK."+side
        for con in (ik,rot):
            fc=con.driver_add("influence")
            d=fc.driver
            v=d.variables.new()
            v.name="active"
            v.type="SINGLE_PROP"
            v.targets[0].id=rig
            v.targets[0].data_path='["Pieds IK"]'
            d.expression="active"
        # Calibrate the pole angle against the same rest knee, with a small lift
        # so the bend is visible and its forward direction can be disambiguated.
        target=rig.pose.bones["CTRL_Pied_IK."+side]
        mat=target.bone.matrix_local.to_3x3().inverted()
        target.location=mat@Vector((0,0,.023))
        rig["Pieds IK"]=1.0
        rig.update_tag()
        expected=rig.data.bones["lowerleg01."+side].head_local+Vector((0,-.085,.01))
        best=None
        for i in range(36):
            a=-math.pi+i*math.tau/36
            ik.pole_angle=a
            bpy.context.view_layer.update()
            rs=rig.evaluated_get(bpy.context.evaluated_depsgraph_get())
            actual=rs.pose.bones["lowerleg01."+side].head
            cost=(actual-expected).length
            if best is None or cost<best[0]:
                best=(cost,a)
        ik.pole_angle=best[1]
        target.location=(0,0,0)
        rig["Pieds IK"]=0.0
        rig.update_tag()
        bpy.context.view_layer.update()
        print("IK",side,math.degrees(best[1]))
    # Keep both control shapes easily selectable near the feet and knees.
    widgets=L.collection("05 · Formes des contrôleurs")
    for side in ("L","R"):
        for control,name,coords in (
            ("CTRL_Pied_IK.","Cercle pied",[(-.8,-.35,0),(.8,-.35,0),(.8,1.10,0),(-.8,1.10,0)]),
            ("CTRL_Genou.","Losange genou",[(0,-.6,0),(.60,0,0),(0,.6,0),(-.6,0,0)]),
        ):
            mesh=bpy.data.meshes.new(name+side)
            mesh.from_pydata(coords,[(i,(i+1)%len(coords)) for i in range(len(coords))],[])
            widget=bpy.data.objects.new(name+side,mesh)
            widgets.objects.link(widget)
            widget.hide_render=True
            widget.hide_set(True)
            pb=rig.pose.bones[control+side]
            pb.custom_shape=widget
            pb.use_custom_shape_bone_size=True
    return c


def test_ik(rig,scene):
    scene.frame_set(1)
    rig["Pieds IK"]=1.0
    rig.update_tag()
    for side in ("L","R"):
        q=rig.pose.bones["CTRL_Pied_IK."+side]
        q.location=q.bone.matrix_local.to_3x3().inverted()@Vector((0,-.058,.095))
        bpy.context.view_layer.update()
        dg=bpy.context.evaluated_depsgraph_get()
        r=rig.evaluated_get(dg)
        requested=r.pose.bones[q.name].head
        actual=r.pose.bones["foot."+side].head
        error=(requested-actual).length
        print("IK TEST",side,round(error*1000,2),"mm")
        assert error<.017,(side,error)
        q.location=(0,0,0)
    rig["Pieds IK"]=0.0
    rig.update_tag()
    bpy.context.view_layer.update()


def main():
    bpy.ops.wm.open_mainfile(filepath=str(ROOT/"personnage_corps_uv_rig_pieds.blend"))
    scene=bpy.context.scene
    scene.frame_set(1)
    rig=bpy.data.objects["RIG_Personnage_FK"]
    body=bpy.data.objects["GEO_Personnage"]
    details=L.collection("06 · Détails déformables")
    skin_atlas(body,scene)
    make_hair(body,rig,details)
    make_brows(body,rig,details)
    cloth_pass()
    finish_trim(body,details)
    smile(body)
    controls=make_ik(rig,scene)
    test_ik(rig,scene)
    scene.camera=bpy.data.objects["CAM_Trois_Quarts"]
    studio=scene.camera.users_collection[0]
    portrait=camera(studio,"CAM_Portrait_Final",(.68,-2.4,1.76),(0,-.01,1.665),.355)
    scene.render.resolution_x=900
    scene.render.resolution_y=1240
    scene.cycles.samples=32
    scene.cycles.use_denoising=True
    scene.render.filepath="//personnage_final.png"
    controls.is_visible=False
    select_only(rig)
    note=bpy.data.texts.new("LIRE · Personnage final")
    note.write(
        "Personnage fini pour présentation. Pose FK : images 1 (repos), 25 et 49 (tests). "
        "Pour les pieds IK : revenez à l’image 1, activez la collection Pieds · IK, "
        "réglez la propriété Pieds IK à 1 puis déplacez CTRL_Pied_IK.L/R en mode Pose. "
        "CTRL_Genou.L/R oriente la flexion. Remettez Pieds IK à 0 pour utiliser les poses FK. "
        "La clé de forme Sourire léger se règle sur GEO_Personnage. "
        "UV_Atlas et atlas peau 2048 intégrés. Coiffure, sourcils et finitions du textile ont leur géométrie propre. "
        "Base anatomique, UV, squelette et poids MakeHuman (CC0), ajustés aux gabarits."
    )
    L.save(str(ROOT/"personnage_final.blend"))
    bpy.ops.render.render(write_still=True)
    scene.frame_set(25)
    scene.render.filepath="//personnage_final_pose.png"
    bpy.ops.render.render(write_still=True)
    scene.frame_set(1)
    scene.camera=portrait
    scene.render.resolution_x=960
    scene.render.resolution_y=960
    scene.render.filepath="//personnage_final_portrait.png"
    bpy.ops.render.render(write_still=True)


if __name__=="__main__":
    L.run(main)
