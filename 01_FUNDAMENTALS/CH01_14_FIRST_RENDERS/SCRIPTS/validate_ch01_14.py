"""
validate_ch01_14.py — Correcteur du premier rendu final (CH01.14).
Vérifie les réglages ET la présence de l'image rendue renders/ch01_14_final.png à côté du .blend.
Usage : blender -b --factory-startup <fichier.blend> --python-exit-code 1 --python validate_ch01_14.py -- --exercise final
Testé avec : Blender 5.3.0.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bpy  # noqa: E402


def main():
    r = L.Report("CH01.14 — Le premier rendu final")
    sc = bpy.context.scene
    rd, cy, im, vs = sc.render, sc.cycles, sc.render.image_settings, sc.view_settings
    r.check(rd.engine == "CYCLES" and cy.device in {"CPU", "GPU"},
            f"Cycles, périphérique {cy.device}", "Render Properties > Render Engine > Cycles.", 2)
    r.check(cy.use_adaptive_sampling and abs(cy.adaptive_threshold - 0.02) < 1e-4 and cy.samples == 128,
            f"Échantillonnage : seuil {cy.adaptive_threshold:.3f}, max {cy.samples}",
            "Sampling > Render : Noise Threshold 0.02, Max Samples 128.", 2)
    r.check(cy.use_denoising, "Débruitage activé", "Sampling > Render > Denoise.", 1)
    r.check((rd.resolution_x, rd.resolution_y, rd.resolution_percentage) == (1920, 1080, 100), "1920 × 1080 à 100 %",
            "Output > Format.", 1)
    r.check(im.file_format == "PNG" and im.color_mode == "RGB" and im.color_depth == "8", "PNG RGB 8 bits",
            "Output > Output > File Format / Color / Color Depth.", 1)
    r.check(rd.filepath.replace("\\", "/").startswith("//renders/"), f"Sortie relative //renders/ ({rd.filepath})",
            "Output > Output : //renders/ch01_14_final_", 1)
    r.check(vs.view_transform == "AgX" and vs.look == "AgX - Medium High Contrast", f"AgX + Look ({vs.look})",
            "Render > Color Management > View Transform, Look.", 2)
    png = bpy.path.abspath("//renders/ch01_14_final.png")
    ok = os.path.exists(png)
    if ok:
        img = bpy.data.images.load(png)
        size = tuple(img.size)
        bpy.data.images.remove(img)
    r.check(ok and size == (1920, 1080), f"Image renders/ch01_14_final.png présente en 1920 × 1080 ({'trouvée ' + str(size) if ok else 'absente'})",
            "F12 puis Image > Save As dans le dossier renders à côté du .blend.", 3)
    lum = L.mean_luminance(png) if ok else 0
    r.check(ok and 0.05 < lum < 0.8, f"Image ni noire ni brûlée (luminance {lum:.2f})", "Revoir l'éclairage ou l'exposition.", 1)
    r.check(os.path.exists(bpy.path.abspath("//renders/ch01_14_eevee.png")), "Bonus : comparaison EEVEE enregistrée",
            "renders/ch01_14_eevee.png", 1, mandatory=False)
    return r.finish()


if __name__ == "__main__":
    L.run(main)
