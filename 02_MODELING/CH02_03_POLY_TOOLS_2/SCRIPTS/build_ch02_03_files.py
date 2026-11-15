"""
build_ch02_03_files.py — « L'atelier de découpe » (CH02.03, outils polygonaux II).

  STARTER_FILES/ch02_03_cutting_starter.blend — 6 postes :
      GEO_Bar     (x = -3)   : pavé 40 × 40 × 120 cm → Bisect à z = 0,8, haut supprimé, coupe remplie ;
      GEO_Messy   (x = -1,6) : cube aux faces inutilement découpées → Limited Dissolve ;
      GEO_Profile (x = 0)    : profil de vase (arêtes seules) → Spin 360° ;
      GEO_Pyramid (x = 1,4)  : cube → Merge At Center des 4 sommets du haut ;
      GEO_Spring  (x = 2,8)  : petit cercle décalé → modificateur Screw (ressort) ;
      GEO_Tile    (x = 4,2)  : carreau (une face) → Knife d'un coin à l'autre.
  COMPLETED_EXAMPLES/ch02_03_cutting_solution.blend (+ _reference.png)
Usage : blender -b --factory-startup --python build_ch02_03_files.py --python-exit-code 1
Testé avec : Blender 5.3.0.
"""
import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bmesh  # noqa: E402
import bpy  # noqa: E402
from mathutils import Matrix, Vector  # noqa: E402

CH = L.chapter_dir(__file__)
NOTE = """CH02.03 — L'ATELIER DE DÉCOUPE (Edit Mode sauf mention)
1. GEO_Bar : Mesh > Bisect. Tracez une ligne horizontale, puis dans le panneau de l'opération :
   Plane Point Z = 0.8 (coordonnées LOCALES : l'origine est au pied), Plane Normal (0, 0, 1),
   cochez Fill et Clear Outer. Le haut disparaît, la coupe est bouchée.
2. GEO_Messy : A, puis X > Limited Dissolve (Max Angle 5°). Un cube propre à 6 faces.
3. GEO_Profile : curseur 3D au centre du monde (Shift+C), A, puis Alt+E > Spin :
   Steps 24, Angle 360°, Axis Z (0,0,1), Auto Merge coché. Puis A et M > By Distance : Auto Merge
   soude la couture mais laisse 24 sommets superposés sur l'axe (mesuré en 5.3.0).
   Un vase fermé au fond, ouvert en haut. Clic droit (Object Mode) > Shade Smooth.
4. GEO_Pyramid : sélectionnez les 4 sommets du HAUT, M > At Center. Une pyramide à 5 sommets.
5. GEO_Spring (Object Mode) : Add Modifier > Generate > Screw : Screw 0.08, Iterations 5.
6. GEO_Tile : K (Knife), cliquez un coin puis le coin opposé, Entrée. Une diagonale coupe le carreau.
Vérification : SCRIPTS/validate_ch02_03.py -- --exercise atelier
"""
PROFILE = [(0.0, 0.0), (0.09, 0.0), (0.11, 0.03), (0.13, 0.09), (0.14, 0.15), (0.12, 0.21),
           (0.08, 0.26), (0.075, 0.29), (0.09, 0.32)]


def mk(name, col, mat, bm, loc):
    me = bpy.data.meshes.new(name.replace("GEO_", "ME_"))
    bm.to_mesh(me)
    bm.free()
    ob = bpy.data.objects.new(name, me)
    ob.location = loc
    col.objects.link(ob)
    me.materials.append(mat)
    return ob


def box(sx, sy, sz, z0=0.0, cuts=0):
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    if cuts:
        bmesh.ops.subdivide_edges(bm, edges=bm.edges[:], cuts=cuts, use_grid_fill=True)
    for v in bm.verts:
        v.co = Vector((v.co.x * sx, v.co.y * sy, z0 + (v.co.z + 0.5) * sz))
    return bm


def build(sol):
    L.reset("SC_Cutting")
    L.studio(subject_height=0.8)
    col = L.collection("ATELIER")
    clay = L.material("MAT_Clay", (0.75, 0.72, 0.68), 0.6)
    glaze = L.material("MAT_Glaze", (0.25, 0.45, 0.65), 0.25)
    steel = L.material("MAT_Steel", (0.7, 0.7, 0.72), 0.3, metallic=1.0)
    bar = mk("GEO_Bar", col, clay, box(0.4, 0.4, 1.2), (-3.0, 0, 0))
    messy = mk("GEO_Messy", col, clay, box(0.7, 0.7, 0.7, cuts=4), (-1.6, 0, 0))
    bm = bmesh.new()
    vs = [bm.verts.new((x, 0, z)) for x, z in PROFILE]
    for a, b in zip(vs, vs[1:]):
        bm.edges.new((a, b))
    prof = mk("GEO_Profile", col, glaze, bm, (0, 0, 0))
    pyr = mk("GEO_Pyramid", col, clay, box(0.6, 0.6, 0.6), (1.4, 0, 0))
    bm = bmesh.new()
    bmesh.ops.create_circle(bm, cap_ends=False, segments=12, radius=0.035,
                            matrix=Matrix.Translation((0.18, 0, 0.04)) @ Matrix.Rotation(math.radians(90), 4, "X"))
    spring = mk("GEO_Spring", col, steel, bm, (2.8, 0, 0))
    bm = bmesh.new()
    bmesh.ops.create_grid(bm, x_segments=1, y_segments=1, size=0.4)
    for v in bm.verts:
        v.co.z = 0.005
    tile = mk("GEO_Tile", col, clay, bm, (4.2, 0, 0))
    if sol:
        solve(bar, messy, prof, pyr, spring, tile)
    cam = L.obj("CAM_Main")
    cam.location = (0.6, -8.5, 2.6)
    cam.data.lens = 32
    L.obj("EMP_Target").location = (0.6, 0, 0.35)
    L.render_defaults("BLENDER_EEVEE", 50)
    L.instructions(NOTE)


def edit(ob, fn):
    bm = bmesh.new()
    bm.from_mesh(ob.data)
    fn(bm)
    bm.normal_update()
    bm.to_mesh(ob.data)
    ob.data.update()
    bm.free()


def solve(bar, messy, prof, pyr, spring, tile):
    def bisect(bm):
        geom = bm.verts[:] + bm.edges[:] + bm.faces[:]
        bmesh.ops.bisect_plane(bm, geom=geom, plane_co=(0, 0, 0.8), plane_no=(0, 0, 1), clear_outer=True)
        bnd = [e for e in bm.edges if e.is_boundary]
        bmesh.ops.edgeloop_fill(bm, edges=bnd)
    edit(bar, bisect)
    edit(messy, lambda bm: bmesh.ops.dissolve_limit(bm, angle_limit=math.radians(5), verts=bm.verts[:], edges=bm.edges[:]))

    # Spin : mêmes opérateurs que la consigne (mesuré : Auto Merge ne fusionne pas les 24 points de l'axe)
    bpy.ops.object.select_all(action="DESELECT")
    bpy.context.view_layer.objects.active = prof
    prof.select_set(True)
    bpy.context.scene.cursor.location = (0, 0, 0)
    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.mesh.select_all(action="SELECT")
    bpy.ops.mesh.spin(steps=24, angle=math.radians(360), center=(0, 0, 0), axis=(0, 0, 1), use_auto_merge=True)
    bpy.ops.mesh.select_all(action="SELECT")
    bpy.ops.mesh.remove_doubles(threshold=0.0001)
    bpy.ops.object.mode_set(mode="OBJECT")
    bpy.ops.object.shade_smooth()

    def merge(bm):
        top = [v for v in bm.verts if v.co.z > 0.59]
        bmesh.ops.pointmerge(bm, verts=top, merge_co=sum((v.co for v in top), Vector()) / len(top))
    edit(pyr, merge)
    m = spring.modifiers.new("Screw", "SCREW")
    m.screw_offset = 0.08
    m.iterations = 5
    m.steps = 24
    m.render_steps = 24

    def knife(bm):
        a = min(bm.verts, key=lambda v: v.co.x + v.co.y)
        b = max(bm.verts, key=lambda v: v.co.x + v.co.y)
        bmesh.ops.connect_verts(bm, verts=[a, b])
    edit(tile, knife)


def main():
    build(False)
    L.save(os.path.join(CH, "STARTER_FILES", "ch02_03_cutting_starter.blend"))
    build(True)
    p = L.save(os.path.join(CH, "COMPLETED_EXAMPLES", "ch02_03_cutting_solution.blend"))
    bpy.context.scene.render.filepath = os.path.join(os.path.dirname(p), "ch02_03_cutting_reference.png")
    bpy.ops.render.render(write_still=True)


if __name__ == "__main__":
    L.run(main)
