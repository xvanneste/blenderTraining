"""
validate_ch01_02.py — Correcteur de l'exercice 3 de CH01.02 (trois caméras orthographiques).
Usage : blender -b --factory-startup <fichier.blend> --python-exit-code 1 --python validate_ch01_02.py -- --exercise cameras
Testé avec : Blender 5.3.0.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bpy  # noqa: E402
from bpy_extras.object_utils import world_to_camera_view  # noqa: E402
from mathutils import Vector  # noqa: E402

EXPECT = {"CAM_Front": (Vector((0, 1, 0)), "Num 1 (vue de face) puis Ctrl+Alt+Num 0"),
          "CAM_Right": (Vector((-1, 0, 0)), "Num 3 (vue de droite) puis Ctrl+Alt+Num 0"),
          "CAM_Top": (Vector((0, 0, -1)), "Num 7 (vue de dessus) puis Ctrl+Alt+Num 0")}


def main():
    r = L.Report("CH01.02 — Trois caméras orthographiques")
    sc = bpy.context.scene
    bpy.context.view_layer.update()
    statue = L.obj("GEO_Statue")
    corners = [statue.matrix_world @ Vector(c) for c in statue.bound_box]
    for name, (fwd, hint) in EXPECT.items():
        cam = L.obj(name)
        if not r.check(cam is not None, f"{name} présente", "Ne supprimez pas les caméras.", 1):
            continue
        d = cam.matrix_world.to_quaternion() @ Vector((0, 0, -1))
        r.check(d.dot(fwd) > 0.98, f"{name} : bonne direction de visée", hint, 2)
        r.check(cam.data.type == "ORTHO", f"{name} : orthographique", "Object Data (caméra) > Lens > Type = Orthographic", 1)
        pts = [world_to_camera_view(sc, cam, c) for c in corners]
        inside = all(0 <= p.x <= 1 and 0 <= p.y <= 1 and p.z > 0 for p in pts)
        r.check(inside, f"{name} : statue entièrement dans le cadre", "Augmentez Orthographic Scale ou recentrez la caméra.", 1)
        span = max(max(p.x for p in pts) - min(p.x for p in pts), max(p.y for p in pts) - min(p.y for p in pts))
        r.check(span > 0.35, f"{name} : statue bien cadrée ({span * 100:.0f} % du cadre > 35 %)",
                "Réduisez Orthographic Scale pour que la statue remplisse mieux l'image.", 1)
    return r.finish()


if __name__ == "__main__":
    L.run(main)
