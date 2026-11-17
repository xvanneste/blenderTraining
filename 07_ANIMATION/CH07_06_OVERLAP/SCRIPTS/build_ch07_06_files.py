"""
build_ch07_06_files.py — « Arcs, overlap, follow-through » (CH07.06 : une antenne souple, quatre bones en chaîne).

RIG_Antenna : base (0 → 0,4 m), tail_1 (0,4 → 0,8), tail_2 (0,8 → 1,2), tail_3 (1,2 → 1,6) en chaîne verticale ; rotation X locale (la chaîne se plie d'avant en arrière).
  Solution (rotation X en degrés, 24 i/s, plage 1–48) :
    base   : 1 : 0 ; 13 : +25 ; 25 : 0 ; 48 : 0                       (le mouvement principal : un aller-retour)
    tail_1 : 1 : 0 ; 15 : +18 ; 27 : 0 ; 48 : 0                       (retard de 2 images)
    tail_2 : 1 : 0 ; 17 : +14 ; 29 : 0 ; 48 : 0                       (retard de 4 images)
    tail_3 : 1 : 0 ; 19 : +10 ; 31 : 0 ; 35 : −6 ; 44 : 0 ; 48 : 0    (retard de 6 images, FOLLOW-THROUGH : continue après l'arrêt de la base, dépasse le repos puis se stabilise)
  STARTER_FILES/ch07_06_overlap_starter.blend : seule la base est animée ; les trois bones de queue sont immobiles.
  COMPLETED_EXAMPLES/ch07_06_overlap_solution.blend (+ _reference.png : courbes d'angle des quatre bones et trajectoire de la pointe)
  COUNTER_EXAMPLES/ : no_overlap, too_late, no_followthrough, no_overshoot, no_settle, stiff
Usage : blender -b --factory-startup --python-exit-code 1 --python build_ch07_06_files.py
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
NAMES = ("base", "tail_1", "tail_2", "tail_3")
KEYS = {
    "base": [(1, 0), (13, 25), (25, 0), (48, 0)],
    "tail_1": [(1, 0), (15, 18), (27, 0), (48, 0)],
    "tail_2": [(1, 0), (17, 14), (29, 0), (48, 0)],
    "tail_3": [(1, 0), (19, 10), (31, 0), (35, -6), (44, 0), (48, 0)],
}
NOTE = """CH07.06 — ARCS, OVERLAP, FOLLOW-THROUGH (RIG_Antenna)
La base de l'antenne fait un aller-retour (rotation X : 0 → +25° à l'image 13 → 0 à l'image 25). Les trois bones de queue sont immobiles : l'antenne est raide. Animez-les en cascade :
1. OVERLAP : chaque bone atteint son maximum un peu APRÈS son parent : tail_1 à l'image 15 (+18°), tail_2 à 17 (+14°), tail_3 à 19 (+10°). Retard de 2 images par bone.
2. FOLLOW-THROUGH : la queue continue quand la base s'arrête (image 25) : tail_3 revient à 0 à l'image 31, dépasse (−6° à l'image 35) puis se stabilise à 0 à l'image 44 ; tail_1 et tail_2 reviennent à 0 aux images 27 et 29.
3. Tout est au repos (0°) à l'image 48. Plage 1–48.
4. ARC : la pointe suit une courbe, pas une droite (vérifié sur sa trajectoire).
Le correcteur lit les angles évalués image par image : retards, suite du mouvement, dépassement, repos final, courbure de la trajectoire.
Vérification : SCRIPTS/validate_ch07_06.py -- --exercise overlap
"""


def make(kind):
    L.reset("SC_OVERLAP")
    sc = bpy.context.scene
    sc.render.fps = 24
    sc.frame_start, sc.frame_end = 1, 48
    arm = bpy.data.armatures.new("ARM_Antenna")
    rig = bpy.data.objects.new("RIG_Antenna", arm)
    bpy.context.scene.collection.objects.link(rig)
    bpy.context.view_layer.objects.active = rig
    rig.select_set(True)
    bpy.ops.object.mode_set(mode="EDIT")
    prev = None
    for i, n in enumerate(NAMES):
        b = arm.edit_bones.new(n)
        b.head, b.tail = Vector((0, 0, 0.4 * i)), Vector((0, 0, 0.4 * (i + 1)))
        if prev:
            b.parent = prev
            b.use_connect = True
        prev = b
    bpy.ops.object.mode_set(mode="POSE")
    pb = rig.pose.bones
    for n in NAMES:
        pb[n].rotation_mode = "XYZ"
    keys = {k: list(v) for k, v in KEYS.items()}
    if kind == "starter":
        keys = {"base": keys["base"]}
    elif kind == "no_overlap":
        keys = {"base": KEYS["base"], "tail_1": [(1, 0), (13, 18), (25, 0), (48, 0)], "tail_2": [(1, 0), (13, 14), (25, 0), (48, 0)], "tail_3": [(1, 0), (13, 10), (25, 0), (35, -6), (44, 0), (48, 0)]}
    elif kind == "too_late":
        keys = {"base": KEYS["base"], "tail_1": [(1, 0), (19, 18), (31, 0), (48, 0)], "tail_2": [(1, 0), (25, 14), (37, 0), (48, 0)], "tail_3": [(1, 0), (31, 10), (43, 0), (48, 0)]}
    elif kind == "no_followthrough":
        keys = {"base": KEYS["base"], "tail_1": [(1, 0), (15, 18), (25, 0), (48, 0)], "tail_2": [(1, 0), (17, 14), (25, 0), (48, 0)], "tail_3": [(1, 0), (19, 10), (25, 0), (35, -6), (44, 0), (48, 0)]}
    elif kind == "no_overshoot":
        keys["tail_3"] = [(1, 0), (19, 10), (31, 0), (48, 0)]
    elif kind == "no_settle":
        keys["tail_3"] = [(1, 0), (19, 10), (31, 0), (35, -6), (44, 5), (48, 5)]
    elif kind == "stiff":
        keys = {"base": KEYS["base"], "tail_1": [(1, 0), (48, 0)], "tail_2": [(1, 0), (48, 0)], "tail_3": [(1, 0), (48, 0)]}
    for n, kl in keys.items():
        for f, a in kl:
            pb[n].rotation_euler = (math.radians(a), 0, 0)
            pb[n].keyframe_insert("rotation_euler", index=0, frame=f)
        pb[n].rotation_euler = (0, 0, 0)
    bpy.ops.object.mode_set(mode="OBJECT")
    rig.show_in_front = True
    sc.frame_set(1)
    L.instructions(NOTE)
    return rig


def angles(rig):
    sc = bpy.context.scene
    out = {n: [] for n in NAMES}
    tip = []
    for f in range(1, 49):
        sc.frame_set(f)
        bpy.context.view_layer.update()
        for n in NAMES:
            out[n].append(math.degrees(rig.pose.bones[n].rotation_euler.x))
        tip.append(rig.matrix_world @ rig.pose.bones["tail_3"].tail)
    return out, tip


def sketch(path):
    rig = make("solution")
    ang, tip = angles(rig)
    W, H = 780, 340
    img = np.full((H, W, 3), 0.08, np.float32)
    cols = {"base": (0.85, 0.85, 0.85), "tail_1": (0.9, 0.55, 0.2), "tail_2": (0.3, 0.8, 0.5), "tail_3": (0.3, 0.7, 1.0)}
    y0 = 150
    img[y0, 20:W - 20] = (0.25, 0.25, 0.25)
    for n in NAMES:
        for f in range(48):
            x, y = int(20 + f / 47 * 460), int(y0 - ang[n][f] / 30 * 120)
            img[y - 1:y + 2, x - 1:x + 2] = cols[n]
    for f in (13, 15, 17, 19):
        img[20:300, int(20 + (f - 1) / 47 * 460)] = (0.2, 0.2, 0.2)
    for i, p in enumerate(tip):                                          # trajectoire de la pointe (y, z), à droite
        x, y = int(640 + p.y * 160), int(300 - p.z * 150)
        img[y - 2:y + 3, x - 2:x + 3] = (0.3, 0.7, 1.0)
    rgba = np.concatenate([img, np.ones(img.shape[:2] + (1,), np.float32)], axis=2)
    out = bpy.data.images.new("sk", W, H)
    out.pixels = rgba[::-1].ravel()
    out.filepath_raw = path
    out.file_format = "PNG"
    out.save()


def main():
    out = os.path.join(CH, "COMPLETED_EXAMPLES")
    make("starter")
    L.save(os.path.join(CH, "STARTER_FILES", "ch07_06_overlap_starter.blend"))
    for k in ("no_overlap", "too_late", "no_followthrough", "no_overshoot", "no_settle", "stiff"):
        make(k)
        L.save(os.path.join(out, "COUNTER_EXAMPLES", f"ch07_06_overlap_{k}.blend"))
    make("solution")
    L.save(os.path.join(out, "ch07_06_overlap_solution.blend"))
    sketch(os.path.join(out, "ch07_06_overlap_reference.png"))


if __name__ == "__main__":
    L.run(main)
