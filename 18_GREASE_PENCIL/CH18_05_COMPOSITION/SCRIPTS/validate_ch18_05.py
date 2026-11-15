"""
validate_ch18_05.py — Correcteur CH18.05 (s'appuie sur SCRIPTS/bcma_gp_check.py et gp_spec.json).
Usage : blender -b --factory-startup <fichier.blend> --python validate_ch18_05.py --python-exit-code 1 -- --exercise composition
Vérifie la quantité et l'emplacement du dessin ; la qualité s'auto-évalue avec la grille d'EXERCISES.md.
Testé avec : Blender 5.3.0.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "SCRIPTS"))
import bcma_gp_check as C  # noqa: E402
import bcma_lib as L  # noqa: E402

if __name__ == "__main__":
    L.run(lambda: C.main(__file__))
