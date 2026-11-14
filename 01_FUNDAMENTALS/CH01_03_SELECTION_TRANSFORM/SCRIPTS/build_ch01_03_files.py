"""
build_ch01_03_files.py — Le puzzle des transformations (CH01.03).

  STARTER_FILES/ch01_03_puzzle_starter.blend
      4 pièces GEO_Piece_A…D à ranger dans leurs silhouettes fil de fer TGT_A…D :
        A cube : déplacement seul
        B cône : déplacement + rotation 90° sur X
        C cylindre : déplacement + mise à l'échelle ×2 sur Z
        D Suzanne : déplacement + rotation 45° sur Z + échelle 0,5
      + 30 « cailloux » GEO_Pebble_* pour s'entraîner aux sélections (box, cercle, lasso).
  COMPLETED_EXAMPLES/ch01_03_puzzle_solution.blend
Usage : blender -b --factory-startup --python build_ch01_03_files.py --python-exit-code 1
Testé avec : Blender 5.3.0.
"""
import math
import os
import random
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bpy  # noqa: E402

CH = L.chapter_dir(__file__)
# nom : (opérateur, kwargs, départ (loc, rot°, scale), cible (loc, rot°, scale))
PIECES = {
    "A": (bpy.ops.mesh.primitive_cube_add, {"size": 1},
          ((-3, -3, 0.5), (0, 0, 0), (1, 1, 1)), ((2, 2, 0.5), (0, 0, 0), (1, 1, 1))),
    "B": (bpy.ops.mesh.primitive_cone_add, {"radius1": 0.5, "depth": 1.2},
          ((-1, -3, 0.6), (0, 0, 0), (1, 1, 1)), ((4, 2, 0.5), (90, 0, 0), (1, 1, 1))),
    "C": (bpy.ops.mesh.primitive_cylinder_add, {"radius": 0.4, "depth": 1},
          ((1, -3, 0.5), (0, 0, 0), (1, 1, 1)), ((2, 4, 1.0), (0, 0, 0), (1, 1, 2))),
    "D": (bpy.ops.mesh.primitive_monkey_add, {"size": 1},
          ((3, -3, 0.6), (0, 0, 0), (1, 1, 1)), ((4, 4, 0.3), (0, 0, 45), (0.5, 0.5, 0.5))),
}
NOTE = """CH01.03 — LE PUZZLE
Rangez chaque pièce GEO_Piece_X exactement dans sa silhouette TGT_X (fil de fer).
Valeurs exactes (à saisir au clavier : G, R, S + axe + nombre + Entrée) :
  A : position (2, 2, 0.5)
  B : position (4, 2, 0.5), rotation X = 90°
  C : position (2, 4, 1),   échelle Z = 2
  D : position (4, 4, 0.3), rotation Z = 45°, échelle 0.5 (uniforme)
Méthode conseillée : sélectionner la pièce, Alt+G (remise à zéro), puis G X 2 Entrée…
Vérifiez dans la sidebar (N > Item).
"""


def apply(o, tr):
    loc, rot, sca = tr
    o.location = loc
    o.rotation_euler = [math.radians(a) for a in rot]
    o.scale = sca


def build(solution):
    L.reset("SC_Puzzle")
    L.studio(subject_height=1.0)
    pcol, tcol, pb = L.collection("PIECES"), L.collection("TARGETS"), L.collection("PEBBLES")
    colors = {"A": (0.9, 0.2, 0.1), "B": (0.1, 0.5, 0.9), "C": (0.2, 0.8, 0.3), "D": (0.95, 0.75, 0.1)}
    for k, (op, kw, start, target) in PIECES.items():
        p = L.mesh(op, f"GEO_Piece_{k}", pcol, L.material(f"MAT_Piece_{k}", colors[k], 0.4), **kw)
        t = bpy.data.objects.new(f"TGT_{k}", p.data.copy())
        t.data.name = f"ME_Target_{k}"
        tcol.objects.link(t)
        t.display_type = "WIRE"
        t.hide_render = True
        t.hide_select = True
        apply(t, target)
        apply(p, target if solution else start)
    random.seed(3)
    m = L.material("MAT_Pebble", (0.4, 0.4, 0.42))
    for i in range(30):
        L.sphere(f"GEO_Pebble_{i:02d}", pb, m, radius=0.12, segments=12, ring_count=6,
                 location=(random.uniform(-6, -2), random.uniform(1, 6), 0.12))
    L.render_defaults("BLENDER_EEVEE", 50)
    L.instructions(NOTE)


def main():
    build(False)
    L.save(os.path.join(CH, "STARTER_FILES", "ch01_03_puzzle_starter.blend"))
    build(True)
    L.save(os.path.join(CH, "COMPLETED_EXAMPLES", "ch01_03_puzzle_solution.blend"))


if __name__ == "__main__":
    L.run(main)
