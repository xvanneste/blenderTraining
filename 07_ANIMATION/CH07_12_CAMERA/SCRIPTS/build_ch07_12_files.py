"""
build_ch07_12_files.py — « Animation de caméra » (CH07.12 : travelling, suivi, caméra à l'épaule).

Un plan de 72 images (24 i/s, plage 1–72) : un sujet EMP_Subject (Empty, hauteur 1,0 m) traverse le champ de gauche à droite (X de −1 à +1 en interpolation LINÉAIRE) ; la caméra CAM_Main :
  TRAVELLING : avance sur l'axe Y de −8 m (image 1) à −4 m (image 72), hauteur 1,6 m, en BEZIER (départ et arrivée doux : vitesse aux extrémités ≤ 25 % de la vitesse maximale) ;
  SUIVI : contrainte Track To vers EMP_Subject (axe de visée −Z, haut Y) : le sujet reste au centre de l'image ;
  ÉPAULE : modificateur Noise (Strength 0,1, Scale 8 images) sur les courbes X et Z de la position (pas sur Y : le travelling reste propre) ;
  pas de roulis : l'horizon reste horizontal (roulis ≤ 1°).
  STARTER_FILES/ch07_12_camera_starter.blend : sujet animé, caméra fixe à (0, −8, 1,6) sans contrainte ni animation. COMPLETED_EXAMPLES/ch07_12_camera_solution.blend (+ _reference.png : vue de dessus de la trajectoire et courbes de la position)
  COUNTER_EXAMPLES/ : no_tracking, linear_dolly, too_shaky, no_handheld, rolled, short_dolly
Usage : blender -b --factory-startup --python-exit-code 1 --python build_ch07_12_files.py
Testé avec : Blender 5.3.0.
"""
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bpy  # noqa: E402
import numpy as np  # noqa: E402
from mathutils import Vector  # noqa: E402

CH = L.chapter_dir(__file__)
NOTE = """CH07.12 — ANIMATION DE CAMÉRA (CAM_Main, EMP_Subject)
Le sujet (EMP_Subject) traverse le champ de gauche à droite. Animez la caméra CAM_Main (plage 1–72, 24 i/s) :
1. TRAVELLING : position Y de −8 m (image 1) à −4 m (image 72), hauteur 1,6 m ; interpolation Bezier : la caméra démarre et s'arrête en douceur.
2. SUIVI : contrainte Track To vers EMP_Subject : Track Axis −Z, Up Axis Y : le sujet reste au centre.
3. ÉPAULE : modificateur Noise sur les courbes X Location et Z Location de la caméra (Strength 0,1 ; Scale 8) : léger tremblé ; pas sur Y.
4. Horizon horizontal : aucun roulis.
Le correcteur lit la caméra évaluée : trajet, vitesse aux extrémités, suivi du sujet, tremblé, roulis, et la présence de la contrainte et des modificateurs.
Vérification : SCRIPTS/validate_ch07_12.py -- --exercise camera
"""


def fcurves(act):
    try:
        return list(act.fcurves)
    except AttributeError:
        return [f for l in act.layers for st in l.strips for cb in st.channelbags for f in cb.fcurves]


def build(kind):
    L.reset("SC_CAMERA")
    sc = bpy.context.scene
    sc.render.fps = 24
    sc.frame_start, sc.frame_end = 1, 72
    sub = bpy.data.objects.new("EMP_Subject", None)
    sub.empty_display_type = "SPHERE"
    sub.empty_display_size = 0.3
    sc.collection.objects.link(sub)
    for f, x in ((1, -1.0), (72, 1.0)):
        sub.location = (x, 0, 1.0)
        sub.keyframe_insert("location", frame=f)
    for fc in fcurves(sub.animation_data.action):
        for kp in fc.keyframe_points:
            kp.interpolation = "LINEAR"
    cd = bpy.data.cameras.new("CAM_Main")
    cd.lens = 35
    cam = bpy.data.objects.new("CAM_Main", cd)
    sc.collection.objects.link(cam)
    sc.camera = cam
    cam.location = (0, -8, 1.6)
    cam.rotation_euler = (math.radians(90), 0, 0)
    if kind != "starter":
        y_end = -6.0 if kind == "short_dolly" else -4.0
        for f, y in ((1, -8.0), (72, y_end)):
            cam.location = (0, y, 1.6)
            cam.keyframe_insert("location", frame=f)
        fcs = {(f.data_path, f.array_index): f for f in fcurves(cam.animation_data.action)}
        if kind == "linear_dolly":
            for kp in fcs[("location", 1)].keyframe_points:
                kp.interpolation = "LINEAR"
        if kind == "rolled":                                         # Damped Track garde le roulis de départ (8°) : l'horizon penche
            cam.rotation_euler = (math.radians(90), math.radians(8), 0)
            c = cam.constraints.new("DAMPED_TRACK")
            c.target = sub
            c.track_axis = "TRACK_NEGATIVE_Z"
        elif kind != "no_tracking":
            c = cam.constraints.new("TRACK_TO")
            c.target = sub
            c.track_axis = "TRACK_NEGATIVE_Z"
            c.up_axis = "UP_Y"
        if kind != "no_handheld":
            for idx in (0, 2):
                m = fcs[("location", idx)].modifiers.new("NOISE")
                m.scale = 8.0
                m.phase = 1.0 + 4.0 * idx                           # phases différentes : X et Z ne tremblent pas à l identique
                m.strength = 0.5 if kind == "too_shaky" else 0.1
        sc.frame_set(1)
    L.instructions(NOTE)
    return cam, sub


def sketch(path):
    cam, sub = build("solution")
    sc = bpy.context.scene
    W, H = 800, 340
    img = np.full((H, W, 3), 0.08, np.float32)
    # vue de dessus (x, y) à gauche
    def top(p):
        return int(120 + p.x * 40), int(300 + p.y * 28)
    pts = []
    for f in range(1, 73):
        sc.frame_set(f)
        bpy.context.view_layer.update()
        c = cam.matrix_world.translation
        s = sub.matrix_world.translation
        x, y = top(c)
        img[y - 1:y + 2, x - 1:x + 2] = (0.9, 0.55, 0.2)
        x2, y2 = top(s)
        img[y2 - 1:y2 + 2, x2 - 1:x2 + 2] = (0.3, 0.8, 0.5)
        if f in (1, 24, 48, 72):
            n = 60
            for k in range(n + 1):
                xx = int(x + (x2 - x) * k / n)
                yy = int(y + (y2 - y) * k / n)
                img[yy, xx] = (0.5, 0.5, 0.5)
    # courbes de position X et Z à droite
    for f in range(1, 73):
        sc.frame_set(f)
        bpy.context.view_layer.update()
        c = cam.matrix_world.translation
        x = int(300 + (f - 1) / 71 * 470)
        for v, ycen, col in ((c.x, 90, (0.3, 0.7, 1.0)), (c.z - 1.6, 230, (0.9, 0.9, 0.9)), ((c.y + 8) / 4, 0, None)):
            if col is None:
                continue
            y = int(ycen - v * 1000)
            if 3 <= y < H - 3:
                img[y - 2:y + 3, x - 2:x + 3] = col
    rgba = np.concatenate([img, np.ones(img.shape[:2] + (1,), np.float32)], axis=2)
    out = bpy.data.images.new("sk", W, H)
    out.pixels = rgba[::-1].ravel()
    out.filepath_raw = path
    out.file_format = "PNG"
    out.save()


def main():
    out = os.path.join(CH, "COMPLETED_EXAMPLES")
    build("starter")
    L.save(os.path.join(CH, "STARTER_FILES", "ch07_12_camera_starter.blend"))
    for k in ("no_tracking", "linear_dolly", "too_shaky", "no_handheld", "rolled", "short_dolly"):
        build(k)
        L.save(os.path.join(out, "COUNTER_EXAMPLES", f"ch07_12_camera_{k}.blend"))
    build("solution")
    L.save(os.path.join(out, "ch07_12_camera_solution.blend"))
    sketch(os.path.join(out, "ch07_12_camera_reference.png"))


if __name__ == "__main__":
    L.run(main)
