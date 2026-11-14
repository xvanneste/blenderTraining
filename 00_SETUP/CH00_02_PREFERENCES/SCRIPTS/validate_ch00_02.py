"""
validate_ch00_02.py — Correcteur de l'exercice 3 de CH00.02 (cadrer l'aiguille).

Usage :
  blender -b --factory-startup <fichier.blend> --python validate_ch00_02.py --python-exit-code 1 -- --exercise needle [--render]
Vérifie que CAM_Needle est la caméra active, qu'elle est proche de l'aiguille (< 3 m),
que l'aiguille est dans le cadre et occupe une part visible de l'image.
Testé avec : Blender 5.3.0.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bpy  # noqa: E402
from bpy_extras.object_utils import world_to_camera_view  # noqa: E402


def main():
    sc = bpy.context.scene
    r = L.Report("CH00.02 — Cadrer l'aiguille")
    cam, needle = L.obj("CAM_Needle"), L.obj("GEO_Needle")
    r.check(cam and needle, "Objets CAM_Needle et GEO_Needle présents", "Ne renommez pas les objets du fichier.", 1)
    if not (cam and needle):
        return r.finish()
    r.check(sc.camera == cam, "CAM_Needle est la caméra active",
            "Sélectionnez CAM_Needle puis View > Cameras > Set Active Object as Camera (Ctrl+Num 0)", 2)
    dist = (cam.matrix_world.translation - needle.matrix_world.translation).length
    r.check(dist < 3.0, f"Caméra proche de l'aiguille ({dist:.2f} m < 3 m)",
            "Naviguez jusqu'à l'aiguille puis Ctrl+Alt+Num 0 (Align Active Camera to View)", 2)
    p = world_to_camera_view(sc, cam, needle.matrix_world.translation)
    inside = 0 <= p.x <= 1 and 0 <= p.y <= 1 and p.z > 0
    r.check(inside, f"Aiguille dans le cadre (x={p.x:.2f}, y={p.y:.2f})",
            "L'aiguille doit être visible dans la vue caméra (Num 0)", 2)
    from mathutils import Vector
    zs = [v[2] for v in needle.bound_box]
    top = needle.matrix_world @ Vector((0, 0, max(zs)))
    bottom = needle.matrix_world @ Vector((0, 0, min(zs)))
    pt, pb = world_to_camera_view(sc, cam, top), world_to_camera_view(sc, cam, bottom)
    size = abs(pt.y - pb.y)
    r.check(size > 0.15, f"Aiguille en gros plan ({size * 100:.0f} % de la hauteur d'image > 15 %)",
            "Rapprochez la caméra ou augmentez la focale (Object Data > Lens > Focal Length)", 2)
    if L.flag("--render"):
        lum = L.quick_render(15, 4)
        r.check(lum > 0.02, f"Rendu de contrôle non noir ({lum:.3f})", "", 1)
    return r.finish()


if __name__ == "__main__":
    L.run(main)
