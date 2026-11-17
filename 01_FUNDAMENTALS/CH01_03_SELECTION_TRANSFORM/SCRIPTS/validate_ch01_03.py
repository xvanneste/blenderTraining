"""
validate_ch01_03.py — Correcteur du puzzle (CH01.03).
Compare la forme de chaque pièce, en coordonnées du monde, à sa silhouette cible
(tolérance 2 cm : les symétries d'un cube ou d'un cylindre sont acceptées).
Usage : blender -b --factory-startup <fichier.blend> --python-exit-code 1 --python validate_ch01_03.py -- --exercise puzzle
Testé avec : Blender 5.3.0.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bpy  # noqa: E402
from mathutils.kdtree import KDTree  # noqa: E402

HINTS = {"A": "G puis X/Y/Z et la valeur ; ou sidebar N > Item > Location",
         "B": "R X 90 Entrée pour la rotation",
         "C": "S Z 2 Entrée pour l'échelle sur Z",
         "D": "R Z 45 Entrée, puis S 0.5 Entrée"}


def world_pts(o):
    return [o.matrix_world @ v.co for v in o.data.vertices]


def max_gap(a, b):
    tree = KDTree(len(b))
    for i, p in enumerate(b):
        tree.insert(p, i)
    tree.balance()
    return max(tree.find(p)[2] for p in a)


def main():
    r = L.Report("CH01.03 — Le puzzle des transformations")
    for k in "ABCD":
        p, t = L.obj(f"GEO_Piece_{k}"), L.obj(f"TGT_{k}")
        if not r.check(p and t, f"Pièce {k} et cible présentes", "Ne supprimez/renommez pas les objets.", 1):
            continue
        gap = max(max_gap(world_pts(p), world_pts(t)), max_gap(world_pts(t), world_pts(p)))
        r.check(gap < 0.02, f"Pièce {k} dans sa silhouette (écart max {gap * 100:.1f} cm < 2 cm)", HINTS[k], 3)
    pebbles = [o for o in bpy.context.scene.objects if o.name.startswith("GEO_Pebble_")]
    r.check(len(pebbles) == 30, "Les 30 cailloux sont toujours là", "Pas de suppression accidentelle (X / Suppr).", 1)
    return r.finish()


if __name__ == "__main__":
    L.run(main)
