"""
build_ch01_06_files.py — Le déménagement (CH01.06 : appliquer, orientations, snapping).

  STARTER_FILES/ch01_06_moving_starter.blend
      GEO_Crate : caisse de 2 × 1 × 0,5 m obtenue par une ÉCHELLE (2, 1, 0.5) non appliquée.
      GEO_Table : table (plateau à 0,8 m). GEO_Book : livre qui flotte à 1,6 m.
      GEO_Shelf : étagère à plaquer contre le mur GEO_Wall (face intérieure à y = 2).
      GEO_Plank : planche tournée de 30° sur Z, à déplacer le long de SA longueur.
  COMPLETED_EXAMPLES/ch01_06_moving_solution.blend
      Échelle de la caisse appliquée, livre posé sur la table, étagère contre le mur,
      planche avancée de 1 m dans sa direction locale X.
Usage : blender -b --factory-startup --python-exit-code 1 --python build_ch01_06_files.py
Testé avec : Blender 5.3.0.
"""
import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bpy  # noqa: E402

CH = L.chapter_dir(__file__)
NOTE = """CH01.06 — LE DÉMÉNAGEMENT
1. GEO_Crate : appliquez son échelle (Ctrl+A > Scale) -> Scale = 1,1,1 et Dimensions = 2 × 1 × 0,5.
2. GEO_Book : posez-le À PLAT sur le plateau de la table (snapping Face, ou calcul : le
   plateau est à z = 0,8 m, le livre fait 4 cm d'épaisseur).
3. GEO_Shelf : plaquez son dos contre le mur (la face du mur est à y = 2), sans changer X ni Z.
4. GEO_Plank : avancez-la de 1 m le long de SA PROPRE longueur (axe X local) : G X X 1.
"""


def build(solution):
    L.reset("SC_Moving")
    L.studio(subject_height=1.2)
    room, props = L.collection("ROOM"), L.collection("PROPS")
    wood = L.material("MAT_Wood", (0.45, 0.3, 0.16), 0.6)
    L.cube("GEO_Wall", room, L.material("MAT_Wall", (0.8, 0.78, 0.74), 0.9), size=1,
           location=(0, 2.1, 1.5), scale=(8, 0.2, 3))
    crate = L.cube("GEO_Crate", props, L.material("MAT_Crate", (0.6, 0.45, 0.25), 0.7), size=1,
                   location=(-3, -1, 0.25), scale=(2, 1, 0.5))
    top = L.cube("GEO_Table", props, wood, size=1, location=(1, -1, 0.775), scale=(1.4, 0.8, 0.05))
    for i, (x, y) in enumerate([(-.6, -.3), (.6, -.3), (-.6, .3), (.6, .3)]):
        L.cube(f"GEO_TableLeg_{i + 1}", props, wood, size=1, location=(1 + x, -1 + y, 0.375), scale=(0.05, 0.05, 0.75))
    book = L.cube("GEO_Book", props, L.material("MAT_Book", (0.6, 0.1, 0.1), 0.5), size=1,
                  location=(1.1, -1.05, 1.6), scale=(0.24, 0.17, 0.04))
    shelf = L.cube("GEO_Shelf", props, wood, size=1, location=(-1.5, 1.2, 1.2), scale=(1.2, 0.3, 1.6))
    plank = L.cube("GEO_Plank", props, wood, size=1, location=(3, 0, 0.05), scale=(2, 0.2, 0.05))
    plank.rotation_euler.z = math.radians(30)
    if solution:
        bpy.ops.object.select_all(action="DESELECT")
        crate.select_set(True)
        bpy.context.view_layer.objects.active = crate
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
        book.location.z = 0.8 + 0.02
        shelf.location.y = 2.0 - 0.15
        d = plank.matrix_world.to_quaternion() @ __import__("mathutils").Vector((1, 0, 0))
        plank.location += d * 1.0
    L.render_defaults("BLENDER_EEVEE", 50)
    L.instructions(NOTE)


def main():
    build(False)
    L.save(os.path.join(CH, "STARTER_FILES", "ch01_06_moving_starter.blend"))
    build(True)
    L.save(os.path.join(CH, "COMPLETED_EXAMPLES", "ch01_06_moving_solution.blend"))


if __name__ == "__main__":
    L.run(main)
