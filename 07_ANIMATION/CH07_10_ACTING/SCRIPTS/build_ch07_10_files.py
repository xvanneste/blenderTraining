"""
build_ch07_10_files.py — « Acting » (CH07.10 : un plan d'acting muet : intention, temps de pensée, anticipation).

Le mannequin FK (CHR_Mannequin, RIG_Mannequin) joue une petite scène muette de 72 images (24 i/s, plage 1–72) : il REMARQUE quelque chose sur sa gauche, y réfléchit, puis se prépare à agir.
  Solution (rotations monde calculées par script, une clé par image) :
    1–19 : immobile (idle) ;
    REMARQUE : la tête tourne vite (de l'image 20 à 27, 0 → 55° autour de Z) ; le corps SUIT avec retard : le buste tourne de l'image 24 à 38 (0 → 30°), les hanches de l'image 28 à 44 (0 → 15°) ;
    TEMPS DE PENSÉE : maintien de la tête de l'image 27 à 45 (la tête ne bouge presque plus : ± 1°) ;
    ANTICIPATION : de 44 à 50 la colonne se penche en ARRIÈRE (−8°), puis ACTION : de 50 à 58 elle se penche vers l'AVANT (+14°) ; retour à +6° à l'image 72.
  Rotations : lacet autour de l'axe Z monde, inclinaison avant/arrière autour de l'axe X monde (positif : vers l'avant, −Y).
  STARTER_FILES/ch07_10_acting_starter.blend : mannequin immobile, sans animation. COMPLETED_EXAMPLES/ch07_10_acting_solution.blend (+ _reference.png : courbes de lacet de la tête, du buste et des hanches et inclinaison de la colonne)
  COUNTER_EXAMPLES/ : no_hold, no_lag, no_anticipation, no_idle, too_slow, small_turn
Usage : blender -b --factory-startup --python-exit-code 1 --python build_ch07_10_files.py
Testé avec : Blender 5.3.0.
"""
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "SCRIPTS"))
sys.path.insert(0, os.path.join(HERE, "..", "..", "CH07_08_WALK", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import build_ch07_08_files as W  # noqa: E402  (mannequin)
import bpy  # noqa: E402
import numpy as np  # noqa: E402
from mathutils import Matrix, Vector  # noqa: E402

CH = L.chapter_dir(__file__)
NOTE = """CH07.10 — ACTING MUET (CHR_Mannequin, RIG_Mannequin)
Une scène de 72 images (24 i/s, plage 1–72) : le personnage remarque quelque chose à sa gauche, y réfléchit, puis se prépare à agir.
1. IDLE : immobile jusqu'à l'image 19 (aucun bone ne bouge de plus de 2°).
2. REMARQUE : la tête tourne VITE (images 20 à 27, jusqu'à 55° autour de Z) ; le corps SUIT avec retard : le buste commence quelques images après la tête (images 24 à 38, jusqu'à 30°), les hanches encore après (28 à 44, jusqu'à 15°).
3. TEMPS DE PENSÉE : la tête reste fixe de l'image 27 à 45 (± 3°) : on lit la pensée.
4. ANTICIPATION puis ACTION : la colonne se penche en ARRIÈRE de 8° au moins (image 50), puis vers l'AVANT de 8° au moins (image 58).
Le correcteur mesure le lacet de la tête, du buste et des hanches (axe Z) et l'inclinaison de la colonne sur les 72 images : repos initial, vitesse de la tête, retard du corps, maintien, anticipation.
Vérification : SCRIPTS/validate_ch07_10.py -- --exercise acting
"""


def smooth(a, b, f0, f1, f):
    u = max(0.0, min(1.0, (f - f0) / (f1 - f0)))
    u = u * u * (3 - 2 * u)
    return a + (b - a) * u


def curves(f, kind):
    hd0, hd1 = (5, 12) if kind == "no_idle" else ((20, 40) if kind == "too_slow" else (20, 27))
    amp = 20.0 if kind == "small_turn" else 55.0
    head = smooth(0, amp, hd0, hd1, f)
    if kind == "no_hold" and f > 27:
        head += smooth(0, 15, 27, 45, f)                           # la tête dérive pendant le temps de pensée
    chest = smooth(0, 30, 24 if kind != "no_lag" else hd0, 38 if kind != "no_lag" else hd1, f)
    hips = smooth(0, 15, 28 if kind != "no_lag" else hd0, 44 if kind != "no_lag" else hd1, f)
    pitch = 0.0
    if f > 44:
        pitch = smooth(0, -8 if kind != "no_anticipation" else 0, 44, 50, f)
        if f > 50:
            pitch = smooth(-8 if kind != "no_anticipation" else 0, 14, 50, 58, f)
        if f > 58:
            pitch = smooth(14, 6, 58, 72, f)
    return head, chest, hips, pitch


def pose_frame(rig, f, kind):
    pb = rig.pose.bones
    for b in pb:
        b.matrix_basis = Matrix()
    bpy.context.view_layer.update()
    head, chest, hips, pitch = curves(f, kind)

    def rot(name, axis, deg):
        b = pb[name]
        bpy.context.view_layer.update()
        h = Vector(b.head)
        b.matrix = Matrix.Translation(h) @ Matrix.Rotation(math.radians(deg), 4, axis) @ Matrix.Translation(-h) @ b.matrix
        bpy.context.view_layer.update()
    rot("hips", "Z", hips)
    rot("spine", "X", pitch)
    rot("chest", "Z", chest - hips)
    rot("head", "Z", head - chest)
    for side in ("L", "R"):
        pa, pf = pb["upper_arm." + side], pb["fore." + side]
        W.set_dir(pa, Vector(pa.head), Vector((0, 0, -1)))
        bpy.context.view_layer.update()
        W.set_dir(pf, Vector(pa.tail), Vector((0, 0, -1)))
        bpy.context.view_layer.update()


def build(kind):
    L.reset("SC_ACTING")
    sc = bpy.context.scene
    sc.render.fps = 24
    sc.frame_start, sc.frame_end = 1, 72
    body = W.make_body()
    rig = W.make_rig()
    m = body.modifiers.new("Armature", "ARMATURE")
    m.object = rig
    body.parent = rig
    for n in rig.pose.bones.keys():
        rig.pose.bones[n].rotation_mode = "XYZ"
    for side in ("L", "R"):                                    # bras le long du corps
        pa, pf = rig.pose.bones["upper_arm." + side], rig.pose.bones["fore." + side]
        W.set_dir(pa, Vector(pa.bone.head_local), Vector((0, 0, -1)))
        bpy.context.view_layer.update()
        W.set_dir(pf, Vector(pa.tail), Vector((0, 0, -1)))
        bpy.context.view_layer.update()
    if kind != "starter":
        for f in range(1, 73):
            pose_frame(rig, f, kind)
            for n in rig.pose.bones.keys():
                rig.pose.bones[n].keyframe_insert("rotation_euler", frame=f)
        sc.frame_set(1)
    L.instructions(NOTE)
    return body, rig


def sketch(path):
    build("solution")
    Wd, H = 800, 320
    img = np.full((H, Wd, 3), 0.08, np.float32)
    img[160, 20:Wd - 20] = (0.25, 0.25, 0.25)
    for f in range(1, 73):
        head, chest, hips, pitch = curves(f, "solution")
        x = int(20 + (f - 1) / 71 * (Wd - 40))
        for v, col in ((head, (0.9, 0.55, 0.2)), (chest, (0.3, 0.8, 0.5)), (hips, (0.3, 0.7, 1.0)), (pitch, (0.9, 0.9, 0.9))):
            y = int(160 - v / 60 * 140)
            img[y - 2:y + 3, x - 2:x + 3] = col
    for f in (20, 27, 45, 50, 58):
        img[10:H - 10, int(20 + (f - 1) / 71 * (Wd - 40))] = (0.2, 0.2, 0.2)
    rgba = np.concatenate([img, np.ones(img.shape[:2] + (1,), np.float32)], axis=2)
    out = bpy.data.images.new("sk", Wd, H)
    out.pixels = rgba[::-1].ravel()
    out.filepath_raw = path
    out.file_format = "PNG"
    out.save()


def main():
    out = os.path.join(CH, "COMPLETED_EXAMPLES")
    build("starter")
    L.save(os.path.join(CH, "STARTER_FILES", "ch07_10_acting_starter.blend"))
    for k in ("no_hold", "no_lag", "no_anticipation", "no_idle", "too_slow", "small_turn"):
        build(k)
        L.save(os.path.join(out, "COUNTER_EXAMPLES", f"ch07_10_acting_{k}.blend"))
    build("solution")
    L.save(os.path.join(out, "ch07_10_acting_solution.blend"))
    sketch(os.path.join(out, "ch07_10_acting_reference.png"))


if __name__ == "__main__":
    L.run(main)
