"""Publish and round-trip the existing fitted full character for the chapter."""
import json
import sys
from pathlib import Path

import bpy
from mathutils import Vector

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
OUT=HERE/"assets"/"projet_humain"
sys.path.insert(0,str(ROOT/"SCRIPTS"))
import bcma_lib as L


def bounds(subjects):
    deps=bpy.context.evaluated_depsgraph_get()
    coords=[]
    for ob in subjects:
        ev=ob.evaluated_get(deps)
        coords.extend(ev.matrix_world @ v.co for v in ev.data.vertices)
    return [min(v.z for v in coords), max(v.z for v in coords)]


def choose(scene, name):
    scene.camera=bpy.data.objects[name]


def still(scene,name):
    scene.render.filepath=str(OUT/f"{name}.png")
    bpy.ops.render.render(write_still=True)


def main():
    OUT.mkdir(parents=True,exist_ok=True)
    bpy.ops.wm.open_mainfile(filepath=str(ROOT/"PROPOSITIONS/RECONSTRUCTION_2_VUES/personnage_final_pieds_ajustes.blend"))
    scene=bpy.context.scene
    rig=bpy.data.objects["RIG_Personnage_FK"]
    scene.frame_set(1)
    rig["Pieds IK"]=0.0
    rig.update_tag()
    bpy.context.view_layer.update()
    mesh=[ob for ob in scene.objects if ob.type=="MESH" and
          any(m.type=="ARMATURE" and m.object==rig for m in ob.modifiers)]
    h=bounds(mesh)
    original=[i for i in bpy.data.images if i.name.startswith("reference_")]
    assert len(original)==2 and all(i.packed_file for i in original)
    assert bpy.data.images["Peau finale · 2048"].packed_file
    note=bpy.data.texts.new("LIRE · Projet final du cours")
    note.write("Démonstration avancée à partir de deux gabarits synthétiques, fondée sur MakeHuman (CC0). Pose neutre image 1, poses de contrôle 25 et 49. Utilisez les photos autorisées de votre choix pour votre propre projet et le tutoriel pour construire votre cage. Le GLB vérifié exporte les déformations FK et les matériaux principaux. Les contrôleurs et les finitions procédurales restent dans ce fichier Blender.")
    L.save(str(OUT/"personnage_source.blend"))
    bpy.ops.object.select_all(action="DESELECT")
    for ob in [rig]+mesh:
        ob.select_set(True)
    bpy.context.view_layer.objects.active=rig
    target=OUT/"personnage.glb"
    bpy.ops.export_scene.gltf(filepath=str(target),export_format="GLB",
                              use_selection=True,export_apply=True,
                              export_animations=True,export_skins=True,export_morph=False,
                              export_animation_mode="SCENE")
    scene.render.engine="CYCLES"
    scene.cycles.samples=12
    scene.cycles.use_denoising=True
    scene.render.resolution_x=540
    scene.render.resolution_y=660
    scene.render.resolution_percentage=100
    scene.render.image_settings.media_type="IMAGE"
    scene.render.image_settings.file_format="PNG"
    for cam,name,frame in (("CAM_Face","face",1),("CAM_Profil","profil",1),
                            ("CAM_Trois_Quarts","trois_quarts",1),
                            ("CAM_Trois_Quarts","pose_01",25),("CAM_Trois_Quarts","pose_02",49)):
        scene.frame_set(frame)
        choose(scene,cam)
        still(scene,name)

    bpy.ops.wm.read_factory_settings(use_empty=True)
    for obj in list(bpy.context.scene.objects):
        bpy.data.objects.remove(obj, do_unlink=True)
    bpy.ops.import_scene.gltf(filepath=str(target))
    scene=bpy.context.scene
    skeletons=[o for o in scene.objects if o.type=="ARMATURE"]
    imported=[o for o in scene.objects if o.type=="MESH"]
    skinned=[o for o in imported if any(m.type=="ARMATURE" for m in o.modifiers)]
    assert len(skeletons)==1 and len(skinned)>=8
    assert len(bpy.data.actions)>0
    rig=skeletons[0]
    scene.frame_set(1)
    k=bounds(skinned)
    assert abs((k[1]-k[0])-(h[1]-h[0]))<.03,(h,k)
    probe=next(o for o in skinned if o.name == "GEO_Personnage")
    def coords(f):
        scene.frame_set(f)
        dep=bpy.context.evaluated_depsgraph_get()
        return [v.co.copy() for v in probe.evaluated_get(dep).data.vertices]
    rest=coords(1)
    disps=[max((a-b).length for a,b in zip(rest,coords(f))) for f in (25,49)]
    assert min(disps)>.05,disps
    assert any(m.use_nodes and any(n.type=="TEX_IMAGE" and n.image and n.image.size[0] > 0
               for n in m.node_tree.nodes) for m in bpy.data.materials)
    scene.frame_set(1)
    bpy.ops.file.pack_all()
    bpy.ops.object.select_all(action="DESELECT")
    rig.select_set(True)
    bpy.context.view_layer.objects.active=rig
    for scr in bpy.data.screens:
        for area in scr.areas:
            if area.type=="VIEW_3D":
                r=area.spaces.active.region_3d
                r.view_location=(0,0,.91)
                r.view_distance=2.6
                r.view_rotation=Vector((.3,-1,.08)).to_track_quat("Z","Y")
                r.view_perspective="ORTHO"
                area.spaces.active.shading.color_type="MATERIAL"
    L.save(str(OUT/"verification_import.blend"))
    report={"version_blender":bpy.app.version_string,"format":"glTF 2.0 / GLB",
            "hauteur_source_m":round(h[1]-h[0],4),"hauteur_import_m":round(k[1]-k[0],4),
            "maillages_exportes":len(mesh),"maillages_pondérés":len(skinned),"os":len(rig.data.bones),
            "actions":len(bpy.data.actions),"deplacement_max_m_sur_le_corps":[round(v,4) for v in disps],
            "images_importees":[i.name for i in bpy.data.images if i.size[0] > 0]}
    (OUT/"verification.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print("REIMPORT",report)


if __name__=="__main__":
    L.run(main)
