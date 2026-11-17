"""
build_ch09_07_files.py — « Composition » (CH09.07 : règle des tiers, ligne d'horizon, taille du sujet, cadrage).

Scène (rendu Workbench, lumière plate, couleurs d'objet) : Ground (plan de 400 × 400 m, gris), ciel = couleur du monde (bleu), Subject (cylindre rouge de 0,5 m de diamètre et 1,8 m de haut posé en (0, 8, 0)),
  CAM à (0, 0, 1,6) regardant vers +Y (rotation X = 90°), focale 35 mm, rendu 160 × 90 (16:9). Au départ : le sujet est au centre de l'image et l'horizon au milieu.
  Consigne : recomposer le plan avec les décalages d'objectif (Camera > Lens > Shift X / Y) et/ou la rotation de la caméra, SANS déplacer le sujet : le sujet sur le tiers GAUCHE (x = 33 % ± 5 %), l'horizon sur le tiers HAUT (ligne d'horizon à 33 % de la hauteur à partir du haut ± 5 %,
  c'est-à-dire plus de sol que de ciel ; à 67 % les pieds du sujet sortiraient du cadre : mesuré), le sujet entièrement dans le cadre avec une marge d'au moins 3 %, et au moins 25 % de la hauteur de l'image.
  Mesures : voir validate_ch09_07.py. Solution : Shift X = +0,167, Shift Y = −0,1 (mesuré : cx 0,334 ; horizon 0,333 ; sujet de 0,289 à 0,678 de la hauteur).
  STARTER_FILES/ch09_07_composition_starter.blend ; COMPLETED_EXAMPLES/ch09_07_composition_solution.blend (+ _reference.png : rendu de départ et solution avec la grille des tiers)
  COUNTER_EXAMPLES/ : centered (départ), subject_right (sujet au tiers droit), horizon_middle (horizon au milieu : 0,51), cropped (caméra avancée de 6 m : sujet coupé en haut et en bas), tiny_subject (sujet trop petit : caméra reculée)
Usage : blender -b --factory-startup --python-exit-code 1 --python build_ch09_07_files.py
Testé avec : Blender 5.3.0.
"""
import math
import os
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bmesh  # noqa: E402
import bpy  # noqa: E402
import numpy as np  # noqa: E402

CH = L.chapter_dir(__file__)
NOTE = """CH09.07 — COMPOSITION (Subject, Ground, CAM)
Le sujet (cylindre rouge) est au centre de l'image et l'horizon au milieu : une composition statique. Recomposez le plan en ne touchant qu'à la caméra (CAM).
1. Camera > Lens > Shift X : décale le cadre horizontalement (le sujet se déplace dans l'image) ; Shift Y : verticalement (une valeur négative fait monter l'horizon dans l'image, mesuré : −0,1 → 33 %).
2. Cible : sujet sur le tiers GAUCHE de l'image (33 % de la largeur, ± 5 %) ; horizon sur le tiers HAUT (à 33 % de la hauteur en partant du haut, ± 5 % : plus de sol que de ciel).
3. Le sujet reste entier dans le cadre (marge ≥ 3 %) et occupe au moins 25 % de la hauteur.
Vérification : SCRIPTS/validate_ch09_07.py -- --exercise composition
"""
SUBJECT_Y = 8.0


def build(kind):
    L.reset("SC_COMPOSE")
    sc = bpy.context.scene
    sc.render.engine = "BLENDER_WORKBENCH"
    sc.view_settings.view_transform = "Standard"
    sc.view_settings.look = "None"
    sh = sc.display.shading
    sh.light, sh.color_type = "FLAT", "OBJECT"
    wo = bpy.data.worlds.new("WO_Sky")
    wo.color = (0.4, 0.6, 1.0)
    sc.world = wo
    bm = bmesh.new()
    bmesh.ops.create_grid(bm, x_segments=1, y_segments=1, size=200)
    me = bpy.data.meshes.new("ME_Ground")
    bm.to_mesh(me)
    bm.free()
    g = bpy.data.objects.new("Ground", me)
    sc.collection.objects.link(g)
    g.color = (0.35, 0.35, 0.35, 1)
    bm = bmesh.new()
    bmesh.ops.create_cone(bm, cap_ends=True, segments=24, radius1=0.25, radius2=0.25, depth=1.8)
    me = bpy.data.meshes.new("ME_Subject")
    bm.to_mesh(me)
    bm.free()
    s = bpy.data.objects.new("Subject", me)
    sc.collection.objects.link(s)
    s.location = (0, SUBJECT_Y, 0.9)
    s.color = (1.0, 0.0, 0.0, 1)
    cam = bpy.data.objects.new("CAM", bpy.data.cameras.new("CAM"))
    sc.collection.objects.link(cam)
    cam.location = (0, 0, 1.6)
    cam.rotation_euler = (math.radians(90), 0, 0)
    cam.data.lens = 35
    sc.camera = cam
    sx, sy, dy = {"starter": (0, 0, 0), "centered": (0, 0, 0), "solution": (0.167, -0.1, 0), "subject_right": (-0.167, -0.1, 0), "horizon_middle": (0.167, 0.0, 0), "cropped": (0.167, -0.1, -6), "tiny_subject": (0.167, -0.1, 12)}[kind]
    cam.data.shift_x, cam.data.shift_y = sx, sy
    cam.location.y -= dy
    sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage = 160, 90, 100
    sc.frame_set(1)
    L.instructions(NOTE)


def render():
    sc = bpy.context.scene
    sc.render.image_settings.file_format = "PNG"
    sc.render.image_settings.color_mode = "RGB"
    p = os.path.join(tempfile.gettempdir(), "bcma_ch0907.png")
    sc.render.filepath = p
    bpy.ops.render.render(write_still=True)
    im = bpy.data.images.load(p)
    px = np.array(im.pixels[:], np.float32).reshape(90, 160, 4)[..., :3][::-1].copy()  # ligne 0 = HAUT de l'image
    bpy.data.images.remove(im)
    return px


def analyse(px):
    R, G, B = px[..., 0], px[..., 1], px[..., 2]
    subj = (R > 0.7) & (G < 0.3) & (B < 0.3)
    sky = (B > 0.7) & (R < 0.7) & (G > 0.35)
    H, W = subj.shape
    ys, xs = np.nonzero(subj)
    if len(xs) == 0:
        return None
    cx = (xs.mean() + 0.5) / W
    top, bot, left, right = ys.min() / H, (ys.max() + 1) / H, xs.min() / W, (xs.max() + 1) / W
    cols = [c for c in range(W) if not subj[:, c].any()]
    hor = float(np.mean([np.nonzero(sky[:, c])[0].max() + 1 for c in cols if sky[:, c].any()])) / H if cols else -1
    return {"cx": cx, "top": top, "bot": bot, "left": left, "right": right, "height": bot - top, "horizon": hor}


def calibrate():
    for kind in ("starter", "solution", "subject_right", "horizon_middle", "cropped", "tiny_subject"):
        build(kind)
        a = analyse(render())
        print(f"[comp] {kind:14s}", {k: round(float(v), 3) for k, v in a.items()} if a else None)


def sketch(path):
    W, H = 780, 270
    img = np.zeros((H, W, 3), np.float32)
    for i, kind in enumerate(("starter", "solution")):
        build(kind)
        px = render()
        big = np.kron(px, np.ones((3, 3, 1), np.float32))  # 270 × 480 -> trop large : réduire
        big = px[::1, ::1]
        tile = np.kron(big, np.ones((2, 2, 1), np.float32))  # 180 × 320
        y0, x0 = 45, 30 + i * 380
        img[y0:y0 + 180, x0:x0 + 320, :] = tile
        for f in (1 / 3, 2 / 3):  # grille des tiers
            img[y0:y0 + 180, x0 + int(f * 320), :] = (1, 1, 0)
            img[y0 + int(f * 180), x0:x0 + 320, :] = (1, 1, 0)
    rgba = np.concatenate([img, np.ones(img.shape[:2] + (1,), np.float32)], axis=2)
    out = bpy.data.images.new("sk", W, H)
    out.pixels = rgba[::-1].ravel()
    out.filepath_raw = path
    out.file_format = "PNG"
    out.save()


def main():
    out = os.path.join(CH, "COMPLETED_EXAMPLES")
    calibrate()
    build("starter")
    L.save(os.path.join(CH, "STARTER_FILES", "ch09_07_composition_starter.blend"))
    for k in ("centered", "subject_right", "horizon_middle", "cropped", "tiny_subject"):
        build(k)
        L.save(os.path.join(out, "COUNTER_EXAMPLES", f"ch09_07_composition_{k}.blend"))
    sketch(os.path.join(out, "ch09_07_composition_reference.png"))
    build("solution")
    L.save(os.path.join(out, "ch09_07_composition_solution.blend"))


if __name__ == "__main__":
    L.run(main)
