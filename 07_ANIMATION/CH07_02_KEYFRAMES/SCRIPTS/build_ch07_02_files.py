"""
build_ch07_02_files.py — « Keyframes et timeline » (CH07.02 : clés, interpolation, plage, marqueurs).

Une caisse GEO_Crate (cube de 1 m posé sur le sol) à animer, 72 images à 24 i/s :
  Position X : image 1 : 0 ; 24 : 4 (arrivée) ; 48 : 4 (REPOS, la caisse tourne sur place) ; 72 : 0 (retour).
  Rotation Z : image 24 : 0° ; 48 : 90° ; 72 : 90° ; interpolation LINÉAIRE (vitesse constante : à l'image 30, 22,5°).
  Timeline : plage 1–72 à 24 i/s ; marqueurs « arrive » (image 24) et « turn_end » (image 48) ; image courante 1.
  STARTER_FILES/ch07_02_keyframes_starter.blend : la caisse avec une seule clé (image 1), plage par défaut 1–250.
  COMPLETED_EXAMPLES/ch07_02_keyframes_solution.blend (+ _reference.png : courbes X et rotation, clés et marqueurs)
  COUNTER_EXAMPLES/ : wrong_range, no_hold, bezier_rot, no_markers, off_frames, no_rot
Usage : blender -b --factory-startup --python-exit-code 1 --python build_ch07_02_files.py
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
NOTE = """CH07.02 — KEYFRAMES ET TIMELINE (GEO_Crate)
1. Timeline : plage de 1 à 72, 24 images/s ; image courante 1.
2. Position X : clés aux images 1 (X = 0), 24 (X = 4), 48 (X = 4 : la caisse reste), 72 (X = 0).
3. Rotation Z : clés aux images 24 (0°), 48 (90°), 72 (90°) ; interpolation LINÉAIRE (vitesse constante : 22,5° à l'image 30).
4. Marqueurs : « arrive » à l'image 24, « turn_end » à l'image 48.
Astuce : insérez la position et la rotation par deux clés distinctes (I > Location, I > Rotation) ; changez l'interpolation des clés de rotation (Dope Sheet / Graph Editor : T > Linear).
Le correcteur lit les clés (images, valeurs) et l'animation évaluée (repos, vitesse de rotation, pas de dépassement).
Vérification : SCRIPTS/validate_ch07_02.py -- --exercise keyframes
"""


def fcurves(act):
    try:
        return list(act.fcurves)
    except AttributeError:
        return [f for l in act.layers for st in l.strips for cb in st.channelbags for f in cb.fcurves]


def make_crate():
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    bmesh.ops.translate(bm, verts=bm.verts, vec=(0, 0, 0.5))
    me = bpy.data.meshes.new("ME_Crate")
    bm.to_mesh(me)
    bm.free()
    ob = bpy.data.objects.new("GEO_Crate", me)
    bpy.context.scene.collection.objects.link(ob)
    return ob


def build(kind):
    L.reset("SC_KEYS")
    sc = bpy.context.scene
    sc.render.fps = 24
    ob = make_crate()
    ed = bpy.context.preferences.edit
    ed.keyframe_new_interpolation_type = "BEZIER"
    ob.location = (0, 0, 0)
    ob.rotation_euler = (0, 0, 0)
    ob.keyframe_insert("location", frame=1)
    if kind == "starter":
        sc.frame_start, sc.frame_end = 1, 250
        L.instructions(NOTE)
        return ob
    sc.frame_start, sc.frame_end = 1, (60 if kind == "wrong_range" else 72)
    shift = 1 if kind == "off_frames" else 0
    x48 = 3.5 if kind == "no_hold" else 4.0
    for f, x in ((24 + shift, 4.0), (48 + shift, x48), (72, 0.0)):
        ob.location = (x, 0, 0)
        ob.keyframe_insert("location", frame=f)
    if kind != "no_rot":
        for f, a in ((24, 0.0), (48, 90.0), (72, 90.0)):
            ob.rotation_euler = (0, 0, math.radians(a))
            ob.keyframe_insert("rotation_euler", frame=f)
        if kind != "bezier_rot":                           # l'interpolation d'insertion par défaut est Bezier : on passe les clés de rotation en LINÉAIRE
            for fc in fcurves(ob.animation_data.action):
                if fc.data_path == "rotation_euler":
                    for kp in fc.keyframe_points:
                        kp.interpolation = "LINEAR"
    if kind != "no_markers":
        sc.timeline_markers.new("arrive", frame=24)
        sc.timeline_markers.new("turn_end", frame=48)
    sc.frame_set(1)
    L.instructions(NOTE)
    return ob


def sketch(path):
    ob = build("solution")
    sc = bpy.context.scene
    W, H = 760, 340
    img = np.full((H, W, 3), 0.08, np.float32)

    def px(f, v, lo, hi, top, bot):
        return int(30 + (f - 1) / 71 * (W - 60)), int(bot - (v - lo) / (hi - lo) * (bot - top))
    for f in (24, 48):
        x = px(f, 0, 0, 1, 20, 320)[0]
        img[10:330, x] = (0.45, 0.45, 0.2)
    for ch, (lo, hi, col) in enumerate(((0.0, 4.0, (0.3, 0.8, 0.5)), (0.0, 90.0, (0.9, 0.55, 0.2)))):
        pts = []
        for f in range(1, 73):
            sc.frame_set(f)
            v = ob.location.x if ch == 0 else math.degrees(ob.rotation_euler.z)
            pts.append(px(f, v, lo, hi, 20 + ch * 8, 320 - ch * 8))
        for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
            n = max(abs(x1 - x0), abs(y1 - y0)) + 1
            for k in range(n + 1):
                x, y = int(x0 + (x1 - x0) * k / n), int(y0 + (y1 - y0) * k / n)
                img[y - 1:y + 2, x - 1:x + 2] = col
        keys = (1, 24, 48, 72) if ch == 0 else (24, 48, 72)
        for f in keys:
            sc.frame_set(f)
            v = ob.location.x if ch == 0 else math.degrees(ob.rotation_euler.z)
            x, y = px(f, v, lo, hi, 20 + ch * 8, 320 - ch * 8)
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
    L.save(os.path.join(CH, "STARTER_FILES", "ch07_02_keyframes_starter.blend"))
    for k in ("wrong_range", "no_hold", "bezier_rot", "no_markers", "off_frames", "no_rot"):
        build(k)
        L.save(os.path.join(out, "COUNTER_EXAMPLES", f"ch07_02_keyframes_{k}.blend"))
    build("solution")
    L.save(os.path.join(out, "ch07_02_keyframes_solution.blend"))
    sketch(os.path.join(out, "ch07_02_keyframes_reference.png"))


if __name__ == "__main__":
    L.run(main)
