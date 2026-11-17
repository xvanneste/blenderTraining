"""
validate_ch01_12.py — Correcteur du portrait (CH01.12).
Usage : blender -b --factory-startup <fichier.blend> --python-exit-code 1 --python validate_ch01_12.py -- --exercise portrait [--render]
Testé avec : Blender 5.3.0.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bpy  # noqa: E402
from bpy_extras.object_utils import world_to_camera_view  # noqa: E402


def main():
    r = L.Report("CH01.12 — Le portrait du gardien")
    sc = bpy.context.scene
    bpy.context.view_layer.update()
    cam, head, lh = L.obj("CAM_Shot"), L.obj("EMP_Head"), L.obj("GEO_Lighthouse")
    if not r.check(cam and head and lh, "Objets présents", "", 1):
        return r.finish()
    r.check(sc.camera == cam, "CAM_Shot est la caméra active", "Ctrl+Num 0 sur CAM_Shot.", 1)
    r.check(cam.data.type == "PERSP" and 50 <= cam.data.lens <= 85, f"Focale portrait ({cam.data.lens:.0f} mm)",
            "Object Data > Lens > Focal Length entre 50 et 85.", 2)
    z = cam.matrix_world.translation.z
    dist = (cam.matrix_world.translation - head.matrix_world.translation).length
    r.check(1.4 <= z <= 1.9, f"Hauteur d'œil ({z:.2f} m)", "Placez la caméra entre 1,4 et 1,9 m.", 2)
    r.check(2 <= dist <= 6, f"Distance au sujet ({dist:.1f} m)", "Entre 2 et 6 m.", 1)
    p = world_to_camera_view(sc, cam, head.matrix_world.translation)
    third_y = abs(p.y - 2 / 3) < 0.07
    third_x = min(abs(p.x - 1 / 3), abs(p.x - 2 / 3)) < 0.07
    r.check(p.z > 0 and third_y, f"Tête sur le tiers supérieur (y = {p.y:.2f}, cible 0,67)",
            "Activez les guides Thirds et placez la tête sur la ligne horizontale du haut.", 3)
    r.check(p.z > 0 and third_x, f"Tête sur un tiers vertical (x = {p.x:.2f}, cible 0,33 ou 0,67)",
            "Décalez le cadrage pour mettre la tête sur une ligne verticale des tiers.", 3)
    q = world_to_camera_view(sc, cam, lh.matrix_world.translation)
    r.check(0 <= q.x <= 1 and 0 <= q.y <= 1 and q.z > 0, "Le phare est visible à l'arrière-plan",
            "Orientez la caméra pour garder le phare dans le cadre.", 2)
    dof = cam.data.dof
    r.check(dof.use_dof and dof.focus_object == head and dof.aperture_fstop <= 4,
            f"Profondeur de champ sur EMP_Head (f/{dof.aperture_fstop:.1f})",
            "Depth of Field coché, Focus on Object = EMP_Head, Aperture > F-Stop ≤ 4.", 3)
    if L.flag("--render"):
        lum = L.quick_render(15, 8)
        r.check(lum > 0.02, f"Rendu de contrôle non noir ({lum:.3f})", "", 1)
    return r.finish()


if __name__ == "__main__":
    L.run(main)
