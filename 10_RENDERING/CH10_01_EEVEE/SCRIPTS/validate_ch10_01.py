"""
validate_ch10_01.py — Correcteur « EEVEE en profondeur » (CH10.01).
Usage : … --python-exit-code 1 --python validate_ch10_01.py -- --exercise eevee [--debug]
Objets : Floor, Wall, Ball, Chrome, SUN (3 W/m²), CAM. Le correcteur rend la scène AVEC LES RÉGLAGES EEVEE de l'élève (seule la résolution est imposée : 240 × 135) et mesure :
  moteur de rendu = EEVEE ; ombres : rapport (luminance moyenne de la zone d'ombre de la boule) / (zone éclairée du sol) ≤ 0,85 (sans ombres : 0,96 ; avec : 0,70) ;
  ray tracing : écart-type de la luminance de la sphère chromée ≥ 0,05 (sans ray tracing : 0,008 ; avec : 0,08) ; échantillons de rendu (Sampling > Render > Samples) de 16 à 128.
La scène (SUN 3 W/m², matériau de Chrome métallique 1,0) ne doit pas être modifiée.
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
    r = L.Report("CH10.01 — EEVEE en profondeur")
    names = ("Floor", "Wall", "Ball", "Chrome", "SUN", "CAM")
    if not r.check(all(bpy.data.objects.get(n) for n in names), "Floor, Wall, Ball, Chrome, SUN et CAM présents", "Partez du fichier de départ.", 2):
        return r.finish()
    sc = bpy.context.scene
    chrome = bpy.data.objects["Chrome"].data.materials[0].node_tree.nodes["Principled BSDF"].inputs["Metallic"].default_value
    r.check(abs(bpy.data.objects["SUN"].data.energy - 3.0) < 1e-3 and abs(chrome - 1.0) < 1e-3, "Scène inchangée : soleil 3 W/m², Chrome métallique 1,0", "Réglez EEVEE, pas la scène.", 3)
    if not r.check(sc.render.engine == "BLENDER_EEVEE", f"Moteur de rendu : {sc.render.engine}", "Render Properties > Render Engine : EEVEE.", 6):
        return r.finish()
    ev = sc.eevee
    sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage = 240, 135, 100
    sc.render.image_settings.file_format = "PNG"
    sc.render.image_settings.color_mode = "RGB"
    path = os.path.join(tempfile.gettempdir(), "bcma_ch1001_val.png")
    sc.render.filepath = path
    bpy.ops.render.render(write_still=True)
    im = bpy.data.images.load(path)
    px = np.array(im.pixels[:], np.float32).reshape(135, 240, 4)[..., :3][::-1].copy()
    bpy.data.images.remove(im)
    Y = px[..., 0] * 0.2126 + px[..., 1] * 0.7152 + px[..., 2] * 0.0722
    ratio = float(Y[48:58, 50:90].mean() / max(Y[100:120, 150:200].mean(), 1e-6))
    std = float(Y[62:84, 172:212].std())
    r.check(ratio <= 0.85, f"Ombres : rapport ombre / lumière {ratio:.2f} (≤ 0,85) ; Shadows {'activé' if ev.use_shadows else 'désactivé'}", "Sampling > Shadows : cochez la case de l'en-tête.", 8)
    r.check(std >= 0.05, f"Ray tracing : la sphère chromée a un écart-type de luminance de {std:.3f} (≥ 0,05) ; Raytracing {'activé' if ev.use_raytracing else 'désactivé'}", "Raytracing : cochez la case de l'en-tête.", 8)
    r.check(16 <= ev.taa_render_samples <= 128, f"Échantillons de rendu : {ev.taa_render_samples} (16–128)", "Sampling > Render > Samples : 16 à 128.", 5)
    if debug:
        print("[DEBUG] ratio", round(ratio, 3), "std", round(std, 3), "shadows", ev.use_shadows, "rt", ev.use_raytracing, "samples", ev.taa_render_samples)
    return r.finish()


if __name__ == "__main__":
    L.run(main)
