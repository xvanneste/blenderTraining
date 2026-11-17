"""
build_ch07_14_files.py — « Motion capture » (CH07.14 : importer un BVH bruité et le nettoyer).

Le fichier BVH synthétique STARTER_FILES/ch07_14_mocap_noisy.bvh (96 images à 24 i/s ; squelette de quatre joints : Hips (position + rotation), Spine, Head, Arm_L ; une oscillation de période 24 images par joint)
est produit par ce script, avec le défaut typique d'une capture : un BRUIT d'écart-type 1° sur les rotations (3 mm sur la hauteur et l'avancée des hanches) et trois GLITCHES (+9° sur Spine, Head et Arm_L aux images 21, 48, 72 ; +4 cm sur la hauteur des hanches à l'image 48).
  STARTER_FILES/ch07_14_mocap_starter.blend : le BVH importé (bpy.ops.import_anim.bvh : RIG_Mocap, action active « MOCAP », 15 courbes de 96 clés) + une copie intacte « MOCAP_RAW » (utilisateur fictif, ne pas toucher) ; plage 1–96.
  Solution (calculée par script) : pour chaque courbe de « MOCAP » : suppression des glitches (médiane glissante sur 5 images), lissage gaussien (σ = 1,2 image), décimation (Ramer-Douglas-Peucker, tolérance 3 % de l'amplitude), clés en Bezier.
  COMPLETED_EXAMPLES/ch07_14_mocap_solution.blend (+ _reference.png : la courbe de rotation Z de Spine, brute puis nettoyée)
  COUNTER_EXAMPLES/ : not_cleaned, over_smoothed, kept_spikes, too_many_keys, linear_keys, raw_modified
Usage : blender -b --factory-startup --python-exit-code 1 --python build_ch07_14_files.py
Testé avec : Blender 5.3.0.
"""
import math
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bpy  # noqa: E402
import numpy as np  # noqa: E402

CH = L.chapter_dir(__file__)
BVH = os.path.join(CH, "STARTER_FILES", "ch07_14_mocap_noisy.bvh")
SPIKES = (21, 48, 72)
HIER = """HIERARCHY
ROOT Hips
{
\tOFFSET 0 0.95 0
\tCHANNELS 6 Xposition Yposition Zposition Zrotation Xrotation Yrotation
\tJOINT Spine
\t{
\t\tOFFSET 0 0.3 0
\t\tCHANNELS 3 Zrotation Xrotation Yrotation
\t\tJOINT Head
\t\t{
\t\t\tOFFSET 0 0.5 0
\t\t\tCHANNELS 3 Zrotation Xrotation Yrotation
\t\t\tEnd Site
\t\t\t{
\t\t\t\tOFFSET 0 0.25 0
\t\t\t}
\t\t}
\t\tJOINT Arm_L
\t\t{
\t\t\tOFFSET 0.2 0.4 0
\t\t\tCHANNELS 3 Zrotation Xrotation Yrotation
\t\t\tEnd Site
\t\t\t{
\t\t\t\tOFFSET 0.5 0 0
\t\t\t}
\t\t}
\t}
}
MOTION
Frames: 96
Frame Time: 0.0416667
"""
NOTE = """CH07.14 — MOTION CAPTURE (RIG_Mocap)
Le BVH « ch07_14_mocap_noisy.bvh » est une capture bruitée (bruit de 1° et trois glitches de 9° aux images 21, 48 et 72). Il est déjà importé : action active « MOCAP » (15 courbes de 96 clés). « MOCAP_RAW » est une copie de référence : NE LA MODIFIEZ PAS.
Nettoyez « MOCAP » dans le Graph Editor :
1. Retirer les glitches puis lisser : Key > Smooth > Smooth (Gaussian) (ou Smooth (Legacy) / Butterworth) sur toutes les courbes.
2. Décimer : Key > Density > Decimate (Allowed Change) puis Clean Keyframes : il doit rester au plus 38 clés par courbe (96 au départ).
3. Interpolation Bezier sur les clés restantes (T > Bezier).
Contrôles (par courbe, comparées à MOCAP_RAW) : rugosité divisée par deux au moins ; forme fidèle (écart quadratique ≤ 8 % de l amplitude de la courbe de référence) ; amplitude conservée (≥ 90 %) ; glitches supprimés (écart maximal ≤ 15 % de l'amplitude) ; au plus 38 clés ; toutes en Bezier ; MOCAP_RAW intacte (96 clés par courbe).
Vérification : SCRIPTS/validate_ch07_14.py -- --exercise mocap
"""


def write_bvh():
    random.seed(7)
    rows = []
    for f in range(96):
        t = f / 24.0
        r = [0.0] * 15
        r[1] = 0.02 * math.sin(4 * math.pi * t)
        r[2] = 0.025 * f
        r[3] = 3 * math.sin(2 * math.pi * t)
        r[6] = 8 * math.sin(2 * math.pi * t)
        r[7] = 5 + 2 * math.sin(4 * math.pi * t)
        r[9] = 10 * math.sin(2 * math.pi * t + 0.8)
        r[12] = 25 * math.sin(2 * math.pi * t + math.pi)
        for i in (1, 2):
            r[i] += random.gauss(0, 0.003)
        for i in range(3, 15):
            r[i] += random.gauss(0, 1.0)
        if f + 1 in SPIKES:
            r[6] += 9.0
            r[9] += 9.0
            r[12] += 9.0
            if f + 1 == 48:
                r[1] += 0.04
        rows.append(r)
    text = HIER + "\n".join(" ".join(f"{v:.4f}" for v in r) for r in rows) + "\n"
    os.makedirs(os.path.dirname(BVH), exist_ok=True)
    open(BVH, "w", encoding="utf-8", newline="\n").write(text)


def fcurves(act):
    try:
        return list(act.fcurves)
    except AttributeError:
        return [f for l in act.layers for st in l.strips for cb in st.channelbags for f in cb.fcurves]


def values(fc, n=96):
    return np.array([fc.evaluate(f) for f in range(1, n + 1)])


def floor(fc):
    return 0.05 if fc.data_path.endswith("rotation_euler") else 0.02          # amplitude minimale de référence (rad ou m) : les courbes qui ne contiennent que du bruit n'ont pas d'amplitude utile


def median5(y):
    pad = np.pad(y, 2, mode="edge")
    return np.array([np.median(pad[i:i + 5]) for i in range(len(y))])


def gauss(y, sigma):
    r = max(1, int(round(3 * sigma)))
    k = np.exp(-0.5 * (np.arange(-r, r + 1) / sigma) ** 2)
    k /= k.sum()
    return np.convolve(np.pad(y, r, mode="edge"), k, mode="valid")


def rdp(pts, eps):
    if len(pts) < 3:
        return pts
    a, b = np.array(pts[0]), np.array(pts[-1])
    d = b - a
    n = np.hypot(*d)
    dist = [abs(d[0] * (p[1] - a[1]) - d[1] * (p[0] - a[0])) / n if n else np.hypot(p[0] - a[0], p[1] - a[1]) for p in pts[1:-1]]
    i = int(np.argmax(dist))
    if dist[i] > eps:
        left = rdp(pts[:i + 2], eps)
        right = rdp(pts[i + 1:], eps)
        return left[:-1] + right
    return [pts[0], pts[-1]]


def rewrite(fc, frames_values, interp):
    fc.keyframe_points.clear()
    for f, v in frames_values:
        kp = fc.keyframe_points.insert(f, float(v), options={"FAST"})
        kp.interpolation = interp
        kp.handle_left_type = kp.handle_right_type = "AUTO_CLAMPED"
    fc.update()


def clean(act, kind):
    for fc in fcurves(act):
        y = values(fc)
        ptp = float(np.ptp(y))
        eps = max(0.03 * ptp, 0.25 * floor(fc))                       # tolérance de décimation : 3 % de l'amplitude, au moins le quart du plancher (les courbes de pur bruit se réduisent à quelques clés)
        if kind == "over_smoothed":
            z = gauss(median5(y), 6.0)
        elif kind == "kept_spikes":
            z = gauss(y, 0.8)
        else:
            z = gauss(median5(y), 1.2)
        if kind == "too_many_keys":
            pts = [(f + 1, z[f]) for f in range(96)]
        else:
            pts = rdp([(f + 1, float(z[f])) for f in range(96)], eps)
        rewrite(fc, pts, "LINEAR" if kind == "linear_keys" else "BEZIER")


def build(kind):
    L.reset("SC_MOCAP")
    sc = bpy.context.scene
    sc.render.fps = 24
    bpy.ops.import_anim.bvh(filepath=BVH, global_scale=1.0, frame_start=1, use_fps_scale=False, rotate_mode="NATIVE", axis_forward="-Z", axis_up="Y")
    rig = next(o for o in bpy.data.objects if o.type == "ARMATURE")
    rig.name = "RIG_Mocap"
    act = rig.animation_data.action
    raw = act.copy()
    raw.name = "MOCAP_RAW"
    raw.use_fake_user = True
    act.name = "MOCAP"
    sc.frame_start, sc.frame_end = 1, 96
    if kind in ("solution", "over_smoothed", "kept_spikes", "too_many_keys", "linear_keys"):
        clean(act, kind)
    elif kind == "raw_modified":
        clean(act, "solution")
        clean(raw, "solution")
    sc.frame_set(1)
    L.instructions(NOTE)
    return rig, act, raw


def sketch(path):
    rig, act, raw = build("solution")
    fc = next(f for f in fcurves(act) if f.data_path == 'pose.bones["Spine"].rotation_euler' and f.array_index == 2)
    fr = next(f for f in fcurves(raw) if f.data_path == 'pose.bones["Spine"].rotation_euler' and f.array_index == 2)
    W, H = 800, 320
    img = np.full((H, W, 3), 0.08, np.float32)
    img[160, 20:W - 20] = (0.25, 0.25, 0.25)
    yr, yc = values(fr), values(fc)
    lim = max(np.abs(yr).max(), 1e-6)

    def px(f, v):
        return int(20 + (f - 1) / 95 * (W - 40)), int(160 - v / lim * 130)
    for f in range(1, 97):
        x, y = px(f, yr[f - 1])
        img[y - 1:y + 2, x - 1:x + 2] = (0.45, 0.45, 0.5)
    for f in np.linspace(1, 96, 760):
        x, y = px(f, fc.evaluate(float(f)))
        img[y - 1:y + 2, x - 1:x + 2] = (0.9, 0.55, 0.2)
    for kp in fc.keyframe_points:
        x, y = px(kp.co[0], kp.co[1])
        img[y - 4:y + 5, x - 4:x + 5] = (1, 1, 1)
    rgba = np.concatenate([img, np.ones(img.shape[:2] + (1,), np.float32)], axis=2)
    out = bpy.data.images.new("sk", W, H)
    out.pixels = rgba[::-1].ravel()
    out.filepath_raw = path
    out.file_format = "PNG"
    out.save()
    print(f"[mocap] Spine Z : {len(fc.keyframe_points)} clés (96 au départ) ; total des clés : {sum(len(f.keyframe_points) for f in fcurves(act))}")


def main():
    out = os.path.join(CH, "COMPLETED_EXAMPLES")
    write_bvh()
    build("starter")
    L.save(os.path.join(CH, "STARTER_FILES", "ch07_14_mocap_starter.blend"))
    for k in ("not_cleaned", "over_smoothed", "kept_spikes", "too_many_keys", "linear_keys", "raw_modified"):
        build(k)
        L.save(os.path.join(out, "COUNTER_EXAMPLES", f"ch07_14_mocap_{k}.blend"))
    build("solution")
    L.save(os.path.join(out, "ch07_14_mocap_solution.blend"))
    sketch(os.path.join(out, "ch07_14_mocap_reference.png"))


if __name__ == "__main__":
    L.run(main)
