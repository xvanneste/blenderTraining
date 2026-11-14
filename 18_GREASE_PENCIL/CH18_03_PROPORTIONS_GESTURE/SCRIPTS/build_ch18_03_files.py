"""
build_ch18_03_files.py — Feuille « proportions, silhouettes, gestuelle » (CH18.03).

  STARTER_FILES/ch18_03_gesture_starter.blend
      GUIDE (verrouillé) : échelle de proportions (8 graduations de 1 tête), mannequin de face,
        4 lignes d'action types (droite, C, S, inversée), zones de travail.
      USER_Gesture     : vide — 20 croquis gestuels de 30 s (une ligne d'action + tête + bassin).
      USER_Mannequins  : vide — 8 mannequins dans 8 poses différentes.
      USER_Silhouettes : vide — 4 silhouettes noires remplies, lisibles sans détail.
  COMPLETED_EXAMPLES/ch18_03_gesture_solution.blend (+ _reference.png)
Usage : blender -b --factory-startup --python build_ch18_03_files.py --python-exit-code 1
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
NOTE = """CH18.03 — PROPORTIONS, SILHOUETTES, GESTUELLE (GP_Practice, Draw Mode, Num 0)
1. USER_Gesture (bande du haut) : 20 croquis gestuels de 30 secondes chacun (chronomètre !),
   d'après des photos de poses (sport, danse, travail) : d'abord la LIGNE D'ACTION, puis
   tête, cage thoracique, bassin, membres en traits.
2. USER_Mannequins (zone du bas) : 8 mannequins (≈ 7,5 têtes) dans 8 poses différentes :
   debout, marche, course, saut, assis, accroupi, porter, montrer du doigt.
3. USER_Silhouettes (zone de droite) : 4 silhouettes noires remplies (matériau MAT_GP_Black,
   U) qui restent lisibles sans aucun détail intérieur.
"""


def s_curve(d, x, z, h, bend, mat=0, radius=0.006):
    pts = [(x + bend * math.sin(math.pi * t / 12 * 1.2), z + h * t / 12) for t in range(13)]
    G.polyline(d, pts, radius, mat)


def guides(ob, d):
    blue = G.material(ob, "MAT_GP_Guide", (0.25, 0.45, 0.85))
    # échelle de proportions : 8 têtes de 0,3 m
    x0, z0, H = -5.6, -2.9, 0.3
    G.line(d, (x0, z0), (x0, z0 + 8 * H), 0.004, blue)
    for i in range(9):
        G.line(d, (x0 - 0.08, z0 + i * H), (x0 + 0.08, z0 + i * H), 0.004, blue)
    G.mannequin(d, x0 + 0.6, z0, 7.5 * H, "stand", 0.006, 0)
    # lignes d'action types
    for i, bend in enumerate((0.0, 0.25, 0.35, -0.25)):
        s_curve(d, -4.2 + i * 0.55, -2.9, 2.0, bend, blue, 0.006)
    # zones
    G.rect(d, -5.9, 0.6, 5.9, 3.2, 0.006, blue)       # USER_Gesture
    G.rect(d, -1.9, -3.2, 3.2, 0.3, 0.006, blue)      # USER_Mannequins
    G.rect(d, 3.4, -3.2, 5.9, 0.3, 0.006, blue)       # USER_Silhouettes


def solution(ob, drw):
    ink = 0
    black = G.material(ob, "MAT_GP_Black", (0.02, 0.02, 0.02), fill=(0.02, 0.02, 0.02))
    d = drw["USER_Gesture"]
    for i in range(20):
        x = -5.6 + i * 0.57
        bend = 0.3 * math.sin(i * 1.7)
        s_curve(d, x, 0.9, 1.6, bend, ink, 0.007)

        def at(t):  # point de la ligne d'action à la fraction t (0 = pieds, 1 = tête)
            return (x + bend * math.sin(math.pi * t * 1.2), 0.9 + 1.6 * t)
        hx, hz = at(1.0)
        G.ellipse(d, (hx, hz + 0.1), 0.08, 0.1, 0.005, ink, 16)          # tête au bout de la ligne
        px, pz = at(0.45)
        G.ellipse(d, (px, pz), 0.12, 0.07, 0.005, ink, 16)               # bassin sur la ligne
        cx, cz = at(0.75)
        G.ellipse(d, (cx, cz), 0.1, 0.14, 0.005, ink, 16)                # cage thoracique
    d = drw["USER_Mannequins"]
    poses = ["stand", "walk", "reach", "sit", "walk", "reach", "stand", "sit"]
    for i, p in enumerate(poses):
        G.mannequin(d, -1.5 + (i % 4) * 1.2, -3.0 + (i // 4) * 1.75, 1.6, p, 0.005, ink)
    d = drw["USER_Silhouettes"]
    # silhouettes « au feutre » : mannequins tracés en traits très épais avec le matériau noir
    for i, p in enumerate(["walk", "reach", "sit", "stand"]):
        G.mannequin(d, 3.95 + (i % 2) * 1.25, -3.0 + (i // 2) * 1.7, 1.45, p, 0.05, black)


def build(sol):
    L.reset("SC_Gesture")
    ob, cam, drw = G.sheet("GP_Practice", 12.0, 6.75, ("GUIDE",), ("USER_Gesture", "USER_Mannequins", "USER_Silhouettes"))
    G.material(ob, "MAT_GP_Black", (0.02, 0.02, 0.02), fill=(0.02, 0.02, 0.02))
    ob.data.layers["GUIDE"].lock = False
    guides(ob, drw["GUIDE"])
    ob.data.layers["GUIDE"].lock = True
    if sol:
        solution(ob, drw)
    L.instructions(NOTE)


def main():
    build(False)
    L.save(os.path.join(CH, "STARTER_FILES", "ch18_03_gesture_starter.blend"))
    build(True)
    p = L.save(os.path.join(CH, "COMPLETED_EXAMPLES", "ch18_03_gesture_solution.blend"))
    sc = bpy.context.scene
    sc.render.resolution_percentage = 60
    sc.render.filepath = os.path.join(os.path.dirname(p), "ch18_03_gesture_reference.png")
    bpy.ops.render.render(write_still=True)


if __name__ == "__main__":
    L.run(main)
