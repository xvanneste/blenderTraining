"""
build_ch02_04_files.py — « Les ombrages ratés » (CH02.04, normales).

  STARTER_FILES/ch02_04_normals_starter.blend
      GEO_Flipped : cube subdivisé dont 7 faces ont la normale inversée (vers l'intérieur) ;
      GEO_Can     : boîte de conserve (cylindre 32 côtés) en Shade Smooth intégral : couvercles
                    dégradés, arêtes molles ;
      GEO_Block   : pavé chanfreiné (bevel 1 segment) en Shade Smooth : grandes faces tachées.
  COMPLETED_EXAMPLES/ch02_04_normals_solution.blend (+ _reference.png, + _starter_view.png)
      GEO_Flipped : Recalculate Outside ; GEO_Can : Shade Auto Smooth 30° ; GEO_Block : Weighted
      Normal (Face Influence, Keep Sharp).
Usage : blender -b --factory-startup --python-exit-code 1 --python build_ch02_04_files.py
Testé avec : Blender 5.3.0.
"""
import math
import os
import random
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bmesh  # noqa: E402
import bpy  # noqa: E402

CH = L.chapter_dir(__file__)
NOTE = """CH02.04 — LES OMBRAGES RATÉS
Activez Viewport Overlays > Face Orientation : bleu = extérieur, rouge = intérieur (normale inversée).
1. GEO_Flipped : des faces sont rouges. Edit Mode, A, Mesh > Normals > Recalculate Outside (Shift+N).
2. GEO_Can : couvercles et arêtes « molles ». Object Mode : Object > Shade Auto Smooth,
   Angle 30° (un modificateur « Smooth by Angle » est ajouté).
3. GEO_Block : grandes faces tachées de dégradés. Add Modifier > Normals > Weighted Normal :
   cochez Keep Sharp et Face Influence, Weight 100 (l'objet doit être en Shade Smooth).
Vérification : SCRIPTS/validate_ch02_04.py -- --exercise normals
"""


def mk(name, col, mat, bm, loc):
    me = bpy.data.meshes.new(name.replace("GEO_", "ME_"))
    bm.normal_update()
    bm.to_mesh(me)
    bm.free()
    ob = bpy.data.objects.new(name, me)
    ob.location = loc
    col.objects.link(ob)
    me.materials.append(mat)
    return ob


def build(sol):
    L.reset("SC_Normals")
    L.studio(subject_height=1.0)
    col = L.collection("PATIENTS")
    paint = L.material("MAT_Paint", (0.55, 0.12, 0.1), 0.35)
    tin = L.material("MAT_Tin", (0.8, 0.8, 0.82), 0.25, metallic=1.0)
    plastic = L.material("MAT_Plastic", (0.15, 0.35, 0.6), 0.3)
    # 1. faces inversées
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=0.9)
    bmesh.ops.subdivide_edges(bm, edges=bm.edges[:], cuts=1, use_grid_fill=True)
    for v in bm.verts:
        v.co.z += 0.45
    rnd = random.Random(7)
    bm.faces.ensure_lookup_table()
    for i in rnd.sample(range(len(bm.faces)), 7):
        bm.faces[i].normal_flip()
    flipped = mk("GEO_Flipped", col, paint, bm, (-1.7, 0, 0))
    # 2. boîte de conserve lissée partout
    bm = bmesh.new()
    bmesh.ops.create_cone(bm, cap_ends=True, segments=32, radius1=0.35, radius2=0.35, depth=0.8)
    for v in bm.verts:
        v.co.z += 0.4
    can = mk("GEO_Can", col, tin, bm, (0, 0, 0))
    for p in can.data.polygons:
        p.use_smooth = True
    # 3. pavé chanfreiné lissé
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    for v in bm.verts:
        v.co.x *= 0.9
        v.co.y *= 0.6
        v.co.z = (v.co.z + 0.5) * 0.7
    bmesh.ops.bevel(bm, geom=bm.edges[:], offset=0.06, segments=1, affect="EDGES", profile=0.5)
    block = mk("GEO_Block", col, plastic, bm, (1.8, 0, 0))
    for p in block.data.polygons:
        p.use_smooth = True
    if sol:
        bm = bmesh.new()
        bm.from_mesh(flipped.data)
        bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])
        bm.to_mesh(flipped.data)
        bm.free()
        bpy.ops.object.select_all(action="DESELECT")
        bpy.context.view_layer.objects.active = can
        can.select_set(True)
        bpy.ops.object.shade_auto_smooth(angle=math.radians(30))      # opérateur de l'interface
        m = block.modifiers.new("WeightedNormal", "WEIGHTED_NORMAL")
        m.use_face_influence = True
        m.keep_sharp = True
        m.weight = 100        # mesuré : grandes faces parfaitement plates dès Weight ≥ 75 (50 = 0,994)
    cam = L.obj("CAM_Main")
    cam.location = (0.2, -5.2, 2.4)
    cam.data.lens = 40
    L.obj("EMP_Target").location = (0, 0, 0.4)
    L.render_defaults("BLENDER_EEVEE", 50)
    L.instructions(NOTE)


def main():
    build(False)
    p0 = L.save(os.path.join(CH, "STARTER_FILES", "ch02_04_normals_starter.blend"))
    sc = bpy.context.scene
    sc.render.filepath = os.path.join(CH, "COMPLETED_EXAMPLES", "ch02_04_normals_starter_view.png")
    bpy.ops.render.render(write_still=True)
    build(True)
    p = L.save(os.path.join(CH, "COMPLETED_EXAMPLES", "ch02_04_normals_solution.blend"))
    bpy.context.scene.render.filepath = os.path.join(os.path.dirname(p), "ch02_04_normals_reference.png")
    bpy.ops.render.render(write_still=True)


if __name__ == "__main__":
    L.run(main)
