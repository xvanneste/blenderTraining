"""
build_ch01_10_files.py — Le petit pont (CH01.10 : pile de modificateurs non destructive).

  STARTER_FILES/ch01_10_bridge_starter.blend
      GEO_Plank      une seule planche (1 × 0,25 × 0,05 m) au début du pont
      GEO_Railing    la MOITIÉ droite d'une rambarde (x de 0 à 2,5 m)
      GEO_Pillar     un pilier cubique aux arêtes vives (échelle appliquée)
      GEO_Bucket     un seau : cylindre ouvert SANS épaisseur, facettes visibles
  COMPLETED_EXAMPLES/ch01_10_bridge_solution.blend
      Array (10 planches), Mirror (rambarde complète), Bevel (pilier), Solidify puis
      Subdivision Surface (seau). Aucun modificateur appliqué : tout reste réglable.
Usage : blender -b --factory-startup --python build_ch01_10_files.py --python-exit-code 1
Testé avec : Blender 5.3.0.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bmesh  # noqa: E402
import bpy  # noqa: E402

CH = L.chapter_dir(__file__)
NOTE = """CH01.10 — LE PETIT PONT (Properties > Modifiers > Add Modifier)
1. GEO_Plank : Array (Generate > Array), Count 10, Relative Offset X ≈ 1,05 -> tablier de pont.
2. GEO_Railing : Mirror sur X -> rambarde complète (de -2,5 à +2,5 m).
3. GEO_Pillar : Bevel, Amount 0,02 m, Segments 3 -> arêtes adoucies.
4. GEO_Bucket : Solidify (Thickness 0,02 m) PUIS Subdivision Surface (Levels Viewport 1,
   Render 2). Ordre dans la pile : Solidify au-dessus de Subdivision.
Ne cliquez pas « Apply » : on garde la pile modifiable (non destructif).
"""


def bucket_mesh():
    me = bpy.data.meshes.new("ME_Bucket")
    bm = bmesh.new()
    res = bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=12, radius1=0.25, radius2=0.32, depth=0.5)
    top = [f for f in bm.faces if f.normal.z > 0.9 and len(f.verts) > 4]
    bmesh.ops.delete(bm, geom=top, context="FACES_ONLY")
    bmesh.ops.translate(bm, vec=(0, 0, 0.25), verts=bm.verts)
    bm.to_mesh(me)
    bm.free()
    return me


def build(solution):
    L.reset("SC_Bridge")
    L.studio(subject_height=1.0)
    col = L.collection("BRIDGE")
    wood = L.material("MAT_Wood", (0.42, 0.28, 0.15), 0.7)
    plank = L.cube("GEO_Plank", col, wood, size=1, location=(-2.4, 0, 0.5), scale=(0.25, 1.0, 0.05))
    rail = L.cube("GEO_Railing", col, wood, size=1, location=(0, 0.55, 1.0), scale=(1, 1, 1))
    rail.data.transform(__import__("mathutils").Matrix.Diagonal((2.5, 0.06, 0.06, 1)) @
                        __import__("mathutils").Matrix.Translation((0.5, 0, 0)))
    pillar = L.cube("GEO_Pillar", col, L.material("MAT_Stone", (0.5, 0.5, 0.48), 0.8), size=1,
                    location=(-2.6, -0.8, 0.25), scale=(0.3, 0.3, 0.5))
    bucket = bpy.data.objects.new("GEO_Bucket", bucket_mesh())
    bucket.location = (1.5, -1.2, 0)
    col.objects.link(bucket)
    bucket.data.materials.append(L.material("MAT_Bucket", (0.2, 0.35, 0.6), 0.4, 0.8))
    for o in (plank, pillar):
        bpy.ops.object.select_all(action="DESELECT")
        o.select_set(True)
        bpy.context.view_layer.objects.active = o
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    if solution:
        a = plank.modifiers.new("Array", "ARRAY")
        a.count = 10
        a.relative_offset_displace = (1.05, 0, 0)
        m = rail.modifiers.new("Mirror", "MIRROR")
        m.use_axis[0] = True
        b = pillar.modifiers.new("Bevel", "BEVEL")
        b.width = 0.02
        b.segments = 3
        s = bucket.modifiers.new("Solidify", "SOLIDIFY")
        s.thickness = 0.02
        sub = bucket.modifiers.new("Subdivision", "SUBSURF")
        sub.levels, sub.render_levels = 1, 2
        for p in bucket.data.polygons:
            p.use_smooth = True
    L.render_defaults("BLENDER_EEVEE", 50)
    L.instructions(NOTE)


def main():
    build(False)
    L.save(os.path.join(CH, "STARTER_FILES", "ch01_10_bridge_starter.blend"))
    build(True)
    L.save(os.path.join(CH, "COMPLETED_EXAMPLES", "ch01_10_bridge_solution.blend"))


if __name__ == "__main__":
    L.run(main)
