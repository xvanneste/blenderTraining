"""
validate_ch09_06.py — Correcteur « Exposition et contraste » (CH09.06).
Usage : … --python-exit-code 1 --python validate_ch09_06.py -- --exercise exposure [--debug]
Objets : Floor, Bright (sphère émissive), Mid, Dark, SUN, CAM. Le correcteur rend l'image AFFICHÉE (PNG 8 bits, gestion des couleurs de la scène : View Transform, Look, Exposure ; Cycles CPU, 96 × 96, 48 échantillons)
  et lit : pourcentage de pixels brûlés (luminance ≥ 0,99) ≤ 1 % ; luminance moyenne de 0,3 à 0,55 ; écart p95 − p5 de la luminance ≥ 0,55 (contraste conservé).
  La scène (Bright, Mid, Dark, SUN) ne doit pas être modifiée : Bright garde une émission de 6 et le soleil 3 W/m².
Testé avec : Blender 5.3.0.
"""
import os
import sys
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bpy  # noqa: E402
import numpy as np  # noqa: E402


def main():
    debug = L.flag("--debug")
    r = L.Report("CH09.06 — Exposition et contraste")
    names = ("Floor", "Bright", "Mid", "Dark", "SUN", "CAM")
    if not r.check(all(bpy.data.objects.get(n) for n in names), "Floor, Bright, Mid, Dark, SUN et CAM présents", "Partez du fichier de départ.", 2):
        return r.finish()
    sc = bpy.context.scene
    emit = bpy.data.objects["Bright"].data.materials[0].node_tree.nodes["Principled BSDF"].inputs["Emission Strength"].default_value
    r.check(abs(emit - 6.0) < 1e-3 and abs(bpy.data.objects["SUN"].data.energy - 3.0) < 1e-3, f"Scène inchangée : émission {emit:.1f} (6), soleil {bpy.data.objects['SUN'].data.energy:.1f} W/m² (3)", "Réglez la gestion des couleurs, pas la scène.", 3)
    vs = sc.view_settings
    sc.render.engine = "CYCLES"
    sc.cycles.device = "CPU"
    sc.cycles.use_denoising = False
    sc.cycles.samples = 48
    sc.render.resolution_x = sc.render.resolution_y = 96
    sc.render.resolution_percentage = 100
    sc.render.image_settings.file_format = "PNG"
    sc.render.image_settings.color_mode = "RGB"
    p = os.path.join(tempfile.gettempdir(), "bcma_ch0906_val.png")
    sc.render.filepath = p
    bpy.ops.render.render(write_still=True)
    im = bpy.data.images.load(p)
    px = np.array(im.pixels[:], np.float32).reshape(96, 96, 4)[..., :3]
    bpy.data.images.remove(im)
    Y = px[..., 0] * 0.2126 + px[..., 1] * 0.7152 + px[..., 2] * 0.0722
    mean, clip, spread = float(Y.mean()), 100.0 * float((Y >= 0.99).mean()), float(np.percentile(Y, 95) - np.percentile(Y, 5))
    r.check(clip <= 1.0, f"Hautes lumières : {clip:.1f} % de pixels brûlés (≤ 1 %) avec {vs.view_transform}, look {vs.look}, exposition {vs.exposure:+.1f}", "AgX, Khronos PBR Neutral ou Filmic compriment les hautes lumières ; Standard les écrête.", 8)
    r.check(0.3 <= mean <= 0.55, f"Exposition : luminance moyenne {mean:.3f} (0,3–0,55)", "Exposure : ajustez par pas de 0,5 (une valeur = un diaphragme).", 8)
    r.check(spread >= 0.55, f"Contraste : écart p95 − p5 = {spread:.2f} (≥ 0,55)", "Une exposition trop basse ou trop haute écrase l'image.", 7)
    if debug:
        print("[DEBUG]", vs.view_transform, vs.look, round(vs.exposure, 2), "mean", round(mean, 3), "clip%", round(clip, 2), "spread", round(spread, 3))
    return r.finish()


if __name__ == "__main__":
    L.run(main)
