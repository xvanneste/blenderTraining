"""Body, packed UV atlas and posed MakeHuman-derived armature for the two views."""
import json
import math
import sys
from pathlib import Path

import bpy
import bmesh
import numpy as np
from mathutils import Vector

sys.path.insert(0, str(Path(__file__).resolve().parent))
from fit_anatomy import read_template, fit_template, camera
from build_from_views import L, ROOT, UNIT, SOLE, CENTER_FRONT, CENTER_SIDE, FRONT, SIDE, guide_image


def smoother(value, a, b):
    t=np.clip((value-a)/(b-a),0,1)
    return t*t*(3-2*t)


def body_fit(raw, faces, pixels):
    """Warp the arm chains separately while keeping the same connected skin."""
    x,h,depth=raw.T
    vertical=np.interp(h,[-8.25,-7.46,-3.10,1.15,2.085,3.40,4.78,5.81,6.86,9.3],
                      [962,883,685,470,422,337,269,224,174,42])
    lateral=np.interp(h,[-8.25,-7.46,-3.10,0,1.2,2.8,4.0,5.8,6.8,9.3],
                     [31,33,36,39,43,39,43,53,48,48])
    centre=np.interp(h,[-8,-7.2,-3.1,0,2,4.8,6.8],[1159,1163,1158,1151,1148,1155,1162])
    bod=np.column_stack((x*lateral,centre-depth*43,vertical))
    start=np.array([1.882,5.815,.214])
    elbow=np.array([3.553,3.899,.192])
    wrist=np.array([4.882,2.634,2.068])
    new_start=np.array([104,-224,CENTER_SIDE-1179])
    new_elbow=np.array([135,-352,CENTER_SIDE-1175])
    new_wrist=np.array([173,-474,CENTER_SIDE-1148])
    arm_in=np.column_stack((np.abs(x),h,depth))

    def segment(a,b,c,d):
        old=Vector(b-a)
        new=Vector(d-c)
        rot=np.asarray(old.rotation_difference(new).to_matrix())
        return (arm_in-a)@rot.T*(new.length/old.length)+c

    upper=segment(start,elbow,new_start,new_elbow)
    lower=segment(elbow,wrist,new_elbow,new_wrist)
    t=smoother(4.25-h,0,.60)[:,None]
    arm=upper*(1-t)+lower*t
    arm=np.column_stack((np.sign(x)*arm[:,0],CENTER_SIDE-arm[:,2],-arm[:,1]))
    threshold=np.interp(h,[1.0,3,4,4.7,5.4,6,6.6],[3.1,2.35,2.18,1.75,1.48,1.37,1.60])
    influence=(smoother(np.abs(x)-threshold,-.12,.40)
               *(1-smoother(h,5.86,6.36)))[:,None]
    bod=bod*(1-influence)+arm*influence
    # Relax the front of the dressed pelvis as a trouser block.
    fit_z=(SOLE-bod[:,2])*UNIT
    flat=np.exp(-(x/.42)**2-((h-.55)/.52)**2)
    bod[:,1]+=np.maximum(0,(1101-bod[:,1]))*flat*.73
    world=np.column_stack((bod[:,0]*UNIT,(bod[:,1]-CENTER_SIDE)*UNIT,fit_z))
    upper_fit=fit_template(raw,faces,pixels)
    amount=smoother(h,5.9,6.72)[:,None]
    return world*(1-amount)+upper_fit*amount


def read_uv(remap,faces):
    tex=[]
    indices=[]
    group=None
    seen_faces=[]
    lines=(ROOT/"makehuman_base_cc0.obj").read_text(encoding="utf-8").splitlines()
    for line in lines:
        k,*vals=line.split() if line.strip() else ("",)
        if k=="vt":
            tex.append(tuple(map(float,vals[:2])))
        elif k=="g":
            group=vals[0]
        elif k=="f" and group=="body":
            tokens=[value.split("/") for value in vals]
            seen_faces.append(tuple(int(value[0])-1 for value in tokens))
            indices.extend(int(value[1])-1 for value in tokens)
    assert seen_faces==faces and min(indices)>=0
    return np.asarray(tex,dtype=np.float32)[indices].flatten()


def make_body(raw,faces,world,pixels,col):
    ids=sorted(set(i for f in faces for i in f))
    remap={old:i for i,old in enumerate(ids)}
    mesh=bpy.data.meshes.new("Corps continu · UV MakeHuman")
    mesh.from_pydata(world[ids].tolist(),[],[tuple(remap[i] for i in f) for f in faces])
    mesh.update()
    uv=mesh.uv_layers.new(name="UV_Atlas")
    uv.uv.foreach_set("vector",read_uv(remap,faces))
    body=bpy.data.objects.new("GEO_Personnage",mesh)
    col.objects.link(body)
    for p in mesh.polygons:
        p.use_smooth=True
    attr=mesh.color_attributes.new(name="Couleur projetée",type="FLOAT_COLOR",domain="POINT")
    xyz=world[ids]
    x,y,z=xyz.T
    px=CENTER_FRONT+x/UNIT
    sx=CENTER_SIDE+y/UNIT
    p=SOLE-z/UNIT
    front=pixels[np.clip(np.rint(p).astype(int),0,1023),np.clip(np.rint(px).astype(int),0,1535),:3]
    side=pixels[np.clip(np.rint(p).astype(int),0,1023),np.clip(np.rint(sx).astype(int),0,1535),:3]
    ns=np.empty(len(ids)*3,dtype=np.float32)
    mesh.vertices.foreach_get("normal",ns)
    n=ns.reshape(-1,3)
    f=np.maximum(0,-n[:,1])**2
    s=(abs(n[:,0])+np.maximum(0,n[:,1]))**2
    # Limit bleed of the figure's bright background after projecting across
    # the orthographic silhouettes, and keep clothing opaque in all views.
    low=1.045+.258*smoother(abs(x),.133,.170)
    high=1.505+.075*smoother(y,-.044,.075)+.13*smoother(abs(x),.055,.095)
    shirt=(z>low+.002)&(z<high-.002)
    trousers=(p>=426)&(p<905)&(abs(x)<.177)
    footwear=(p>=898)&(abs(x)<.18)
    skin=~(shirt|trousers|footwear)
    palette=np.tile([.68,.49,.37],(len(ids),1))
    palette[shirt]=[.22,.28,.37]
    palette[trousers]=[.21,.21,.22]
    palette[footwear]=[.09,.11,.13]
    def filter_colors(c, weight):
        rr,gg,bb=c.T
        good=(c.min(axis=1)<.79)&(((rr>bb*1.06)|(p<78))==skin)
        return weight*good
    f=filter_colors(front,f)
    s=filter_colors(side,s)
    mix=(f[:,None]*front+s[:,None]*side)/(f+s+1e-7)[:,None]
    confidence=np.clip((f+s)*3,0,1)[:,None]
    color=confidence*mix+(1-confidence)*palette
    color=np.where(color<.04045,color/12.92,((color+.055)/1.055)**2.4)
    attr.data.foreach_set("color",np.column_stack((color,np.ones(len(ids)))).astype(np.float32).flatten())
    return body,remap


def select_only(ob):
    bpy.ops.object.select_all(action="DESELECT")
    ob.select_set(True)
    bpy.context.view_layer.objects.active=ob


def bake_atlas(scene,body):
    mat=L.material("Personnage · atlas couleur UV",(.55,.43,.38),.61)
    body.data.materials.append(mat)
    nt=mat.node_tree
    out=next(node for node in nt.nodes if node.type=="OUTPUT_MATERIAL")
    bsdf=next(node for node in nt.nodes if node.type=="BSDF_PRINCIPLED")
    vc=nt.nodes.new("ShaderNodeVertexColor")
    vc.layer_name="Couleur projetée"
    emission=nt.nodes.new("ShaderNodeEmission")
    nt.links.new(vc.outputs["Color"],emission.inputs["Color"])
    nt.links.new(emission.outputs[0],out.inputs["Surface"])
    img=bpy.data.images.new("Atlas_Personnage_2048",width=2048,height=2048,alpha=False)
    tex=nt.nodes.new("ShaderNodeTexImage")
    tex.image=img
    tex.label="Texture couleur empaquetée"
    nt.nodes.active=tex
    tex.select=True
    uv=nt.nodes.new("ShaderNodeUVMap")
    uv.uv_map="UV_Atlas"
    nt.links.new(uv.outputs["UV"],tex.inputs["Vector"])
    select_only(body)
    scene.render.engine="CYCLES"
    scene.cycles.samples=8
    scene.render.bake.margin=10
    bpy.ops.object.bake(type="EMIT")
    img.filepath_raw=str(ROOT/"atlas_personnage_2048.png")
    img.file_format="PNG"
    img.save()
    img.pack()
    nt.links.new(bsdf.outputs["BSDF"],out.inputs["Surface"])
    nt.links.new(tex.outputs["Color"],bsdf.inputs["Base Color"])
    nt.nodes.remove(emission)
    nt.nodes.remove(vc)
    return img


def rig_body(body,remap,world,col):
    spec=json.loads((ROOT/"makehuman_rig_cc0.mhskel").read_text(encoding="utf-8"))
    weights=json.loads((ROOT/"makehuman_weights_cc0.mhw").read_text(encoding="utf-8"))["weights"]
    joints={name:np.mean(world[index],axis=0) for name,index in spec["joints"].items()}
    data=bpy.data.armatures.new("Armature CC0 · ajustée aux gabarits")
    rig=bpy.data.objects.new("RIG_Personnage_FK",data)
    col.objects.link(rig)
    data.display_type="STICK"
    rig.show_in_front=True
    select_only(rig)
    bpy.ops.object.mode_set(mode="EDIT")
    for name,bb in spec["bones"].items():
        eb=data.edit_bones.new(name)
        a,b=map(Vector,(joints[bb["head"]],joints[bb["tail"]]))
        eb.head=a
        eb.tail=b if (b-a).length>.0002 else a+Vector((0,0,.001))
        ids=spec["planes"][bb["rotation_plane"]]
        p,q,r=(Vector(joints[i]) for i in ids)
        n=(q-p).cross(r-p)
        if n.length>.00000001:
            eb.align_roll(n.normalized())
        eb.use_deform=name in weights
    for name,bb in spec["bones"].items():
        if bb["parent"]:
            eb=data.edit_bones[name]
            parent=data.edit_bones[bb["parent"]]
            eb.parent=parent
            eb.use_connect=(parent.tail-eb.head).length<.0001
    bpy.ops.object.mode_set(mode="OBJECT")
    collections={name:data.collections.new(name) for name in ("Corps · FK","Doigts","Visage · déformation","Os intermédiaires")}
    major=("clavicle","shoulder01","upperarm01","lowerarm01","wrist","pelvis","upperleg01",
           "lowerleg01","foot","head","neck01","spine01","spine02","spine03","root")
    facial=("eye","jaw","oculi","oris","temporalis","levator","risorius","orbicularis","tongue")
    for bone in data.bones:
        name=bone.name
        if name.startswith(major):
            key="Corps · FK"
        elif name.startswith(("finger","metacarpal")):
            key="Doigts"
        elif name.startswith(facial):
            key="Visage · déformation"
        else:
            key="Os intermédiaires"
        collections[key].assign(bone)
    for name,c in collections.items():
        c.is_visible=(name=="Corps · FK")
    sums=np.zeros(len(remap))
    for pairs in weights.values():
        for index,value in pairs:
            if index in remap:
                sums[remap[index]]+=value
    for name,pairs in weights.items():
        vg=body.vertex_groups.new(name=name)
        for index,value in pairs:
            if index in remap and value>0:
                i=remap[index]
                vg.add([i],value/sums[i],"REPLACE")
    missing=np.flatnonzero(sums<=0)
    if len(missing):
        vg=body.vertex_groups.get("root") or body.vertex_groups.new(name="root")
        vg.add(missing.tolist(),1,"REPLACE")
        data.bones["root"].use_deform=True
    print("WEIGHTS",len(weights),"fallback",len(missing))
    mod=body.modifiers.new("Déformation du squelette","ARMATURE")
    mod.object=rig
    mod.use_deform_preserve_volume=True
    body.parent=rig
    sub=body.modifiers.new("Subdivision de présentation","SUBSURF")
    sub.levels=1
    sub.render_levels=1
    return rig


def bind_to_head(ob,rig):
    ob.parent=rig
    group=ob.vertex_groups.new(name="head")
    group.add(list(range(len(ob.data.vertices))),1.0,"REPLACE")
    mod=ob.modifiers.new("Suivi de la tête","ARMATURE")
    mod.object=rig


def foot_cover(col,rig,sign,mat,solemat):
    # Draw a continuous closed boot shell from horizontal sections. One
    # material boundary defines the sole; the shell moves at the ankle.
    outlines=[
        (.008,-.173,.101,.061),(.022,-.176,.102,.062),(.038,-.174,.099,.061),
        (.061,-.153,.096,.059),(.096,-.108,.090,.058),(.137,-.074,.083,.058),
        (.167,-.061,.078,.056),(.179,-.052,.077,.055)
    ]
    count=40
    v=[]
    center=.123*sign
    for z,front,back,w in outlines:
        for k in range(count):
            a=math.tau*k/count
            c,s=math.cos(a),math.sin(a)
            exp=2/3.6
            v.append((center+w*math.copysign(abs(c)**exp,c),
                      (front+back)*.5+(back-front)*.5*math.copysign(abs(s)**exp,s),z))
    faces=[]
    for i in range(len(outlines)-1):
        for k in range(count):
            j=(k+1)%count
            faces.append((i*count+k,i*count+j,(i+1)*count+j,(i+1)*count+k))
    faces.extend((tuple(reversed(range(count))),tuple(range(len(v)-count,len(v)))))
    m=bpy.data.meshes.new("Volume raccordé de la botte")
    m.from_pydata(v,[],faces)
    m.update()
    obj=bpy.data.objects.new("Botte."+("L" if sign>0 else "R"),m)
    col.objects.link(obj)
    m.materials.append(mat);m.materials.append(solemat)
    for poly in m.polygons:
        poly.use_smooth=True
        poly.material_index=int(poly.index<2*count or poly.index==len(m.polygons)-2)
    vg=obj.vertex_groups.new(name="foot."+("L" if sign>0 else "R"))
    vg.add(list(range(len(m.vertices))),1,"REPLACE")
    obj.parent=rig
    mod=obj.modifiers.new("Cheville","ARMATURE");mod.object=rig
    sub=obj.modifiers.new("Arrondi botte","SUBSURF");sub.levels=sub.render_levels=2
    return obj


def eyes(col,rig):
    sx=L.material("Sclérotique",(.77,.72,.65),.25)
    brown=L.material("Iris brun",(.16,.073,.025),.25)
    black=L.material("Pupille",(.004,.005,.006),.22)
    for side in (-1,1):
        x=side*.0310
        z=(SOLE-93.8)*UNIT
        for name,y,size,material in (
            ("Globe",-.055,(.0134,.0178,.0136),sx),
            ("Iris",-.0724,(.0044,.0019,.0045),brown),
            ("Pupille",-.0739,(.0019,.0007,.0021),black)):
            ob=L.sphere(f"{name}.{side:+d}",col,material,location=(x,y,z),segments=32,ring_count=16)
            ob.scale=size
            bind_to_head(ob,rig)


def apply_mask(obj, name, values, blend=.022):
    vg=obj.vertex_groups.new(name=name)
    k=np.clip(.5+values/blend,0,1)
    for i,w in enumerate(k):
        if w>0:
            vg.add([i],float(w),"REPLACE")
    mask=obj.modifiers.new(name,"MASK")
    mask.vertex_group=vg.name
    mask.threshold=.5
    mask.use_smooth=True
    obj.modifiers.move(len(obj.modifiers)-1,0)


def garments(body,collection):
    # Reuse the weighted topology and its UV layout. Interpolate the hem
    # between vertices before subdivision so the edge follows the cut.
    xyz=np.array([tuple(v.co) for v in body.data.vertices])
    x,y,z=xyz.T
    normal=np.array([tuple(v.normal) for v in body.data.vertices])
    lower=1.045+.258*smoother(abs(x),.133,.170)
    upper=1.505+.075*smoother(y,-.044,.075)+.13*smoother(abs(x),.055,.095)
    shirt=np.minimum(z-lower,upper-z)
    pants=np.minimum.reduce((1.058-z,z-.137,.216-abs(x)))
    fabrics=(
        ("Tee-shirt ajusté",shirt,(.060,.078,.118),.0042),
        ("Pantalon droit",pants,(.044,.042,.048),.0046),
    )
    for name,mask,rgb,offset in fabrics:
        ob=body.copy()
        ob.data=body.data.copy()
        ob.name=name
        collection.objects.link(ob)
        ob.data.materials.clear()
        fabric=L.material("Toile · "+name,rgb,.72)
        cloth=fabric.node_tree
        bsdf=next(n for n in cloth.nodes if n.type=="BSDF_PRINCIPLED")
        bsdf.inputs["Sheen Weight"].default_value=.22
        ob.data.materials.append(fabric)
        positions=xyz+normal*offset
        if name.startswith("Pantalon"):
            # Trousers keep a little ease over the shin and cover the ankle.
            radial=np.clip((.80-z)/.63,0,1)*np.clip((z-.116)/.12,0,1)
            positions[:,0]+=(x-np.sign(x)*.119)*radial*.55
            positions[:,1]+=(y-.020)*radial*.23
        ob.data.vertices.foreach_set("co",positions.astype(np.float32).flatten())
        ob.data.update()
        apply_mask(ob,"Coupe textile",mask)
        solid=ob.modifiers.new("Épaisseur textile","SOLIDIFY")
        solid.thickness=.0019
        solid.offset=-.1
    # Remove the visible toe geometry under the opaque boot shells.
    apply_mask(body,"Masquer le pied sous la botte",z-.150,blend=.035)


def pose_action(scene,rig):
    # Global armature-space axes converted to the local axes of each rest bone.
    frames={
        1:{},
        25:{"lowerarm01.L":((1,0,0),-52),"upperarm01.L":((0,1,0),-15),
            "upperleg01.R":((1,0,0),-18),"lowerleg01.R":((1,0,0),39),
            "head":((0,0,1),-9),"spine02":((0,0,1),6)},
        49:{"lowerarm01.R":((1,0,0),-47),"upperarm01.R":((0,1,0),17),
            "upperleg01.L":((1,0,0),-16),"lowerleg01.L":((1,0,0),36),
            "head":((0,0,1),10)},
        73:{},
    }
    names=sorted({name for pose in frames.values() for name in pose})
    for frame,pose in frames.items():
        for name in names:
            pb=rig.pose.bones[name]
            pb.rotation_mode="QUATERNION"
            if name in pose:
                axis,angle=pose[name]
                axis_local=pb.bone.matrix_local.to_3x3().inverted()@Vector(axis)
                from mathutils import Quaternion
                pb.rotation_quaternion=Quaternion(axis_local,math.radians(angle))
            else:
                pb.rotation_quaternion=(1,0,0,0)
            pb.keyframe_insert(data_path="rotation_quaternion",frame=frame,group=name)
    rig.animation_data.action.name="Test FK · coude et genou"
    scene.frame_end=73
    for name,frame in (("Repos",1),("Bras G et genou D",25),("Bras D et genou G",49),("Repos",73)):
        scene.timeline_markers.new(name,frame=frame)
    scene.frame_set(1)


def main():
    L.reset("Personnage · corps, UV et rig")
    geo=L.collection("01 · Corps et accessoires")
    rig_col=L.collection("02 · Armature FK")
    ref=L.collection("03 · Gabarits")
    studio=L.collection("04 · Studio")
    src=bpy.data.images.load(str(ROOT/"planche_source.png"))
    pixels=np.empty(1536*1024*4,dtype=np.float32)
    src.pixels.foreach_get(pixels)
    pixels=pixels.reshape((1024,1536,4))[::-1]
    for rect,is_side,name in ((FRONT,False,"reference_face"),(SIDE,True,"reference_profil")):
        image=bpy.data.images.load(str(ROOT/(name+".png")))
        image.pack()
        guide_image(image,rect,is_side,ref)
    raw,faces=read_template()
    world=body_fit(raw,faces,pixels)
    body,remap=make_body(raw,faces,world,pixels,geo)
    scene=bpy.context.scene
    bake_atlas(scene,body)
    rig=rig_body(body,remap,world,rig_col)
    eyes(geo,rig)
    garments(body,geo)
    mat=L.material("Cuir anthracite",(.039,.046,.056),.57)
    sole=L.material("Semelle graphite",(.018,.021,.025),.73)
    for sign in (-1,1):
        foot_cover(geo,rig,sign,mat,sole)
    pose_action(scene,rig)

    target=(0,0,.91)
    front=camera(studio,"CAM_Face",(0,-4,.91),target,2.04)
    front.data.clip_end=100
    camera(studio,"CAM_Profil",(4,0,.91),target,2.04)
    angle=camera(studio,"CAM_Trois_Quarts",(2.55,-5.6,1.75),target,2.11)
    L.world((.16,.20,.27),.48)
    for name,pos,power,size in (("Key",(-2,-3,4),380,3),("Fill",(2,-2,2.25),125,2.4),
                                ("Rim",(1.6,2,3.2),400,2)):
        lamp=L.light(name,studio,location=pos,energy=power,size=size)
        lamp.rotation_euler=(Vector(target)-lamp.location).to_track_quat("-Z","Y").to_euler()
    floor=L.plane("Fond",studio,L.material("Fond ardoise",(.072,.100,.133),.74),size=200)
    floor.location.z=0
    scene.unit_settings.system="METRIC"
    scene.cycles.samples=24
    scene.cycles.use_denoising=True
    scene.render.resolution_x=760
    scene.render.resolution_y=1040
    scene.render.resolution_percentage=100
    scene.render.image_settings.file_format="PNG"
    scene.camera=angle
    scene.render.filepath="//personnage_neutre.png"
    select_only(rig)
    for screen in bpy.data.screens:
        for area in screen.areas:
            if area.type=="VIEW_3D":
                area.spaces.active.region_3d.view_perspective="CAMERA"
    note=bpy.data.texts.new("LIRE · Corps, UV, rig")
    note.write("Image 1 : repos. Images 25 et 49 : poses FK de contrôle. Le corps possède des UV MakeHuman et un atlas couleur 2048 intégré. Le tee-shirt et le pantalon sont des coques UV et skinnées sur la même armature. L’atlas couleur du corps est intégré. Maillage, morphotype, UV, os et poids d’origine MakeHuman sous CC0 ; proportions et pose ajustées aux gabarits. Les collections de doigts, visage et os intermédiaires sont disponibles dans les propriétés de l’armature.")
    L.save(str(ROOT/"personnage_corps_uv_rig.blend"))
    bpy.ops.render.render(write_still=True)
    scene.frame_set(25)
    scene.render.filepath="//personnage_pose_fk.png"
    bpy.ops.render.render(write_still=True)


if __name__=="__main__":
    L.run(main)
