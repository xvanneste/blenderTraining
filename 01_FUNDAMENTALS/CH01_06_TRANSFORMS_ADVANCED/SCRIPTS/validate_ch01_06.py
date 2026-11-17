"""
validate_ch01_06.py — Correcteur du déménagement (CH01.06).
Usage : blender -b --factory-startup <fichier.blend> --python-exit-code 1 --python validate_ch01_06.py -- --exercise moving
Testé avec : Blender 5.3.0.
"""
import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
from mathutils import Vector  # noqa: E402


def bbox(o):
    pts = [o.matrix_world @ Vector(c) for c in o.bound_box]
    return (min(p.x for p in pts), max(p.x for p in pts), min(p.y for p in pts), max(p.y for p in pts),
            min(p.z for p in pts), max(p.z for p in pts))


def main():
    r = L.Report("CH01.06 — Le déménagement")
    crate, book, shelf, plank = (L.obj(n) for n in ("GEO_Crate", "GEO_Book", "GEO_Shelf", "GEO_Plank"))
    if not r.check(all((crate, book, shelf, plank)), "Objets présents", "Ne renommez pas les objets.", 1):
        return r.finish()
    r.check(all(abs(s - 1) < 1e-4 for s in crate.scale), f"Caisse : échelle appliquée {tuple(round(s, 3) for s in crate.scale)}",
            "Ctrl+A > Scale avec la caisse sélectionnée.", 3)
    dims = crate.dimensions
    r.check(abs(dims.x - 2) < 0.01 and abs(dims.y - 1) < 0.01 and abs(dims.z - 0.5) < 0.01,
            f"Caisse : dimensions conservées ({dims.x:.2f} × {dims.y:.2f} × {dims.z:.2f})",
            "Appliquer l'échelle ne doit pas changer la taille réelle.", 2)
    bx = bbox(book)
    r.check(abs(bx[4] - 0.8) < 0.005, f"Livre posé sur le plateau (dessous à z = {bx[4]:.3f} m)",
            "Snapping (Shift+Tab) en mode Face, ou G Z avec la bonne valeur.", 3)
    r.check(0.3 <= bx[0] and bx[1] <= 1.7 and -1.4 <= bx[2] and bx[3] <= -0.6, "Livre au-dessus de la table (X/Y)",
            "Ne déplacez le livre que sur Z.", 1)
    r.check(abs(book.rotation_euler.x) < 1e-3 and abs(book.rotation_euler.y) < 1e-3, "Livre à plat", "", 1)
    sb = bbox(shelf)
    r.check(abs(sb[3] - 2.0) < 0.005, f"Étagère contre le mur (dos à y = {sb[3]:.3f} m)",
            "Snapping Face ou Vertex vers le mur, contraint à Y (G Y).", 3)
    r.check(abs(shelf.location.x + 1.5) < 0.01 and abs(shelf.location.z - 1.2) < 0.01, "Étagère : X et Z inchangés",
            "Contraignez le déplacement à l'axe Y.", 1)
    start = Vector((3, 0, 0.05))
    d = plank.location - start
    axis = Vector((math.cos(math.radians(30)), math.sin(math.radians(30)), 0))
    r.check(abs(d.length - 1) < 0.01 and d.normalized().dot(axis) > 0.999 if d.length > 0 else False,
            f"Planche avancée de 1 m le long de son axe local X (déplacement {d.length:.2f} m)",
            "G X X 1 Entrée : deux pressions sur X = axe local.", 3)
    return r.finish()


if __name__ == "__main__":
    L.run(main)
