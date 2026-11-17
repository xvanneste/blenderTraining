"""
validate_ch10_03.py — Correcteur « Bruit et débruitage » (CH10.03).
Usage : … --python-exit-code 1 --python validate_ch10_03.py -- --exercise denoising [--debug]
Objets : Floor, Ball (damier fin), Light (zone 60 W), CAM. Le correcteur rend la scène avec les RÉGLAGES CYCLES de l'élève (CPU, graine 0, adaptatif désactivé, 160 × 90 imposés) puis rend une RÉFÉRENCE de 256 échantillons sans débruitage, et mesure sur la zone du damier (rangées 55–84, colonnes 30–129) :
  budget : échantillons de rendu de 1 à 8 ; débruitage activé avec OpenImageDenoise et un préfiltre autre que None (None n'apporte rien : mesuré 0,071 contre 0,073 sans débruitage) ;
  EQM (racine de l'écart quadratique moyen de la luminance) avec la référence ≤ 0,065 (4 échantillons : 0,073 sans débruitage, 0,056 avec) ;
  contraste du damier : écart-type de l'image rendue / celui de la référence de 0,85 à 1,15 (le bruit l'augmente, un flou excessif le baisserait).
La scène (Light 60 W) ne doit pas être modifiée.
Testé avec : Blender 5.3.0.
"""
import os
import sys
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bpy  # noqa: E402
import numpy as np  # noqa: E402

PATCH = (slice(55, 85), slice(30, 130))


def lum(sc, tag):
    p = os.path.join(tempfile.gettempdir(), f"bcma_ch1003_val_{tag}.png")
    sc.render.filepath = p
    bpy.ops.render.render(write_still=True)
    im = bpy.data.images.load(p)
    px = np.array(im.pixels[:], np.float32).reshape(90, 160, 4)[..., :3][::-1].copy()
    bpy.data.images.remove(im)
    return px[..., 0] * 0.2126 + px[..., 1] * 0.7152 + px[..., 2] * 0.0722


def main():
    debug = L.flag("--debug")
    r = L.Report("CH10.03 — Bruit et débruitage")
    if not r.check(all(bpy.data.objects.get(n) for n in ("Floor", "Ball", "Light", "CAM")), "Floor, Ball, Light et CAM présents", "Partez du fichier de départ.", 2):
        return r.finish()
    sc = bpy.context.scene
    cy = sc.cycles
    r.check(abs(bpy.data.objects["Light"].data.energy - 60.0) < 1e-3, "Scène inchangée : Light 60 W", "Réglez le débruitage, pas la scène.", 3)
    sc.render.engine = "CYCLES"
    cy.device = "CPU"
    cy.use_adaptive_sampling = False
    cy.seed = 0
    sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage = 160, 90, 100
    sc.render.image_settings.file_format = "PNG"
    sc.render.image_settings.color_mode = "RGB"
    samples, den, pre, dn = cy.samples, cy.use_denoising, cy.denoising_prefilter, cy.denoiser
    y = lum(sc, "student")
    cy.samples, cy.use_denoising = 256, False
    ref = lum(sc, "ref")
    cy.samples, cy.use_denoising = samples, den
    rmse = float(np.sqrt(((y[PATCH] - ref[PATCH]) ** 2).mean()))
    ctr = float(y[PATCH].std() / ref[PATCH].std())
    r.check(1 <= samples <= 8, f"Budget : {samples} échantillons (1–8)", "Le rendu doit rester dans le budget : ne montez pas les échantillons, débruitez.", 6)
    r.check(den and dn == "OPENIMAGEDENOISE" and pre != "NONE", f"Débruitage : {'activé' if den else 'désactivé'}, {dn}, préfiltre {pre}", "Sampling > Render > Denoise : cochez, OpenImageDenoise, préfiltre Fast ou Accurate.", 8)
    r.check(rmse <= 0.065, f"Écart avec la référence : EQM {rmse:.4f} (≤ 0,065)", "Débruitez avec les passes Albedo and Normal et le préfiltre Accurate.", 8)
    r.check(0.85 <= ctr <= 1.15, f"Contraste du damier : {ctr:.2f} de la référence (0,85–1,15)", "Trop de bruit (> 1,15) ou image trop lissée (< 0,85).", 6)
    if debug:
        print("[DEBUG] rmse", round(rmse, 4), "contrast", round(ctr, 3), "samples", samples, den, dn, pre, cy.denoising_input_passes)
    return r.finish()


if __name__ == "__main__":
    L.run(main)
