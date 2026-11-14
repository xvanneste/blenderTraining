"""
build_ch01_07_files.py — La porte et la roue (CH01.07 : origines, pivots, curseur 3D).

  STARTER_FILES/ch01_07_door_starter.blend
      GEO_Door : porte de 0,9 × 0,04 × 2 m, ORIGINE AU CENTRE (x de -0,45 à 0,45, base à z = 0,
      dans un encadrement GEO_Frame). Charnière prévue : arête verticale gauche (x = -0,45).
      GEO_Wheel : roue posée à plat, centre (2, 0, 0,1) ; GEO_Bolt_1..3 : trois boulons à
      0°, 120° et 200° autour du centre (rayon 0,3 m).
  COMPLETED_EXAMPLES/ch01_07_door_solution.blend
      Origine de la porte placée sur la charnière (-0,45 ; 0 ; 0), porte ouverte de 90° ;
      boulons tournés de 45° autour du CENTRE DE LA ROUE (pivot = 3D Cursor).
Usage : blender -b --factory-startup --python build_ch01_07_files.py --python-exit-code 1
Testé avec : Blender 5.3.0.
"""
import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bpy  # noqa: E402
from mathutils import Matrix, Vector  # noqa: E402

CH = L.chapter_dir(__file__)
WHEEL = Vector((2, 0, 0.1))
NOTE = """CH01.07 — LA PORTE ET LA ROUE
Porte : l'origine (point orange) est au centre : la porte tourne sur elle-même comme une
girouette. Placez l'ORIGINE sur la charnière (arête verticale gauche, au sol) :
  Edit Mode > sélectionnez les 2 sommets bas-gauche (avant + arrière : l'arête du bas, côté
  charnière) > Shift+S > Cursor to Selected (milieu de l'arête) >
  Object Mode > Object > Set Origin > Origin to 3D Cursor.
Puis ouvrez la porte : R Z 90.
Roue : tournez les 3 boulons de 45° autour du centre de la roue (et non autour de leur
propre centre) : Shift+S > Cursor to Selected (roue sélectionnée), pivot (.) = 3D Cursor,
sélectionnez les boulons, R Z 45.
"""


def build(solution):
    L.reset("SC_Door")
    L.studio(subject_height=1.8)
    col = L.collection("PROPS")
    wood = L.material("MAT_Door", (0.5, 0.33, 0.18), 0.5)
    frame = L.material("MAT_Frame", (0.85, 0.85, 0.82), 0.6)
    for nm, loc, sc in [("GEO_Frame_L", (-0.5, 0, 1.025), (0.1, 0.12, 2.05)), ("GEO_Frame_R", (0.5, 0, 1.025), (0.1, 0.12, 2.05)),
                        ("GEO_Frame_Top", (0, 0, 2.05), (1.1, 0.12, 0.1))]:
        L.cube(nm, col, frame, size=1, location=loc, scale=sc)
    door = L.cube("GEO_Door", col, wood, size=1, location=(0, 0, 1.0), scale=(0.9, 0.04, 2.0))
    bpy.ops.object.select_all(action="DESELECT")
    door.select_set(True)
    bpy.context.view_layer.objects.active = door
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    metal = L.material("MAT_Metal", (0.7, 0.7, 0.72), 0.3, 1.0)
    L.cylinder("GEO_Wheel", col, L.material("MAT_Rubber", (0.05, 0.05, 0.05), 0.8), radius=0.5, depth=0.2,
               location=tuple(WHEEL), vertices=48)
    bolts = []
    for i, ang in enumerate((0, 120, 200)):
        a = math.radians(ang)
        bolts.append(L.cylinder(f"GEO_Bolt_{i + 1}", col, metal, radius=0.04, depth=0.06, vertices=6,
                                location=(WHEEL.x + 0.3 * math.cos(a), WHEEL.y + 0.3 * math.sin(a), 0.22)))
    if solution:
        hinge = Vector((-0.45, 0, 0))
        offset = door.location - hinge          # déplacer l'origine sans bouger la géométrie
        door.data.transform(Matrix.Translation(offset))
        door.location = hinge
        door.rotation_euler.z = math.radians(90)
        rot = Matrix.Rotation(math.radians(45), 4, "Z")
        for b in bolts:
            p = b.location - Vector((WHEEL.x, WHEEL.y, 0))
            p = rot @ p
            b.location = Vector((WHEEL.x, WHEEL.y, 0)) + p
            b.rotation_euler.z += math.radians(45)
    L.render_defaults("BLENDER_EEVEE", 50)
    L.instructions(NOTE)


def main():
    build(False)
    L.save(os.path.join(CH, "STARTER_FILES", "ch01_07_door_starter.blend"))
    build(True)
    L.save(os.path.join(CH, "COMPLETED_EXAMPLES", "ch01_07_door_solution.blend"))


if __name__ == "__main__":
    L.run(main)
