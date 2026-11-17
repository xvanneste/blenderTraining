"""
build_ch07_13_files.py — « Animation non linéaire » (CH07.13 : NLA, strips, répétition, fondu).

Une caisse GEO_Crate et deux ACTIONS (interpolation linéaire, 24 images chacune) :
  « Slide » : position X de 0 (image 1) à 4 (image 25) ; « Spin » : rotation Z de 0° (image 1) à 180° (image 25).
  Solution : l'animation est montée dans l'éditeur NLA, sans action active :
    piste « Move » : un strip « Slide » à partir de l'image 1, répété 2 fois (repeat = 2) : images 1 à 49 ;
    piste « Spin » : un strip « Spin » à partir de l'image 13 (images 13 à 37), fondu d'entrée de 6 images (blend_in = 6) ;
    plage de la scène : 1–49 à 24 i/s.
  Mesures de la solution : X(13) = 2 ; X(30) = 0,833 ; X(37) = 2 (deuxième passage de l'action) ; rotation : 0° (image 13), 11,25° environ (image 16, fondu), 90° (image 25), 180° (image 37).
  STARTER_FILES/ch07_13_nla_starter.blend : la caisse avec l'action Slide ACTIVE ; l'action Spin conservée (utilisateur fictif) ; aucun montage NLA ; plage 1–25.
  COMPLETED_EXAMPLES/ch07_13_nla_solution.blend (+ _reference.png : l'éditeur NLA en numpy : deux pistes, strips, répétition, fondu)
  COUNTER_EXAMPLES/ : no_repeat, late_spin, no_blend, active_action, missing_spin_track, wrong_scale
Usage : blender -b --factory-startup --python-exit-code 1 --python build_ch07_13_files.py
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
NOTE = """CH07.13 — ANIMATION NON LINÉAIRE (GEO_Crate)
La caisse a deux actions : « Slide » (X de 0 à 4 en 24 images) et « Spin » (rotation Z de 0° à 180° en 24 images). Montez-les dans l'éditeur NLA :
1. « Slide » est ACTIVE : poussez-la dans une piste NLA (Push Down) : piste « Move », strip « Slide » à l'image 1 ; mettez Repeat à 2 : le strip couvre les images 1 à 49. Plus aucune action active.
2. Nouvelle piste « Spin » avec l'action « Spin » : strip à l'image 13 (images 13 à 37) ; fondu d'entrée (Blend In) de 6 images.
3. Plage de la scène : 1–49.
Le correcteur lit les pistes, les strips (action, début, fin, répétition, fondu) et l'animation évaluée : X(13) = 2, X(30) = 0,83, X(37) = 2 (deuxième passage), rotation 90° à l'image 25 et 180° à l'image 37, fondu à l'image 16.
Vérification : SCRIPTS/validate_ch07_13.py -- --exercise nla
"""


def fcurves(act):
    try:
        return list(act.fcurves)
    except AttributeError:
        return [f for l in act.layers for st in l.strips for cb in st.channelbags for f in cb.fcurves]


def make_actions(ob):
    for f, x in ((1, 0.0), (25, 4.0)):
        ob.location = (x, 0, 0)
        ob.keyframe_insert("location", index=0, frame=f)
    a1 = ob.animation_data.action
    a1.name = "Slide"
    a1.use_fake_user = True
    ob.animation_data.action = None
    ob.location = (0, 0, 0)
    for f, a in ((1, 0.0), (25, 180.0)):
        ob.rotation_euler = (0, 0, math.radians(a))
        ob.keyframe_insert("rotation_euler", index=2, frame=f)
    a2 = ob.animation_data.action
    a2.name = "Spin"
    a2.use_fake_user = True
    ob.animation_data.action = None
    ob.rotation_euler = (0, 0, 0)
    for a in (a1, a2):
        for fc in fcurves(a):
            for kp in fc.keyframe_points:
                kp.interpolation = "LINEAR"
    return a1, a2


def build(kind):
    L.reset("SC_NLA")
    sc = bpy.context.scene
    sc.render.fps = 24
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    bmesh.ops.translate(bm, verts=bm.verts, vec=(0, 0, 0.5))
    me = bpy.data.meshes.new("ME_Crate")
    bm.to_mesh(me)
    bm.free()
    ob = bpy.data.objects.new("GEO_Crate", me)
    sc.collection.objects.link(ob)
    a1, a2 = make_actions(ob)
    ad = ob.animation_data
    if kind == "starter":
        ad.action = a1
        sc.frame_start, sc.frame_end = 1, 25
        L.instructions(NOTE)
        return ob
    sc.frame_start, sc.frame_end = 1, 49
    t1 = ad.nla_tracks.new()
    t1.name = "Move"
    s1 = t1.strips.new("Slide", 1, a1)
    if kind != "no_repeat":
        s1.repeat = 2
    if kind != "missing_spin_track":
        t2 = ad.nla_tracks.new()
        t2.name = "Spin"
        s2 = t2.strips.new("Spin", 1 if kind == "late_spin" else 13, a2)
        if kind == "wrong_scale":
            s2.scale = 0.5
        s2.blend_in = 0.0 if kind == "no_blend" else 6.0
    if kind == "active_action":
        ad.action = a1
        ad.action_slot = a1.slots[0]
    else:
        ad.action = None
    sc.frame_set(1)
    L.instructions(NOTE)
    return ob


def sketch(path):
    ob = build("solution")
    Wd, H = 780, 260
    img = np.full((H, Wd, 3), 0.08, np.float32)

    def fx(f):
        return int(30 + (f - 1) / 48 * (Wd - 60))
    for f in (1, 13, 25, 37, 49):
        img[10:H - 10, fx(f)] = (0.22, 0.22, 0.22)
    # piste Move : un strip de 1 à 49 avec séparateur à 25 (répétition)
    img[40:90, fx(1):fx(49)] = (0.3, 0.55, 0.3)
    img[40:90, fx(25) - 1:fx(25) + 2] = (0.1, 0.1, 0.1)
    # piste Spin : strip 13–37 avec rampe de fondu (6 images)
    img[130:180, fx(13):fx(37)] = (0.55, 0.4, 0.2)
    for i in range(fx(13), fx(19)):
        k = (i - fx(13)) / max(fx(19) - fx(13), 1)
        img[130:180, i] = (0.55 * k + 0.08 * (1 - k), 0.4 * k + 0.08 * (1 - k), 0.2 * k + 0.08 * (1 - k))
    rgba = np.concatenate([img, np.ones(img.shape[:2] + (1,), np.float32)], axis=2)
    out = bpy.data.images.new("sk", Wd, H)
    out.pixels = rgba[::-1].ravel()
    out.filepath_raw = path
    out.file_format = "PNG"
    out.save()


def main():
    out = os.path.join(CH, "COMPLETED_EXAMPLES")
    build("starter")
    L.save(os.path.join(CH, "STARTER_FILES", "ch07_13_nla_starter.blend"))
    for k in ("no_repeat", "late_spin", "no_blend", "active_action", "missing_spin_track", "wrong_scale"):
        build(k)
        L.save(os.path.join(out, "COUNTER_EXAMPLES", f"ch07_13_nla_{k}.blend"))
    build("solution")
    L.save(os.path.join(out, "ch07_13_nla_solution.blend"))
    sketch(os.path.join(out, "ch07_13_nla_reference.png"))


if __name__ == "__main__":
    L.run(main)
