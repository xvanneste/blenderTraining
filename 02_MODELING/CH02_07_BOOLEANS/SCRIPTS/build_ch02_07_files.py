"""
build_ch02_07_files.py — « La platine percée » (CH02.07, booléens non destructifs).

  STARTER_FILES/ch02_07_plate_starter.blend
      GEO_Plate : platine 60 × 40 × 3 cm (8 sommets), aucun modificateur.
  COMPLETED_EXAMPLES/ch02_07_plate_solution.blend (+ _reference.png, + _moved.png)
      Collection CUTTERS (5 cutters : 4 cylindres Ø 5 cm aux coins + 1 lumière 20 × 4 cm au centre),
      affichés en fil de fer, désactivés au rendu ; GEO_Plate : Boolean (Collection CUTTERS,
      Difference, Exact) → Bevel (Angle 30°, 1,5 mm, 2 segments, Harden Normals), Shade Smooth.
      _moved.png : même fichier après déplacement d'un cutter (preuve du non destructif).
Usage : blender -b --factory-startup --python build_ch02_07_files.py --python-exit-code 1
Testé avec : Blender 5.3.0.
"""
import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bmesh  # noqa: E402
import bpy  # noqa: E402

CH = L.chapter_dir(__file__)
NOTE = """CH02.07 — LA PLATINE PERCÉE (non destructif : rien n'est appliqué)
GEO_Plate : 60 × 40 × 3 cm, posée au sol (z de 0 à 0,03).
1. Créez une collection CUTTERS. Dedans, 5 « cutters » qui TRAVERSENT la platine :
   4 cylindres (rayon 0.025, hauteur 0.1) en (±0.24, ±0.14, 0.015) et un pavé 0.2 × 0.04 × 0.1
   au centre (0, 0, 0.015). Nommez-les CUT_*.
2. Pour chaque cutter : Object Properties > Viewport Display > Display As : Wire ;
   Visibility > Show In : décochez Renders (ou l'icône caméra de l'Outliner).
3. GEO_Plate : Add Modifier > Generate > Boolean : Difference, Operand Type : Collection,
   Collection : CUTTERS, Solver : Exact.
4. APRÈS le Boolean : Add Modifier > Bevel (Limit Method Angle, Width 0.0015, Segments 2,
   Harden Normals). Object > Shade Smooth.
5. Testez : déplacez un cutter, le trou suit. Ne cliquez jamais Apply.
Vérification : SCRIPTS/validate_ch02_07.py -- --exercise plate
"""
CUTS = [("CUT_Hole_FR", (0.24, -0.14)), ("CUT_Hole_FL", (-0.24, -0.14)),
        ("CUT_Hole_BR", (0.24, 0.14)), ("CUT_Hole_BL", (-0.24, 0.14))]


def build(sol):
    L.reset("SC_Plate")
    L.studio(subject_height=0.2)
    col = L.collection("PROPS")
    steel = L.material("MAT_Steel_Brushed", (0.62, 0.63, 0.66), 0.35, metallic=1.0)
    me = bpy.data.meshes.new("ME_Plate")
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    for v in bm.verts:
        v.co.x *= 0.6
        v.co.y *= 0.4
        v.co.z = (v.co.z + 0.5) * 0.03
    bm.to_mesh(me)
    bm.free()
    plate = bpy.data.objects.new("GEO_Plate", me)
    col.objects.link(plate)
    me.materials.append(steel)
    if sol:
        cut_col = L.collection("CUTTERS")
        cutters = []
        for name, (x, y) in CUTS:
            c = L.cylinder(name, cut_col, None, radius=0.025, depth=0.1, location=(x, y, 0.015), vertices=32)
            cutters.append(c)
        cutters.append(L.cube("CUT_Slot", cut_col, None, size=1.0, location=(0, 0, 0.015), scale=(0.2, 0.04, 0.1)))
        bpy.ops.object.select_all(action="DESELECT")
        for c in cutters:
            c.select_set(True)
            bpy.context.view_layer.objects.active = c
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
        for c in cutters:
            c.display_type = "WIRE"
            c.hide_render = True
        b = plate.modifiers.new("Boolean", "BOOLEAN")
        b.operation = "DIFFERENCE"
        b.operand_type = "COLLECTION"
        b.collection = cut_col
        b.solver = "EXACT"
        bv = plate.modifiers.new("Bevel", "BEVEL")
        bv.limit_method = "ANGLE"
        bv.angle_limit = math.radians(30)
        bv.width = 0.0015
        bv.segments = 2
        bv.harden_normals = True
        for p in me.polygons:
            p.use_smooth = True
    cam = L.obj("CAM_Main")
    cam.location = (0.55, -0.75, 0.6)
    cam.data.lens = 45
    L.obj("EMP_Target").location = (0, 0, 0.0)
    L.render_defaults("BLENDER_EEVEE", 50)
    L.instructions(NOTE)


def main():
    build(False)
    L.save(os.path.join(CH, "STARTER_FILES", "ch02_07_plate_starter.blend"))
    build(True)
    p = L.save(os.path.join(CH, "COMPLETED_EXAMPLES", "ch02_07_plate_solution.blend"))
    sc = bpy.context.scene
    sc.render.filepath = os.path.join(os.path.dirname(p), "ch02_07_plate_reference.png")
    bpy.ops.render.render(write_still=True)
    # preuve du non destructif : on déplace la lumière centrale (non enregistré)
    L.obj("CUT_Slot").location.x = 0.12
    L.obj("CUT_Slot").rotation_euler.z = math.radians(90)
    sc.render.filepath = os.path.join(os.path.dirname(p), "ch02_07_plate_moved.png")
    bpy.ops.render.render(write_still=True)


if __name__ == "__main__":
    L.run(main)
