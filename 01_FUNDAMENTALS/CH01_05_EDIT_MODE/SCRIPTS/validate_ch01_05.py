"""
validate_ch01_05.py — Correcteur « de la boîte à la maison » (CH01.05).
Usage : blender -b --factory-startup <fichier.blend> --python-exit-code 1 --python validate_ch01_05.py -- --exercise house
Note : enregistrez en Object Mode (en Edit Mode, les dernières modifications peuvent ne pas
être écrites dans le maillage lu par le correcteur).
Testé avec : Blender 5.3.0.
"""
import os
import sys

import bmesh

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402


def main():
    r = L.Report("CH01.05 — De la boîte à la maison")
    h = L.obj("GEO_House")
    if not r.check(h is not None, "GEO_House présent", "Ne renommez pas l'objet.", 1):
        return r.finish()
    pts = [h.matrix_world @ v.co for v in h.data.vertices]
    zmax = max(p.z for p in pts)
    r.check(abs(zmax - 3.0) < 0.05, f"Faîtage à 3 m (z max = {zmax:.2f})", "E puis 1 Entrée sur la face du haut.", 3)
    top = [p for p in pts if p.z > zmax - 0.01]
    r.check(top and all(abs(p.x) < 0.02 for p in top), "Faîtage centré (sommets du haut à x = 0)",
            "S X 0 Entrée avec la face extrudée sélectionnée.", 3)
    r.check(top and max(p.y for p in top) - min(p.y for p in top) > 1.9, "Faîtage parallèle à Y (long de 2 m)",
            "Mettez à l'échelle 0 sur X (pas sur Y).", 2)
    base = [p for p in pts if p.z < 0.01]
    r.check(len(base) == 4 and all(abs(abs(p.x) - 1) < 0.01 and abs(abs(p.y) - 1) < 0.01 for p in base),
            "Murs intacts (base 2 × 2 m au sol)", "Ne déplacez que la partie haute.", 2)
    bm = bmesh.new()
    try:
        bm.from_mesh(h.data)
        clean = (len(bm.faces) >= 9 and all(edge.is_manifold for edge in bm.edges)
                 and all(face.calc_area() > 1e-7 for face in bm.faces)
                 and bm.calc_volume(signed=True) > 0)
    finally:
        bm.free()
    r.check(clean, "Toit fermé et faces sans écrasement",
            "Fusionnez le faîtage par distance et recalculez les normales avec Shift+N.", 1)
    g = L.obj("GEO_Practice")
    if g is not None:
        gz = max(v.co.z for v in g.data.vertices)
        rising = sum(1 for v in g.data.vertices if 0.05 < v.co.z < gz - 0.05)
        r.check(gz > 0.9 and rising >= 4, f"Colline proportionnelle (sommet {gz:.2f} m, {rising} sommets intermédiaires)",
                "O (édition proportionnelle), molette pour le rayon pendant G Z 1.", 2, mandatory=False)
    return r.finish()


if __name__ == "__main__":
    L.run(main)
