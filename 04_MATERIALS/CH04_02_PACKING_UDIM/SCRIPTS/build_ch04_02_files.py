"""
build_ch04_02_files.py — « Packing et UDIM » (CH04.02).

Le coffre de CH04.01 est réparti sur DEUX tuiles UDIM : corps + sangles sur 1001, couvercle sur 1002 (plus de résolution pour le couvercle).
Tuile = (u, v) entier : numéro = 1001 + u + 10 × v.
  STARTER_FILES/ch04_02_udim_starter.blend : UV propres mais TOUT dans la tuile 1001 (matériau à image UDIM 1001–1002 déjà prêt).
  COMPLETED_EXAMPLES/ch04_02_udim_solution.blend (+ _reference.png : deux vues ; _uv_layout.png : deux tuiles côte à côte)
  COMPLETED_EXAMPLES/COUNTER_EXAMPLES/ : straddle (un îlot à cheval sur deux tuiles), single_tile, missing_tile (image sans tuile 1002),
                                         overlap_tile (deux îlots superposés dans une tuile)
Usage : blender -b --factory-startup --python-exit-code 1 --python build_ch04_02_files.py
Testé avec : Blender 5.3.0.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "SCRIPTS"))
sys.path.insert(0, os.path.join(HERE, "..", "..", "CH04_01_UV_UNWRAP", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bcma_shots as S  # noqa: E402
import bmesh  # noqa: E402
import bpy  # noqa: E402
import build_ch04_01_files as B1  # noqa: E402
import numpy as np  # noqa: E402

CH = L.chapter_dir(__file__)
NOTE = """CH04.02 — PACKING ET UDIM (PROP_Chest ; matériau MAT_UDIM : image UDIM_Grid, tuiles 1001 et 1002)
Une tuile UDIM = un carré UV [0,1]². Tuile 1001 : u ∈ [0,1], v ∈ [0,1] ; tuile 1002 : u ∈ [1,2] ; 1011 : v ∈ [1,2]. Numéro = 1001 + u + 10·v.
1. Les faces du couvercle ont l'index de matériau 1 (Edit Mode : Material > Select).
2. Déplier chaque groupe SÉPARÉMENT : sélectionner le groupe, UV > Pack Islands (il remplit le carré [0,1]²).
3. Déplacer les îlots du couvercle dans la tuile 1002 : G, X, 1 (une unité en U).
4. Aucun îlot à cheval sur deux tuiles ; pas de chevauchement dans une tuile ; densité uniforme DANS chaque tuile.
Vérification : SCRIPTS/validate_ch04_02.py -- --exercise udim
"""


def make_chest_groups():
    """Coffre de CH04.01 avec index de matériau : couvercle = 1, le reste = 0."""
    bm = bmesh.new()
    B1.box(bm, (1.0, 0.6, 0.45), (0, 0, 0.225), cuts=2)
    B1.lid(bm, 1.0, 0.30, (0, 0, 0.45))
    for x in (-0.3, 0.3):
        B1.box(bm, (0.08, 0.64, 0.50), (x, 0, 0.25), cuts=1)
    bm.faces.ensure_lookup_table()
    import math
    for f in bm.faces:       # couvercle = faces dont TOUS les sommets sont sur le cylindre de rayon 0,30 (axe y = 0, z = 0,45), au-dessus du corps
        on_cyl = all(abs(math.hypot(v.co.y, v.co.z - 0.45) - 0.30) < 1e-3 and v.co.z >= 0.45 - 1e-6 for v in f.verts)
        f.material_index = 1 if on_cyl else 0
    me = bpy.data.meshes.new("ME_PROP_Chest")
    bm.to_mesh(me)
    bm.free()
    ob = bpy.data.objects.new("PROP_Chest", me)
    bpy.context.scene.collection.objects.link(ob)
    for p in me.polygons:
        p.use_smooth = False
    return ob


def udim_material(tiles=(1001, 1002)):
    mat = bpy.data.materials.new("MAT_UDIM")
    nt = mat.node_tree
    img = bpy.data.images.new("UDIM_Grid", 1024, 1024, tiled=True)
    img.generated_type = "UV_GRID"
    for t in tiles:
        if t != 1001:
            img.tiles.new(t, label="Lid" if t == 1002 else str(t))
    tex = nt.nodes.new("ShaderNodeTexImage")
    tex.image = img
    nt.links.new(tex.outputs["Color"], nt.nodes["Principled BSDF"].inputs["Base Color"])
    return mat


def select_group(ob, index):
    me = ob.data
    bpy.context.view_layer.objects.active = ob
    bpy.ops.object.select_all(action="DESELECT")
    ob.select_set(True)
    bpy.ops.object.mode_set(mode="EDIT")
    bm = bmesh.from_edit_mesh(me)
    for f in bm.faces:
        f.select_set(f.material_index == index)
    bm.select_flush(False)
    bmesh.update_edit_mesh(me)


def uv_single_tile(ob):
    B1.unwrap_good(ob)                      # tout dans la tuile 1001, déjà propre


def uv_two_tiles(ob):
    """Dépliage global puis packing séparé de chaque groupe dans son propre carré ; le couvercle passe en tuile 1002."""
    B1.unwrap_good(ob)
    for idx in (0, 1):
        select_group(ob, idx)
        bpy.ops.uv.pack_islands(margin=0.02, rotate=True)
        bpy.ops.object.mode_set(mode="OBJECT")
    me = ob.data
    uv = me.uv_layers.active.data
    for p in me.polygons:
        if p.material_index == 1:
            for li in p.loop_indices:
                u = uv[li].uv
                uv[li].uv = (u[0] + 1.0, u[1])
    me.update()


def mod_uv(ob, fn):
    me = ob.data
    uv = me.uv_layers.active.data
    isl = B1.islands(ob)
    for p in me.polygons:
        for li in p.loop_indices:
            uv[li].uv = fn(isl[p.index], p, uv[li].uv)
    me.update()


def build(kind):
    L.reset("SC_UDIM")
    L.studio(subject_height=1.0)
    c = L.collection("CAMERAS")
    cam = L.camera("CAM_Front", c, (1.9, -2.4, 1.4), 50, make_active=True)
    S.look_at(cam, (0, 0, 0.35))
    cam2 = L.camera("CAM_Back", c, (-1.7, 2.3, 1.2), 50, make_active=False)
    S.look_at(cam2, (0, 0, 0.35))
    sc = L.render_defaults("BLENDER_EEVEE", 50)
    sc.camera = cam
    ob = make_chest_groups()
    ob.data.materials.append(udim_material((1001,) if kind == "missing_tile" else (1001, 1002)))
    ob.data.materials.append(ob.data.materials[0])          # index 1 : même matériau UDIM
    if kind in ("starter", "single_tile"):
        uv_single_tile(ob)
    else:
        uv_two_tiles(ob)
    isl = B1.islands(ob)
    me = ob.data
    uvd = me.uv_layers.active.data

    def pts_of(k):
        return np.array([uvd[li].uv[:] for p in me.polygons if isl[p.index] == k for li in p.loop_indices])
    body_isl = sorted({int(isl[p.index]) for p in me.polygons if p.material_index == 0})
    if kind == "straddle":                                   # un îlot du corps centré sur la frontière u = 1 : à cheval sur 1001 et 1002
        k = max(body_isl, key=lambda q: pts_of(q)[:, 0].max())
        du = 1.0 - pts_of(k)[:, 0].mean()
        mod_uv(ob, lambda i, p, uv: (uv[0] + du, uv[1]) if i == k else tuple(uv))
    if kind == "overlap_tile":                               # deux îlots du corps superposés dans la tuile 1001
        ka, kb = body_isl[0], body_isl[1]
        d = pts_of(ka).min(0) - pts_of(kb).min(0)
        mod_uv(ob, lambda i, p, uv: (uv[0] + d[0], uv[1] + d[1]) if i == kb else tuple(uv))
    ob["rest_scale"] = 1.0
    L.instructions(NOTE)
    return sc, ob


def uv_layout_png(ob, path, size=512):
    me = ob.data
    uv = me.uv_layers.active.data
    W = size * 2
    img = np.zeros((size, W, 4), np.float32)
    img[..., 3] = 1.0
    img[..., :3] = 0.08
    img[:, size - 1:size + 1, :3] = 0.5                      # frontière de tuile
    for p in me.polygons:
        col = (0.95, 0.85, 0.3) if p.material_index == 0 else (0.4, 0.8, 0.95)
        pts = [Vector_(uv[li].uv) for li in p.loop_indices]
        pts = [(q[0] * (size - 1), q[1] * (size - 1)) for q in pts]
        for a, b in zip(pts, pts[1:] + pts[:1]):
            n = int(max(abs(b[0] - a[0]), abs(b[1] - a[1]))) + 1
            for t in np.linspace(0, 1, n):
                x = int(np.clip(a[0] + (b[0] - a[0]) * t, 0, W - 1))
                y = int(np.clip(a[1] + (b[1] - a[1]) * t, 0, size - 1))
                img[y, x, :3] = col
    im = bpy.data.images.new("uvl", W, size)
    im.pixels = img.ravel()
    im.filepath_raw = path
    im.file_format = "PNG"
    im.save()


def Vector_(v):
    return (v[0], v[1])


def main():
    out = os.path.join(CH, "COMPLETED_EXAMPLES")
    build("starter")
    L.save(os.path.join(CH, "STARTER_FILES", "ch04_02_udim_starter.blend"))
    for k in ("straddle", "single_tile", "missing_tile", "overlap_tile"):
        build(k)
        L.save(os.path.join(out, "COUNTER_EXAMPLES", f"ch04_02_udim_{k}.blend"))
    sc, ob = build("solution")
    L.save(os.path.join(out, "ch04_02_udim_solution.blend"))
    uv_layout_png(ob, os.path.join(out, "ch04_02_udim_uv_layout.png"))
    B1.views(sc, os.path.join(out, "ch04_02_udim_reference.png"))


if __name__ == "__main__":
    L.run(main)
