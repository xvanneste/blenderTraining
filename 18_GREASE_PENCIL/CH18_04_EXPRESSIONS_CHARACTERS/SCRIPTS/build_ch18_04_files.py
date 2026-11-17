"""
build_ch18_04_files.py — Feuille « têtes, expressions, feuille de modèle » (CH18.04).

  STARTER_FILES/ch18_04_expressions_starter.blend
      GUIDE (verrouillé) : construction de la tête (cercle du crâne, mâchoire, axe central,
        ligne des yeux à mi-hauteur, ligne du nez, ligne de la bouche), une tête de trois-quarts,
        repères de la feuille de modèle (3 lignes horizontales communes), zones de travail.
      USER_Heads       : vide — 6 têtes construites sous 6 angles.
      USER_Expressions : vide — les 6 émotions de base sur le même personnage.
      USER_ModelSheet  : vide — face, trois-quarts, profil alignés sur les repères.
  COMPLETED_EXAMPLES/ch18_04_expressions_solution.blend (+ _reference.png)
Usage : blender -b --factory-startup --python-exit-code 1 --python build_ch18_04_files.py
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
NOTE = """CH18.04 — EXPRESSIONS ET PERSONNAGES (GP_Practice, Draw Mode, Num 0)
1. USER_Heads (bande du haut) : 6 têtes CONSTRUITES (cercle + mâchoire + axe + ligne des
   yeux) sous 6 angles : face, trois-quarts gauche/droite, profil, plongée, contre-plongée.
2. USER_Expressions (zone en bas à gauche) : le même personnage avec les 6 émotions de base :
   joie, tristesse, colère, peur, surprise, dégoût. Jouez sur sourcils, paupières, bouche.
3. USER_ModelSheet (zone en bas à droite) : votre personnage de face, trois-quarts et profil,
   alignés sur les 3 lignes repères (sommet du crâne, yeux, menton).
"""


def head(d, cx, cz, r, mat=0, emotion=None, turn=0.0, construction=True, guide_mat=None, radius=0.005):
    """Tête construite : crâne, mâchoire, axe vertical (décalé par turn ∈ [-1, 1]), yeux, bouche."""
    gm = guide_mat if guide_mat is not None else mat
    G.circle(d, (cx, cz), r, radius, mat, 40)
    jaw = [(cx - r * 0.85, cz - r * 0.35), (cx - r * 0.45, cz - r * 1.25), (cx + turn * r * 0.4, cz - r * 1.45),
           (cx + r * 0.45, cz - r * 1.25), (cx + r * 0.85, cz - r * 0.35)]
    G.polyline(d, jaw, radius, mat)
    ax = cx + turn * r * 0.55
    if construction:
        G.line(d, (ax, cz + r), (ax + turn * r * 0.1, cz - r * 1.45), radius * 0.5, gm)
        G.line(d, (cx - r, cz - r * 0.15), (cx + r, cz - r * 0.15), radius * 0.5, gm)   # ligne des yeux
    ey = cz - r * 0.15
    if abs(turn) >= 0.3 or emotion is not None:
        # nez : pointe décalée du côté où regarde la tête (lisibilité de l'orientation)
        nx = ax + turn * r * 0.35
        G.polyline(d, [(ax, ey - r * 0.1), (nx + (0.12 * r if turn >= 0 else -0.12 * r), cz - r * 0.55), (ax, cz - r * 0.58)],
                   radius, mat)
    if emotion is None:
        return
    brow = {"joy": 0.1, "sad": -0.35, "anger": 0.45, "fear": -0.45, "surprise": 0.0, "disgust": 0.25}[emotion]
    lift = {"joy": 0.32, "sad": 0.28, "anger": 0.22, "fear": 0.42, "surprise": 0.48, "disgust": 0.25}[emotion]
    eye_open = {"joy": 0.05, "sad": 0.07, "anger": 0.06, "fear": 0.12, "surprise": 0.14, "disgust": 0.05}[emotion]
    for side in (-1, 1):
        ex = ax + side * r * 0.38
        G.ellipse(d, (ex, ey), r * 0.13, r * eye_open, radius, mat, 20)
        # sourcil : l'extrémité intérieure monte (peur, tristesse) ou descend (colère)
        inner = (ex - side * r * 0.15, ey + r * (lift - brow * 0.25))
        outer = (ex + side * r * 0.18, ey + r * (lift + brow * 0.25))
        G.line(d, inner, outer, radius * 1.2, mat)
    my = cz - r * 0.78
    w = r * 0.35
    if emotion == "surprise":
        G.ellipse(d, (ax, my), r * 0.12, r * 0.18, radius, mat, 24)
    elif emotion == "fear":
        G.polyline(d, [(ax - w, my - 0.02 * r), (ax - w * 0.3, my + 0.06 * r), (ax + w * 0.3, my - 0.06 * r),
                       (ax + w, my + 0.02 * r)], radius, mat)
    else:
        curve = {"joy": -0.22, "sad": 0.18, "anger": 0.1, "disgust": 0.0}[emotion]
        pts = [(ax + w * t, my + curve * r * (1 - t * t)) for t in [i / 8 - 1 for i in range(17)]]
        if emotion == "disgust":
            pts = [(x, y + 0.08 * r * (x - ax) / w) for x, y in pts]   # bouche asymétrique
        G.polyline(d, pts, radius, mat)


def guides(ob, d):
    blue = G.material(ob, "MAT_GP_Guide", (0.25, 0.45, 0.85))
    head(d, -4.8, -1.0, 0.7, 0, None, 0.0, True, blue)
    G.line(d, (-5.5, -1.0 + 0.7), (-4.1, -1.0 + 0.7), 0.003, blue)   # sommet
    G.line(d, (-5.5, -1.0 - 0.7 * 0.8), (-4.1, -1.0 - 0.7 * 0.8), 0.003, blue)  # nez
    G.line(d, (-5.5, -1.0 - 0.7 * 0.85), (-4.1, -1.0 - 0.7 * 0.85), 0.002, blue)
    head(d, -3.2, -1.0, 0.55, 0, None, 0.6, True, blue)
    G.rect(d, -5.9, 0.4, 5.9, 3.2, 0.006, blue)       # USER_Heads
    G.rect(d, -2.3, -3.2, 2.0, 0.2, 0.006, blue)      # USER_Expressions
    G.rect(d, 2.2, -3.2, 5.9, 0.2, 0.006, blue)       # USER_ModelSheet
    for z in (-0.4, -0.975, -1.625):                  # repères : sommet du crâne, yeux, menton
        G.line(d, (2.3, z), (5.8, z), 0.003, blue)


def solution(ob, drw):
    ink = 0
    d = drw["USER_Heads"]
    for i, turn in enumerate((0.0, -0.6, 0.6, -1.0, 0.2, -0.2)):
        cz = 1.8 + (0.15 if i == 5 else 0) - (0.15 if i == 4 else 0)
        head(d, -5.0 + i * 1.95, cz, 0.55, ink, None, turn, True, ink, 0.005)
    d = drw["USER_Expressions"]
    for i, emo in enumerate(("joy", "sad", "anger", "fear", "surprise", "disgust")):
        head(d, -1.6 + (i % 3) * 1.45, -0.6 - (i // 3) * 1.6, 0.48, ink, emo, 0.0, False)
    d = drw["USER_ModelSheet"]
    for i, turn in enumerate((0.0, 0.6, 1.0)):
        head(d, 2.9 + i * 1.2, -0.9, 0.5, ink, "joy" if i < 2 else None, turn, True, ink)


def build(sol):
    L.reset("SC_Expressions")
    ob, cam, drw = G.sheet("GP_Practice", 12.0, 6.75, ("GUIDE",), ("USER_Heads", "USER_Expressions", "USER_ModelSheet"))
    ob.data.layers["GUIDE"].lock = False
    guides(ob, drw["GUIDE"])
    ob.data.layers["GUIDE"].lock = True
    if sol:
        solution(ob, drw)
    L.instructions(NOTE)


def main():
    build(False)
    L.save(os.path.join(CH, "STARTER_FILES", "ch18_04_expressions_starter.blend"))
    build(True)
    p = L.save(os.path.join(CH, "COMPLETED_EXAMPLES", "ch18_04_expressions_solution.blend"))
    sc = bpy.context.scene
    sc.render.resolution_percentage = 60
    sc.render.filepath = os.path.join(os.path.dirname(p), "ch18_04_expressions_reference.png")
    bpy.ops.render.render(write_still=True)


if __name__ == "__main__":
    L.run(main)
