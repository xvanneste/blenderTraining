"""
validate_ch09_08.py — Correcteur « Objectifs et focales » (CH09.08).
Usage : … --python-exit-code 1 --python validate_ch09_08.py -- --exercise lenses [--debug]
Objets : Ground, Subject (cylindre rouge, ne doit pas bouger : (-0,4, 8, 0,9) à 1 cm), Backdrop (cylindre vert, (0,4, 16, 0,9) à 1 cm), CAM.
Le correcteur rend lui-même un Workbench plat de 160 × 90 (couleurs d'objet) et segmente par couleur :
  hauteur du sujet = 40 % de l'image (± 5 %) ; rapport hauteur du fond / hauteur du sujet ≥ 0,72 (départ : 0,46 mesuré, valeur théorique 0,5 ; solution : 0,78, théorique 0,8) ;
  focale de la caméra ≥ 70 mm (téléobjectif).
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
from mathutils import Vector  # noqa: E402


def main():
    debug = L.flag("--debug")
    r = L.Report("CH09.08 — Objectifs et focales")
    sub, bk, cam, gr = (bpy.data.objects.get(n) for n in ("Subject", "Backdrop", "CAM", "Ground"))
    if not r.check(all((sub, bk, cam, gr)), "Subject, Backdrop, Ground et CAM présents", "Partez du fichier de départ.", 2):
        return r.finish()
    ok = (sub.matrix_world.translation - Vector((-0.4, 8, 0.9))).length <= 0.01 and (bk.matrix_world.translation - Vector((0.4, 16, 0.9))).length <= 0.01
    r.check(ok, "Les cylindres n'ont pas bougé", "Ne déplacez que la caméra : Subject à (-0,4, 8, 0,9), Backdrop à (0,4, 16, 0,9).", 3)
    sc = bpy.context.scene
    sc.render.engine = "BLENDER_WORKBENCH"
    sc.view_settings.view_transform = "Standard"
    sc.view_settings.look = "None"
    sh = sc.display.shading
    sh.light, sh.color_type = "FLAT", "OBJECT"
    sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage = 160, 90, 100
    sc.camera = cam
    sc.render.image_settings.file_format = "PNG"
    sc.render.image_settings.color_mode = "RGB"
    path = os.path.join(tempfile.gettempdir(), "bcma_ch0908_val.png")
    sc.render.filepath = path
    bpy.ops.render.render(write_still=True)
    im = bpy.data.images.load(path)
    px = np.array(im.pixels[:], np.float32).reshape(90, 160, 4)[..., :3][::-1].copy()
    bpy.data.images.remove(im)
    Rr, G, B = px[..., 0], px[..., 1], px[..., 2]
    red = (Rr > 0.7) & (G < 0.3) & (B < 0.3)
    green = (G > 0.7) & (Rr < 0.3) & (B < 0.3)
    H = red.shape[0]

    def height(m):
        ys = np.nonzero(m)[0]
        return (ys.max() + 1 - ys.min()) / H if len(ys) else 0.0
    hs, hb = height(red), height(green)
    if not r.check(red.sum() >= 5 and green.sum() >= 5, f"Sujet ({int(red.sum())} px) et fond ({int(green.sum())} px) visibles", "Un des cylindres est hors cadre ou trop petit : recadrez.", 6):
        return r.finish()
    ratio = hb / hs
    r.check(abs(hs - 0.40) <= 0.05, f"Hauteur du sujet : {100 * hs:.0f} % de l'image (40 % ± 5)", "Focale ≈ hauteur voulue × distance × 20,25 / 1,8 (distance = 8 + recul).", 8)
    r.check(ratio >= 0.72, f"Compression : le fond fait {100 * ratio:.0f} % de la hauteur du sujet (≥ 72 %)", "Reculez la caméra : rapport = (8 + c) / (16 + c).", 8)
    f = cam.data.lens
    fov = math.degrees(cam.data.angle_x)
    r.check(f >= 70, f"Téléobjectif : {f:.0f} mm, champ horizontal {fov:.1f}° (focale ≥ 70 mm)", "Camera > Lens > Focal Length.", 5)
    if debug:
        print("[DEBUG] sujet", round(hs, 3), "fond", round(hb, 3), "ratio", round(ratio, 3), "f", f, "y cam", round(cam.location.y, 2))
    return r.finish()


if __name__ == "__main__":
    L.run(main)
