"""
validate_ch09_03.py — Correcteur « Naturel et HDRI » (CH09.03).
Usage : … --python-exit-code 1 --python validate_ch09_03.py -- --exercise hdri [--debug]
Objets : Ground, Pole, CAM (orthographique, au zénith) ; monde à nœuds.
  Configuration : une Environment Texture dotée d'une image FLOTTANTE (HDRI) est reliée (directement ou par un Mapping) à la couleur du Background, relié à la sortie du monde.
  Rendu (Cycles CPU, 128 × 128, 64 échantillons, EXR linéaire, fichier temporaire) :
    ombre du poteau (pixels de luminance < 50 % de la médiane, hors sommet du poteau) : au moins 30 pixels, orientée vers +X à ± 20° (le soleil vient de la gauche) ;
    luminance médiane du sol de 0,35 à 0,8 ; ombre bleutée (bleu / rouge ≥ 1,3 : elle n'est éclairée que par le ciel).
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


def render(res=128, samples=64):
    sc = bpy.context.scene
    sc.render.engine = "CYCLES"
    sc.cycles.device = "CPU"
    sc.cycles.use_denoising = False
    sc.cycles.samples = samples
    sc.render.resolution_x = sc.render.resolution_y = res
    sc.render.resolution_percentage = 100
    sc.render.image_settings.file_format = "OPEN_EXR"
    sc.render.image_settings.color_depth = "32"
    p = os.path.join(tempfile.gettempdir(), "bcma_ch0903_val.exr")
    sc.render.filepath = p
    bpy.ops.render.render(write_still=True)
    im = bpy.data.images.load(p)
    px = np.array(im.pixels[:], np.float32).reshape(res, res, 4)[..., :3].copy()
    bpy.data.images.remove(im)
    return px


def upstream(node, kind):
    """Cherche en amont d'un nœud un nœud du type donné."""
    seen, stack = set(), [node]
    while stack:
        n = stack.pop()
        if n in seen:
            continue
        seen.add(n)
        if n.type == kind:
            return n
        for i in n.inputs:
            for lk in i.links:
                stack.append(lk.from_node)
    return None


def main():
    debug = L.flag("--debug")
    r = L.Report("CH09.03 — Naturel et HDRI")
    sc = bpy.context.scene
    if not r.check(all(bpy.data.objects.get(n) for n in ("Ground", "Pole", "CAM")), "Ground, Pole et CAM présents", "Partez du fichier de départ.", 2):
        return r.finish()
    wo = sc.world
    nt = wo.node_tree if wo else None
    out = next((n for n in nt.nodes if n.type == "OUTPUT_WORLD"), None) if nt else None
    bg = out.inputs["Surface"].links[0].from_node if out and out.inputs["Surface"].links and out.inputs["Surface"].links[0].from_node.type == "BACKGROUND" else None
    env = upstream(bg, "TEX_ENVIRONMENT") if bg and bg.inputs["Color"].links else None
    img = env.image if env else None
    r.check(env is not None and img is not None, f"Environment Texture avec image reliée au Background : {'oui (' + img.name + ')' if img else 'non'}", "World > Surface : Color = Environment Texture.", 6)
    r.check(img is not None and img.is_float, f"Image à grande plage dynamique (flottante) : {'oui' if img and img.is_float else 'non'}", "Une image 8 bits écrête le soleil à 1 : pas d'ombre nette.", 6)
    px = render()
    R = px.shape[0]
    Y = px[..., 0] * 0.2126 + px[..., 1] * 0.7152 + px[..., 2] * 0.0722
    med = float(np.median(Y))
    mask = Y < 0.5 * med
    mask[R // 2 - 3:R // 2 + 4, R // 2 - 3:R // 2 + 4] = False
    ys, xs = np.nonzero(mask)
    n = len(xs)
    ang = math.degrees(math.atan2(ys.mean() - R / 2 + 0.5, xs.mean() - R / 2 + 0.5)) if n else 999.0
    shd = px[mask].mean(axis=0) if n else np.zeros(3)
    bR = float(shd[2] / max(shd[0], 1e-9)) if n else 0.0
    r.check(n >= 30 and abs(ang) <= 20, f"Ombre du poteau : {n} pixels (≥ 30), direction {ang:.0f}° (0° = vers +X, ± 20°)", "Mapping > Rotation Z : 180° amène le soleil à gauche.", 8)
    r.check(0.35 <= med <= 0.8, f"Exposition : luminance médiane du sol {med:.2f} (0,35–0,8)", "Background > Strength ≈ 1.", 6)
    r.check(n >= 30 and bR >= 1.3, f"Ombre bleutée : bleu / rouge = {bR:.2f} (≥ 1,3)", "L'ombre n'est éclairée que par le ciel bleu.", 4)
    if debug:
        print("[DEBUG] med", round(med, 3), "n", n, "ang", round(ang, 1), "b/r", round(bR, 2), "float", img.is_float if img else None)
    return r.finish()


if __name__ == "__main__":
    L.run(main)
