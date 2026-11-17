"""
build_ch02_09_files.py — « Retopologiser un rocher » (CH02.09).

  STARTER_FILES/ch02_09_retopo_starter.blend
      GEO_Sculpt : « sculpture » de rocher, 20 480 triangles (Ico Sphere déformée), verrouillée
      en sélection (hide_select) pour ne pas la modifier par erreur.
  COMPLETED_EXAMPLES/ch02_09_retopo_solution.blend (+ _reference.png, + _wire.png)
      GEO_Retopo : cage de 216 quads (cube subdivisé arrondi) + modificateur Shrinkwrap
      (Nearest Surface Point, cible GEO_Sculpt, offset 5 mm) ; GEO_Sculpt masquée au rendu.
Usage : blender -b --factory-startup --python-exit-code 1 --python build_ch02_09_files.py
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
NOTE = """CH02.09 — RETOPOLOGISER UN ROCHER
GEO_Sculpt : 20 480 triangles, inutilisable en animation ou en UV. Objectif : GEO_Retopo, une
cage LÉGÈRE (100 à 3 000 faces) en QUADS qui épouse la surface (écart moyen < 2 cm).
Méthode rapide pour une forme fermée simple (méthode « Shrinkwrap ») :
1. Add > Mesh > Cube (même centre que le rocher), F2 > GEO_Retopo.
2. Edit Mode : A, clic droit > Subdivide, Number of Cuts 5 ; puis Shift+Alt+S (To Sphere) 1.
   Object Mode : N > Dimensions ≈ 2 × 1,56 × 1,32 m (la cage ENVELOPPE le rocher), Ctrl+A > Scale.
   Une cage trop petite se colle au centre et laisse des zones non couvertes (mesuré : 63 %).
3. Object Mode : Add Modifier > Deform > Shrinkwrap : Target GEO_Sculpt,
   Wrap Method Nearest Surface Point, Offset 0.005.
4. Masquez GEO_Sculpt au rendu ; vérifiez avec l'overlay Retopology (Edit Mode).
Méthode manuelle (formes complexes) : Poly Build + Snap Target for Individual Elements :
Face Project — voir le TUTORIAL.
Vérification : SCRIPTS/validate_ch02_09.py -- --exercise retopo
"""
CENTER = (0.0, 0.0, 0.62)


def rock_radius(d):
    x, y, z = d
    return 1.0 + 0.14 * math.sin(3.1 * x + 0.4) * math.sin(2.3 * y) + 0.09 * math.sin(4.7 * z + 1.3) \
        + 0.05 * math.sin(7.0 * x * y + 2.0)


def build(sol):
    L.reset("SC_Retopo")
    L.studio(subject_height=1.2)
    col = L.collection("ASSETS")
    stone = L.material("MAT_Stone", (0.45, 0.43, 0.4), 0.8)
    me = bpy.data.meshes.new("ME_Sculpt")
    bm = bmesh.new()
    bmesh.ops.create_icosphere(bm, subdivisions=6, radius=1.0)   # bmesh : 6 → 20 480 faces
    for v in bm.verts:
        d = v.co.normalized()
        r = rock_radius(d)
        v.co = d * r
        v.co.x *= 0.85
        v.co.y *= 0.65
        v.co.z *= 0.55
    bm.to_mesh(me)
    bm.free()
    sculpt = bpy.data.objects.new("GEO_Sculpt", me)
    sculpt.location = CENTER
    col.objects.link(sculpt)
    me.materials.append(stone)
    for p in me.polygons:
        p.use_smooth = True
    sculpt.hide_select = True
    if sol:
        rm = bpy.data.meshes.new("ME_Retopo")
        bm = bmesh.new()
        bmesh.ops.create_cube(bm, size=1.0)
        bmesh.ops.subdivide_edges(bm, edges=bm.edges[:], cuts=5, use_grid_fill=True)
        for v in bm.verts:                       # To Sphere, puis enveloppe grossière du rocher
            v.co = v.co.normalized()
            v.co.x *= 1.0
            v.co.y *= 0.78
            v.co.z *= 0.66
        bm.to_mesh(rm)
        bm.free()
        retopo = bpy.data.objects.new("GEO_Retopo", rm)
        retopo.location = CENTER
        col.objects.link(retopo)
        rm.materials.append(L.material("MAT_Retopo", (0.3, 0.55, 0.85), 0.5))
        for p in rm.polygons:
            p.use_smooth = True
        sw = retopo.modifiers.new("Shrinkwrap", "SHRINKWRAP")
        sw.target = sculpt
        sw.wrap_method = "NEAREST_SURFACEPOINT"
        sw.offset = 0.005
        sculpt.hide_render = True
    cam = L.obj("CAM_Main")
    cam.location = (1.9, -3.2, 2.0)
    cam.data.lens = 45
    L.obj("EMP_Target").location = (0, 0, 0.55)
    L.render_defaults("BLENDER_EEVEE", 50)
    L.instructions(NOTE)


def main():
    build(False)
    L.save(os.path.join(CH, "STARTER_FILES", "ch02_09_retopo_starter.blend"))
    build(True)
    p = L.save(os.path.join(CH, "COMPLETED_EXAMPLES", "ch02_09_retopo_solution.blend"))
    sc = bpy.context.scene
    sc.render.filepath = os.path.join(os.path.dirname(p), "ch02_09_retopo_reference.png")
    bpy.ops.render.render(write_still=True)
    # image fil de fer de la cage (non enregistré)
    ret = L.obj("GEO_Retopo")
    w = ret.modifiers.new("Wire", "WIREFRAME")
    w.thickness = 0.008
    w.use_replace = False
    w.material_offset = 1
    ret.data.materials.append(L.material("MAT_WireDark", (0.02, 0.02, 0.03), 0.9))
    sc.render.filepath = os.path.join(os.path.dirname(p), "ch02_09_retopo_wire.png")
    bpy.ops.render.render(write_still=True)


if __name__ == "__main__":
    L.run(main)
