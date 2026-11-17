"""
build_ch09_10_files.py — « Mouvements et grammaire » (CH09.10 : échelle de plans, ligne des 180°, découpage, travelling avant).

Scène (rendu Workbench, lumière plate, couleurs d'objet) : deux personnages-cylindres de 1,8 m face à face sur l'axe X : A rouge en (-1, 0, 0,9), B bleu en (1, 0, 0,9). LIGNE D'ACTION = l'axe X (la droite qui relie A et B).
  Trois caméras (focale en mm, capteur 36 mm, 160 × 90) : CAM_WIDE (plan large), CAM_MED (plan moyen), CAM_CLOSE (gros plan), toutes visant le milieu des deux personnages.
  Au départ (fichier à corriger) : CAM_WIDE en (0, −12, 0,9) f 35 ; CAM_MED en (0, −8, 0,9) f 50 (fixe) ; CAM_CLOSE en (0, +4, 0,9) f 35 ORIENTÉE VERS −Y : elle a traversé la ligne d'action ;
  aucun repère de timeline.
  Consigne : (1) remettre CAM_CLOSE du bon côté de la ligne (y < 0) : A doit rester à gauche de B dans les trois plans ; (2) lier chaque caméra à un repère de timeline :
  WIDE à l'image 1, MED à l'image 25, CLOSE à l'image 49 (dans cet ordre : large → moyen → serré) ; (3) faire un TRAVELLING AVANT de CAM_MED (images 25 → 48 : y de −8 à −6) ;
  (4) échelles mesurées par rendu : hauteur de A dans l'image : WIDE ≤ 0,35 ; MED à l'image 25 : 0,40–0,65 ; CLOSE : 0,70–0,95 ; à l'image 48 la hauteur de MED ≥ 1,15 × celle de l'image 25 (le plan se resserre).
  Solution : CAM_CLOSE en (0, −4, 0,9) f 35 (hauteur 0,82) ; repères 1 / 25 / 49 ; clés de CAM_MED : y = −8 (image 25), y = −6 (image 48), interpolation linéaire (hauteur 0,58 → 0,78).
  STARTER_FILES/ch09_10_movements_starter.blend ; COMPLETED_EXAMPLES/ch09_10_movements_solution.blend (+ _reference.png : planches du départ et de la solution)
  COUNTER_EXAMPLES/ : cross_line (CLOSE du mauvais côté), no_markers, wrong_order (CLOSE, MED, WIDE), static_med (pas de travelling), dolly_out (recul), no_progression (MED aussi large que WIDE)
Usage : blender -b --factory-startup --python-exit-code 1 --python build_ch09_10_files.py
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
NOTE = """CH09.10 — MOUVEMENTS ET GRAMMAIRE (A rouge, B bleu, CAM_WIDE, CAM_MED, CAM_CLOSE)
A (rouge, x = −1) et B (bleu, x = +1) se font face : la LIGNE D'ACTION est l'axe X. Toutes les caméras doivent rester du MÊME côté (y < 0) : A reste à gauche de B dans chaque plan.
1. CAM_CLOSE a traversé la ligne (y > 0, tournée vers −Y) : replacez-la en (0, −4, 0,9), rotation (90°, 0, 0).
2. Timeline : un repère (M dans la timeline) par plan, lié à sa caméra : CAM_WIDE à l'image 1, CAM_MED à l'image 25, CAM_CLOSE à l'image 49.
3. Travelling avant de CAM_MED : Location Y = −8 à l'image 25, −6 à l'image 48 (interpolation linéaire).
Cible : large (A ≤ 35 % de la hauteur), moyen (40–65 %), serré (70–95 %), le moyen se resserre d'au moins 15 % pendant le travelling.
Vérification : SCRIPTS/validate_ch09_10.py -- --exercise movements
"""


def cyl(sc, name, x, col):
    bm = bmesh.new()
    bmesh.ops.create_cone(bm, cap_ends=True, segments=24, radius1=0.25, radius2=0.25, depth=1.8)
    me = bpy.data.meshes.new("ME_" + name)
    bm.to_mesh(me)
    bm.free()
    o = bpy.data.objects.new(name, me)
    sc.collection.objects.link(o)
    o.location = (x, 0, 0.9)
    o.color = col
    return o


def mkcam(sc, name, y, f, facing=1):
    c = bpy.data.objects.new(name, bpy.data.cameras.new(name))
    sc.collection.objects.link(c)
    c.location = (0, y, 0.9)
    c.rotation_euler = (math.radians(90), 0, 0 if facing > 0 else math.radians(180))
    c.data.lens = f
    c.data.sensor_width = 36
    return c


def key_dolly(cam, y0, y1, f0=25, f1=48):
    cam.location.y = y0
    cam.keyframe_insert("location", index=1, frame=f0)
    cam.location.y = y1
    cam.keyframe_insert("location", index=1, frame=f1)
    act = cam.animation_data.action
    for fc in [fc for la in act.layers for st in la.strips for cb in st.channelbags for fc in cb.fcurves]:
        for kp in fc.keyframe_points:
            kp.interpolation = "LINEAR"


def build(kind):
    L.reset("SC_GRAMMAR")
    sc = bpy.context.scene
    sc.render.engine = "BLENDER_WORKBENCH"
    sc.view_settings.view_transform = "Standard"
    sc.view_settings.look = "None"
    sh = sc.display.shading
    sh.light, sh.color_type = "FLAT", "OBJECT"
    wo = bpy.data.worlds.new("WO_Grey")
    wo.color = (0.15, 0.15, 0.15)
    sc.world = wo
    cyl(sc, "A", -1.0, (1, 0, 0, 1))
    cyl(sc, "B", 1.0, (0, 0, 1, 1))
    solved = kind != "starter"
    w = mkcam(sc, "CAM_WIDE", -12, 35)
    med_y, med_f = (-8, 50) if kind != "no_progression" else (-12, 35)
    m = mkcam(sc, "CAM_MED", med_y, med_f)
    if kind in ("starter", "cross_line"):
        c = mkcam(sc, "CAM_CLOSE", 4, 35, facing=-1)
    else:
        c = mkcam(sc, "CAM_CLOSE", -4, 35)
    if kind == "solution" or kind in ("cross_line", "no_markers", "wrong_order", "no_progression"):
        if kind != "no_progression":
            key_dolly(m, -8, -6)
    if kind == "dolly_out":
        key_dolly(m, -8, -10)
        m.animation_data.action.name = "ACT_dolly_out"
    if kind in ("solution", "cross_line", "static_med", "dolly_out", "no_progression"):
        order = (("WIDE", w, 1), ("MED", m, 25), ("CLOSE", c, 49))
    elif kind == "wrong_order":
        order = (("CLOSE", c, 1), ("MED", m, 25), ("WIDE", w, 49))
    else:
        order = ()
    for nm, cam, fr in order:
        mk = sc.timeline_markers.new(nm, frame=fr)
        mk.camera = cam
    sc.frame_start, sc.frame_end = 1, 72
    sc.camera = w
    sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage = 160, 90, 100
    sc.frame_set(1)
    L.instructions(NOTE)
    return solved


def render_frame(cam, frame):
    sc = bpy.context.scene
    sc.frame_set(frame)
    sc.camera = cam
    sc.render.image_settings.file_format = "PNG"
    sc.render.image_settings.color_mode = "RGB"
    p = os.path.join(tempfile.gettempdir(), "bcma_ch0910.png")
    sc.render.filepath = p
    bpy.ops.render.render(write_still=True)
    im = bpy.data.images.load(p)
    px = np.array(im.pixels[:], np.float32).reshape(90, 160, 4)[..., :3][::-1].copy()
    bpy.data.images.remove(im)
    return px


def analyse(px):
    R, G, B = px[..., 0], px[..., 1], px[..., 2]
    red = (R > 0.7) & (G < 0.3) & (B < 0.3)
    blue = (B > 0.7) & (R < 0.3) & (G < 0.3)
    H = red.shape[0]
    out = {"red_px": int(red.sum()), "blue_px": int(blue.sum())}
    if red.sum() and blue.sum():
        ys, xs = np.nonzero(red)
        out["h"] = (ys.max() + 1 - ys.min()) / H
        out["red_x"] = (xs.mean() + 0.5) / red.shape[1]
        out["blue_x"] = (np.nonzero(blue)[1].mean() + 0.5) / red.shape[1]
    return out


def calibrate():
    for kind in ("starter", "solution", "dolly_out", "no_progression"):
        build(kind)
        sc = bpy.context.scene
        cams = {n: bpy.data.objects[n] for n in ("CAM_WIDE", "CAM_MED", "CAM_CLOSE")}
        res = {"wide@1": analyse(render_frame(cams["CAM_WIDE"], 1)), "med@25": analyse(render_frame(cams["CAM_MED"], 25)),
               "med@48": analyse(render_frame(cams["CAM_MED"], 48)), "close@49": analyse(render_frame(cams["CAM_CLOSE"], 49))}
        print(f"[gram] {kind}", {k: {a: round(float(b), 3) for a, b in v.items()} for k, v in res.items()})


def sketch(path):
    W, H = 1000, 420
    img = np.zeros((H, W, 3), np.float32)
    for row, kind in enumerate(("starter", "solution")):
        build(kind)
        cams = {n: bpy.data.objects[n] for n in ("CAM_WIDE", "CAM_MED", "CAM_CLOSE")}
        for i, (n, fr) in enumerate((("CAM_WIDE", 1), ("CAM_MED", 25), ("CAM_MED", 48), ("CAM_CLOSE", 49))):
            px = render_frame(cams[n], fr)
            y0, x0 = 20 + row * 200, 10 + i * 245
            img[y0:y0 + 90, x0:x0 + 160, :] = np.kron(px, np.ones((1, 1, 1), np.float32))
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
    L.save(os.path.join(CH, "STARTER_FILES", "ch09_10_movements_starter.blend"))
    for k in ("cross_line", "no_markers", "wrong_order", "static_med", "dolly_out", "no_progression"):
        build(k)
        L.save(os.path.join(out, "COUNTER_EXAMPLES", f"ch09_10_movements_{k}.blend"))
    sketch(os.path.join(out, "ch09_10_movements_reference.png"))
    build("solution")
    L.save(os.path.join(out, "ch09_10_movements_solution.blend"))


if __name__ == "__main__":
    L.run(main)
