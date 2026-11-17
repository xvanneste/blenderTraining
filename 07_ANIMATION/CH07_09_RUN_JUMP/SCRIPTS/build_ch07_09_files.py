"""
build_ch07_09_files.py — « Course, saut, interactions » (CH07.09 : un saut crédible en 40 images).

Le mannequin FK de CH07.07/08 (CHR_Mannequin, RIG_Mannequin) saute SUR PLACE : anticipation (flexion), impulsion, vol parabolique, réception amortie, retour debout. 24 i/s, plage 1–40.
  Solution (calculée par script, IK analytique des jambes ; hanches = bone « hips » en position Z) :
    images 1–4 : debout (hanches 0,95 m) ; 4 → 8 : flexion jusqu'à 0,65 m (ANTICIPATION) ; 8 → 10 : impulsion jusqu'à 0,95 m (décollage à l'image 10 : les pieds quittent le sol) ;
    10 → 24 : VOL de 14 images, parabole sous gravité (g = 0,01703 m/image²) : sommet 1,367 m à l'image 17 (0,417 m au-dessus du décollage) ; contact à l'image 24 ;
    24 → 28 : réception AMORTIE jusqu'à 0,68 m ; 28 → 36 : retour debout (0,95 m) ; 36–40 : debout.
    chevilles : au sol (z = 0,05 m) hors du vol ; en vol z = hanches − e, e passant de 0,90 m à 0,78 m (images 10–12) puis de 0,78 à 0,90 (22–24) ; bras : balancement arrière puis levée.
  STARTER_FILES/ch07_09_jump_starter.blend : mannequin debout, sans animation. COMPLETED_EXAMPLES/ch07_09_jump_solution.blend (+ _reference.png : courbe de hauteur des hanches et des chevilles)
  COUNTER_EXAMPLES/ : no_anticipation, no_landing, floaty, too_low, feet_slide, no_return
Usage : blender -b --factory-startup --python-exit-code 1 --python build_ch07_09_files.py
Testé avec : Blender 5.3.0.
"""
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "SCRIPTS"))
sys.path.insert(0, os.path.join(HERE, "..", "..", "CH07_08_WALK", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import build_ch07_08_files as W  # noqa: E402  (mannequin, IK, orientation des bones)
import bpy  # noqa: E402
import numpy as np  # noqa: E402
from mathutils import Matrix, Vector  # noqa: E402

CH = L.chapter_dir(__file__)
G_FRAME = 9.81 / 576.0
NOTE = """CH07.09 — SAUT (CHR_Mannequin, RIG_Mannequin)
Le mannequin doit sauter sur place en 40 images (24 images par seconde, plage 1–40) :
1. ANTICIPATION : debout (hanches 0,95 m) jusqu'à l'image 4, puis il fléchit jusqu'à 0,65 m à l'image 8.
2. IMPULSION : il se redresse et décolle à l'image 10 (hanches 0,95 m, pieds qui quittent le sol).
3. VOL : 14 images (contact à l'image 24) ; les hanches suivent une PARABOLE (sommet 1,37 m à l'image 17, soit 0,42 m au-dessus du décollage) ; pieds sans glissement avant et après.
4. RÉCEPTION : il amortit (hanches à 0,68 m à l'image 28), puis revient debout (0,95 m) à l'image 36 ; plage jusqu'à 40.
Le correcteur mesure les hanches (bone hips) et les chevilles sur les 40 images : flexion, durée du vol, hauteur, gravité, amortissement, pieds plantés, retour debout.
Vérification : SCRIPTS/validate_ch07_09.py -- --exercise jump
"""


def smooth(a, b, f0, f1, f):
    u = max(0.0, min(1.0, (f - f0) / (f1 - f0)))
    u = u * u * (3 - 2 * u)
    return a + (b - a) * u


def hips_z(f, kind):
    crouch = 0.65 if kind != "no_anticipation" else 0.95
    land = 0.68 if kind != "no_landing" else 0.95
    T = 14
    apex = {"too_low": 0.12}.get(kind, 0.4166)
    if kind == "floaty":
        T = 22
    g = 8 * apex / (T * T)                                       # gravité effective (h = g·T²/8)
    t_off, t_land = 10, 10 + T
    if f <= 4:
        return 0.95
    if f <= 8:
        return smooth(0.95, crouch, 4, 8, f)
    if f <= t_off:
        return smooth(crouch, 0.95, 8, t_off, f)
    if f <= t_land:
        v = g * T / 2
        return 0.95 + v * (f - t_off) - 0.5 * g * (f - t_off) ** 2
    t1 = t_land + 4
    if f <= t1:
        return smooth(0.95, land, t_land, t1, f)
    if f <= t1 + 8:
        return smooth(land, 0.95, t1, t1 + 8, f)
    return 0.95


def ext(f, kind):
    T = 22 if kind == "floaty" else 14
    t_off, t_land = 10, 10 + T
    if f <= t_off or f >= t_land:
        return 0.90
    if f <= t_off + 2:
        return smooth(0.90, 0.78, t_off, t_off + 2, f)
    if f >= t_land - 2:
        return smooth(0.78, 0.90, t_land - 2, t_land, f)
    return 0.78


def pose_frame(rig, f, kind):
    pb = rig.pose.bones
    zh = hips_z(f, kind)
    pb["hips"].matrix = Matrix.Translation((0, 0, zh - 0.95)) @ pb["hips"].bone.matrix_local
    bpy.context.view_layer.update()
    drift = 0.0
    if kind == "feet_slide" and (f <= 9 or f >= 26):
        drift = 0.12 * math.sin(math.pi * (f % 8) / 8.0)             # les pieds glissent au sol
    for side in ("L", "R"):
        x = 0.10 if side == "L" else -0.10
        az = max(W.ANK, zh - ext(f, kind)) if (10 < f < 24) else W.ANK
        if kind == "floaty" and 10 < f < 32:
            az = max(W.ANK, zh - ext(f, kind))
        ank = Vector((x, drift, az))
        hip = Vector((x, 0, zh))
        knee = W.leg_ik(hip, ank)
        W.set_dir(pb["thigh." + side], hip, knee - hip)
        bpy.context.view_layer.update()
        W.set_dir(pb["shin." + side], knee, ank - knee)
        bpy.context.view_layer.update()
    # bras : abaissés ; balancement arrière pendant la flexion, levée au décollage
    sw = {1: 0, 4: 0, 8: 40, 10: -60, 17: -70, 24: -20, 28: 25, 36: 0, 40: 0}
    ks = sorted(sw)
    a = sw[ks[0]]
    for i in range(len(ks) - 1):
        if ks[i] <= f <= ks[i + 1]:
            a = smooth(sw[ks[i]], sw[ks[i + 1]], ks[i], ks[i + 1], f)
    for side in ("L", "R"):
        pa, pf = pb["upper_arm." + side], pb["fore." + side]
        d = Vector((0, math.sin(math.radians(a)), -math.cos(math.radians(a))))
        W.set_dir(pa, Vector(pa.bone.head_local), d)
        bpy.context.view_layer.update()
        W.set_dir(pf, Vector(pa.tail), d)
        bpy.context.view_layer.update()


def build(kind):
    L.reset("SC_JUMP")
    sc = bpy.context.scene
    sc.render.fps = 24
    sc.frame_start, sc.frame_end = 1, 40
    body = W.make_body()
    rig = W.make_rig()
    m = body.modifiers.new("Armature", "ARMATURE")
    m.object = rig
    body.parent = rig
    for n in rig.pose.bones.keys():
        rig.pose.bones[n].rotation_mode = "XYZ"
    if kind == "starter":
        for side in ("L", "R"):
            pa = rig.pose.bones["upper_arm." + side]
            W.set_dir(pa, Vector(pa.bone.head_local), Vector((0, 0, -1)))
            bpy.context.view_layer.update()
            pf = rig.pose.bones["fore." + side]
            W.set_dir(pf, Vector(pa.tail), Vector((0, 0, -1)))
            bpy.context.view_layer.update()
    else:
        end = 36 if kind == "no_return" else 40
        for f in range(1, 41):
            pose_frame(rig, f if kind != "no_return" or f <= 30 else 30, kind)
            for n in rig.pose.bones.keys():
                pb = rig.pose.bones[n]
                pb.keyframe_insert("rotation_euler", frame=f)
                if n == "hips":
                    pb.keyframe_insert("location", frame=f)
        sc.frame_set(1)
    L.instructions(NOTE)
    return body, rig


def sketch(path):
    body, rig = build("solution")
    sc = bpy.context.scene
    Wd, H = 800, 300
    img = np.full((H, Wd, 3), 0.08, np.float32)

    def px(f, z):
        return int(20 + (f - 1) / 39 * (Wd - 40)), int(H - 20 - z / 1.5 * (H - 40))
    img[H - 20 - int(0.05 / 1.5 * (H - 40)), 20:Wd - 20] = (0.25, 0.25, 0.25)
    for f in range(1, 41):
        sc.frame_set(f)
        bpy.context.view_layer.update()
        hz = rig.pose.bones["hips"].head.z
        az = rig.pose.bones["shin.L"].tail.z
        for z, col in ((hz, (0.9, 0.55, 0.2)), (az, (0.3, 0.7, 1.0))):
            x, y = px(f, z)
            img[y - 3:y + 4, x - 3:x + 4] = col
    for f in (4, 8, 10, 17, 24, 28, 36):
        x = px(f, 0)[0]
        img[10:H - 10, x] = (0.2, 0.2, 0.2)
    rgba = np.concatenate([img, np.ones(img.shape[:2] + (1,), np.float32)], axis=2)
    out = bpy.data.images.new("sk", Wd, H)
    out.pixels = rgba[::-1].ravel()
    out.filepath_raw = path
    out.file_format = "PNG"
    out.save()


def main():
    out = os.path.join(CH, "COMPLETED_EXAMPLES")
    build("starter")
    L.save(os.path.join(CH, "STARTER_FILES", "ch07_09_jump_starter.blend"))
    for k in ("no_anticipation", "no_landing", "floaty", "too_low", "feet_slide", "no_return"):
        build(k)
        L.save(os.path.join(out, "COUNTER_EXAMPLES", f"ch07_09_jump_{k}.blend"))
    build("solution")
    L.save(os.path.join(out, "ch07_09_jump_solution.blend"))
    sketch(os.path.join(out, "ch07_09_jump_reference.png"))


if __name__ == "__main__":
    L.run(main)
