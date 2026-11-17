"""
build_ch02_01_files.py — « La clinique de la topologie » (CH02.01).

  STARTER_FILES/ch02_01_topology_starter.blend — 5 patients, chacun avec un défaut :
      GEO_Ngon    : panneau octogonal fait d'UNE face à 8 côtés (n-gon) ;
      GEO_Tris    : sphère entièrement triangulée ;
      GEO_Doubles : cube subdivisé dont toutes les faces sont détachées (sommets en double) ;
      GEO_Hole    : cylindre sans couvercle (trou, arêtes non-manifold) ;
      GEO_Poles   : cube subdivisé à diagnostiquer (compter les pôles) ;
      Texte DIAGNOSTIC (Text Editor) à compléter : « POLES = ? ».
  COMPLETED_EXAMPLES/ch02_01_topology_solution.blend (+ _reference.png avec fil de fer)
Usage : blender -b --factory-startup --python-exit-code 1 --python build_ch02_01_files.py
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
NOTE = """CH02.01 — LA CLINIQUE DE LA TOPOLOGIE
Affichez les statistiques : Viewport Overlays > Statistics. Travaillez en Edit Mode (Tab).
1. GEO_Ngon : la face unique a 8 côtés. Remplacez-la par des quads SANS changer le contour :
   sélectionnez la face, X > Only Faces (le contour reste), sélectionnez le contour (Alt+clic),
   Face > Grid Fill. Plus aucune face de plus de 4 côtés.
2. GEO_Tris : tout est triangulé. Sélectionnez tout (A), Face > Triangles to Quads (Alt+J).
   Au moins 80 % de quads (les 48 triangles des deux pôles restent : maximum 83 %).
3. GEO_Doubles : faces détachées, sommets en double. A, puis M > By Distance.
   Il ne doit plus rester aucun sommet superposé.
4. GEO_Hole : le cylindre n'a pas de couvercle. Select > Select All by Trait > Non Manifold,
   puis Alt+F (Fill) ou F. Plus aucune arête non-manifold.
5. GEO_Poles : comptez les pôles (sommets reliés à 3 arêtes ou à 5 et plus).
   Astuce : Select > Select All by Trait > ... n'existe pas pour les pôles : observez le
   maillage (Statistics, vue fil de fer Z). Écrivez le nombre dans le texte DIAGNOSTIC :
   POLES = 8   (par exemple) — Text Editor > DIAGNOSTIC.
Vérification : SCRIPTS/validate_ch02_01.py -- --exercise clinic
"""
DIAG = "DIAGNOSTIC — complétez la ligne suivante (nombre entier) :\nPOLES = ?\n"


def bm_to(ob, bm):
    bm.normal_update()
    bm.to_mesh(ob.data)
    ob.data.update()
    bm.free()


def build(sol):
    L.reset("SC_Topology")
    L.studio(subject_height=1.5)
    col = L.collection("PATIENTS")
    mat = L.material("MAT_Clay", (0.75, 0.72, 0.68), 0.6)
    # 1. n-gon octogonal
    ng = L.mesh(bpy.ops.mesh.primitive_circle_add, "GEO_Ngon", col, mat, vertices=8, radius=0.8,
                fill_type="NGON", location=(-4.2, 0, 1.0), rotation=(math.radians(90), 0, 0))
    # 2. sphère triangulée
    tr = L.mesh(bpy.ops.mesh.primitive_uv_sphere_add, "GEO_Tris", col, mat, segments=24, ring_count=12,
                radius=0.75, location=(-2.1, 0, 0.75))
    bm = bmesh.new(); bm.from_mesh(tr.data)
    bmesh.ops.triangulate(bm, faces=bm.faces[:])
    bm_to(tr, bm)
    # 3. sommets en double : cube subdivisé, faces détachées
    db = L.mesh(bpy.ops.mesh.primitive_cube_add, "GEO_Doubles", col, mat, size=1.3, location=(0, 0, 0.65))
    bm = bmesh.new(); bm.from_mesh(db.data)
    bmesh.ops.subdivide_edges(bm, edges=bm.edges[:], cuts=1, use_grid_fill=True)
    bmesh.ops.split_edges(bm, edges=bm.edges[:])
    bm_to(db, bm)
    # 4. trou : cylindre sans couvercle supérieur
    ho = L.mesh(bpy.ops.mesh.primitive_cylinder_add, "GEO_Hole", col, mat, vertices=16, radius=0.6, depth=1.4,
                location=(2.1, 0, 0.7))
    bm = bmesh.new(); bm.from_mesh(ho.data)
    top = max(bm.faces, key=lambda f: f.calc_center_median().z)
    bmesh.ops.delete(bm, geom=[top], context="FACES_ONLY")
    bm_to(ho, bm)
    # 5. pôles : cube subdivisé (2 niveaux, appliqués)
    po = L.mesh(bpy.ops.mesh.primitive_cube_add, "GEO_Poles", col, mat, size=1.2, location=(4.2, 0, 0.75))
    bm = bmesh.new(); bm.from_mesh(po.data)
    bmesh.ops.subdivide_edges(bm, edges=bm.edges[:], cuts=2, use_grid_fill=True)
    bm_to(po, bm)
    txt = bpy.data.texts.get("DIAGNOSTIC") or bpy.data.texts.new("DIAGNOSTIC")
    txt.clear()
    txt.write(DIAG)
    txt.use_fake_user = True
    if sol:
        solve(ng, tr, db, ho, po, txt)
    cam = L.obj("CAM_Main")
    cam.location = (0, -11.5, 3.2)
    cam.data.lens = 40
    L.render_defaults("BLENDER_EEVEE", 50)
    L.instructions(NOTE)


def solve(ng, tr, db, ho, po, txt):
    # 1. n-gon -> quads (on garde le contour, on le remplit en grille)
    # mêmes opérations que la consigne (opérateurs de l'interface) : X > Only Faces, puis Grid Fill
    bpy.ops.object.select_all(action="DESELECT")
    bpy.context.view_layer.objects.active = ng
    ng.select_set(True)
    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.mesh.select_mode(type="FACE")
    bpy.ops.mesh.select_all(action="SELECT")
    bpy.ops.mesh.delete(type="ONLY_FACE")
    bpy.ops.mesh.select_mode(type="EDGE")
    bpy.ops.mesh.select_all(action="SELECT")
    bpy.ops.mesh.fill_grid()
    bpy.ops.object.mode_set(mode="OBJECT")
    # 2. triangles -> quads
    bm = bmesh.new(); bm.from_mesh(tr.data)
    bmesh.ops.join_triangles(bm, faces=bm.faces[:], angle_face_threshold=math.radians(40),
                             angle_shape_threshold=math.radians(40))
    bm_to(tr, bm)
    # 3. fusion des doublons
    bm = bmesh.new(); bm.from_mesh(db.data)
    bmesh.ops.remove_doubles(bm, verts=bm.verts[:], dist=0.0001)
    bm_to(db, bm)
    # 4. boucher le trou
    bm = bmesh.new(); bm.from_mesh(ho.data)
    bnd = [e for e in bm.edges if e.is_boundary]
    bmesh.ops.edgeloop_fill(bm, edges=bnd)
    bm_to(ho, bm)
    # 5. diagnostic
    txt.clear()
    txt.write(DIAG.replace("POLES = ?", f"POLES = {count_poles(po)}"))


def count_poles(ob):
    bm = bmesh.new(); bm.from_mesh(ob.data)
    n = sum(1 for v in bm.verts if not any(e.is_boundary for e in v.link_edges) and len(v.link_edges) != 4)
    bm.free()
    return n


def wire_overlay():
    """Pour l'image de référence uniquement : copie fil de fer sombre de chaque patient."""
    dark = L.material("MAT_Wire", (0.02, 0.02, 0.03), 0.9)
    for name in ("GEO_Ngon", "GEO_Tris", "GEO_Doubles", "GEO_Hole", "GEO_Poles"):
        src = L.obj(name)
        w = src.copy()
        w.data = src.data.copy()
        w.name = "WIRE_" + name
        src.users_collection[0].objects.link(w)
        m = w.modifiers.new("Wire", "WIREFRAME")
        m.thickness = 0.012
        m.use_replace = True
        w.data.materials.clear()
        w.data.materials.append(dark)


def main():
    build(False)
    L.save(os.path.join(CH, "STARTER_FILES", "ch02_01_topology_starter.blend"))
    build(True)
    p = L.save(os.path.join(CH, "COMPLETED_EXAMPLES", "ch02_01_topology_solution.blend"))
    wire_overlay()                     # ajouté APRÈS l'enregistrement : n'existe que dans l'image
    sc = bpy.context.scene
    sc.render.filepath = os.path.join(os.path.dirname(p), "ch02_01_topology_reference.png")
    bpy.ops.render.render(write_still=True)


if __name__ == "__main__":
    L.run(main)
