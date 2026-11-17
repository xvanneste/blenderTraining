"""
validate_ch09_04.py — Correcteur « Dramatique et stylisé » (CH09.04).
Usage : … --python-exit-code 1 --python validate_ch09_04.py -- --exercise dramatic [--debug]
Fichier à deux scènes : LOWKEY (lampes LOW_Key, LOW_Fill, LOW_Rim) et HIGHKEY (HIGH_Key, HIGH_Fill, HIGH_Rim) ; sujet, caméra et visée partagés.
  Le correcteur rend chaque scène (Cycles CPU, 96 × 96, 48 échantillons, EXR linéaire, fichier temporaire) avec toutes les lampes puis sans la Rim, et lit les zones du sujet (flanc éclairé, flanc d'ombre, bande du haut).
  LOWKEY  : flanc éclairé / flanc d'ombre ≥ 7 ; luminance moyenne des deux flancs ≤ 0,15 ; la Rim apporte au moins 25 % de la bande du haut ; teintes (HSV) de la Key et de la Rim distantes d'au moins 120° (couleurs complémentaires) et saturées (≥ 0,3).
  HIGHKEY : ratio de 0,7 à 1,6 ; luminance moyenne des deux flancs ≥ 0,45.
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


def render(scene, prefix, hide=(), res=96, samples=48):
    sc = bpy.data.scenes[scene]
    sc.render.engine = "CYCLES"
    sc.cycles.device = "CPU"
    sc.cycles.use_denoising = False
    sc.cycles.samples = samples
    sc.render.resolution_x = sc.render.resolution_y = res
    sc.render.resolution_percentage = 100
    for role in ("Key", "Fill", "Rim"):
        bpy.data.objects[f"{prefix}_{role}"].hide_render = role in hide
    sc.render.image_settings.file_format = "OPEN_EXR"
    sc.render.image_settings.color_depth = "32"
    p = os.path.join(tempfile.gettempdir(), "bcma_ch0904_val.exr")
    sc.render.filepath = p
    bpy.ops.render.render(write_still=True, scene=scene)
    im = bpy.data.images.load(p)
    px = np.array(im.pixels[:], np.float32).reshape(res, res, 4)[..., :3].copy()
    bpy.data.images.remove(im)
    return px[..., 0] * 0.2126 + px[..., 1] * 0.7152 + px[..., 2] * 0.0722


def zones(Y):
    c = Y.shape[0] // 2
    return float(Y[c - 8:c + 8, c - 25:c - 10].mean()), float(Y[c - 8:c + 8, c + 10:c + 25].mean()), float(Y[c + 22:c + 27, c - 8:c + 8].mean())


def hs(col):
    h, s, v = colorsys.rgb_to_hsv(*col[:3])
    return h * 360.0, s


def main():
    debug = L.flag("--debug")
    r = L.Report("CH09.04 — Dramatique et stylisé")
    need = [f"{p}_{x}" for p in ("LOW", "HIGH") for x in ("Key", "Fill", "Rim")] + ["Subject", "CAM"]
    if not r.check(all(n in bpy.data.objects for n in need) and "LOWKEY" in bpy.data.scenes and "HIGHKEY" in bpy.data.scenes, "Scènes LOWKEY et HIGHKEY, sujet, caméra et six lampes présents", "Partez du fichier de départ.", 2):
        return r.finish()
    a = zones(render("LOWKEY", "LOW"))
    nr = zones(render("LOWKEY", "LOW", hide=("Rim",)))
    lr = (a[2] - nr[2]) / max(a[2], 1e-9)
    ratio = a[0] / max(a[1], 1e-9)
    mean = (a[0] + a[1]) / 2
    hk, sk = hs(bpy.data.objects["LOW_Key"].data.color)
    hr, sr = hs(bpy.data.objects["LOW_Rim"].data.color)
    dh = abs(hk - hr)
    dh = min(dh, 360 - dh)
    r.check(ratio >= 7, f"LOWKEY — contraste : flanc éclairé / flanc d'ombre = {ratio:.1f} (≥ 7)", "Fill presque éteinte (0,5 W).", 7)
    r.check(mean <= 0.15, f"LOWKEY — image sombre : luminance moyenne des flancs {mean:.3f} (≤ 0,15)", "Key 70 W : peu de lumière, beaucoup d'ombre.", 7)
    r.check(lr >= 0.25 and a[2] - nr[2] >= 0.01, f"LOWKEY — contre-jour : la Rim apporte {100 * lr:.0f} % de la bande du haut (≥ 25 %)", "Rim 250 W bleu-vert.", 6)
    r.check(dh >= 120 and sk >= 0.3 and sr >= 0.3, f"LOWKEY — couleurs : teinte Key {hk:.0f}°, Rim {hr:.0f}° (écart {dh:.0f}° ≥ 120°), saturations {sk:.2f} et {sr:.2f} (≥ 0,3)", "Key orange, Rim bleu-vert (complémentaires).", 6)
    b = zones(render("HIGHKEY", "HIGH"))
    hratio = b[0] / max(b[1], 1e-9)
    hmean = (b[0] + b[1]) / 2
    r.check(0.7 <= hratio <= 1.6, f"HIGHKEY — contraste doux : ratio {hratio:.2f} (0,7–1,6)", "Fill 150 W, proche de la Key.", 7)
    r.check(hmean >= 0.45, f"HIGHKEY — image claire : luminance moyenne des flancs {hmean:.2f} (≥ 0,45)", "Key 250 W, Fill 150 W.", 7)
    if debug:
        print("[DEBUG] LOW ratio", round(ratio, 1), "mean", round(mean, 3), "rim", round(lr, 2), "dh", round(dh), "| HIGH ratio", round(hratio, 2), "mean", round(hmean, 3))
    return r.finish()


if __name__ == "__main__":
    L.run(main)
