"""
validate_ch18_20.py — Correcteur « Du board au layout 3D » (CH18.20).
Usage : … --python validate_ch18_20.py --python-exit-code 1 -- --exercise layout [--render]
Pour chaque marqueur lié à une caméra : compare, en coordonnées d'image de cette caméra, la boîte de
la silhouette dessinée (BOARD_SHxxxx, enfant de la caméra) et celle du mannequin CHR_A évalué à
l'image du marqueur (recouvrement IoU ≥ 0,5, pieds alignés). Vérifie aussi : caméras inchangées
(matrices d'origine mémorisées), clés de CHR_A en interpolation Constant, boards exclus du rendu.
Testé avec : Blender 5.3.0.
"""
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bpy  # noqa: E402
from bpy_extras.object_utils import world_to_camera_view  # noqa: E402
from mathutils import Vector  # noqa: E402


def bbox2d(sc, cam, pts):
    uv = [world_to_camera_view(sc, cam, p) for p in pts]
    uv = [q for q in uv if q.z > 0]
    if not uv:
        return None
    return (min(q.x for q in uv), min(q.y for q in uv), max(q.x for q in uv), max(q.y for q in uv))


def iou(a, b):
    ix = max(0, min(a[2], b[2]) - max(a[0], b[0]))
    iy = max(0, min(a[3], b[3]) - max(a[1], b[1]))
    inter = ix * iy
    ua = (a[2] - a[0]) * (a[3] - a[1]) + (b[2] - b[0]) * (b[3] - b[1]) - inter
    return inter / ua if ua > 0 else 0


def board_points(ob):
    mw = ob.matrix_world
    return [mw @ Vector(p.position) for lay in ob.data.layers for fr in lay.frames for s in fr.drawing.strokes for p in s.points]


def fcurves(ob):
    ad = ob.animation_data
    out = []
    if ad and ad.action:
        for lay in getattr(ad.action, "layers", []):
            for st in lay.strips:
                for bag in getattr(st, "channelbags", []):
                    out.extend(bag.fcurves)
    return out


def main():
    sc = bpy.context.scene
    r = L.Report("CH18.20 — Du board au layout 3D")
    chr_ = bpy.data.objects.get("CHR_A")
    stored = json.loads(sc.get("bcma_cams", "{}"))
    mks = sorted([m for m in sc.timeline_markers if m.camera], key=lambda m: m.frame)
    if not r.check(chr_ is not None and len(mks) >= 3, f"Personnage CHR_A et {len(mks)} marqueurs liés à des caméras",
                   "Repartez du starter.", 1):
        return r.finish()
    moved = []
    for m in mks:
        ref = stored.get(m.name)
        if ref:
            cur = m.camera.matrix_world
            if max(abs(cur[i][j] - ref[i][j]) for i in range(4) for j in range(4)) > 1e-3:
                moved.append(m.camera.name)
    r.check(not moved, "Caméras du board inchangées", f"Modifiées : {moved} (Ctrl+Z, ou repartez du starter).", 2)
    good, details = 0, []
    dg = bpy.context.evaluated_depsgraph_get()
    for m in mks:
        sc.frame_set(m.frame)
        bpy.context.view_layer.update()
        b = bpy.data.objects.get("BOARD_" + m.name)
        if b is None:
            details.append(f"{m.name} : board absent")
            continue
        bb = bbox2d(sc, m.camera, board_points(b))
        ev = chr_.evaluated_get(dg)
        verts = [ev.matrix_world @ v.co for v in ev.data.vertices]
        cb = bbox2d(sc, m.camera, verts)
        if not bb or not cb:
            details.append(f"{m.name} : hors champ")
            continue
        v = iou(bb, cb)
        feet = abs(bb[1] - cb[1])
        ok = v >= 0.5 and feet <= 0.05
        good += ok
        details.append(f"{m.name} IoU {v:.2f}, pieds Δ{feet:.3f}")
    r.check(good == len(mks), f"Blocking conforme au board ({good}/{len(mks)} plans) — " + " ; ".join(details),
            "À chaque marqueur, vue caméra : superposez le mannequin à la silhouette dessinée puis K > Location & Rotation.", 6)
    fcs = fcurves(chr_)
    keys = [k for fc in fcs for k in fc.keyframe_points]
    r.check(bool(keys) and all(k.interpolation == "CONSTANT" for k in keys),
            f"Clés du personnage en Constant ({sum(k.interpolation == 'CONSTANT' for k in keys)}/{len(keys)})",
            "Sélection des clés, T > Constant : le personnage change de place à la coupe sans glisser.", 2)
    boards = [o for o in bpy.data.objects if o.name.startswith("BOARD_")]
    r.check(boards and all(o.hide_render for o in boards), "Boards exclus du rendu final", "Outliner : Disable in Renders.", 1)
    if L.flag("--render"):
        sc.frame_set(mks[0].frame)
        lum = L.quick_render(15, 4)
        r.check(lum > 0.05, f"Rendu de contrôle non noir ({lum:.3f})", "", 1)
    return r.finish()


if __name__ == "__main__":
    L.run(main)
