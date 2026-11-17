"""
build_ch18_05_files.py — Feuille « composition et dessin cinématographique » (CH18.05).

  STARTER_FILES/ch18_05_composition_starter.blend
      GUIDE (verrouillé) : 6 cadres 16:9 avec grille des tiers (vignettes), un grand cadre pour
        l'étude de valeurs, un exemple « décor en 3 plans » et un cadre vide pour le vôtre.
      USER_Thumbnails : vide — 6 vignettes de composition (une règle différente par vignette).
      USER_Values     : vide — une vignette en 3 valeurs (clair / moyen / sombre) au trait.
      USER_Planes     : vide — un décor en 3 plans (premier plan, plan moyen, arrière-plan).
  COMPLETED_EXAMPLES/ch18_05_composition_solution.blend (+ _reference.png)
Usage : blender -b --factory-startup --python-exit-code 1 --python build_ch18_05_files.py
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
NOTE = """CH18.05 — COMPOSITION (GP_Practice, Draw Mode, Num 0)
1. USER_Thumbnails (6 cadres en haut à gauche) : une vignette par règle : tiers, lignes
   directrices, symétrie, diagonale, cadre dans le cadre, gros plan avec espace de regard.
2. USER_Values (grand cadre en haut à droite) : un paysage avec personnage en 3 VALEURS au
   trait : arrière-plan clair (hachures espacées), plan moyen gris (hachures moyennes),
   premier plan sombre (hachures serrées). Le personnage doit se détacher.
3. USER_Planes (cadre en bas à droite) : un décor en 3 plans, en vous inspirant de l'exemple
   de gauche (premier plan qui encadre, plan moyen avec le sujet, arrière-plan simple).
"""

THUMB_W, THUMB_H = 1.7, 1.7 * 9 / 16


def thumb_frames():
    out = []
    for r in range(2):
        for c in range(3):
            x0 = -5.75 + c * 1.9
            z1 = 3.05 - r * 1.25
            out.append((x0, z1 - THUMB_H, x0 + THUMB_W, z1))
    return out


VAL = (0.9, 0.62, 5.3, 0.62 + 4.4 * 9 / 16)
PLANE_EX = (-5.5, -3.1, -0.6, -3.1 + 4.9 * 9 / 16)
PLANE_USER = (0.6, -3.1, 5.5, -3.1 + 4.9 * 9 / 16)


def frame_with_thirds(d, f, radius, mat, thirds_mat):
    x0, z0, x1, z1 = f
    G.rect(d, x0, z0, x1, z1, radius, mat)
    for k in (1, 2):
        x = x0 + (x1 - x0) * k / 3
        z = z0 + (z1 - z0) * k / 3
        G.line(d, (x, z0), (x, z1), radius * 0.4, thirds_mat)
        G.line(d, (x0, z), (x1, z), radius * 0.4, thirds_mat)


def hatch_under(d, xa, xb, z0, profile, spacing, radius, mat, opacity=1.0):
    """Hachures verticales entre z0 et la courbe profile(x) : une « valeur » au trait."""
    x = xa
    while x <= xb + 1e-6:
        top = profile(x)
        if top > z0 + 0.01:
            G.polyline(d, [(x, z0), (x, top)], radius, mat, opacity=opacity)
        x += spacing


def outline(d, xa, xb, profile, radius, mat, n=40):
    G.polyline(d, [(xa + (xb - xa) * i / n, profile(xa + (xb - xa) * i / n)) for i in range(n + 1)], radius, mat)


def tree(d, x, z, h, radius, mat):
    """Arbre simple : tronc + couronne."""
    G.polyline(d, [(x - 0.06 * h, z), (x - 0.04 * h, z + 0.55 * h)], radius, mat)
    G.polyline(d, [(x + 0.06 * h, z), (x + 0.04 * h, z + 0.55 * h)], radius, mat)
    G.ellipse(d, (x, z + 0.75 * h), 0.28 * h, 0.27 * h, radius, mat, 32)


def house(d, x, z, w, h, radius, mat):
    G.rect(d, x, z, x + w, z + h, radius, mat)
    G.polyline(d, [(x - 0.05 * w, z + h), (x + w / 2, z + 1.55 * h), (x + w * 1.05, z + h)], radius, mat)
    G.rect(d, x + 0.4 * w, z, x + 0.6 * w, z + 0.5 * h, radius * 0.8, mat)


def guides(ob, d):
    blue = G.material(ob, "MAT_GP_Guide", (0.25, 0.45, 0.85))
    pale = G.material(ob, "MAT_GP_Thirds", (0.62, 0.72, 0.92))
    for f in thumb_frames():
        frame_with_thirds(d, f, 0.006, blue, pale)
    frame_with_thirds(d, VAL, 0.008, blue, pale)
    G.rect(d, *PLANE_USER, 0.008, blue)
    # Exemple « décor en 3 plans » (rue : réverbère au premier plan, maison au plan moyen, collines au fond)
    x0, z0, x1, z1 = PLANE_EX
    G.rect(d, x0, z0, x1, z1, 0.008, blue)
    hz = z0 + (z1 - z0) * 0.45
    outline(d, x0, x1, lambda x: hz + 0.25 + 0.18 * math.sin((x - x0) * 2.1), 0.003, pale)       # fond : trait fin
    house(d, x0 + 1.7, hz - 0.1, 0.9, 0.55, 0.006, blue)                                         # plan moyen
    G.mannequin(d, x0 + 3.0, hz - 0.15, 0.55, "walk", 0.006, blue)
    G.polyline(d, [(x1 - 0.7, z0), (x1 - 0.7, z1 - 0.15), (x1 - 1.2, z1 - 0.15)], 0.02, blue)    # premier plan : épais
    G.ellipse(d, (x1 - 1.2, z1 - 0.3), 0.12, 0.1, 0.012, blue, 16)
    G.line(d, (x0, hz - 0.15), (x1, hz - 0.15), 0.004, blue)


def thumbnails(d, ink):
    fr = thumb_frames()
    # 0 — règle des tiers : horizon sur le tiers bas, personnage sur le tiers droit
    x0, z0, x1, z1 = fr[0]
    w, h = x1 - x0, z1 - z0
    G.line(d, (x0, z0 + h / 3), (x1, z0 + h / 3), 0.006, ink)
    G.mannequin(d, x0 + 2 * w / 3, z0 + h / 3 - 0.05, 0.42, "stand", 0.004, ink)
    tree(d, x0 + 0.25, z0 + h / 3, 0.35, 0.004, ink)
    # 1 — lignes directrices : route vers le personnage
    x0, z0, x1, z1 = fr[1]
    w, h = x1 - x0, z1 - z0
    vp = (x0 + 2 * w / 3, z0 + 2 * h / 3)
    G.line(d, (x0, z0 + 2 * h / 3), (x1, z0 + 2 * h / 3), 0.004, ink)
    G.line(d, (x0 + 0.2, z0), vp, 0.006, ink)
    G.line(d, (x1 - 0.1, z0), vp, 0.006, ink)
    G.mannequin(d, vp[0], vp[1] - 0.02, 0.18, "walk", 0.003, ink)
    # 2 — symétrie : couloir vers le centre
    x0, z0, x1, z1 = fr[2]
    w, h = x1 - x0, z1 - z0
    c = (x0 + w / 2, z0 + h / 2)
    for p in ((x0, z0), (x1, z0), (x0, z1), (x1, z1)):
        G.line(d, p, (c[0] + (p[0] - c[0]) * 0.25, c[1] + (p[1] - c[1]) * 0.25), 0.005, ink)
    G.rect(d, c[0] - w * 0.125, c[1] - h * 0.125, c[0] + w * 0.125, c[1] + h * 0.125, 0.005, ink)
    G.mannequin(d, c[0], c[1] - h * 0.125, 0.2, "stand", 0.003, ink)
    # 3 — diagonale : pente, personnage qui grimpe
    x0, z0, x1, z1 = fr[3]
    w, h = x1 - x0, z1 - z0
    G.line(d, (x0, z0 + 0.1), (x1, z1 - 0.2), 0.007, ink)
    G.mannequin(d, x0 + 2 * w / 3, z0 + 0.1 + (2 / 3) * (h - 0.3), 0.3, "walk", 0.004, ink)
    G.line(d, (x0 + 0.15, z1 - 0.15), (x0 + 0.45, z1 - 0.15), 0.004, ink)
    # 4 — cadre dans le cadre : porte, personnage dedans
    x0, z0, x1, z1 = fr[4]
    w, h = x1 - x0, z1 - z0
    G.rect(d, x0 + w * 0.36, z0 + 0.05, x0 + w * 0.64, z1 - 0.1, 0.008, ink)
    G.rect(d, x0 + w * 0.3, z0 + 0.05, x0 + w * 0.7, z1 - 0.05, 0.006, ink)
    G.mannequin(d, x0 + w / 2, z0 + 0.1, 0.55, "stand", 0.004, ink)
    G.line(d, (x0, z0 + 0.05), (x1, z0 + 0.05), 0.005, ink)
    # 5 — gros plan, espace de regard : tête sur le tiers gauche, regard vers la droite
    x0, z0, x1, z1 = fr[5]
    w, h = x1 - x0, z1 - z0
    hx, hz = x0 + w / 3, z0 + h * 0.58
    G.circle(d, (hx, hz), 0.27, 0.006, ink, 32)
    G.polyline(d, [(hx - 0.22, hz - 0.15), (hx - 0.05, hz - 0.42), (hx + 0.2, hz - 0.3)], 0.006, ink)
    G.polyline(d, [(hx + 0.24, hz - 0.02), (hx + 0.36, hz - 0.1), (hx + 0.25, hz - 0.14)], 0.005, ink)
    G.ellipse(d, (hx + 0.14, hz + 0.02), 0.04, 0.03, 0.004, ink, 12)
    G.polyline(d, [(hx - 0.25, z0), (hx - 0.18, hz - 0.35), (hx + 0.1, hz - 0.4), (hx + 0.35, z0)], 0.006, ink)
    G.arrow(d, (hx + 0.45, hz), (x1 - 0.15, hz), 0.003, ink, 0.06)


def values(d, ink):
    """Trois valeurs au trait : fond clair, plan moyen gris, premier plan sombre ; personnage contrasté."""
    x0, z0, x1, z1 = VAL
    w, h = x1 - x0, z1 - z0
    far = lambda x: z0 + h * 0.55 + 0.35 * math.sin((x - x0) * 1.3) + 0.15 * math.sin((x - x0) * 3.7)
    mid = lambda x: z0 + h * 0.35 + 0.18 * math.sin((x - x0) * 2.2 + 1.0)
    fg = lambda x: z0 + max(0.0, 0.9 * (1 - (x - x0) / (w * 0.38))) + 0.08
    outline(d, x0, x1, far, 0.004, ink)
    hatch_under(d, x0 + 0.05, x1 - 0.05, mid(x0), far, 0.16, 0.0025, ink, 0.6)   # clair
    outline(d, x0, x1, mid, 0.005, ink)
    hatch_under(d, x0 + 0.03, x1 - 0.03, z0 + 0.02, mid, 0.07, 0.004, ink)       # moyen
    outline(d, x0, x0 + w * 0.38, fg, 0.008, ink)
    hatch_under(d, x0 + 0.02, x0 + w * 0.38, z0 + 0.02, fg, 0.03, 0.009, ink)    # sombre
    # Arbre sombre au premier plan (cadre à gauche)
    G.polyline(d, [(x0 + 0.35, z0 + 0.5), (x0 + 0.42, z1 - 0.6)], 0.03, ink)
    G.hatch_ellipse(d, (x0 + 0.45, z1 - 0.45), 0.45, 0.35, 0.03, 0.8, 0.008, ink)
    # Personnage sombre sur le ciel clair, au tiers droit
    px, pz = x0 + 2 * w / 3, mid(x0 + 2 * w / 3) - 0.05
    G.mannequin(d, px, pz, 0.85, "stand", 0.012, ink)


def planes(d, ink):
    x0, z0, x1, z1 = PLANE_USER
    w, h = x1 - x0, z1 - z0
    hz = z0 + h * 0.4
    outline(d, x0, x1, lambda x: hz + 0.35 + 0.3 * math.sin((x - x0) * 1.6), 0.003, ink)        # arrière-plan
    outline(d, x0 + 2.6, x1, lambda x: hz + 0.55 + 0.25 * math.sin((x - x0) * 3.0), 0.003, ink)
    G.line(d, (x0, hz), (x1, hz), 0.005, ink)                                                     # plan moyen
    house(d, x0 + 2.6, hz, 1.0, 0.6, 0.006, ink)
    tree(d, x0 + 3.9, hz, 0.7, 0.006, ink)
    G.mannequin(d, x0 + 2.0, hz - 0.1, 0.6, "walk", 0.006, ink)
    G.polyline(d, [(x0 + 0.35, z0), (x0 + 0.45, z1)], 0.03, ink)                                 # premier plan
    G.polyline(d, [(x0 + 0.75, z0), (x0 + 0.7, z1)], 0.03, ink)
    G.polyline(d, [(x0 + 0.45, z1 - 0.5), (x0 + 1.3, z1 - 0.2), (x0 + 1.6, z1)], 0.015, ink)
    G.hatch_ellipse(d, (x0 + 0.55, z0 + 0.25), 0.55, 0.3, 0.04, 0.6, 0.008, ink)


def build(sol):
    L.reset("SC_Composition")
    ob, cam, drw = G.sheet("GP_Practice", 12.0, 6.75, ("GUIDE",), ("USER_Thumbnails", "USER_Values", "USER_Planes"))
    ob.data.layers["GUIDE"].lock = False
    guides(ob, drw["GUIDE"])
    ob.data.layers["GUIDE"].lock = True
    if sol:
        thumbnails(drw["USER_Thumbnails"], 0)
        values(drw["USER_Values"], 0)
        planes(drw["USER_Planes"], 0)
    L.instructions(NOTE)


def main():
    build(False)
    L.save(os.path.join(CH, "STARTER_FILES", "ch18_05_composition_starter.blend"))
    build(True)
    p = L.save(os.path.join(CH, "COMPLETED_EXAMPLES", "ch18_05_composition_solution.blend"))
    sc = bpy.context.scene
    sc.render.resolution_percentage = 60
    sc.render.filepath = os.path.join(os.path.dirname(p), "ch18_05_composition_reference.png")
    bpy.ops.render.render(write_still=True)


if __name__ == "__main__":
    L.run(main)
