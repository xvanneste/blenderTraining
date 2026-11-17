"""
validate_ch09_10.py — Correcteur « Mouvements et grammaire » (CH09.10).
Usage : … --python-exit-code 1 --python validate_ch09_10.py -- --exercise movements [--debug]
Objets : A (rouge, (-1, 0, 0,9)), B (bleu, (1, 0, 0,9)) : ne doivent pas bouger (1 cm) ; CAM_WIDE, CAM_MED, CAM_CLOSE.
Repères de timeline : trois, triés par image, liés dans l'ordre à CAM_WIDE, CAM_MED, CAM_CLOSE ; images 1 / 25 / 49 (à 1 image près).
Le correcteur rend lui-même (Workbench plat 160 × 90) l'image du repère de chaque plan (et l'image 48 pour le travelling de CAM_MED) et mesure :
  ligne d'action : dans chaque plan, A (rouge) est à GAUCHE de B (bleu) ;
  échelles : hauteur de A dans l'image : WIDE ≤ 0,35 ; MED (image 25) 0,40–0,65 ; CLOSE 0,70–0,95 ;
  travelling : hauteur de A avec CAM_MED à l'image 48 ≥ 1,15 × celle de l'image 25 (le plan se resserre) ;
  A et B entiers dans le cadre à chaque plan (marge de 1 %).
Testé avec : Blender 5.3.0.
"""
import os
import sys
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bpy  # noqa: E402
import numpy as np  # noqa: E402
from mathutils import Vector  # noqa: E402


def shot(sc, cam, frame, tag):
    sc.frame_set(frame)
    sc.camera = cam
    p = os.path.join(tempfile.gettempdir(), f"bcma_ch0910_val_{tag}.png")
    sc.render.filepath = p
    bpy.ops.render.render(write_still=True)
    im = bpy.data.images.load(p)
    px = np.array(im.pixels[:], np.float32).reshape(90, 160, 4)[..., :3][::-1].copy()
    bpy.data.images.remove(im)
    R, G, B = px[..., 0], px[..., 1], px[..., 2]
    red = (R > 0.7) & (G < 0.3) & (B < 0.3)
    blue = (B > 0.7) & (R < 0.3) & (G < 0.3)
    if red.sum() < 5 or blue.sum() < 5:
        return None
    ys, xs = np.nonzero(red)
    yb, xb = np.nonzero(blue)
    H, W = red.shape
    inside = min(ys.min(), yb.min()) >= 0.01 * H and max(ys.max(), yb.max()) + 1 <= 0.99 * H and min(xs.min(), xb.min()) >= 0.01 * W and max(xs.max(), xb.max()) + 1 <= 0.99 * W
    return {"h": (ys.max() + 1 - ys.min()) / H, "rx": (xs.mean() + 0.5) / W, "bx": (xb.mean() + 0.5) / W, "inside": bool(inside)}


def main():
    debug = L.flag("--debug")
    r = L.Report("CH09.10 — Mouvements et grammaire")
    sc = bpy.context.scene
    a, b = bpy.data.objects.get("A"), bpy.data.objects.get("B")
    cams = {n: bpy.data.objects.get(n) for n in ("CAM_WIDE", "CAM_MED", "CAM_CLOSE")}
    if not r.check(a is not None and b is not None and all(cams.values()), "A, B, CAM_WIDE, CAM_MED et CAM_CLOSE présents", "Partez du fichier de départ.", 2):
        return r.finish()
    sc.frame_set(1)
    ok = (a.matrix_world.translation - Vector((-1, 0, 0.9))).length <= 0.01 and (b.matrix_world.translation - Vector((1, 0, 0.9))).length <= 0.01
    r.check(ok, "Les personnages n'ont pas bougé", "Ne déplacez que les caméras.", 3)
    mk = sorted(sc.timeline_markers, key=lambda m: m.frame)
    names = [m.camera.name if m.camera else None for m in mk]
    good = len(mk) == 3 and names == ["CAM_WIDE", "CAM_MED", "CAM_CLOSE"]
    r.check(good, f"Repères liés aux caméras dans l'ordre large → moyen → serré : {names}", "Timeline : un repère (M) par plan, lié à sa caméra (Marker > Bind Camera to Markers), dans l'ordre CAM_WIDE, CAM_MED, CAM_CLOSE.", 8)
    frames = [m.frame for m in mk]
    r.check(good and all(abs(f - e) <= 1 for f, e in zip(frames, (1, 25, 49))), f"Images des repères : {frames} (attendu 1, 25, 49 à ±1)", "Placez les repères aux images 1, 25 et 49.", 4)
    sc.render.engine = "BLENDER_WORKBENCH"
    sc.view_settings.view_transform = "Standard"
    sc.view_settings.look = "None"
    sh = sc.display.shading
    sh.light, sh.color_type = "FLAT", "OBJECT"
    sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage = 160, 90, 100
    sc.render.image_settings.file_format = "PNG"
    sc.render.image_settings.color_mode = "RGB"
    s_w = shot(sc, cams["CAM_WIDE"], 1, "w")
    s_m = shot(sc, cams["CAM_MED"], 25, "m")
    s_m2 = shot(sc, cams["CAM_MED"], 48, "m2")
    s_c = shot(sc, cams["CAM_CLOSE"], 49, "c")
    shots = (("plan large", s_w), ("plan moyen", s_m), ("gros plan", s_c))
    for nm, s in shots:
        if s is None:
            r.check(False, f"{nm} : A et B visibles", "Un personnage est hors cadre.", 6)
    if debug:
        print("[DEBUG]", s_w, s_m, s_m2, s_c)
    if any(s is None for _, s in shots) or s_m2 is None:
        return r.finish()
    r.check(all(s["inside"] for _, s in shots) and s_m2["inside"], "A et B entiers dans le cadre dans tous les plans", "Cadrez les deux personnages en entier.", 5)
    sides = [(nm, s["rx"] < s["bx"]) for nm, s in shots]
    r.check(all(v for _, v in sides), "Ligne d'action respectée : A à gauche de B dans les trois plans (" + ", ".join(f"{nm} {'✓' if v else '✗'}" for nm, v in sides) + ")", "Une caméra a traversé la ligne : replacez-la du côté y < 0.", 10)
    r.check(s_w["h"] <= 0.35, f"Plan large : A fait {100 * s_w['h']:.0f} % de la hauteur (≤ 35 %)", "Reculez ou raccourcissez la focale.", 5)
    r.check(0.40 <= s_m["h"] <= 0.65, f"Plan moyen (image 25) : {100 * s_m['h']:.0f} % (40–65 %)", "CAM_MED en y = −8 à l'image 25.", 5)
    r.check(0.70 <= s_c["h"] <= 0.95, f"Gros plan : {100 * s_c['h']:.0f} % (70–95 %)", "CAM_CLOSE en y = −4.", 5)
    r.check(s_m2["h"] >= 1.15 * s_m["h"], f"Travelling avant : {100 * s_m['h']:.0f} % → {100 * s_m2['h']:.0f} % (≥ ×1,15)", "Clés de CAM_MED : y = −8 (image 25) puis −6 (image 48).", 8)
    return r.finish()


if __name__ == "__main__":
    L.run(main)
