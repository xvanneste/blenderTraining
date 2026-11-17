"""
build_ch04_01_files.py — « UV Unwrapping avancé » (CH04.01 : seams, îlots, distorsion, densité de texels).

  STARTER_FILES/ch04_01_chest_starter.blend
      PROP_Chest (coffre : corps, couvercle arrondi, deux sangles) avec des UV VOLONTAIREMENT mauvaises (projection plane :
      étirement fort, îlots qui se chevauchent) ; matériau damier (UV Grid) pour VOIR la distorsion.
  COMPLETED_EXAMPLES/ch04_01_chest_solution.blend (+ _reference.png : 3 vues avec damier, + _uv_layout.png)
      Seams sur les arêtes vives (> 50°), unwrap (Angle Based), densité de texels égalisée (Average Islands Scale), packing.
  COMPLETED_EXAMPLES/COUNTER_EXAMPLES/ : overlapping, unequal_density, out_of_bounds, tiny_pack, stretched
Usage : blender -b --factory-startup --python-exit-code 1 --python build_ch04_01_files.py
Testé avec : Blender 5.3.0.
"""
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bcma_shots as S  # noqa: E402
import bmesh  # noqa: E402
import bpy  # noqa: E402
import numpy as np  # noqa: E402
from mathutils import Matrix, Vector  # noqa: E402

CH = L.chapter_dir(__file__)
NOTE = """CH04.01 — UV PROPRES (PROP_Chest, Edit Mode, éditeur UV : espace de travail UV Editing)
Le damier (UV Grid) montre la distorsion : des carrés réguliers = de bonnes UV.
1. Seams : sélectionnez les arêtes vives (angle > 50°) et Edge > Mark Seam (Ctrl+E). Les arêtes d'une même surface courbe ne se coupent pas.
2. Tout sélectionner (A) puis UV > Unwrap (U) : Angle Based (ou Conformal).
3. Densité de texels égale : UV > Average Islands Scale (éditeur UV). Un damier de carrés de MÊME taille partout.
4. Packing : UV > Pack Islands (marge ≈ 2 %) : tout dans [0, 1], sans chevauchement, ≥ 50 % de l'espace utilisé.
Vérification : SCRIPTS/validate_ch04_01.py -- --exercise uv
"""


def box(bm, size, loc, cuts=2):
    r = bmesh.ops.create_cube(bm, size=1.0)
    verts = r["verts"]
    bmesh.ops.scale(bm, vec=Vector(size), verts=verts)
    bmesh.ops.translate(bm, vec=Vector(loc), verts=verts)
    edges = list({e for v in verts for e in v.link_edges})
    if cuts:
        bmesh.ops.subdivide_edges(bm, edges=edges, cuts=cuts, use_grid_fill=True)


def lid(bm, length, radius, loc, seg=16):
    r = bmesh.ops.create_cone(bm, cap_ends=True, segments=seg * 2, radius1=radius, radius2=radius, depth=length)
    verts = r["verts"]
    bmesh.ops.rotate(bm, verts=verts, cent=(0, 0, 0), matrix=Matrix.Rotation(math.radians(90), 3, "Y"))
    bmesh.ops.translate(bm, vec=Vector(loc), verts=verts)
    geom = [g for g in bm.verts[:] + bm.edges[:] + bm.faces[:] if g in verts or (hasattr(g, "verts") and all(v in verts for v in g.verts))]
    res = bmesh.ops.bisect_plane(bm, geom=geom, plane_co=loc, plane_no=(0, 0, 1), clear_inner=True)
    edges = [e for e in res["geom_cut"] if isinstance(e, bmesh.types.BMEdge)]
    bmesh.ops.holes_fill(bm, edges=edges, sides=0)


def make_chest():
    bm = bmesh.new()
    box(bm, (1.0, 0.6, 0.45), (0, 0, 0.225), cuts=2)
    lid(bm, 1.0, 0.30, (0, 0, 0.45))
    for x in (-0.3, 0.3):                                     # sangles
        box(bm, (0.08, 0.64, 0.50), (x, 0, 0.25), cuts=1)
    me = bpy.data.meshes.new("ME_PROP_Chest")
    bm.to_mesh(me)
    bm.free()
    ob = bpy.data.objects.new("PROP_Chest", me)
    bpy.context.scene.collection.objects.link(ob)
    for p in me.polygons:
        p.use_smooth = False
    return ob


def checker_material():
    mat = bpy.data.materials.new("MAT_Checker")
    nt = mat.node_tree
    img = bpy.data.images.new("UV_Grid", 1024, 1024)
    img.generated_type = "UV_GRID"
    tex = nt.nodes.new("ShaderNodeTexImage")
    tex.image = img
    bsdf = nt.nodes["Principled BSDF"]
    nt.links.new(tex.outputs["Color"], bsdf.inputs["Base Color"])
    bsdf.inputs["Roughness"].default_value = 0.6
    return mat


def planar_uv(ob):
    """UV de départ MAUVAISES : projection plane sur XY (étirement des flancs, dessus/dessous superposés)."""
    uv = ob.data.uv_layers.new(name="UVMap")
    me = ob.data
    for p in me.polygons:
        for li in p.loop_indices:
            co = me.vertices[me.loops[li].vertex_index].co
            uv.data[li].uv = (co.x * 0.4 + 0.5, co.y * 0.5 + 0.5)


def unwrap_good(ob, margin=0.02):
    me = ob.data
    if not me.uv_layers:
        me.uv_layers.new(name="UVMap")
    bpy.context.view_layer.objects.active = ob
    bpy.ops.object.select_all(action="DESELECT")
    ob.select_set(True)
    bpy.ops.object.mode_set(mode="EDIT")
    bm = bmesh.from_edit_mesh(me)
    for e in bm.edges:
        e.seam = len(e.link_faces) == 2 and e.calc_face_angle(0) > math.radians(50)
    bmesh.update_edit_mesh(me)
    bpy.ops.mesh.select_all(action="SELECT")
    bpy.ops.uv.unwrap(method="ANGLE_BASED", margin=0.003)
    bpy.ops.uv.average_islands_scale()
    bpy.ops.uv.pack_islands(margin=margin, rotate=True)
    bpy.ops.object.mode_set(mode="OBJECT")


def islands(ob):
    """Étiquette d'îlot par face (faces reliées par un sommet 3D ET une UV communs)."""
    me = ob.data
    uv = me.uv_layers.active.data
    parent = list(range(len(me.polygons)))

    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a
    corner = {}
    for p in me.polygons:
        for li in p.loop_indices:
            key = (me.loops[li].vertex_index, round(uv[li].uv[0], 5), round(uv[li].uv[1], 5))
            if key in corner:
                ra, rb = find(corner[key]), find(p.index)
                parent[ra] = rb
            else:
                corner[key] = p.index
    return np.array([find(i) for i in range(len(me.polygons))])


def transform_uv(ob, fn):
    """fn(uv_array (N,2), face_island (per loop)) -> new uv."""
    me = ob.data
    uv = me.uv_layers.active.data
    isl = islands(ob)
    n = len(uv)
    a = np.empty(n * 2, np.float32)
    uv.foreach_get("uv", a)
    a = a.reshape(-1, 2)
    li_isl = np.empty(n, int)
    for p in me.polygons:
        for li in p.loop_indices:
            li_isl[li] = isl[p.index]
    a = fn(a, li_isl)
    uv.foreach_set("uv", a.ravel())
    me.update()


def bbox_translate_to_origin(a, isl):
    out = a.copy()
    for k in np.unique(isl):
        m = isl == k
        out[m] -= a[m].min(0)
    return out


def variants(kind, ob):
    if kind == "overlapping":
        transform_uv(ob, bbox_translate_to_origin)
    elif kind == "unequal_density":
        def f(a, isl):                                   # un îlot sur deux agrandi ×2,6 ; puis Pack Islands (sans changer les échelles relatives)
            out = a.copy()
            for i, k in enumerate(np.unique(isl)):
                m = isl == k
                c = a[m].mean(0)
                out[m] = c + (a[m] - c) * (2.6 if i % 2 else 1.0)
            return out
        transform_uv(ob, f)
        bpy.context.view_layer.objects.active = ob
        bpy.ops.object.select_all(action="DESELECT")
        ob.select_set(True)
        bpy.ops.object.mode_set(mode="EDIT")
        bpy.ops.mesh.select_all(action="SELECT")
        bpy.ops.uv.pack_islands(margin=0.02, rotate=True)
        bpy.ops.object.mode_set(mode="OBJECT")
    elif kind == "out_of_bounds":
        transform_uv(ob, lambda a, isl: a * 1.7 - 0.3)
    elif kind == "tiny_pack":
        transform_uv(ob, lambda a, isl: a * 0.3 + 0.02)


def build(kind):
    L.reset("SC_UV")
    L.studio(subject_height=1.0)
    c = L.collection("CAMERAS")
    cam = L.camera("CAM_Front", c, (1.9, -2.4, 1.4), 50, make_active=True)
    S.look_at(cam, (0, 0, 0.35))
    cam2 = L.camera("CAM_Back", c, (-1.7, 2.3, 1.2), 50, make_active=False)
    S.look_at(cam2, (0, 0, 0.35))
    sc = L.render_defaults("BLENDER_EEVEE", 50)
    sc.camera = cam
    ob = make_chest()
    ob.data.materials.append(checker_material())
    if kind == "starter":
        planar_uv(ob)
    else:
        unwrap_good(ob)
        variants(kind, ob)
    ob["rest_scale"] = 1.0
    L.instructions(NOTE)
    return sc, ob


def uv_layout_png(ob, path, size=768):
    me = ob.data
    uv = me.uv_layers.active.data
    img = np.zeros((size, size, 4), np.float32)
    img[..., 3] = 1.0
    img[..., :3] = 0.08
    sq = size // 8
    img[::sq, :, :3] = 0.2
    img[:, ::sq, :3] = 0.2
    for p in me.polygons:
        pts = [Vector(uv[li].uv) * (size - 1) for li in p.loop_indices]
        for a, b in zip(pts, pts[1:] + pts[:1]):
            n = int(max(abs(b.x - a.x), abs(b.y - a.y))) + 1
            for t in np.linspace(0, 1, n):
                x = int(np.clip(a.x + (b.x - a.x) * t, 0, size - 1))
                y = int(np.clip(a.y + (b.y - a.y) * t, 0, size - 1))
                img[y, x, :3] = (0.95, 0.85, 0.3)
    im = bpy.data.images.new("uvl", size, size)
    im.pixels = img.ravel()
    im.filepath_raw = path
    im.file_format = "PNG"
    im.save()


def views(sc, out):
    sc.render.resolution_x, sc.render.resolution_y = 640, 640
    tiles = []
    for cam in ("CAM_Front", "CAM_Back"):
        sc.camera = bpy.data.objects[cam]
        p = os.path.join(bpy.app.tempdir, cam + ".png")
        sc.render.filepath = p
        bpy.ops.render.render(write_still=True)
        im = bpy.data.images.load(p)
        W, H = im.size
        tiles.append(np.array(im.pixels[:], dtype=np.float32).reshape(H, W, 4))
        bpy.data.images.remove(im)
    sheet = np.concatenate(tiles, axis=1)
    img = bpy.data.images.new("v", sheet.shape[1], sheet.shape[0])
    img.pixels = sheet.ravel()
    img.filepath_raw = out
    img.file_format = "PNG"
    img.save()
    sc.camera = bpy.data.objects["CAM_Front"]


def main():
    out = os.path.join(CH, "COMPLETED_EXAMPLES")
    build("starter")
    L.save(os.path.join(CH, "STARTER_FILES", "ch04_01_chest_starter.blend"))
    for k in ("overlapping", "unequal_density", "out_of_bounds", "tiny_pack"):
        build(k)
        L.save(os.path.join(out, "COUNTER_EXAMPLES", f"ch04_01_chest_{k}.blend"))
    sc, ob = build("solution")
    L.save(os.path.join(out, "ch04_01_chest_solution.blend"))
    uv_layout_png(ob, os.path.join(out, "ch04_01_chest_uv_layout.png"))
    views(sc, os.path.join(out, "ch04_01_chest_reference.png"))


if __name__ == "__main__":
    L.run(main)
