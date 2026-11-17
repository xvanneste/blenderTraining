"""
build_ch07_01_files.py — « Les 12 principes » (CH07.01 : squash & stretch, anticipation, volume constant, pivot au contact).

Une balle GEO_Ball (sphère de rayon 0,5 m dont l'ORIGINE est à sa base : z de 0 à 1 m) fait un saut en place, 40 images à 24 i/s :
  images clés de position (déjà dans le starter) : 1 sol, 8 décollage (sol), 18 sommet (z = 2,0 m), 28 atterrissage (sol), 40 repos.
  Solution : images clés d'ÉCHELLE (sx = sy = 1 / √sz : volume constant) : 1 : sz 1 ; 5 : sz 0,72 (ANTICIPATION, écrasée) ; 8 : sz 1,35 (étirée au décollage) ; 13 : sz 1,25 ;
             18 : sz 1 (sommet, forme neutre) ; 23 : sz 1,2 ; 28 : sz 0,6 (CONTACT : écrasée) ; 32 : sz 1,1 (rebond) ; 40 : sz 1.
  STARTER_FILES/ch07_01_principles_starter.blend : le saut sans déformation (position seule).
  COMPLETED_EXAMPLES/ch07_01_principles_solution.blend (+ _reference.png : neuf images du saut, silhouettes)
  COUNTER_EXAMPLES/ : no_squash, no_anticipation, no_stretch, volume_break, floating, no_settle
Usage : blender -b --factory-startup --python-exit-code 1 --python build_ch07_01_files.py
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
LOC = {1: 0.0, 8: 0.0, 18: 2.0, 28: 0.0, 40: 0.0}
SZ = {1: 1.0, 5: 0.72, 8: 1.35, 13: 1.25, 18: 1.0, 23: 1.2, 28: 0.6, 32: 1.1, 40: 1.0}
NOTE = """CH07.01 — LES 12 PRINCIPES : squash & stretch, anticipation (GEO_Ball)
La balle saute (position déjà animée : décollage image 8, sommet image 18, atterrissage image 28). Son ORIGINE est à sa base : elle se déforme à partir du sol.
1. Image 1 : échelle (1, 1, 1) — clé.
2. ANTICIPATION : image 5, la balle s'écrase avant de partir (Scale Z ≈ 0,72).
3. STRETCH : image 8 (décollage), étirée (Scale Z ≈ 1,35) ; reste étirée en vol (images 13 et 23).
4. Image 18 (sommet) : forme neutre. Image 28 (contact) : écrasée (Scale Z ≈ 0,6). Image 32 : petit rebond (Scale Z ≈ 1,1). Image 40 : repos.
5. VOLUME CONSTANT : Scale X = Scale Y = 1 / √(Scale Z) à chaque clé (une balle écrasée s'élargit, étirée s'affine).
Le correcteur lit l'animation évaluée : contact au sol, anticipation, étirement, volume, sommet neutre, contact écrasé, repos final.
Vérification : SCRIPTS/validate_ch07_01.py -- --exercise principles
"""


def make_ball(centered=False):
    bm = bmesh.new()
    bmesh.ops.create_uvsphere(bm, u_segments=32, v_segments=16, radius=0.5)
    if not centered:
        bmesh.ops.translate(bm, verts=bm.verts, vec=(0, 0, 0.5))
    me = bpy.data.meshes.new("ME_Ball")
    bm.to_mesh(me)
    bm.free()
    for p in me.polygons:
        p.use_smooth = True
    ob = bpy.data.objects.new("GEO_Ball", me)
    bpy.context.scene.collection.objects.link(ob)
    return ob


def build(kind):
    L.reset("SC_PRINCIPLES")
    sc = bpy.context.scene
    sc.render.fps = 24
    sc.frame_start, sc.frame_end = 1, 40
    ob = make_ball(centered=(kind == "floating"))
    off = 0.5 if kind == "floating" else 0.0
    for f, z in LOC.items():
        ob.location = (0, 0, z + off)
        ob.keyframe_insert("location", frame=f)
    if kind != "starter":
        for f, sz in SZ.items():
            k = sz
            if kind == "no_squash":
                k = 1.0
            elif kind == "no_anticipation" and f == 5:
                k = 1.0
            elif kind == "no_stretch" and f in (8, 13, 23):
                k = 1.0
            elif kind == "no_settle" and f in (32, 40):
                k = 1.25 if f == 40 else 1.1
            sx = 1.0 / math.sqrt(k)
            if kind == "volume_break":
                sx = 1.0
            ob.scale = (sx, sx, k)
            ob.keyframe_insert("scale", frame=f)
    sc.frame_set(1)
    L.instructions(NOTE)
    return ob


def sketch(path):
    ob = build("solution")
    sc = bpy.context.scene
    frames = (1, 5, 8, 13, 18, 23, 28, 32, 40)
    W, H = 110, 340
    img = np.full((H, W * len(frames), 3), 0.08, np.float32)
    for i, f in enumerate(frames):
        sc.frame_set(f)
        bpy.context.view_layer.update()
        z0 = ob.matrix_world.translation.z
        sx, sz = ob.scale.x, ob.scale.z
        for t in np.linspace(0, 2 * math.pi, 240):
            x = W * i + W / 2 + 0.5 * sx * math.cos(t) * 80
            y = H - 20 - (z0 + 0.5 * sz * (1 + math.sin(t))) * 80
            if 0 <= y < H:
                img[int(y), int(x)] = (0.9, 0.55, 0.2) if sz < 0.95 else ((0.3, 0.8, 0.5) if sz > 1.05 else (0.8, 0.8, 0.8))
        img[H - 20, W * i + 5:W * (i + 1) - 5] = (0.35, 0.35, 0.35)
    rgba = np.concatenate([img, np.ones(img.shape[:2] + (1,), np.float32)], axis=2)
    out = bpy.data.images.new("sk", img.shape[1], H)
    out.pixels = rgba[::-1].ravel()
    out.filepath_raw = path
    out.file_format = "PNG"
    out.save()


def main():
    out = os.path.join(CH, "COMPLETED_EXAMPLES")
    build("starter")
    L.save(os.path.join(CH, "STARTER_FILES", "ch07_01_principles_starter.blend"))
    for k in ("no_squash", "no_anticipation", "no_stretch", "volume_break", "floating", "no_settle"):
        build(k)
        L.save(os.path.join(out, "COUNTER_EXAMPLES", f"ch07_01_principles_{k}.blend"))
    build("solution")
    L.save(os.path.join(out, "ch07_01_principles_solution.blend"))
    sketch(os.path.join(out, "ch07_01_principles_reference.png"))


if __name__ == "__main__":
    L.run(main)
