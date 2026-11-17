"""
validate_ch01_01.py — Correcteur de l'exercice 3 de CH01.01 (workspace personnalisé).
Usage : blender -b --factory-startup <fichier.blend> --python-exit-code 1 --python validate_ch01_01.py -- --exercise workspace
Testé avec : Blender 5.3.0.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bpy  # noqa: E402

NEEDED = {"VIEW_3D": "3D Viewport", "OUTLINER": "Outliner", "PROPERTIES": "Properties",
          "TEXT_EDITOR": "Text Editor"}


def main():
    r = L.Report("CH01.01 — Workspace BCMA_Study")
    ws = bpy.data.workspaces.get("BCMA_Study")
    r.check(ws is not None, "Workspace « BCMA_Study » présent",
            "Double-cliquez sur l'onglet d'un workspace pour le renommer (après l'avoir dupliqué : clic droit > Duplicate).", 3)
    types = {a.type for s in ws.screens for a in s.areas} if ws else set()
    for t, label in NEEDED.items():
        r.check(t in types, f"Éditeur {label} présent", f"Menu Editor Type (icône en haut à gauche d'une zone) > {label}", 1)
    r.check(L.obj("GEO_Clue_A") and L.obj("GEO_Clue_B"), "Scène d'origine intacte", "", 1)
    return r.finish()


if __name__ == "__main__":
    L.run(main)
