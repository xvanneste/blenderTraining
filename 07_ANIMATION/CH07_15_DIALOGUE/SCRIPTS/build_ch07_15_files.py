"""
build_ch07_15_files.py — « Scène dialoguée » (CH07.15 : blocking, splining, polish).

Une tête GEO_Head (sphère de 0,25 m, nez en cône pour lire l'orientation) joue le regard d'un personnage dans une scène à trois partenaires (A à sa gauche, B à sa droite, la caméra de face) ; 73 images à 24 i/s :
  BLOCKING (action « BLOCK », clés en interpolation CONSTANT : le regard saute de pose en pose) : lacet de la tête autour de Z, aux images 1, 13, 25, 37, 49, 61, 73 : 0°, +40°, +40°, −30°, −30°, 0°, 0°
        (neutre ; regarde A ; écoute A ; regarde B ; écoute B ; regarde la caméra ; maintien final).
  SPLINING (action « FINAL », active) : les mêmes poses en Bezier (poignées Auto Clamped) + trois breakdowns aux images 7 (+22°), 31 (+5°) et 55 (−12°) : les mouvements entre les poses sont lisses, les maintiens restent plats.
  Marqueurs « beat_1 » à « beat_7 » aux images des poses.
  STARTER_FILES/ch07_15_dialogue_starter.blend : BLOCK active (7 clés, CONSTANT), pas de FINAL, pas de marqueurs, plage 1–73. COMPLETED_EXAMPLES/ch07_15_dialogue_solution.blend (+ _reference.png : blocking en escalier, splining en courbe)
  COUNTER_EXAMPLES/ : still_stepped, no_breakdowns, drift, hold_lost, no_markers, block_active
Usage : blender -b --factory-startup --python-exit-code 1 --python build_ch07_15_files.py
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

CH = L.chapter_dir(__file__)
BEATS = [(1, 0.0), (13, 40.0), (25, 40.0), (37, -30.0), (49, -30.0), (61, 0.0), (73, 0.0)]
BREAKDOWNS = [(7, 22.0), (31, 5.0), (55, -12.0)]
NOTE = """CH07.15 — SCÈNE DIALOGUÉE : BLOCKING, SPLINING, POLISH (GEO_Head)
La tête suit un dialogue : elle regarde A (+40°), l'écoute, regarde B (−30°), l'écoute, puis regarde la caméra. L'action « BLOCK » est le BLOCKING : 7 poses clés aux images 1, 13, 25, 37, 49, 61, 73 (lacet 0, +40, +40, −30, −30, 0, 0), interpolation Constant : le regard saute.
1. Dupliquez « BLOCK » en « FINAL » et assignez-la : FINAL doit être l'action ACTIVE ; « BLOCK » reste intacte.
2. SPLINING : dans FINAL, passez toutes les clés en Bezier (poignées Auto Clamped) et ajoutez au moins deux BREAKDOWNS (par exemple image 7 : +22°, image 31 : +5°, image 55 : −12°) : les poses gardent leurs valeurs, les maintiens (images 13–25, 37–49, 61–73) restent plats.
3. Marqueurs « beat_1 » à « beat_7 » aux images des poses.
4. Plage de la scène : 1–73.
Le correcteur lit les deux actions et l'animation évaluée : clés, interpolation, valeurs des poses, vitesse maximale, maintiens, marqueurs.
Vérification : SCRIPTS/validate_ch07_15.py -- --exercise dialogue
"""


def fcurves(act):
    try:
        return list(act.fcurves)
    except AttributeError:
        return [f for l in act.layers for st in l.strips for cb in st.channelbags for f in cb.fcurves]


def make_head():
    bm = bmesh.new()
    bmesh.ops.create_uvsphere(bm, u_segments=24, v_segments=12, radius=0.25)
    ret = bmesh.ops.create_cone(bm, cap_ends=True, segments=12, radius1=0.06, radius2=0.0, depth=0.18)
    for v in ret["verts"]:
        v.co = (v.co.x, -0.34 + v.co.z * 1.0, v.co.y)           # nez le long de −Y (le visage regarde −Y)
        v.co = (v.co.x, v.co.y, v.co.z)
    me = bpy.data.meshes.new("ME_Head")
    bm.to_mesh(me)
    bm.free()
    ob = bpy.data.objects.new("GEO_Head", me)
    bpy.context.scene.collection.objects.link(ob)
    ob.location = (0, 0, 1.0)
    return ob


def key_action(ob, name, keys, interp):
    ob.animation_data_create()
    ob.animation_data.action = None
    for f, a in keys:
        ob.rotation_euler = (0, 0, math.radians(a))
        ob.keyframe_insert("rotation_euler", index=2, frame=f)
    act = ob.animation_data.action
    act.name = name
    for fc in fcurves(act):
        for kp in fc.keyframe_points:
            kp.interpolation = interp
            if interp == "BEZIER":
                kp.handle_left_type = kp.handle_right_type = "AUTO_CLAMPED"
        fc.update()
    return act


def build(kind):
    L.reset("SC_DIALOGUE")
    sc = bpy.context.scene
    sc.render.fps = 24
    sc.frame_start, sc.frame_end = 1, 73
    ob = make_head()
    block = key_action(ob, "BLOCK", BEATS, "CONSTANT")
    block.use_fake_user = True
    if kind == "starter":
        L.instructions(NOTE)
        ob.rotation_euler = (0, 0, 0)
        return ob
    keys = list(BEATS)
    if kind == "drift":
        keys[1] = (13, 55.0)
    if kind not in ("no_breakdowns", "still_stepped"):
        keys += BREAKDOWNS
    if kind == "hold_lost":
        keys += BREAKDOWNS + [(19, 25.0)]
    keys = sorted(dict(keys).items())
    interp = "CONSTANT" if kind == "still_stepped" else "BEZIER"
    final = key_action(ob, "FINAL", keys, interp)
    final.use_fake_user = True
    ob.animation_data.action = block if kind == "block_active" else final
    if kind == "block_active":
        ob.animation_data.action_slot = block.slots[0]
    if kind != "no_markers":
        for i, (f, a) in enumerate(BEATS, 1):
            sc.timeline_markers.new(f"beat_{i}", frame=f)
    ob.rotation_euler = (0, 0, 0)
    sc.frame_set(1)
    L.instructions(NOTE)
    return ob


def sketch(path):
    ob = build("solution")
    sc = bpy.context.scene
    Wd, H = 800, 320
    img = np.full((H, Wd, 3), 0.08, np.float32)
    img[160, 20:Wd - 20] = (0.25, 0.25, 0.25)

    def px(f, a):
        return int(20 + (f - 1) / 72 * (Wd - 40)), int(160 - a / 50 * 130)
    for f, a in BEATS:
        img[10:H - 10, px(f, 0)[0]] = (0.2, 0.2, 0.2)
    for f in np.linspace(1, 73, 800):                                   # blocking (escalier, gris)
        a = [v for ff, v in BEATS if ff <= f][-1]
        x, y = px(f, a)
        img[y - 1:y + 2, x - 1:x + 2] = (0.45, 0.45, 0.5)
    for f10 in range(10, 731):
        f = f10 / 10
        sc.frame_set(int(f), subframe=f - int(f))
        bpy.context.view_layer.update()
        x, y = px(f, math.degrees(ob.rotation_euler.z))
        img[y - 1:y + 2, x - 1:x + 2] = (0.9, 0.55, 0.2)
    for f, a in BEATS:
        x, y = px(f, a)
        img[y - 5:y + 6, x - 5:x + 6] = (1, 1, 1)
    for f, a in BREAKDOWNS:
        x, y = px(f, a)
        img[y - 4:y + 5, x - 4:x + 5] = (0.3, 0.8, 0.5)
    rgba = np.concatenate([img, np.ones(img.shape[:2] + (1,), np.float32)], axis=2)
    out = bpy.data.images.new("sk", Wd, H)
    out.pixels = rgba[::-1].ravel()
    out.filepath_raw = path
    out.file_format = "PNG"
    out.save()


def main():
    out = os.path.join(CH, "COMPLETED_EXAMPLES")
    build("starter")
    L.save(os.path.join(CH, "STARTER_FILES", "ch07_15_dialogue_starter.blend"))
    for k in ("still_stepped", "no_breakdowns", "drift", "hold_lost", "no_markers", "block_active"):
        build(k)
        L.save(os.path.join(out, "COUNTER_EXAMPLES", f"ch07_15_dialogue_{k}.blend"))
    build("solution")
    L.save(os.path.join(out, "ch07_15_dialogue_solution.blend"))
    sketch(os.path.join(out, "ch07_15_dialogue_reference.png"))


if __name__ == "__main__":
    L.run(main)
