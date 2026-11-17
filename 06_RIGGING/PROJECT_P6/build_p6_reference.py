"""
build_p6_reference.py — Produit la RÉFÉRENCE du projet P6 « Un personnage contrôlable » à partir du personnage de CH06.05 (CHR_Hero_Body du projet P3, rig Rigify RIG_Hero, 706 bones).

Ajouts de la référence :
  - une Action de TEST DE POSE « P6_PoseTest » sur RIG_Hero : image 1 = repos ; image 24 = pied gauche levé de 0,25 m (foot_ik.L) et tête tournée de 30° (head, rotation Euler) ;
  - la planche renders/p6_posetest.png : trois images (1, 12, 24) de la caméra CAM_Front (EEVEE), côte à côte (1 920 px de large).
Le fichier source est COMPLETED_EXAMPLES/ch06_05_humanoid_solution.blend : regénérez-le d'abord (build_ch06_05_files.py) si vous modifiez CH06.05.
Limite (héritée de CH06.05) : le méta-rig humain a les bras en T alors que le mannequin les a en A : les bras ne sont pas alignés ; le projet teste la racine, les jambes et la tête.
Usage : blender -b --factory-startup --python-exit-code 1 --python build_p6_reference.py
Testé avec : Blender 5.3.0.
"""
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bpy  # noqa: E402
import numpy as np  # noqa: E402
from mathutils import Vector  # noqa: E402

SRC = os.path.join(HERE, "..", "CH06_05_HUMANOID", "COMPLETED_EXAMPLES", "ch06_05_humanoid_solution.blend")
OUT = os.path.join(HERE, "REFERENCE")


def main():
    bpy.ops.wm.open_mainfile(filepath=os.path.abspath(SRC))
    rig = bpy.data.objects["RIG_Hero"]
    sc = bpy.context.scene
    if rig.animation_data and rig.animation_data.action:
        rig.animation_data.action = None
    pb = rig.pose.bones
    pb["head"].rotation_mode = "XYZ"
    foot = pb["foot_ik.L"]
    rest_loc = tuple(foot.location)
    for f in (1, 24):
        sc.frame_set(f)
        if f == 1:
            foot.location = rest_loc
            pb["head"].rotation_euler = (0, 0, 0)
        else:
            foot.location = foot.bone.matrix_local.to_3x3().inverted() @ Vector((0, 0, 0.25))
            pb["head"].rotation_euler = (0, math.radians(30), 0)
        foot.keyframe_insert("location", frame=f)
        pb["head"].keyframe_insert("rotation_euler", frame=f)
    act = rig.animation_data.action
    act.name = "P6_PoseTest"
    # les images clés doivent exister aux images 1 et 24 ; interpolation linéaire pour une lecture simple
    try:
        fcs = list(act.fcurves)
    except AttributeError:
        fcs = []
    for fc in fcs:
        for kp in fc.keyframe_points:
            kp.interpolation = "LINEAR"
    sc.render.resolution_x, sc.render.resolution_y = 640, 900
    sc.render.resolution_percentage = 100
    sc.render.engine = "BLENDER_EEVEE"
    sc.camera = bpy.data.objects["CAM_Front"]
    cam = sc.camera
    cam.location = (0.0, -4.4, 0.95)
    sc.render.image_settings.file_format = "PNG"
    tiles = []
    for f in (1, 12, 24):
        sc.frame_set(f)
        path = os.path.join(OUT, "renders", f"_tmp_{f}.png")
        sc.render.filepath = path
        bpy.ops.render.render(write_still=True)
        img = bpy.data.images.load(path)
        a = np.array(img.pixels[:], np.float32).reshape(img.size[1], img.size[0], 4)
        tiles.append(a)
        bpy.data.images.remove(img)
        os.remove(path)
    sheet = np.concatenate(tiles, axis=1)
    out = bpy.data.images.new("sheet", sheet.shape[1], sheet.shape[0], alpha=False)
    out.pixels = sheet.ravel()
    out.filepath_raw = os.path.join(OUT, "renders", "p6_posetest.png")
    out.file_format = "PNG"
    out.save()
    sc.frame_set(1)
    L.save(os.path.join(OUT, "p6_character_reference.blend"))


if __name__ == "__main__":
    L.run(main)
