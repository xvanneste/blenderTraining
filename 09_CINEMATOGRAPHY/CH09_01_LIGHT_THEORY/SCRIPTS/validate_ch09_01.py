"""
validate_ch09_01.py — Correcteur « Théorie de la lumière » (CH09.01).
Usage : … --python-exit-code 1 --python validate_ch09_01.py -- --exercise light [--debug]
Objets : Plate, Occluder (cube plat à z = 1 m), CAM, LIGHT_Key. Moteur Cycles (CPU), vue Standard, monde noir : le correcteur rend lui-même (EXR linéaire, 64 échantillons, fichier temporaire).
  Configuration : LIGHT_Key est une lampe ponctuelle (Point) au-dessus du centre (|x|, |y| ≤ 0,1 m) à une hauteur de 2,7 à 3,3 m ; Radius de 0,3 m ou plus.
  Rendu 1 (plan seul, 64 × 64) : luminance au centre (0,2126 R + 0,7152 V + 0,0722 B, moyenne de 8 × 8 pixels) = celle de la référence (10 W blanc à 1 m : 0,119) à ± 20 % ;
          lumière chaude : rouge / bleu ≥ 1,25 au centre.
  Rendu 2 (avec l'ombre de Occluder, 128 × 128) : pénombre de l'ombre (transition 10 % → 90 % du bord gauche, profil moyenné sur 8 lignes) d'au moins 6 pixels.
Testé avec : Blender 5.3.0.
"""
import os
import sys
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bpy  # noqa: E402
import numpy as np  # noqa: E402

REF_LUM = 0.11898


def render(res, samples, occluder):
    sc = bpy.context.scene
    sc.cycles.samples = samples
    sc.render.resolution_x = sc.render.resolution_y = res
    sc.render.resolution_percentage = 100
    bpy.data.objects["Occluder"].hide_render = not occluder
    sc.render.image_settings.file_format = "OPEN_EXR"
    sc.render.image_settings.color_depth = "32"
    p = os.path.join(tempfile.gettempdir(), "bcma_ch0901_val.exr")
    sc.render.filepath = p
    bpy.ops.render.render(write_still=True)
    im = bpy.data.images.load(p)
    px = np.array(im.pixels[:], np.float32).reshape(res, res, 4)[..., :3].copy()
    bpy.data.images.remove(im)
    return px


def lum(c):
    return float(0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2])


def penumbra(y):
    ys = np.convolve(y, np.ones(3) / 3, mode="same")
    hi, lo = float(np.median(ys[:12])), float(ys[48:80].min())
    if hi - lo < 1e-4:
        return 0
    t10, t90 = lo + 0.1 * (hi - lo), lo + 0.9 * (hi - lo)
    mid = int(np.argmin(ys[40:88])) + 40
    left = ys[:mid]
    i10 = int(np.where(left > t90)[0].max()) if (left > t90).any() else 0
    i90 = int(np.where(left < t10)[0].min()) if (left < t10).any() else mid
    return max(i90 - i10, 0)


def main():
    debug = L.flag("--debug")
    r = L.Report("CH09.01 — Théorie de la lumière")
    sc = bpy.context.scene
    lo = bpy.data.objects.get("LIGHT_Key")
    if not r.check(lo is not None and lo.type == "LIGHT" and all(bpy.data.objects.get(n) for n in ("Plate", "Occluder", "CAM")), "LIGHT_Key, Plate, Occluder et CAM présents", "Partez du fichier de départ.", 2):
        return r.finish()
    ld = lo.data
    r.check(ld.type == "POINT", f"LIGHT_Key : lampe {ld.type} (Point)", "Light > Type Point.", 3)
    pos = lo.matrix_world.translation
    r.check(abs(pos.x) <= 0.1 and abs(pos.y) <= 0.1 and 2.7 <= pos.z <= 3.3, f"Position ({pos.x:.2f}, {pos.y:.2f}, {pos.z:.2f}) : au-dessus du centre, à 2,7–3,3 m du plan", "Location Z = 3, X = Y = 0.", 6)
    r.check(ld.shadow_soft_size >= 0.3, f"Radius : {ld.shadow_soft_size:.2f} m (≥ 0,3 : ombre douce)", "Light > Radius 0,5.", 4)
    sc.render.engine = "CYCLES"
    sc.cycles.device = "CPU"
    sc.cycles.use_denoising = False
    a = render(64, 64, False)
    c = a[28:36, 28:36].mean(axis=(0, 1))
    y = lum(c)
    ratio = y / REF_LUM
    r.check(0.8 <= ratio <= 1.2, f"Exposition au centre : luminance {y:.3f} = {100 * ratio:.0f} % de la référence {REF_LUM:.3f} (80–120 %)", "Inverse du carré : 3 fois plus loin = 9 fois plus de puissance (≈ 90 à 100 W).", 8)
    rb = float(c[0] / max(float(c[2]), 1e-9))
    r.check(rb >= 1.25, f"Lumière chaude : rouge / bleu = {rb:.2f} (≥ 1,25)", "Color : rouge 1, vert 0,85, bleu 0,65.", 5)
    b = render(128, 64, True)
    row = b[60:68, :, :].mean(axis=0)
    pen = penumbra(row[:, 0] * 0.2126 + row[:, 1] * 0.7152 + row[:, 2] * 0.0722)
    r.check(pen >= 6, f"Pénombre de l'ombre : {pen} pixels (≥ 6)", "Radius 0,5 : une source étendue adoucit l'ombre.", 6)
    if debug:
        print("[DEBUG] lum", round(y, 4), "ratio", round(ratio, 3), "R/B", round(rb, 2), "pen", pen, "pos", tuple(round(v, 2) for v in pos), "radius", ld.shadow_soft_size)
    return r.finish()


if __name__ == "__main__":
    L.run(main)
