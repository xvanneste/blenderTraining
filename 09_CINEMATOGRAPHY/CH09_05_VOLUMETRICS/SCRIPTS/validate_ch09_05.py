"""
validate_ch09_05.py — Correcteur « Volumétrie » (CH09.05).
Usage : … --python-exit-code 1 --python validate_ch09_05.py -- --exercise volumetrics [--debug]
Objets : Fog (cube de volume), Floor, LIGHT_Spot, CAM.
  Configuration : un Principled Volume relié à la sortie Volume du matériau de Fog ; spot de 1 000 W ou plus, d'angle 60° ou moins.
  Rendu (Cycles CPU, 96 × 96, 64 échantillons, EXR linéaire, fichier temporaire) : luminance du centre de l'image (colonnes centrales, tiers médian : le faisceau) de 0,03 à 0,4 ;
          centre au moins 4 fois plus lumineux que les bords (le brouillard hors faisceau).
Testé avec : Blender 5.3.0.
"""
import os
import sys
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bpy  # noqa: E402
import numpy as np  # noqa: E402


def render(res=96, samples=64):
    sc = bpy.context.scene
    sc.render.engine = "CYCLES"
    sc.cycles.device = "CPU"
    sc.cycles.use_denoising = False
    sc.cycles.samples = samples
    sc.render.resolution_x = sc.render.resolution_y = res
    sc.render.resolution_percentage = 100
    sc.render.image_settings.file_format = "OPEN_EXR"
    sc.render.image_settings.color_depth = "32"
    p = os.path.join(tempfile.gettempdir(), "bcma_ch0905_val.exr")
    sc.render.filepath = p
    bpy.ops.render.render(write_still=True)
    im = bpy.data.images.load(p)
    px = np.array(im.pixels[:], np.float32).reshape(res, res, 4)[..., :3].copy()
    bpy.data.images.remove(im)
    return px


def main():
    debug = L.flag("--debug")
    r = L.Report("CH09.05 — Volumétrie")
    fog, spot = bpy.data.objects.get("Fog"), bpy.data.objects.get("LIGHT_Spot")
    if not r.check(fog is not None and spot is not None and all(bpy.data.objects.get(n) for n in ("Floor", "CAM")), "Fog, Floor, LIGHT_Spot et CAM présents", "Partez du fichier de départ.", 2):
        return r.finish()
    ok, dens = False, 0.0
    for mat in fog.data.materials:
        if mat and mat.node_tree:
            for n in mat.node_tree.nodes:
                if n.type == "OUTPUT_MATERIAL" and n.inputs["Volume"].links and n.inputs["Volume"].links[0].from_node.type == "PRINCIPLED_VOLUME":
                    ok = True
                    dens = n.inputs["Volume"].links[0].from_node.inputs["Density"].default_value
    r.check(ok, f"Brouillard : Principled Volume relié à la sortie Volume : {'oui' if ok else 'non'} (Density {dens:.3f})", "Matériau de Fog : Principled Volume > Volume.", 6)
    ld = spot.data
    r.check(ld.type == "SPOT" and ld.energy >= 1000 and ld.spot_size <= 1.0472, f"Spot : {ld.type}, {ld.energy:.0f} W (≥ 1 000), angle {ld.spot_size * 57.2958:.0f}° (≤ 60°)", "Ne changez pas le spot (3 000 W, 40°).", 5)
    px = render()
    Y = px[..., 0] * 0.2126 + px[..., 1] * 0.7152 + px[..., 2] * 0.0722
    R = Y.shape[0]
    rows = slice(R // 3, 2 * R // 3)
    centre = float(Y[rows, R // 2 - 4:R // 2 + 5].mean())
    edge = float(np.concatenate([Y[rows, 4:14], Y[rows, R - 14:R - 4]], axis=1).mean())
    ratio = centre / max(edge, 1e-6)
    r.check(0.03 <= centre <= 0.4, f"Faisceau : luminance du centre {centre:.3f} (0,03–0,4 : lisible sans noyer l'image)", "Density ≈ 0,08 : ni trop mince (invisible) ni trop dense (opaque).", 9)
    r.check(ratio >= 4, f"Contraste faisceau / bords : {ratio:.0f} (≥ 4)", "Le faisceau se détache du brouillard hors cône.", 5)
    if debug:
        print("[DEBUG] density", round(dens, 4), "centre", round(centre, 4), "bords", round(edge, 5), "ratio", round(ratio, 1), "spot", ld.type, ld.energy, round(ld.spot_size * 57.2958))
    return r.finish()


if __name__ == "__main__":
    L.run(main)
