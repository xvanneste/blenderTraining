"""
validate_ch09_09.py — Correcteur « Profondeur de champ » (CH09.09).
Usage : … --python-exit-code 1 --python validate_ch09_09.py -- --exercise dof [--debug]
Objets : Near (barre émissive, ne doit pas bouger : (-0,25, 5, 0,9) à 1 cm), Far ((0,6, 30, 0,9) à 1 cm), CAM (focale 200 mm, position inchangée).
Le correcteur rend lui-même (Cycles CPU, 320 × 180, 32 échantillons, sans débruitage) et mesure le « pic » de chaque barre :
  moyenne des lignes centrales (80 à 99), maximum de la moitié gauche (Near) ou droite (Far) moins la valeur médiane du fond.
  Une barre nette atteint 1,0 ; le flou étale la lumière et baisse le pic.
  Near nette : pic ≥ 0,9 ; Far floue : pic ≤ 0,5 (mesuré : solution 1,00 et 0,31 ; départ 1,00 et 1,00).
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


def main():
    debug = L.flag("--debug")
    r = L.Report("CH09.09 — Profondeur de champ")
    near, far, cam = (bpy.data.objects.get(n) for n in ("Near", "Far", "CAM"))
    if not r.check(all((near, far, cam)), "Near, Far et CAM présents", "Partez du fichier de départ.", 2):
        return r.finish()
    ok = (near.matrix_world.translation - Vector((-0.25, 5, 0.9))).length <= 0.01 and (far.matrix_world.translation - Vector((0.6, 30, 0.9))).length <= 0.01
    r.check(ok, "Les barres n'ont pas bougé", "Ne modifiez que la caméra.", 3)
    r.check((cam.matrix_world.translation - Vector((0, 0, 0.9))).length <= 0.01 and abs(cam.data.lens - 200) <= 0.5, f"Caméra inchangée : position et focale {cam.data.lens:.0f} mm", "La focale (200 mm) et la position restent celles du départ.", 3)
    d = cam.data.dof
    sc = bpy.context.scene
    sc.render.engine = "CYCLES"
    sc.cycles.device = "CPU"
    sc.cycles.samples = 32
    sc.cycles.use_denoising = False
    sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage = 320, 180, 100
    sc.camera = cam
    sc.render.image_settings.file_format = "PNG"
    sc.render.image_settings.color_mode = "RGB"
    path = os.path.join(tempfile.gettempdir(), "bcma_ch0909_val.png")
    sc.render.filepath = path
    bpy.ops.render.render(write_still=True)
    im = bpy.data.images.load(path)
    px = np.array(im.pixels[:], np.float32).reshape(180, 320, 4)[..., :3][::-1].copy()
    bpy.data.images.remove(im)
    Y = px[..., 0] * 0.2126 + px[..., 1] * 0.7152 + px[..., 2] * 0.0722
    band = Y[80:100].mean(axis=0)
    bg = float(np.median(band))
    pn, pf = float(band[:160].max() - bg), float(band[160:].max() - bg)
    r.check(d.use_dof, f"Depth of Field activée ; Focus Distance {d.focus_distance:.1f} m, F-Stop {d.aperture_fstop:.1f}", "Camera > Depth of Field : cochez-la.", 5)
    r.check(pn >= 0.9, f"Barre proche nette : pic {pn:.2f} (≥ 0,9)", "Focus Distance doit valoir 5 m (distance de Near).", 8)
    r.check(pf <= 0.5, f"Barre lointaine floue : pic {pf:.2f} (≤ 0,5)", "Ouvrez le diaphragme : F-Stop 1,0 ou moins.", 8)
    if debug:
        print("[DEBUG] near", round(pn, 3), "far", round(pf, 3), "bg", round(bg, 3), "dof", d.use_dof, d.focus_distance, d.aperture_fstop)
    return r.finish()


if __name__ == "__main__":
    L.run(main)
