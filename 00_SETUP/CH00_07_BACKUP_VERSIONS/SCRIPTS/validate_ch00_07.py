"""
validate_ch00_07.py — Correcteur de l'exercice de récupération (CH00.07).
Usage :
  blender -b --factory-startup <votre_v002.blend> --python validate_ch00_07.py --python-exit-code 1 -- --exercise recover
Testé avec : Blender 5.3.0.
"""
import os
import re
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bpy  # noqa: E402


def main():
    r = L.Report("CH00.07 — Récupération")
    hero = L.obj("GEO_Hero")
    r.check(hero is not None, "GEO_Hero récupéré", "Ouvrez le fichier .blend1 (File > Open, filtre des sauvegardes) ou File > Recover.", 4)
    r.check(hero is not None and any(m.type == "SUBSURF" for m in hero.modifiers),
            "Le héros a gardé son modificateur (récupération, pas recréation)", "Ne recréez pas l'objet : récupérez-le.", 2)
    r.check(L.obj("GEO_Crate") and L.obj("GEO_Barrel"), "Le reste de la scène est intact", "", 1)
    fname = os.path.basename(bpy.data.filepath)
    r.check(re.search(r"_v002\.blend$", fname), f"Enregistré en nouvelle version ({fname})",
            "File > Save As… ch00_07_hero_scene_v002.blend (ou Ctrl+Alt+S depuis la v001).", 2)
    return r.finish()


if __name__ == "__main__":
    L.run(main)
