"""
validate_ch09_11.py — Correcteur « Couleur et émotion » (CH09.11).
Usage : … --python-exit-code 1 --python validate_ch09_11.py -- --exercise color [--debug]
Objets : BG_<NOM> et ACC_<NOM> pour NOM dans JOY, SADNESS, ANGER, CALM, FEAR (10 plans), CAM (orthographique, 500 × 100).
Le correcteur rend lui-même (Workbench plat, Standard, 500 × 100) et mesure la médiane de la couleur AFFICHÉE (teinte H en degrés, saturation S, valeur V) sur le fond (rangées 5–24, bords de la carte) et sur l'accent (centre) :
  JOY : H 20–65, S ≥ 0,6, V ≥ 0,8 ; SADNESS : H 190–250, S 0,15–0,5, V ≤ 0,5 ; ANGER : H ≤ 15 ou ≥ 345, S ≥ 0,7, V 0,35–0,7 ; CALM : H 150–220, S 0,15–0,5, V 0,6–0,85 ; FEAR : fond V ≤ 0,2, accent V ≥ 0,5 ;
  teintes des fonds de JOY, SADNESS, ANGER, CALM distinctes (≥ 25° deux à deux) ; accent contre fond : écart de valeur ≥ 0,2 OU (deux couleurs saturées, S ≥ 0,3) écart de teinte ≥ 120°, sur les cinq cartes.
Les plans ne doivent pas bouger ni changer d'échelle (taille et position vérifiées).
Testé avec : Blender 5.3.0.
"""
import colorsys
import os
import sys
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bpy  # noqa: E402
import numpy as np  # noqa: E402

NAMES = ("JOY", "SADNESS", "ANGER", "CALM", "FEAR")


def hsv_of(px, r0, r1, c0, c1):
    m = np.median(px[r0:r1, c0:c1].reshape(-1, 3), axis=0)
    h, s, v = colorsys.rgb_to_hsv(*[float(t) for t in m])
    return h * 360.0, s, v


def hdist(a, b):
    d = abs(a - b) % 360.0
    return min(d, 360.0 - d)


def main():
    debug = L.flag("--debug")
    r = L.Report("CH09.11 — Couleur et émotion")
    objs = {f"{p}_{n}": bpy.data.objects.get(f"{p}_{n}") for n in NAMES for p in ("BG", "ACC")}
    if not r.check(all(objs.values()) and bpy.data.objects.get("CAM") is not None, "BG_* et ACC_* (10 objets) et CAM présents", "Partez du fichier de départ.", 2):
        return r.finish()
    sc = bpy.context.scene
    geo_ok = all(abs(objs[f"BG_{n}"].location.x - (i - 2) * 2.0) < 1e-3 and abs(objs[f"BG_{n}"].scale.x - 1) < 1e-3 and abs(objs[f"ACC_{n}"].scale.x - 1) < 1e-3 for i, n in enumerate(NAMES))
    r.check(geo_ok, "Cartes à leur place et à leur échelle", "Ne changez que la couleur (Object > Viewport Display > Color).", 3)
    sc.render.engine = "BLENDER_WORKBENCH"
    sc.view_settings.view_transform = "Standard"
    sc.view_settings.look = "None"
    sh = sc.display.shading
    sh.light, sh.color_type = "FLAT", "OBJECT"
    sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage = 500, 100, 100
    sc.camera = bpy.data.objects["CAM"]
    sc.render.image_settings.file_format = "PNG"
    sc.render.image_settings.color_mode = "RGB"
    path = os.path.join(tempfile.gettempdir(), "bcma_ch0911_val.png")
    sc.render.filepath = path
    bpy.ops.render.render(write_still=True)
    im = bpy.data.images.load(path)
    px = np.array(im.pixels[:], np.float32).reshape(100, 500, 4)[..., :3][::-1].copy()
    bpy.data.images.remove(im)
    bg, ac = {}, {}
    for i, n in enumerate(NAMES):
        c0 = i * 100
        bg[n] = hsv_of(px, 5, 25, c0 + 10, c0 + 90)
        ac[n] = hsv_of(px, 40, 60, c0 + 40, c0 + 60)
    fmt = lambda t: f"H {t[0]:.0f}°, S {t[1]:.2f}, V {t[2]:.2f}"
    h, s, v = bg["JOY"]
    r.check(20 <= h <= 65 and s >= 0.6 and v >= 0.8, f"JOY : {fmt(bg['JOY'])} (chaud, vif, clair)", "H 20–65°, S ≥ 0,6, V ≥ 0,8.", 6)
    h, s, v = bg["SADNESS"]
    r.check(190 <= h <= 250 and 0.15 <= s <= 0.5 and v <= 0.5, f"SADNESS : {fmt(bg['SADNESS'])} (froid, terne, sombre)", "H 190–250°, S 0,15–0,5, V ≤ 0,5.", 6)
    h, s, v = bg["ANGER"]
    r.check((h <= 15 or h >= 345) and s >= 0.7 and 0.35 <= v <= 0.7, f"ANGER : {fmt(bg['ANGER'])} (rouge saturé)", "H ≤ 15° ou ≥ 345°, S ≥ 0,7, V 0,35–0,7.", 6)
    h, s, v = bg["CALM"]
    r.check(150 <= h <= 220 and 0.15 <= s <= 0.5 and 0.6 <= v <= 0.85, f"CALM : {fmt(bg['CALM'])} (froid, doux, clair)", "H 150–220°, S 0,15–0,5, V 0,6–0,85.", 6)
    r.check(bg["FEAR"][2] <= 0.2 and ac["FEAR"][2] >= 0.5, f"FEAR : fond V {bg['FEAR'][2]:.2f} (≤ 0,2), accent V {ac['FEAR'][2]:.2f} (≥ 0,5)", "Fond presque noir, petit accent clair.", 6)
    four = ("JOY", "SADNESS", "ANGER", "CALM")
    gaps = {(a, b): hdist(bg[a][0], bg[b][0]) for i, a in enumerate(four) for b in four[i + 1:]}
    worst = min(gaps, key=gaps.get)
    r.check(gaps[worst] >= 25, f"Teintes des fonds distinctes : plus petit écart {gaps[worst]:.0f}° ({worst[0]}/{worst[1]}) (≥ 25°)", "Chaque émotion a sa couleur de fond.", 6)
    low = [n for n in NAMES if abs(ac[n][2] - bg[n][2]) < 0.2 and not (min(ac[n][1], bg[n][1]) >= 0.3 and hdist(ac[n][0], bg[n][0]) >= 120)]
    r.check(not low, "Accent détaché du fond (valeur ≥ 0,2 d'écart, ou teintes opposées ≥ 120°)" if not low else f"Accent trop proche du fond : {', '.join(low)}", "Changez la valeur ou la teinte de l'accent.", 5)
    if debug:
        print("[DEBUG] bg", {n: tuple(round(t, 2) for t in bg[n]) for n in NAMES}, "acc", {n: tuple(round(t, 2) for t in ac[n]) for n in NAMES})
    return r.finish()


if __name__ == "__main__":
    L.run(main)
