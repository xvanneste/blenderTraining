"""
build_ch18_01_files.py — Feuilles d'exercices « formes et volumes » (CH18.01).

  STARTER_FILES/ch18_01_volumes_starter.blend
      Feuille GP (caméra orthographique CAM_Sheet, fond papier) :
        GUIDE (verrouillé) : modèles — ligne d'horizon et 2 points de fuite, une boîte, un
          cylindre, une sphère avec ses zones de valeur (lumière, ombre propre, ombre portée),
          et trois zones de travail encadrées.
        USER_Lines   : vide — échauffement (traits droits, ellipses).
        USER_Boxes   : vide — 10 boîtes en perspective.
        USER_Values  : vide — 3 sphères ombrées en 3 valeurs (formes remplies).
  COMPLETED_EXAMPLES/ch18_01_volumes_solution.blend
      Exemple de feuille complétée (dessin généré par script, à titre de référence technique ;
      votre dessin à main levée sera différent et c'est normal).
  COMPLETED_EXAMPLES/ch18_01_volumes_reference.png   rendu de la solution
Usage : blender -b --factory-startup --python build_ch18_01_files.py --python-exit-code 1
Testé avec : Blender 5.3.0.
"""
import math
import os
import random
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "SCRIPTS"))
import bcma_gp as G  # noqa: E402
import bcma_lib as L  # noqa: E402
import bpy  # noqa: E402

CH = L.chapter_dir(__file__)
HZ, VPL, VPR = 1.4, -5.5, 5.5
NOTE = """CH18.01 — FORMES ET VOLUMES (sélectionnez GP_Practice, Ctrl+Tab > Draw Mode, Num 0)
Calque actif : menu Y (ou panneau Layers de l'onglet Data). Dessinez à la souris ou au stylet.
1. USER_Lines (zone du haut à gauche) : 20 traits droits d'un seul geste + 10 ellipses.
2. USER_Boxes (zone du bas) : 10 boîtes en perspective à 2 points de fuite, en suivant les
   fuyantes du calque GUIDE (horizon et PF dessinés).
3. USER_Values (zone du haut à droite) : 3 sphères ombrées en 3 valeurs, avec un matériau
   de remplissage (U > MAT_GP_Shadow ou MAT_GP_Light).
Effacer : Ctrl + clic gauche glissé. Lisser : Shift + clic gauche glissé. Taille : [ et ].
"""


def guides(ob, d):
    blue = G.material(ob, "MAT_GP_Guide", (0.25, 0.45, 0.85))
    ink = 0
    G.perspective_grid(d, HZ, [VPL, VPR], x_range=(-6, 6), n_rays=10, mat=blue, fan=3.5)
    G.box_two_point(d, -2.3, -1.9, 0.9, 0.12, 0.1, VPL, VPR, HZ, mat=ink)
    G.cylinder_sketch(d, -4.6, -1.9, 0.4, 0.12, 0.9, mat=ink)
    # sphère : contour, terminateur (limite d'ombre), ombre portée
    G.circle(d, (-0.8, -1.1), 0.5, mat=ink)
    G.ellipse(d, (-0.68, -1.1), 0.42, 0.5, mat=blue, angle=0.6)
    G.ellipse(d, (-0.45, -1.68), 0.55, 0.1, mat=blue)
    # zones de travail
    G.rect(d, -5.8, 0.4, -0.3, 3.2, mat=blue)        # USER_Lines
    G.rect(d, 0.3, 0.4, 5.8, 3.2, mat=blue)          # USER_Values
    G.rect(d, 0.3, -3.2, 5.8, -0.2, mat=blue)        # USER_Boxes


def solution_drawing(ob, drw):
    ink = 0
    shadow = G.material(ob, "MAT_GP_Shadow", (0.25, 0.25, 0.28), fill=(0.3, 0.3, 0.33))
    light = G.material(ob, "MAT_GP_Light", (0.6, 0.6, 0.62), fill=(0.72, 0.72, 0.74))
    random.seed(4)
    d = drw["USER_Lines"]
    for i in range(20):
        y = 3.0 - i * 0.12
        G.line(d, (-5.6, y), (-3.2 + random.uniform(-0.3, 0.3), y + random.uniform(-0.05, 0.05)), 0.006, ink, 6)
    for i in range(10):
        G.ellipse(d, (-2.4 + (i % 5) * 0.45, 2.6 - (i // 5) * 1.0), 0.18, 0.06 + 0.03 * (i % 5), 0.006, ink, 32)
    d = drw["USER_Boxes"]
    for i in range(10):
        x = 0.9 + (i % 5) * 1.05
        z = -0.9 - (i // 5) * 1.2
        G.box_two_point(d, x, z, 0.45 + 0.1 * (i % 3), 0.08, 0.06, VPL, VPR, HZ, 0.006, ink)
    d = drw["USER_Values"]
    for i in range(3):
        cx = 1.4 + i * 1.6
        G.circle(d, (cx, 1.8), 0.55, 0.006, ink, 48, fill_mat=light)          # forme (remplie)
        G.hatch_ellipse(d, (cx + 0.2, 1.72), 0.33, 0.44, 0.045, 0.8, 0.004, ink)  # ombre propre
        G.hatch_ellipse(d, (cx + 0.3, 1.72), 0.2, 0.35, 0.03, -0.8, 0.004, ink)   # cœur d'ombre
        G.ellipse(d, (cx + 0.35, 1.18), 0.55, 0.08, 0.004, shadow, 32)
        G.hatch_ellipse(d, (cx + 0.35, 1.18), 0.53, 0.07, 0.025, 0.0, 0.004, ink)  # ombre portée


def build(solution):
    L.reset("SC_Volumes")
    ob, cam, drw = G.sheet("GP_Practice", 12.0, 6.75, ("GUIDE",), ("USER_Lines", "USER_Boxes", "USER_Values"))
    G.material(ob, "MAT_GP_Shadow", (0.25, 0.25, 0.28), fill=(0.3, 0.3, 0.33))
    G.material(ob, "MAT_GP_Light", (0.6, 0.6, 0.62), fill=(0.72, 0.72, 0.74))
    ob.data.layers["GUIDE"].lock = False
    guides(ob, drw["GUIDE"])
    ob.data.layers["GUIDE"].lock = True
    if solution:
        solution_drawing(ob, drw)
    L.instructions(NOTE)
    return ob


def main():
    build(False)
    L.save(os.path.join(CH, "STARTER_FILES", "ch18_01_volumes_starter.blend"))
    build(True)
    p = L.save(os.path.join(CH, "COMPLETED_EXAMPLES", "ch18_01_volumes_solution.blend"))
    sc = bpy.context.scene
    sc.render.resolution_percentage = 60
    sc.render.filepath = os.path.join(os.path.dirname(p), "ch18_01_volumes_reference.png")
    bpy.ops.render.render(write_still=True)


if __name__ == "__main__":
    L.run(main)
