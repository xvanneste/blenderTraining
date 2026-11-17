"""
validate_ch09_07.py — Correcteur « Composition » (CH09.07).
Usage : … --python-exit-code 1 --python validate_ch09_07.py -- --exercise composition [--debug]
Objets : Ground, Subject (cylindre rouge, ne doit pas bouger : (0, 8, 0,9) à 1 cm), CAM. Le correcteur rend lui-même un Workbench plat de 160 × 90 (couleurs d'objet : sujet rouge, sol gris, ciel bleu) et segmente par couleur :
  centre du sujet à 33 % de la largeur (± 5 %) ; ligne d'horizon à 33 % de la hauteur à partir du haut (± 5 %, moyenne des colonnes sans le sujet) ;
  sujet entier dans le cadre (marges de 3 % ou plus de chaque côté) ; hauteur du sujet d'au moins 25 % de l'image.
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
    r = L.Report("CH09.07 — Composition")
    sc = bpy.context.scene
    sub, cam, gr = bpy.data.objects.get("Subject"), bpy.data.objects.get("CAM"), bpy.data.objects.get("Ground")
    if not r.check(sub is not None and cam is not None and gr is not None, "Subject, Ground et CAM présents", "Partez du fichier de départ.", 2):
        return r.finish()
    p0 = sub.matrix_world.translation
    r.check((p0 - __import__("mathutils").Vector((0, 8, 0.9))).length <= 0.01, f"Le sujet n'a pas bougé : ({p0.x:.2f}, {p0.y:.2f}, {p0.z:.2f})", "Recomposez avec la caméra seulement.", 3)
    sc.render.engine = "BLENDER_WORKBENCH"
    sc.view_settings.view_transform = "Standard"
    sc.view_settings.look = "None"
    sh = sc.display.shading
    sh.light, sh.color_type = "FLAT", "OBJECT"
    sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage = 160, 90, 100
    sc.camera = cam
    sc.render.image_settings.file_format = "PNG"
    sc.render.image_settings.color_mode = "RGB"
    path = os.path.join(tempfile.gettempdir(), "bcma_ch0907_val.png")
    sc.render.filepath = path
    bpy.ops.render.render(write_still=True)
    im = bpy.data.images.load(path)
    px = np.array(im.pixels[:], np.float32).reshape(90, 160, 4)[..., :3][::-1].copy()
    bpy.data.images.remove(im)
    Rr, G, B = px[..., 0], px[..., 1], px[..., 2]
    subj = (Rr > 0.7) & (G < 0.3) & (B < 0.3)
    sky = (B > 0.7) & (Rr < 0.7) & (G > 0.35)
    H, W = subj.shape
    ys, xs = np.nonzero(subj)
    if not r.check(len(xs) >= 20, f"Sujet visible dans l'image : {len(xs)} pixels (≥ 20)", "Le sujet est sorti du cadre.", 6):
        return r.finish()
    cx = (xs.mean() + 0.5) / W
    top, bot, left, right = ys.min() / H, (ys.max() + 1) / H, xs.min() / W, (xs.max() + 1) / W
    cols = [c for c in range(W) if not subj[:, c].any() and sky[:, c].any()]
    hor = float(np.mean([np.nonzero(sky[:, c])[0].max() + 1 for c in cols])) / H if cols else -1.0
    r.check(abs(cx - 1 / 3) <= 0.05, f"Sujet au tiers gauche : centre à {100 * cx:.0f} % de la largeur (33 % ± 5)", "Camera > Lens > Shift X ≈ +0,167.", 8)
    r.check(abs(hor - 1 / 3) <= 0.05, f"Horizon au tiers haut : à {100 * hor:.0f} % de la hauteur depuis le haut (33 % ± 5)", "Camera > Lens > Shift Y ≈ −0,1 (négatif : l'horizon monte).", 8)
    r.check(left >= 0.03 and right <= 0.97 and top >= 0.03 and bot <= 0.97, f"Sujet entier dans le cadre : marges gauche {100 * left:.0f} %, droite {100 * (1 - right):.0f} %, haut {100 * top:.0f} %, bas {100 * (1 - bot):.0f} % (≥ 3 %)", "Ne cadrez pas trop serré.", 5)
    r.check(bot - top >= 0.25, f"Taille du sujet : {100 * (bot - top):.0f} % de la hauteur (≥ 25 %)", "Ne reculez pas la caméra.", 5)
    if debug:
        print("[DEBUG] cx", round(cx, 3), "hor", round(hor, 3), "marges", round(left, 3), round(right, 3), round(top, 3), round(bot, 3), "h", round(bot - top, 3), "shift", cam.data.shift_x, cam.data.shift_y)
    return r.finish()


if __name__ == "__main__":
    L.run(main)
