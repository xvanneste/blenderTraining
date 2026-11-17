"""
build_ch07_04_files.py — « Graph Editor » (CH07.04 : polir des courbes : interpolation, poignées, modificateurs de F-curve).

Un pendule GEO_Pendulum (tige de 1 m pendue à son origine, origine = pivot) :
  Rotation Y : images clés 1, 13, 25 : −30°, +30°, −30° (un aller-retour en 24 images).
  Position Z : images clés 1 et 25 à 0 (courbe plate qui portera un modificateur Noise).
  Solution : (1) interpolation BEZIER, poignées AUTO_CLAMPED : ralentis aux extrémités (vitesse nulle à l'image 13, vitesse maximale au milieu) ;
             (2) modificateur Cycles sur la courbe de rotation Y : l'aller-retour se répète sans fin (image 37 = 30°, image 49 = −30°, image 61 = 30°) ;
             (3) modificateur Noise sur la courbe de position Z : un léger frémissement (Strength 0,06, Scale 6 images) ; plage de la scène 1–48.
  STARTER_FILES/ch07_04_graph_starter.blend : clés en interpolation LINÉAIRE, sans modificateur, plage 1–25.
  COMPLETED_EXAMPLES/ch07_04_graph_solution.blend (+ _reference.png : le Graph Editor en numpy sur 72 images)
  COUNTER_EXAMPLES/ : linear, constant, no_cycles, no_noise, noise_too_strong, wrong_keys
Usage : blender -b --factory-startup --python-exit-code 1 --python build_ch07_04_files.py
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
NOTE = """CH07.04 — GRAPH EDITOR (GEO_Pendulum)
Le pendule bouge de façon mécanique : clés en interpolation linéaire, un seul aller-retour. Polissez ses courbes dans le Graph Editor :
1. Courbe Y Euler Rotation : sélectionnez les clés, interpolation Bezier (T > Bezier) et poignées Auto Clamped (V > Auto Clamped) : le pendule ralentit aux extrémités et accélère au milieu.
2. Même courbe : ajoutez un modificateur Cycles (panneau Modifiers de la barre latérale) : l'aller-retour se répète à l'infini.
3. Courbe Z Location (plate à 0) : ajoutez un modificateur Noise : Strength 0,06, Scale 6 : un léger frémissement.
4. Plage de la scène : 1 à 48.
Le correcteur lit les courbes (clés, interpolation, modificateurs) ET l'animation évaluée : vitesse aux extrémités, vitesse au milieu, répétition, amplitude du frémissement.
Vérification : SCRIPTS/validate_ch07_04.py -- --exercise graph
"""


def fcurves(act):
    try:
        return list(act.fcurves)
    except AttributeError:
        return [f for l in act.layers for st in l.strips for cb in st.channelbags for f in cb.fcurves]


def make_pendulum():
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    for v in bm.verts:
        v.co = (v.co.x * 0.08, v.co.y * 0.08, v.co.z * 1.0 - 0.5)
    me = bpy.data.meshes.new("ME_Pendulum")
    bm.to_mesh(me)
    bm.free()
    ob = bpy.data.objects.new("GEO_Pendulum", me)
    bpy.context.scene.collection.objects.link(ob)
    return ob


def build(kind):
    L.reset("SC_GRAPH")
    sc = bpy.context.scene
    sc.render.fps = 24
    ob = make_pendulum()
    amp = 45.0 if kind == "wrong_keys" else 30.0
    for f, a in ((1, -amp), (13, amp), (25, -amp)):
        ob.rotation_euler = (0, math.radians(a), 0)
        ob.location = (0, 0, 0)
        ob.keyframe_insert("rotation_euler", index=1, frame=f)
        if f != 13:
            ob.keyframe_insert("location", index=2, frame=f)
    act = ob.animation_data.action
    fcs = {(f.data_path, f.array_index): f for f in fcurves(act)}
    rot, locz = fcs[("rotation_euler", 1)], fcs[("location", 2)]
    interp = {"starter": "LINEAR", "linear": "LINEAR", "constant": "CONSTANT"}.get(kind, "BEZIER")
    for kp in rot.keyframe_points:
        kp.interpolation = interp
        if interp == "BEZIER":
            kp.handle_left_type = kp.handle_right_type = "AUTO_CLAMPED"
    rot.update()
    if kind == "starter":
        sc.frame_start, sc.frame_end = 1, 25
    else:
        sc.frame_start, sc.frame_end = 1, 48
        if kind != "no_cycles":
            rot.modifiers.new("CYCLES")
        if kind != "no_noise":
            m = locz.modifiers.new("NOISE")
            m.scale = 6.0
            m.strength = 0.5 if kind == "noise_too_strong" else 0.06
    sc.frame_set(1)
    L.instructions(NOTE)
    return ob


def sketch(path):
    ob = build("solution")
    sc = bpy.context.scene
    W, H = 780, 340
    img = np.full((H, W, 3), 0.08, np.float32)

    def px(f, v, lo, hi, top, bot):
        return int(30 + (f - 1) / 72 * (W - 60)), int(bot - (v - lo) / (hi - lo) * (bot - top))
    for f in (13, 25, 37, 49, 61):
        x = px(f, 0, 0, 1, 10, 330)[0]
        img[10:330, x] = (0.22, 0.22, 0.22)
    img[190, 30:W - 30] = (0.25, 0.25, 0.25)
    for ch, (lo, hi, top, bot, col) in enumerate(((-35.0, 35.0, 20, 200, (0.9, 0.55, 0.2)), (-0.08, 0.08, 230, 320, (0.3, 0.8, 0.5)))):
        pts = []
        for f10 in range(10, 721):
            f = f10 / 10
            sc.frame_set(int(f), subframe=f - int(f))
            bpy.context.view_layer.update()
            v = math.degrees(ob.rotation_euler.y) if ch == 0 else ob.location.z
            pts.append(px(f, v, lo, hi, top, bot))
        for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
            n = max(abs(x1 - x0), abs(y1 - y0)) + 1
            for k in range(n + 1):
                x, y = int(x0 + (x1 - x0) * k / n), int(y0 + (y1 - y0) * k / n)
                img[y - 1:y + 2, x - 1:x + 2] = col
    for f, a in ((1, -30), (13, 30), (25, -30)):
        x, y = px(f, a, -35, 35, 20, 200)
        img[y - 4:y + 5, x - 4:x + 5] = (1, 1, 1)
    rgba = np.concatenate([img, np.ones(img.shape[:2] + (1,), np.float32)], axis=2)
    out = bpy.data.images.new("sk", W, H)
    out.pixels = rgba[::-1].ravel()
    out.filepath_raw = path
    out.file_format = "PNG"
    out.save()


def main():
    out = os.path.join(CH, "COMPLETED_EXAMPLES")
    build("starter")
    L.save(os.path.join(CH, "STARTER_FILES", "ch07_04_graph_starter.blend"))
    for k in ("linear", "constant", "no_cycles", "no_noise", "noise_too_strong", "wrong_keys"):
        build(k)
        L.save(os.path.join(out, "COUNTER_EXAMPLES", f"ch07_04_graph_{k}.blend"))
    build("solution")
    L.save(os.path.join(out, "ch07_04_graph_solution.blend"))
    sketch(os.path.join(out, "ch07_04_graph_reference.png"))


if __name__ == "__main__":
    L.run(main)
