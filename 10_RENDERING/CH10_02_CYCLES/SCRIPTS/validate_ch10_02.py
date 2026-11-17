"""
validate_ch10_02.py — Correcteur « Cycles en profondeur » (CH10.02).
Usage : … --python-exit-code 1 --python validate_ch10_02.py -- --exercise cycles [--debug]
Objets : Room, Light (zone 1 × 1 m, 20 W, orientée vers le bas), CAM. Le correcteur rend la scène avec les RÉGLAGES CYCLES de l'élève (moteur Cycles CPU, débruitage désactivé, résolution 128 × 72 imposés ; graine 0 puis 1) et mesure :
  lumière indirecte : luminance moyenne du plafond (rangées 2 à 9, colonnes 40 à 89) ≥ 0,1 (Diffuse 0 : 0,013 ; Diffuse 4 : 0,33) ;
  bruit : écart-type de la différence des deux rendus (deux graines) sur le mur du fond, divisé par √2 ≤ 0,02 (solution 0,0097 ; 4 échantillons 0,049) ;
  échantillonnage adaptatif activé, Noise Threshold ≤ 0,05, Max Samples de 32 à 256.
La scène (Light 20 W) ne doit pas être modifiée.
Testé avec : Blender 5.3.0.
"""
import math
import os
import sys
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bpy  # noqa: E402
import numpy as np  # noqa: E402


def lum(sc, seed):
    sc.cycles.seed = seed
    p = os.path.join(tempfile.gettempdir(), f"bcma_ch1002_val{seed}.png")
    sc.render.filepath = p
    bpy.ops.render.render(write_still=True)
    im = bpy.data.images.load(p)
    px = np.array(im.pixels[:], np.float32).reshape(72, 128, 4)[..., :3][::-1].copy()
    bpy.data.images.remove(im)
    return px[..., 0] * 0.2126 + px[..., 1] * 0.7152 + px[..., 2] * 0.0722


def main():
    debug = L.flag("--debug")
    r = L.Report("CH10.02 — Cycles en profondeur")
    if not r.check(all(bpy.data.objects.get(n) for n in ("Room", "Light", "CAM")), "Room, Light et CAM présents", "Partez du fichier de départ.", 2):
        return r.finish()
    sc = bpy.context.scene
    r.check(abs(bpy.data.objects["Light"].data.energy - 20.0) < 1e-3, "Scène inchangée : Light 20 W", "Réglez Cycles, pas la scène.", 3)
    cy = sc.cycles
    sc.render.engine = "CYCLES"
    cy.device = "CPU"
    cy.use_denoising = False
    sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage = 128, 72, 100
    sc.render.image_settings.file_format = "PNG"
    sc.render.image_settings.color_mode = "RGB"
    a, b = lum(sc, 0), lum(sc, 1)
    ceil = float(a[2:10, 40:90].mean())
    wall = (slice(30, 50), slice(50, 80))
    noise = float(np.std(a[wall] - b[wall]) / math.sqrt(2.0))
    r.check(ceil >= 0.1, f"Lumière indirecte : plafond à {ceil:.2f} (≥ 0,1) ; Diffuse = {cy.diffuse_bounces} rebonds", "Light Paths > Max Bounces > Diffuse ≥ 2.", 8)
    r.check(cy.use_adaptive_sampling, "Échantillonnage adaptatif activé (Noise Threshold coché)", "Sampling > Render : cochez la case de l'en-tête.", 5)
    r.check(cy.adaptive_threshold <= 0.05, f"Noise Threshold : {cy.adaptive_threshold:.3f} (≤ 0,05)", "Un seuil plus bas donne moins de bruit et plus de temps.", 5)
    r.check(32 <= cy.samples <= 256, f"Max Samples : {cy.samples} (32–256)", "Sampling > Render > Max Samples.", 5)
    r.check(noise <= 0.02, f"Bruit mesuré sur le mur : {noise:.4f} (≤ 0,02)", "Plus d'échantillons ou un seuil plus bas.", 8)
    if debug:
        print("[DEBUG] ceil", round(ceil, 3), "noise", round(noise, 4), "diffuse", cy.diffuse_bounces, "adaptive", cy.use_adaptive_sampling, cy.adaptive_threshold, "samples", cy.samples)
    return r.finish()


if __name__ == "__main__":
    L.run(main)
