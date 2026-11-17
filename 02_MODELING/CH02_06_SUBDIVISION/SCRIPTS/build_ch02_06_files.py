"""
build_ch02_06_files.py — « Garder la forme sous la subdivision » (CH02.06).

  STARTER_FILES/ch02_06_subdiv_starter.blend
      Trois cubes de 80 cm, chacun avec un modificateur Subdivision Surface (Levels 2) :
      GEO_Support : devient une boule molle → boucles de maintien ;
      GEO_Crease  : devient une boule molle → crease sur les 4 arêtes du dessus ;
      GEO_Pebble  : galet (Levels 3 en viewport ET au rendu) → optimiser Levels / Render.
  COMPLETED_EXAMPLES/ch02_06_subdiv_solution.blend (+ _reference.png, + _starter_view.png)
Usage : blender -b --factory-startup --python-exit-code 1 --python build_ch02_06_files.py
Testé avec : Blender 5.3.0.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bmesh  # noqa: E402
import bpy  # noqa: E402
from mathutils import Vector  # noqa: E402

CH = L.chapter_dir(__file__)
NOTE = """CH02.06 — GARDER LA FORME SOUS LA SUBDIVISION
Chaque cube a un modificateur Subdivision Surface (Levels 2) : il devient une boule molle.
1. GEO_Support : ajoutez des BOUCLES DE MAINTIEN près de chaque arête : Edit Mode, Ctrl+R sur
   chaque anneau (3 directions), 2 coupes (au tiers : ±13,3 cm du centre), puis S + axe + 2.625
   pour les écarter à ±35 cm, soit 5 cm des bords. Le cube redevient cube, coins doux.
2. GEO_Crease : sélectionnez les 4 arêtes du DESSUS, Shift+E puis 1 (crease). Le dessus devient
   plat et net, le bas reste arrondi.
3. GEO_Pebble : dans le modificateur, Levels Viewport = 1 et Render = 3 (léger à l'écran,
   lisse au rendu).
Ne jamais appliquer les modificateurs. Vérification : SCRIPTS/validate_ch02_06.py -- --exercise subdiv
"""
S = 0.8


def cube_bm():
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=S)
    for v in bm.verts:
        v.co.z += S / 2
    return bm


def mk(name, col, mat, bm, x, levels=2, render=2):
    me = bpy.data.meshes.new(name.replace("GEO_", "ME_"))
    bm.to_mesh(me)
    bm.free()
    ob = bpy.data.objects.new(name, me)
    ob.location = (x, 0, 0)
    col.objects.link(ob)
    me.materials.append(mat)
    for p in me.polygons:
        p.use_smooth = True
    m = ob.modifiers.new("Subdivision", "SUBSURF")
    m.levels, m.render_levels = levels, render
    return ob


def build(sol):
    L.reset("SC_Subdiv")
    L.studio(subject_height=0.8)
    col = L.collection("SUBDIV")
    mat = L.material("MAT_Clay", (0.75, 0.72, 0.68), 0.5)
    bm = cube_bm()
    if sol:
        # boucles de maintien : 2 coupes par direction, écartées à 5 cm des bords
        bmesh.ops.subdivide_edges(bm, edges=bm.edges[:], cuts=2, use_grid_fill=True)
        half = S / 2
        for v in bm.verts:
            for ax in (0, 1):
                if 0.01 < abs(v.co[ax]) < half - 0.01:
                    v.co[ax] = (half - 0.05) * (1 if v.co[ax] > 0 else -1)
            z = v.co.z - half
            if 0.01 < abs(z) < half - 0.01:
                v.co.z = half + (half - 0.05) * (1 if z > 0 else -1)
    mk("GEO_Support", col, mat, bm, -1.3)
    crease = mk("GEO_Crease", col, mat, cube_bm(), 0.0)
    if sol:
        me = crease.data
        att = me.attributes.get("crease_edge") or me.attributes.new("crease_edge", "FLOAT", "EDGE")
        for e in me.edges:
            if all(me.vertices[i].co.z > S - 1e-4 for i in e.vertices):
                att.data[e.index].value = 1.0
    peb = cube_bm()
    for v in peb.verts:
        v.co.x *= 1.3
        v.co.z *= 0.55
    pebble = mk("GEO_Pebble", col, mat, peb, 1.4, levels=3, render=3)
    if sol:
        pebble.modifiers[0].levels = 1
        pebble.modifiers[0].render_levels = 3
    cam = L.obj("CAM_Main")
    cam.location = (0, -4.6, 2.2)
    cam.data.lens = 45
    L.obj("EMP_Target").location = (0, 0, 0.35)
    L.render_defaults("BLENDER_EEVEE", 50)
    L.instructions(NOTE)


def main():
    build(False)
    L.save(os.path.join(CH, "STARTER_FILES", "ch02_06_subdiv_starter.blend"))
    sc = bpy.context.scene
    sc.render.filepath = os.path.join(CH, "COMPLETED_EXAMPLES", "ch02_06_subdiv_starter_view.png")
    bpy.ops.render.render(write_still=True)
    build(True)
    p = L.save(os.path.join(CH, "COMPLETED_EXAMPLES", "ch02_06_subdiv_solution.blend"))
    bpy.context.scene.render.filepath = os.path.join(os.path.dirname(p), "ch02_06_subdiv_reference.png")
    bpy.ops.render.render(write_still=True)


if __name__ == "__main__":
    L.run(main)
