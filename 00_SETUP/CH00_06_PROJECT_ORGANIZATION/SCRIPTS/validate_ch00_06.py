"""
validate_ch00_06.py — Correcteur « scène en désordre » (CH00.06).
Usage :
  blender -b --factory-startup <fichier.blend> --python validate_ch00_06.py --python-exit-code 1 -- --exercise naming
Testé avec : Blender 5.3.0.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bcma_naming_check as N  # noqa: E402
import bpy  # noqa: E402


def main():
    r = L.Report("CH00.06 — Conventions de nommage et chemins")
    meshes = [o for o in bpy.context.scene.objects if o.type == "MESH"]
    r.check(len(meshes) >= 5, f"Objets conservés ({len(meshes)} maillages)", "Ne supprimez pas d'objets.", 1)
    N.check(r, 3)
    names = {c.name for c in bpy.data.collections}
    r.check({"SET", "PROPS", "LIGHTS", "CAMERAS"} <= names, "Collections SET, PROPS, LIGHTS, CAMERAS présentes",
            "Renommez les collections (double-clic dans l'Outliner).", 2)
    return r.finish()


if __name__ == "__main__":
    L.run(main)
