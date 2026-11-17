"""
build_ch18_07_files.py — Feuille « brushes, traits, remplissages, matériaux » (CH18.07).

  STARTER_FILES/ch18_07_brushes_starter.blend
      GUIDE (verrouillé) : 3 bandes de traits (crayon / encre / marqueur), un dessin au trait à
        remplir (maison, tasse, poisson) — formes fermées.
      USER_Lines : vide — 3 × 5 traits avec 3 pinceaux différents.
      USER_Fills : vide — aplats de couleur dans les formes du dessin guide (outil Fill).
  COMPLETED_EXAMPLES/ch18_07_brushes_solution.blend (+ _reference.png)
Usage : blender -b --factory-startup --python-exit-code 1 --python build_ch18_07_files.py
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
NOTE = """CH18.07 — BRUSHES, TRAITS, REMPLISSAGES, MATÉRIAUX (GP_Practice, Draw Mode, Num 0)
1. USER_Lines (3 bandes du haut) : 5 traits par bande, un pinceau différent par bande :
   bande 1 « Pencil », bande 2 « Ink Pen », bande 3 « Marker Bold » (sélecteur de pinceau,
   en-tête de l'outil Draw). Variez la pression : fin → épais → fin.
2. Créez au moins 4 matériaux de couleur (Properties > Material, bouton +, panneau Fill >
   Base Color) : mur, toit, tasse, poisson...
3. USER_Fills : avec l'outil Fill (pinceau « Fill »), Layer Mode = Visible, cliquez dans chaque
   forme fermée du dessin guide (maison, tasse, poisson) avec le matériau voulu (U).
   Au moins 8 zones remplies.
"""

HOUSE = dict(wall=(-5.4, -3.0, -2.6, -1.0), roof=[(-5.7, -1.0), (-4.0, 0.3), (-2.3, -1.0)],
             door=(-4.4, -3.0, -3.7, -1.9), win=(-3.4, -2.2, -2.9, -1.6))


def cup_body():
    return [(-0.6 + 1.6 * t, -1.2 - 0.03 * math.sin(math.pi * t)) for t in (0, 1)] + \
           [(1.0, -1.2), (0.85, -2.9), (-0.45, -2.9), (-0.6, -1.2)]


def fish_body():
    return [(3.9 + 1.3 * math.cos(a), -1.9 + 0.75 * math.sin(a)) for a in [i * 2 * math.pi / 48 for i in range(48)]]


FISH_TAIL = [(2.65, -1.9), (2.0, -1.2), (2.0, -2.6)]


def guides(ob, d):
    blue = G.material(ob, "MAT_GP_Guide", (0.25, 0.45, 0.85))
    ink = 0
    # bandes de traits
    for k in range(3):
        z = 2.9 - k * 0.8
        G.rect(d, -5.9, z - 0.35, 5.9, z + 0.35, 0.004, blue)
    # dessin au trait à remplir (formes FERMÉES, encre noire)
    x0, z0, x1, z1 = HOUSE["wall"]
    G.rect(d, x0, z0, x1, z1, 0.012, ink)
    G.polyline(d, HOUSE["roof"], 0.012, ink, cyclic=True)
    G.rect(d, *HOUSE["door"], 0.01, ink)
    G.rect(d, *HOUSE["win"], 0.01, ink)
    G.polyline(d, cup_body()[2:], 0.012, ink, cyclic=True)
    G.ellipse(d, (0.2, -1.2), 0.8, 0.16, 0.012, ink, 40)
    G.ellipse(d, (1.15, -2.0), 0.35, 0.45, 0.012, ink, 32)
    G.ellipse(d, (1.15, -2.0), 0.18, 0.27, 0.01, ink, 24)
    G.polyline(d, fish_body(), 0.012, ink, cyclic=True)
    G.polyline(d, FISH_TAIL, 0.012, ink, cyclic=True)
    G.circle(d, (4.7, -1.7), 0.14, 0.01, ink, 20)
    G.rect(d, -5.9, -3.25, 5.9, 0.55, 0.004, blue)


def lines(d, ink):
    """Trois bandes : crayon fin et irrégulier, encre à pression, marqueur épais et régulier."""
    for k, (rad, press, op) in enumerate(((0.006, "pencil", 0.7), (0.018, "ink", 1.0), (0.04, "marker", 0.9))):
        z = 2.9 - k * 0.8
        for j in range(5):
            xa = -5.6 + j * 2.3
            pts = [(xa + 1.9 * t, z + 0.18 * math.sin(t * math.pi * 2 + j)) for t in [i / 30 for i in range(31)]]
            if press == "ink":
                pr = [0.15 + math.sin(math.pi * i / 30) for i in range(31)]
            elif press == "pencil":
                pr = [0.8 + 0.2 * math.sin(i * 1.7) for i in range(31)]
            else:
                pr = None
            G.polyline(d, pts, rad, ink, opacity=op, pressure=pr)


def fills(ob, d):
    mats = {n: G.material(ob, n, (0.02, 0.02, 0.02), fill=c) for n, c in (
        ("MAT_GP_Wall", (0.93, 0.82, 0.6)), ("MAT_GP_Roof", (0.75, 0.2, 0.12)),
        ("MAT_GP_Wood", (0.45, 0.27, 0.12)), ("MAT_GP_Glass", (0.6, 0.85, 0.95)),
        ("MAT_GP_Cup", (0.2, 0.45, 0.8)), ("MAT_GP_Coffee", (0.3, 0.18, 0.08)),
        ("MAT_GP_Fish", (0.95, 0.55, 0.12)), ("MAT_GP_White", (1.0, 1.0, 1.0)))}
    def fill(pts, m):
        G.polyline(d, pts, 0.01, mats[m], cyclic=True, fill=True, hide_stroke=True)
    x0, z0, x1, z1 = HOUSE["wall"]
    fill([(x0, z0), (x1, z0), (x1, z1), (x0, z1)], "MAT_GP_Wall")
    fill(HOUSE["roof"], "MAT_GP_Roof")
    a, b, c, e = HOUSE["door"]
    fill([(a, b), (c, b), (c, e), (a, e)], "MAT_GP_Wood")
    a, b, c, e = HOUSE["win"]
    fill([(a, b), (c, b), (c, e), (a, e)], "MAT_GP_Glass")
    fill(cup_body()[2:], "MAT_GP_Cup")
    fill([(0.2 + 0.8 * math.cos(t), -1.2 + 0.16 * math.sin(t)) for t in [i * 2 * math.pi / 40 for i in range(40)]], "MAT_GP_Coffee")
    fill(fish_body(), "MAT_GP_Fish")
    fill(FISH_TAIL, "MAT_GP_Fish")
    fill([(4.7 + 0.14 * math.cos(t), -1.7 + 0.14 * math.sin(t)) for t in [i * 2 * math.pi / 20 for i in range(20)]], "MAT_GP_White")


def build(sol):
    L.reset("SC_Brushes")
    ob, cam, drw = G.sheet("GP_Practice", 12.0, 6.75, ("GUIDE",), ("USER_Lines", "USER_Fills"))
    # Le calque des aplats passe SOUS le dessin guide (les traits noirs restent visibles).
    gp = ob.data
    gp.layers.move_bottom(next(l for l in gp.layers if l.name == "USER_Fills"))
    gp.layers["GUIDE"].lock = False
    guides(ob, drw["GUIDE"])
    gp.layers["GUIDE"].lock = True
    gp.layers["GUIDE"].opacity = 1.0
    if sol:
        lines(drw["USER_Lines"], 0)
        fills(ob, drw["USER_Fills"])
    L.instructions(NOTE)


def main():
    build(False)
    L.save(os.path.join(CH, "STARTER_FILES", "ch18_07_brushes_starter.blend"))
    build(True)
    p = L.save(os.path.join(CH, "COMPLETED_EXAMPLES", "ch18_07_brushes_solution.blend"))
    sc = bpy.context.scene
    sc.render.resolution_percentage = 60
    sc.render.filepath = os.path.join(os.path.dirname(p), "ch18_07_brushes_reference.png")
    bpy.ops.render.render(write_still=True)


if __name__ == "__main__":
    L.run(main)
