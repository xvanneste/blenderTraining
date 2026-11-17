"""Reference geometry for the practical modeling track. Run with Blender 5.3 in background."""
from pathlib import Path
import math
import sys

import bpy
from mathutils import Vector

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "SCRIPTS"))
import bcma_lib as L


def bevel(obj, radius):
    mod = obj.modifiers.new("Biseaux", "BEVEL")
    mod.width, mod.segments = radius, 3
    obj.modifiers.new("Normales pondérées", "WEIGHTED_NORMAL")
    return obj


def box(name, dims, loc, mat, radius=.005):
    ob = L.cube(name, mat=mat, size=1, location=loc)
    ob.dimensions = dims
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    return bevel(ob, radius) if radius else ob


def mesh(name, verts, faces, mat):
    data = bpy.data.meshes.new(name)
    data.from_pydata(verts, [], faces)
    data.update()
    ob = bpy.data.objects.new(name, data)
    bpy.context.scene.collection.objects.link(ob)
    data.materials.append(mat)
    return ob


def shell(name, w, d, h, inset, floor, mat):
    contours = [(w/2,d/2,0), (w/2,d/2,h), (w/2-inset,d/2-inset,h),
                (w/2-inset,d/2-inset,floor)]
    v = [(x*s,y*t,z) for x,y,z in contours for s,t in ((-1,-1),(1,-1),(1,1),(-1,1))]
    f = [(3,2,1,0)]
    for a in range(3):
        for i in range(4):
            j = (i+1)%4
            f.append((a*4+i,a*4+j,(a+1)*4+j,(a+1)*4+i))
    f.append((12,13,14,15))
    return bevel(mesh(name,v,f,mat), .003)


def crate(wood, dark, metal):
    shell("Cuve creuse", .60,.40,.38,.025,.04,wood)
    for y in (-.205,.205):
        for z in (.074,.19,.306):
            box("Latte",(.58,.015,.101),(0,y,z),wood,.003)
        for x in (-.25,.25):
            box("Renfort",(.055,.023,.365),(x,y*1.060,.184),dark,.003)
    return .18,1.00


def table(wood, dark, metal):
    box("Plateau",(1.20,.72,.05),(0,0,.715),wood,.012)
    for x in (-.50,.50):
        for y in (-.26,.26):
            box("Pied",(.065,.065,.69),(x,y,.345),dark,.006)
    for y in (-.26,.26):
        box("Traverse",(1.0,.035,.09),(0,y,.645),dark,.003)
    return .37,1.72


def chair(wood, dark, metal):
    box("Assise",(.43,.43,.04),(0,0,.43),wood,.012)
    for x in (-.177,.177):
        box("Pied avant",(.057,.057,.41),(x,-.175,.205),dark,.006)
        levels=[(0,.177),(.41,.177),(.80,.247)]
        v=[(x+sx*.028,y+sy*.028,z) for z,y in levels for sx,sy in ((-1,-1),(1,-1),(1,1),(-1,1))]
        f=[(3,2,1,0),(8,9,10,11)]
        for row in (0,1):
            f.extend((row*4+k,row*4+(k+1)%4,(row+1)*4+(k+1)%4,(row+1)*4+k) for k in range(4))
        bevel(mesh("Pied et montant arrière",v,f,dark),.005)
    for z in (.625,.746):
        box("Latte de dossier",(.36,.044,.060),(0,.177+(z-.41)*.18,z),wood,.006)
    return .40,1.13


def sword(wood, dark, metal):
    v = [(x,y,z) for z,w,r in ((.28,.061,.018),(.46,.064,.028),(.83,.049,.023),
                                (1.09,.028,.014),(1.22,.002,.002))
         for x,y in ((0,-r),(w,0),(0,r))]
    f=[(2,1,0),(12,13,14)]
    for row in range(4):
        for k in (0,1):
            f.append((row*3+k,row*3+k+1,(row+1)*3+k+1,(row+1)*3+k))
    blade=mesh("Demi-lame · Mirror",v,f,metal)
    m=blade.modifiers.new("Symétrie X","MIRROR")
    m.use_clip=True
    bevel(blade,.0026)
    box("Garde",(.25,.062,.065),(0,0,.273),dark,.013)
    box("Poignée",(.072,.058,.175),(0,0,.153),wood,.013)
    for i in range(5):
        box("Rainure de prise",(.076,.061,.008),(0,0,.093+i*.026),dark,.0025)
    box("Pommeau",(.124,.073,.070),(0,0,.035),dark,.013)
    return .61,1.70


def chest(wood, dark, metal):
    shell("Cuve",.65,.42,.32,.025,.04,wood)
    pivot=L.empty("Axe du couvercle",bpy.context.scene.collection,location=(0,.21,.32))
    u = box("Couvercle",(.65,.42,.10),(0,0,.37),wood,.045)
    u.parent=pivot
    u.matrix_parent_inverse=pivot.matrix_world.inverted()
    for x in (-.225,.225):
        st=box("Ferrure du couvercle",(.044,.412,.012),(x,0,.419),dark,.004)
        st.parent=pivot
        st.matrix_parent_inverse=pivot.matrix_world.inverted()
        box("Renfort avant",(.044,.019,.282),(x,-.215,.16),dark,.004)
        box("Charnière",(.084,.036,.052),(x,.213,.30),metal,.006)
    box("Attache",(.073,.030,.093),(0,-.219,.28),metal,.008)
    pivot.rotation_euler.x=math.radians(-62)
    return .33,1.37


def house(wood, dark, metal):
    plaster=L.material("Enduit clair",(.78,.64,.46))
    roof=L.material("Tuile mate",(.47,.16,.093))
    blue=L.material("Vitrage",(.15,.34,.48))
    box("Maison · murs",(4,3,2.45),(0,0,1.225),plaster,.025)
    v=[(x,y,z) for y in (-1.68,1.68) for x,z in
       ((-2.16,2.40),(-2.16,2.58),(0,3.74),(2.16,2.58),(2.16,2.40))]
    f=[(4,3,2,1,0),(5,6,7,8,9)]
    f.extend((i,(i+1)%5,5+(i+1)%5,5+i) for i in range(5))
    bevel(mesh("Toit à deux versants",v,f,roof),.032)
    for x in (-1.27,1.27):
        box("Cadre fenêtre",(.65,.10,.86),(x,-1.52,1.36),wood,.025)
        box("Vitrage",(.49,.054,.69),(x,-1.572,1.36),blue,.014)
        box("Croisée",(.04,.03,.72),(x,-1.61,1.36),dark,.005)
    box("Porte",(.82,.09,1.85),(0,-1.52,.925),dark,.024)
    return 1.80, 6.3


def main():
    targets=set(L.args_after_dashdash())
    for name,builder in (("caisse",crate),("table",table),("chaise",chair),("epee",sword),("coffre",chest),("maison",house)):
        if targets and name not in targets:
            continue
        L.reset("Atelier · "+name)
        models=L.collection("Studio")
        wood=L.material("Bois miel",(.60,.32,.135))
        dark=L.material("Renfort brun",(.27,.13,.063))
        metal=L.material("Métal froid",(.44,.59,.69),metallic=.7)
        height,scale=builder(wood,dark,metal)
        scene=bpy.context.scene
        cam=L.camera("Caméra de comparaison",models,location=(.95*scale,-1.60*scale,.95*scale+height))
        cam.rotation_euler=(Vector((0,0,height))-cam.location).to_track_quat("-Z","Y").to_euler()
        cam.data.type="ORTHO"; cam.data.ortho_scale=scale
        L.plane("Fond",models,L.material("Fond crème",(.25,.30,.34)),size=200,location=(0,0,-.003))
        scene.unit_settings.system="METRIC"
        scene.render.engine="BLENDER_WORKBENCH"
        shading=scene.display.shading
        shading.color_type="MATERIAL"
        shading.show_shadows=True; shading.show_cavity=True
        shading.cavity_type="BOTH"
        scene.render.resolution_x=900;scene.render.resolution_y=680;scene.render.resolution_percentage=100
        scene.render.image_settings.file_format="PNG"
        scene.render.filepath="//"+name+".png"
        # Show the model in the 3D View immediately after opening it.
        for screen in bpy.data.screens:
            for area in screen.areas:
                if area.type=="VIEW_3D":
                    area.spaces.active.region_3d.view_perspective="CAMERA"
        L.save(str(HERE/"assets"/(name+".blend")))
        bpy.ops.render.render(write_still=True)


if __name__=="__main__":
    L.run(main)
