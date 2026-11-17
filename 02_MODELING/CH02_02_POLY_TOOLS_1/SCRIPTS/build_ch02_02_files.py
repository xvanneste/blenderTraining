"""
build_ch02_02_files.py — « Le tabouret » (CH02.02, outils polygonaux I).

  STARTER_FILES/ch02_02_stool_starter.blend
      GEO_Stool : l'assise seule, pavé 40 × 40 × 6 cm posé à 42 cm du sol (z de 0,42 à 0,48).
  COMPLETED_EXAMPLES/ch02_02_stool_solution.blend (+ _reference.png)
      Assise découpée (Loop Cut ×2 dans chaque sens, écartées à ±15 cm), 4 pieds extrudés
      (en 3 tronçons), 4 traverses (Bridge Edge Loops entre faces en vis-à-vis), arête supérieure
      chanfreinée (Bevel 2 segments), dessus creusé (Inset + léger enfoncement).
Usage : blender -b --factory-startup --python-exit-code 1 --python build_ch02_02_files.py
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
NOTE = """CH02.02 — LE TABOURET (GEO_Stool, Edit Mode)
Dimensions : assise 40 × 40 cm, hauteur totale 48 cm, pieds au sol (z = 0).
1. Loop Cut (Ctrl+R) : 2 coupes dans un sens (molette = nombre de coupes), puis S X 2.25
   (ou S Y) pour écarter les deux boucles à ±15 cm. Idem dans l'autre sens.
   -> la face du dessous est découpée en 3 × 3 ; les 4 carrés d'angle font 5 × 5 cm.
2. Pieds : sélectionnez les 4 carrés d'angle du DESSOUS, E puis Z -0.2 ; E Z -0.05 ; E Z -0.17
   (3 tronçons : le tronçon du milieu servira aux traverses). Les pieds touchent z = 0.
3. Traverses : sur deux pieds voisins, sélectionnez les 2 faces du tronçon du milieu qui se font
   face, Edge > Bridge Edge Loops. Recommencez pour les 4 côtés (au moins 2).
4. Bevel : sélectionnez la boucle d'arêtes du pourtour supérieur de l'assise (Alt+clic),
   Ctrl+B, molette pour 2 segments, largeur ≈ 1 cm.
5. Inset : sélectionnez les faces du dessus de l'assise, I (≈ 2 cm), puis E -0.005 pour creuser.
Vérification : SCRIPTS/validate_ch02_02.py -- --exercise stool
"""


def seat(bm):
    """Pavé 0,4 × 0,4 × 0,06 (z 0,42 → 0,48), découpé 3 × 3 sur les côtés, lignes à ±0,15."""
    bmesh.ops.create_cube(bm, size=1.0)
    for v in bm.verts:
        v.co = Vector((v.co.x * 0.4, v.co.y * 0.4, 0.45 + v.co.z * 0.06))


def solve(bm):
    # 1. Loop Cuts : on subdivise les arêtes horizontales en 3 puis on écarte les lignes à ±0,15
    horiz = [e for e in bm.edges if abs(e.verts[0].co.z - e.verts[1].co.z) < 1e-6]
    bmesh.ops.subdivide_edges(bm, edges=horiz, cuts=2, use_grid_fill=True)
    for v in bm.verts:
        for ax in (0, 1):
            if 0.01 < abs(v.co[ax]) < 0.19:
                v.co[ax] = 0.15 if v.co[ax] > 0 else -0.15
    bm.normal_update()
    # 2. Pieds : 4 faces d'angle du dessous, extrudées en 3 tronçons
    corners = [f for f in bm.faces if f.normal.z < -0.99 and all(abs(c) > 0.16 for c in f.calc_center_median()[:2])]
    for depth in (0.20, 0.05, 0.17):
        res = bmesh.ops.extrude_face_region(bm, geom=corners)
        new_faces = [g for g in res["geom"] if isinstance(g, bmesh.types.BMFace)]
        new_verts = [g for g in res["geom"] if isinstance(g, bmesh.types.BMVert)]
        bmesh.ops.translate(bm, verts=new_verts, vec=(0, 0, -depth))
        bmesh.ops.delete(bm, geom=corners, context="FACES_ONLY")
        corners = new_faces
    bm.normal_update()
    # 3. Traverses : faces du tronçon du milieu (z 0,17–0,22) qui se font face
    def mid_face(sx, sy, axis):
        best = None
        for f in bm.faces:
            c = f.calc_center_median()
            if 0.17 < c.z < 0.22 and abs(f.normal.z) < 0.1 and c.x * sx > 0.15 and c.y * sy > 0.15:
                n = f.normal
                if axis == 0 and n.x * sx < -0.9:
                    best = f
                if axis == 1 and n.y * sy < -0.9:
                    best = f
        return best
    pairs = [((1, 1), (-1, 1), 0), ((1, -1), (-1, -1), 0), ((1, 1), (1, -1), 1), ((-1, 1), (-1, -1), 1)]
    for a, b, axis in pairs:
        fa, fb = mid_face(*a, axis), mid_face(*b, axis)
        # pont sans vrille : chaque sommet de A est relié au sommet de B en vis-à-vis
        # (mêmes coordonnées hors axe) — c'est ce que règle l'option Twist de Bridge Edge Loops
        va = [l.vert for l in fa.loops]
        other = 1 - axis
        def key(v):
            return (round(v.co[other], 4), round(v.co.z, 4))
        vb_by = {key(v): v for v in fb.verts}
        vb = [vb_by[key(v)] for v in va]
        bmesh.ops.delete(bm, geom=[fa, fb], context="FACES_ONLY")
        for i in range(4):
            j = (i + 1) % 4
            bm.faces.new((va[i], va[j], vb[j], vb[i]))
    bm.normal_update()
    # 4. Bevel du pourtour supérieur (arêtes entre dessus et côtés)
    top_edges = [e for e in bm.edges if all(v.co.z > 0.479 for v in e.verts)
                 and any(abs(f.normal.z) < 0.1 for f in e.link_faces)]
    bmesh.ops.bevel(bm, geom=top_edges, offset=0.01, segments=2, affect="EDGES", profile=0.5)
    bm.normal_update()
    # 5. Inset du dessus puis léger creux
    top = [f for f in bm.faces if f.normal.z > 0.99 and f.calc_center_median().z > 0.465]
    bmesh.ops.inset_region(bm, faces=top, thickness=0.02, depth=0.0)       # I : rebord plat
    res = bmesh.ops.extrude_face_region(bm, geom=top)                      # E -0.005 : creux
    inner = [g for g in res["geom"] if isinstance(g, bmesh.types.BMFace)]
    bmesh.ops.translate(bm, verts=list({v for f in inner for v in f.verts}), vec=(0, 0, -0.005))
    bmesh.ops.delete(bm, geom=top, context="FACES")   # supprime aussi les arêtes internes orphelines
    bm.normal_update()


def build(sol):
    L.reset("SC_Stool")
    L.studio(subject_height=0.5)
    col = L.collection("PROPS")
    wood = L.material("MAT_Wood", (0.45, 0.28, 0.14), 0.55)
    me = bpy.data.meshes.new("ME_Stool")
    ob = bpy.data.objects.new("GEO_Stool", me)
    col.objects.link(ob)
    ob.data.materials.append(wood)
    bm = bmesh.new()
    seat(bm)
    if sol:
        solve(bm)
    bm.normal_update()
    bm.to_mesh(me)
    bm.free()
    cam = L.obj("CAM_Main")
    cam.location = (1.1, -1.5, 0.95)
    cam.data.lens = 50
    tgt = L.obj("EMP_Target")
    tgt.location = (0, 0, 0.25)
    L.render_defaults("BLENDER_EEVEE", 50)
    L.instructions(NOTE)


def main():
    build(False)
    L.save(os.path.join(CH, "STARTER_FILES", "ch02_02_stool_starter.blend"))
    build(True)
    p = L.save(os.path.join(CH, "COMPLETED_EXAMPLES", "ch02_02_stool_solution.blend"))
    bpy.context.scene.render.filepath = os.path.join(os.path.dirname(p), "ch02_02_stool_reference.png")
    bpy.ops.render.render(write_still=True)


if __name__ == "__main__":
    L.run(main)
