"""Fit the anatomical foot and ankle to the low shoe in the previous Blender file."""
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
from fit_shoes import smooth
from build_body_uv_rig import select_only


def fit_feet(body,rig,shoes):
    masks=[m for m in body.modifiers if m.type=="MASK" and m.vertex_group=="Masquer le pied sous la botte"]
    for mod in masks:
        body.modifiers.remove(mod)
    deps=bpy.context.evaluated_depsgraph_get()
    trees={s:BVHTree.FromObject(shoe,deps) for s,shoe in shoes.items()}
    records=[]
    deform={b.name for b in rig.data.bones if b.use_deform}
    names={i:g.name for i,g in enumerate(body.vertex_groups)}
    for vert in body.data.vertices:
        x,y,z=vert.co
        if z>.306 or abs(x)<.04:
            continue
        sign=1 if x>0 else -1
        side="L" if sign>0 else "R"
        relative=abs(x)-.129

        # A softer heel, shaped instep and a wider forefoot inside the shoe.
        # The transition back to the original shin is continuous.
        foot=1-smooth((z-.096)/.095)
        fore=smooth((-y-.037)/.112)
        midheel=smooth((y+.028)/.075)
        qy=y+foot*(-.004*fore+.018*midheel)
        qx=abs(x)+(foot*(.16+.38*fore))*relative
        depth_scale=.48+.28*smooth((y+.158)/.079)+.22*smooth((y+.073)/.061)
        compression=(1-depth_scale)*(1-smooth((z-.115)/.071))
        qz=z+(.019+(z-.014)*depth_scale-z)*foot
        qz-=.020*compression*smooth((-y-.055)/.063)

        # The medial and lateral ankle bones emerge at different heights.
        # Keep the Achilles slim at the back and preserve the calf above.
        ankle=math.exp(-((z-.168)/.040)**2)
        side_fraction=smooth((abs(relative)-.007)/.014)
        y_focus=math.exp(-((y-.015)/.033)**2)
        inner=relative<0
        bone_z=.165 if inner else .150
        mal=math.exp(-((z-bone_z)/.014)**2)
        qx+=math.copysign(side_fraction*y_focus*(.0037*mal-.0021*ankle),relative)
        qy+=.0041*ankle*math.exp(-(relative/.011)**2)*smooth((y-.030)/.019)
        qy+=.0085*ankle*smooth((-y-.021)/.039)

        # Seat the instep behind the tongue and taper the skin into the
        # measured collar opening. Outside the opening the foot must lie
        # below the fabric, including on the sloping quarter panels.
        if .072<qz<.172:
            front_limit=-.039-.053*(1-smooth((qz-.074)/.030))
            limit_mix=1-smooth((qz-.144)/.028)
            qy+=max(0,front_limit-qy)*limit_mix
            mouth=(smooth((qz-.072)/.019)*(1-smooth((qz-.116)/.041)))
            cx,cy=.135,.010
            px=(qx-cx)/.029
            py=(qy-cy)/.045
            radial=(abs(px)**2.4+abs(py)**2.4)**(1/2.4)
            if radial>1:
                qx+=(cx+(qx-cx)/radial-qx)*mouth
                qy+=(cy+(qy-cy)/radial-qy)*mouth

        # Measure the actual upper at the proposed footprint. Leave a small
        # skin-to-upper gap, but retain the natural toes in the body mesh.
        if qy<-.051 and z<.145:
            surface,normal,idx,dist=trees[side].ray_cast(Vector((sign*qx,qy,.29)),Vector((0,0,-1)),.30)
            if surface is None:
                qx=qx*.74+.129*.26
                surface,normal,idx,dist=trees[side].ray_cast(Vector((sign*qx,qy,.29)),Vector((0,0,-1)),.30)
            if surface is not None:
                strength=smooth((-.043-qy)/.010)*(1-smooth((z-.139)/.018))
                maximum=surface.z-.0032
                minimum=.016
                qz+=strength*(max(minimum,min(qz,maximum))-qz)
                if strength>.97:
                    records.append((side,qy,max(0.0,surface.z-qz)))

        vert.co=(sign*qx,qy,qz)
        influence=1-smooth((qz-.093)/.077)
        if influence>.0005:
            group=body.vertex_groups["foot."+side]
            current={names[w.group]:w.weight for w in list(vert.groups) if names[w.group] in deform}
            for name,value in current.items():
                if name!=group.name:
                    scaled=value*(1-influence)
                    if scaled>1e-6:
                        body.vertex_groups[name].add([vert.index],scaled,"REPLACE")
                    else:
                        body.vertex_groups[name].remove([vert.index])
            initial=current.get(group.name,0)
            group.add([vert.index],initial*(1-influence)+influence,"REPLACE")

    # Carry the same ankle edits into the expression shape keys; those keys
    # must never bring back the previous foot when the smile slider is used.
    if body.data.shape_keys:
        keys=body.data.shape_keys.key_blocks
        basis=keys[0]
        for vert in body.data.vertices:
            if vert.co.z<=.309 and abs(vert.co.x)>.04:
                i=vert.index
                delta=vert.co-basis.data[i].co
                for key in keys:
                    key.data[i].co+=delta
    body.data.update()
    for side in "LR":
        vals=[r[2] for r in records if r[0]==side]
        assert len(vals)>50
        print("AJUSTEMENT",side,len(vals),"points sous l’avant",round(min(vals)*1000,2),
              round(sum(vals)/len(vals)*1000,2),"mm min/moyen")


def cutaway(shoe):
    # Camera on the outer side of the left foot. Make only its near side
    # transparent in the inspection image without changing the saved model.
    for slot in shoe.material_slots:
        copy=slot.material.copy()
        slot.material=copy
        nt=copy.node_tree
        out=next(n for n in nt.nodes if n.type=="OUTPUT_MATERIAL")
        previous=out.inputs["Surface"].links[0].from_socket
        g=nt.nodes.new("ShaderNodeNewGeometry")
        xyz=nt.nodes.new("ShaderNodeSeparateXYZ")
        nt.links.new(g.outputs["Position"],xyz.inputs[0])
        threshold=nt.nodes.new("ShaderNodeMath")
        threshold.operation="GREATER_THAN"
        nt.links.new(xyz.outputs["X"],threshold.inputs[0])
        threshold.inputs[1].default_value=.131
        transparent=nt.nodes.new("ShaderNodeBsdfTransparent")
        mix=nt.nodes.new("ShaderNodeMixShader")
        nt.links.new(threshold.outputs[0],mix.inputs[0])
        nt.links.new(previous,mix.inputs[1])
        nt.links.new(transparent.outputs[0],mix.inputs[2])
        nt.links.new(mix.outputs[0],out.inputs["Surface"])


def main():
    bpy.ops.wm.open_mainfile(filepath=str(ROOT/"personnage_final_chaussures.blend"))
    scene=bpy.context.scene
    scene.frame_set(1)
    body=bpy.data.objects["GEO_Personnage"]
    rig=bpy.data.objects["RIG_Personnage_FK"]
    pants=bpy.data.objects["Pantalon droit"]
    shoes={s:bpy.data.objects["Chaussure."+s] for s in "LR"}
    fit_feet(body,rig,shoes)
    mask_values(pants,"Coupe textile",lambda p:min(1.072-p.z,p.z-(.148-.012*smooth((p.y+.045)/.12)),.216-abs(p.x)),.022)
    print("CONTACT",verify_floor(scene,[shoes["R"],shoes["L"]]))
    full=bpy.data.objects["CAM_Trois_Quarts"]
    cam=bpy.data.objects["CAM_Détail_Chaussures"]
    cam.location=(.83,-1.39,.418)
    cam.rotation_euler=(Vector((0,-.020,.15))-cam.location).to_track_quat("-Z","Y").to_euler()
    cam.data.ortho_scale=.63
    scene.camera=full
    scene.render.filepath="//personnage_pieds_ajustes.png"
    select_only(rig)
    note=bpy.data.texts.new("LIRE · Pieds ajustés")
    note.write("Le pied anatomique restauré reste continu avec la jambe et dans la chaussure. Le volume de l’avant est ajusté à la tige mesurée. Les poids sous le chaussant suivent le pied. Les malléoles et l’Achille ont été repris, avec un ourlet qui dégage la cheville. Les deux modes de rig sont conservés.")
    L.save(str(ROOT/"personnage_final_pieds_ajustes.blend"))
    scene.camera=cam
    scene.render.resolution_x=950
    scene.render.resolution_y=650
    scene.render.filepath="//pieds_ajustes_detail.png"
    bpy.ops.render.render(write_still=True)
    scene.frame_set(25)
    scene.render.filepath="//pieds_ajustes_pose.png"
    bpy.ops.render.render(write_still=True)
    scene.frame_set(1)
    cam.location=(.88,-.19,.33)
    cam.rotation_euler=(Vector((.127,-.044,.099))-cam.location).to_track_quat("-Z","Y").to_euler()
    cam.data.ortho_scale=.41
    cutaway(shoes["L"])
    for name in ("Lacets.L","Surpiqûres.L","Chaussure.R","Lacets.R","Surpiqûres.R"):
        bpy.data.objects[name].hide_render=True
    scene.render.filepath="//pied_chaussure_coupe.png"
    bpy.ops.render.render(write_still=True)


if __name__=="__main__":
    L.run(main)
