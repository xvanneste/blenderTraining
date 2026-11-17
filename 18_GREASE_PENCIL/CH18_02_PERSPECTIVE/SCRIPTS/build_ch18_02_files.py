"""
build_ch18_02_files.py — Feuille « perspective à 1, 2 et 3 points » (CH18.02).

  STARTER_FILES/ch18_02_perspective_starter.blend
      Trois cadres, chacun avec ses guides (calque GUIDE, verrouillé) :
        gauche  : 1 point de fuite (couloir) — horizon + PF central + fuyantes
        milieu  : 2 points de fuite (coin de rue) — horizon + PF gauche/droite
        droite  : 3 points de fuite (tour vue d'en bas) — PF gauche/droite + PF vertical haut
      Calques de travail vides : USER_OnePoint, USER_TwoPoint, USER_ThreePoint.
  COMPLETED_EXAMPLES/ch18_02_perspective_solution.blend (+ _reference.png)
      Couloir avec portes, rue de bâtiments-boîtes, tour en contre-plongée (générés par script).
Usage : blender -b --factory-startup --python-exit-code 1 --python build_ch18_02_files.py
Testé avec : Blender 5.3.0.
"""
import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "SCRIPTS"))
import bcma_gp as G  # noqa: E402
import bcma_lib as L  # noqa: E402
import bpy  # noqa: E402

CH = L.chapter_dir(__file__)
NOTE = """CH18.02 — PERSPECTIVE (GP_Practice, Draw Mode, Num 0)
Cadre de gauche (USER_OnePoint) : un couloir vu de face, 1 point de fuite : murs, sol,
  plafond, au moins 3 portes et 1 fenêtre, toutes les fuyantes vers le PF central.
Cadre du milieu (USER_TwoPoint) : un coin de rue, au moins 4 bâtiments-boîtes, des fenêtres
  alignées sur les fuyantes, un trottoir.
Cadre de droite (USER_ThreePoint) : une tour vue d'en bas (contre-plongée), verticales qui
  convergent vers le PF du haut.
Conseil : outil Line (barre T) pour les fuyantes, main levée pour les détails.
"""
FRAMES = {"one": (-5.9, -2.1), "two": (-1.9, 1.9), "three": (2.1, 5.9)}   # x0, x1
Z0, Z1 = -2.6, 2.6


def guides(ob, d):
    blue = G.material(ob, "MAT_GP_Guide", (0.25, 0.45, 0.85))
    for x0, x1 in FRAMES.values():
        G.rect(d, x0, Z0, x1, Z1, 0.008, 0)
    # 1 point : horizon au milieu, PF central
    x0, x1 = FRAMES["one"]
    cx, hz = (x0 + x1) / 2, 0.2
    G.line(d, (x0, hz), (x1, hz), 0.005, blue)
    for a in range(16):
        t = 2 * math.pi * a / 16
        G.line(d, (cx, hz), (cx + 2.4 * math.cos(t), hz + 2.4 * math.sin(t)), 0.003, blue, opacity=0.5)
    G.circle(d, (cx, hz), 0.05, 0.006, blue, 16)
    # 2 points : PF hors cadre, sur l'horizon bas
    x0, x1 = FRAMES["two"]
    hz2 = -0.6
    G.line(d, (x0, hz2), (x1, hz2), 0.005, blue)
    for vx, side in ((x0 - 1.6, 1), (x1 + 1.6, -1)):
        for i in range(9):
            a = math.radians(-25 + 50 * i / 8)
            G.line(d, (vx, hz2), (vx + side * 5.0 * math.cos(a), hz2 + 5.0 * math.sin(a)), 0.003, blue, opacity=0.5)
    # 3 points : horizon bas, PF vertical en haut
    x0, x1 = FRAMES["three"]
    hz3, vz = -2.2, 6.5
    cx3 = (x0 + x1) / 2
    G.line(d, (x0, hz3), (x1, hz3), 0.005, blue)
    for i in range(9):
        bx = x0 + (x1 - x0) * i / 8
        G.line(d, (bx, Z0), (bx + (cx3 - bx) * 0.6, Z0 + (vz - Z0) * 0.6), 0.003, blue, opacity=0.5)


def solution(ob, drw):
    ink = 0
    # couloir 1 point
    d = drw["USER_OnePoint"]
    x0, x1 = FRAMES["one"]
    cx, hz = (x0 + x1) / 2, 0.2

    def toward(p, f):
        return (p[0] + (cx - p[0]) * f, p[1] + (hz - p[1]) * f)
    corners = [(x0 + 0.2, Z0 + 0.2), (x1 - 0.2, Z0 + 0.2), (x1 - 0.2, Z1 - 0.2), (x0 + 0.2, Z1 - 0.2)]
    back = [toward(c, 0.7) for c in corners]
    for c, b in zip(corners, back):
        G.line(d, c, b, 0.006, ink)
    G.polyline(d, back, 0.006, ink, cyclic=True)
    for f0, f1, side in [(0.15, 0.3, 0), (0.4, 0.5, 0), (0.2, 0.35, 1)]:
        base = corners[0] if side == 0 else corners[1]
        top = (base[0], base[1] + 2.6)
        a, b = toward(base, f0), toward(base, f1)
        c, e = toward(top, f1), toward(top, f0)
        G.polyline(d, [a, b, c, e], 0.005, ink, cyclic=True)
    # fenêtre (mur droit, plus haute) et lignes de carrelage vers le PF
    wb = (corners[1][0], corners[1][1] + 1.2)
    G.polyline(d, [toward(wb, 0.45), toward(wb, 0.6), toward((wb[0], wb[1] + 1.0), 0.6),
                   toward((wb[0], wb[1] + 1.0), 0.45)], 0.005, ink, cyclic=True)
    for k in range(1, 5):
        fx = corners[0][0] + (corners[1][0] - corners[0][0]) * k / 5
        G.line(d, (fx, corners[0][1]), toward((fx, corners[0][1]), 0.7), 0.003, ink)
    # rue 2 points
    d = drw["USER_TwoPoint"]
    x0, x1 = FRAMES["two"]
    hz2 = -0.6
    vpl, vpr = x0 - 1.6, x1 + 1.6
    for i, (bx, h, wl, wr) in enumerate([(-1.2, 2.0, 0.25, 0.18), (-0.2, 3.0, 0.2, 0.22), (0.9, 1.6, 0.22, 0.2),
                                         (1.5, 2.4, 0.15, 0.12)]):
        G.box_two_point(d, bx, -2.3, h, wl, wr, vpl, vpr, hz2, 0.005, ink)
        for k in range(1, 4):
            z = -2.3 + h * k / 4
            G.line(d, (bx, z), (bx + (vpr - bx) * wr * 0.8, z + (hz2 - z) * wr * 0.8), 0.003, ink)
    G.line(d, (x0 + 0.1, -2.45), (x1 - 0.1, -2.45), 0.004, ink)
    # tour 3 points
    d = drw["USER_ThreePoint"]
    x0, x1 = FRAMES["three"]
    cx3, vz = (x0 + x1) / 2, 6.5
    bl, br = (cx3 - 0.9, -2.3), (cx3 + 0.9, -2.3)
    bm = (cx3, -2.5)
    for p in (bl, bm, br):
        top = (p[0] + (cx3 - p[0]) * 0.55, p[1] + (vz - p[1]) * 0.55)
        G.line(d, p, top, 0.006, ink)
    G.polyline(d, [bl, bm, br], 0.006, ink)
    for k in range(1, 7):
        f = k / 7 * 0.55
        pts = [(p[0] + (cx3 - p[0]) * f, p[1] + (vz - p[1]) * f) for p in (bl, bm, br)]
        G.polyline(d, pts, 0.003, ink)


def build(sol):
    L.reset("SC_Perspective")
    ob, cam, drw = G.sheet("GP_Practice", 12.0, 6.75, ("GUIDE",), ("USER_OnePoint", "USER_TwoPoint", "USER_ThreePoint"))
    ob.data.layers["GUIDE"].lock = False
    guides(ob, drw["GUIDE"])
    ob.data.layers["GUIDE"].lock = True
    if sol:
        solution(ob, drw)
    L.instructions(NOTE)


def main():
    build(False)
    L.save(os.path.join(CH, "STARTER_FILES", "ch18_02_perspective_starter.blend"))
    build(True)
    p = L.save(os.path.join(CH, "COMPLETED_EXAMPLES", "ch18_02_perspective_solution.blend"))
    sc = bpy.context.scene
    sc.render.resolution_percentage = 60
    sc.render.filepath = os.path.join(os.path.dirname(p), "ch18_02_perspective_reference.png")
    bpy.ops.render.render(write_still=True)


if __name__ == "__main__":
    L.run(main)
