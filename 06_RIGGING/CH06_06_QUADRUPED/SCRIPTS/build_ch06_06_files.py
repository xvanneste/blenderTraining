"""
build_ch06_06_files.py — « Rig quadrupède » (CH06.06 : méta-rig Rigify Basic Quadruped).

La créature CHR_Quad est un maillage de capsules construit AUTOUR des os du méta-rig quadrupède de base (34 bones : colonne et queue le long de Y, tête vers −Y, quatre pattes à
quatre segments + orteils). Solution : méta-rig à sa place (échelle 1, position 0), Generate Rig (283 bones), corps lié par Automatic Weights sur les DEF-*, poids normalisés, ≤ 4 influences.
  STARTER_FILES/ch06_06_quadruped_starter.blend : la créature et un méta-rig mal placé (échelle 1,4, décalé de 0,3 m en X et 0,2 m en Z) : à remettre sur la créature.
  COMPLETED_EXAMPLES/ch06_06_quadruped_solution.blend (+ _reference.png : vue de côté, patte avant gauche levée)
  COUNTER_EXAMPLES/ : not_generated, unskinned, wrong_scale, no_modifier, partial_weights, offset
Usage : blender -b --factory-startup --python-exit-code 1 --python build_ch06_06_files.py
Testé avec : Blender 5.3.0.
"""
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bmesh  # noqa: E402
import bpy  # noqa: E402
import numpy as np  # noqa: E402
from mathutils import Vector  # noqa: E402

CH = L.chapter_dir(__file__)
NOTE = """CH06.06 — RIG QUADRUPÈDE (CHR_Quad, méta-rig Rigify Basic Quadruped)
1. Add > Armature > Basic > Basic Quadruped. Placez-le SUR la créature : échelle 1, position (0, 0, 0) (dans le fichier de départ il est trop grand et décalé).
2. Generate Rig (Object Data > Rigify) : 283 bones ; renommez l'objet « rig » en RIG_Quad.
3. Corps : CHR_Quad puis RIG_Quad actif : Ctrl+P > With Automatic Weights ; Normalize All ; Limit Total 4.
Le correcteur vérifie rig généré, ajustement sur la créature (dimensions et centrage), peau, puis DÉPLACE le rig : racine +0,5 m en X ; patte avant gauche (front_foot_ik.L) levée de 0,15 m :
seule cette patte monte.
Vérification : SCRIPTS/validate_ch06_06.py -- --exercise quadruped
"""
RAD = {"spine.004": 0.12, "spine.003": 0.12, "spine.002": 0.07, "spine.001": 0.05, "spine": 0.035, "spine.005": 0.14, "spine.006": 0.15, "spine.007": 0.15, "spine.008": 0.14,
       "spine.009": 0.09, "spine.010": 0.08, "spine.011": 0.09, "thigh": 0.06, "shin": 0.045, "foot": 0.04, "toe": 0.03, "shoulder": 0.07, "front_thigh": 0.06, "front_shin": 0.045, "front_foot": 0.04, "front_toe": 0.03}


def capsule(bm, a, b, r):
    d = b - a
    ln = d.length
    if ln < 1e-6:
        return
    ret = bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=10, radius1=r, radius2=r * 0.85, depth=ln)
    rot = Vector((0, 0, 1)).rotation_difference(d.normalized()).to_matrix().to_4x4()
    for v in ret["verts"]:
        v.co = rot @ v.co + (a + b) / 2


def make_body(meta):
    bm = bmesh.new()
    for b in meta.data.bones:
        key = b.name.split(".")[0] if b.name.startswith(("shoulder", "thigh", "shin", "foot", "toe", "front_")) else b.name
        if b.name.startswith(("breast", "pelvis")):
            continue
        base = b.name[:-2] if b.name[-2:] in (".L", ".R") else b.name
        r = RAD.get(base)
        if r is None:
            continue
        capsule(bm, meta.matrix_world @ b.head_local, meta.matrix_world @ b.tail_local, r)
    me = bpy.data.meshes.new("ME_CHR_Quad")
    bm.to_mesh(me)
    bm.free()
    ob = bpy.data.objects.new("CHR_Quad", me)
    bpy.context.scene.collection.objects.link(ob)
    for p in me.polygons:
        p.use_smooth = True
    return ob


def build(kind):
    L.reset("SC_QUAD")
    L.studio(subject_height=1.0)
    bpy.ops.preferences.addon_enable(module="rigify")
    bpy.ops.object.armature_basic_quadruped_metarig_add()
    meta = bpy.context.active_object
    meta.name = "META_Quad"
    body = make_body(meta)
    if kind == "starter":
        meta.scale = (1.4, 1.4, 1.4)
        meta.location = (0.3, 0, 0.2)
        L.instructions(NOTE)
        return body, meta, None
    if kind == "wrong_scale":
        meta.scale = (1.4, 1.4, 1.4)
        bpy.context.view_layer.update()
        bpy.ops.object.select_all(action="DESELECT")
        meta.select_set(True)
        bpy.context.view_layer.objects.active = meta
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    bpy.ops.object.select_all(action="DESELECT")
    meta.select_set(True)
    bpy.context.view_layer.objects.active = meta
    bpy.ops.pose.rigify_generate()
    rig = next(o for o in bpy.data.objects if o.type == "ARMATURE" and o != meta)
    rig.name = "RIG_Quad"
    if kind == "not_generated":
        bpy.data.objects.remove(rig, do_unlink=True)
        L.instructions(NOTE)
        return body, meta, None
    if kind == "offset":
        rig.location.x = 0.5
    if kind != "unskinned":
        bpy.ops.object.select_all(action="DESELECT")
        body.select_set(True)
        rig.select_set(True)
        bpy.context.view_layer.objects.active = rig
        r = bpy.ops.object.parent_set(type="ARMATURE_AUTO")
        assert "FINISHED" in r, r
        bpy.ops.object.select_all(action="DESELECT")
        body.select_set(True)
        bpy.context.view_layer.objects.active = body
        bpy.ops.object.vertex_group_normalize_all(group_select_mode="ALL", lock_active=False)
        bpy.ops.object.vertex_group_limit_total(group_select_mode="ALL", limit=4)
        bpy.ops.object.vertex_group_normalize_all(group_select_mode="ALL", lock_active=False)
        if kind == "no_modifier":
            for m in list(body.modifiers):
                body.modifiers.remove(m)
        elif kind == "partial_weights":
            idx = [v.index for v in body.data.vertices if v.co.y < -0.1 and v.co.z < 0.6]     # pattes avant
            for g in body.vertex_groups:
                g.remove(idx)
    L.instructions(NOTE)
    return body, meta, rig


def sketch(body, rig, path):
    W, H = 460, 360
    tiles = []
    for lift in (0.0, 0.15):
        img = np.zeros((H, W, 3), np.float32)
        img[...] = 0.08
        pb = rig.pose.bones["front_foot_ik.L"]
        pb.location = pb.bone.matrix_local.to_3x3().inverted() @ Vector((0, 0, lift))
        bpy.context.view_layer.update()
        dg = bpy.context.evaluated_depsgraph_get()
        evb = body.evaluated_get(dg)
        me = evb.to_mesh()
        V = np.array([v.co[:] for v in me.vertices])
        evb.to_mesh_clear()
        for e in body.data.edges:
            a, b2 = V[e.vertices[0]], V[e.vertices[1]]
            x0, y0 = int(W / 2 - a[1] * 280 + 20), int(H - 40 - a[2] * 280)
            x1, y1 = int(W / 2 - b2[1] * 280 + 20), int(H - 40 - b2[2] * 280)
            n = max(abs(x1 - x0), abs(y1 - y0)) + 1
            for k in range(n + 1):
                x, y = int(x0 + (x1 - x0) * k / n), int(y0 + (y1 - y0) * k / n)
                if 0 <= x < W and 0 <= y < H:
                    img[y, x] = (0.35, 0.35, 0.4)
        evr = rig.evaluated_get(dg)
        for b in evr.pose.bones:
            if not b.name.startswith("DEF-"):
                continue
            h, t = evr.matrix_world @ b.head, evr.matrix_world @ b.tail
            x0, y0 = int(W / 2 - h.y * 280 + 20), int(H - 40 - h.z * 280)
            x1, y1 = int(W / 2 - t.y * 280 + 20), int(H - 40 - t.z * 280)
            n = max(abs(x1 - x0), abs(y1 - y0)) + 1
            for k in range(n + 1):
                x, y = int(x0 + (x1 - x0) * k / n), int(y0 + (y1 - y0) * k / n)
                if 0 <= x < W and 0 <= y < H:
                    img[y, x] = (0.95, 0.6, 0.15) if b.name.endswith(".L") else ((0.3, 0.7, 1.0) if b.name.endswith(".R") else (0.9, 0.9, 0.3))
        tiles.append(img)
    sheet = np.concatenate(tiles, axis=1)
    rgba = np.concatenate([sheet, np.ones(sheet.shape[:2] + (1,), np.float32)], axis=2)
    out = bpy.data.images.new("sk", sheet.shape[1], H)
    out.pixels = rgba[::-1].ravel()
    out.filepath_raw = path
    out.file_format = "PNG"
    out.save()
    rig.pose.bones["front_foot_ik.L"].location = (0, 0, 0)


def main():
    out = os.path.join(CH, "COMPLETED_EXAMPLES")
    build("starter")
    L.save(os.path.join(CH, "STARTER_FILES", "ch06_06_quadruped_starter.blend"))
    for k in ("not_generated", "unskinned", "wrong_scale", "no_modifier", "partial_weights", "offset"):
        build(k)
        L.save(os.path.join(out, "COUNTER_EXAMPLES", f"ch06_06_quadruped_{k}.blend"))
    body, meta, rig = build("solution")
    L.save(os.path.join(out, "ch06_06_quadruped_solution.blend"))
    sketch(body, rig, os.path.join(out, "ch06_06_quadruped_reference.png"))


if __name__ == "__main__":
    L.run(main)
