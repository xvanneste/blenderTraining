"""
validate_ch11_03.py — Correcteur « Masques et Cryptomatte » (CH11.03).
Usage : … --python-exit-code 1 --python validate_ch11_03.py -- --exercise masks [--debug]
Objets : Sphere_A (rouge, Pass Index 1), Sphere_B (verte, 2), Sphere_C (bleue, 3), SUN, CAM. Le correcteur lit l'arbre de compositing et rend (Cycles CPU, 192 × 72, 16 échantillons, sans débruitage, compositing de l'élève) :
  structure : arbre relié à Group Output ; au moins un nœud de masque (ID Mask ou Cryptomatte) ; aucun nœud orphelin ; compositing de rendu activé ;
  saturation HSV moyenne : sur Sphere_B (colonnes 90–101, rangées 30–41) ≥ 0,4 (départ : 0,59) ; sur Sphere_A (42–53) et Sphere_C (138–149) ≤ 0,1 (départ 0,47 et 0,42) ; sur le fond (rangées 2–9) ≤ 0,1.
Les Pass Index des sphères (1, 2, 3) ne doivent pas être modifiés.
Testé avec : Blender 5.3.0.
"""
import colorsys
import os
import sys
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bpy  # noqa: E402
import numpy as np  # noqa: E402


def sat(patch):
    m = patch.reshape(-1, 3).mean(axis=0)
    return colorsys.rgb_to_hsv(*[float(t) for t in m])[1]


def main():
    debug = L.flag("--debug")
    r = L.Report("CH11.03 — Masques et Cryptomatte")
    O = bpy.data.objects
    names = ("Sphere_A", "Sphere_B", "Sphere_C")
    if not r.check(all(O.get(n) for n in names + ("SUN", "CAM")), "Sphere_A, Sphere_B, Sphere_C, SUN et CAM présents", "Partez du fichier de départ.", 2):
        return r.finish()
    sc = bpy.context.scene
    r.check([O[n].pass_index for n in names] == [1, 2, 3], f"Pass Index inchangés : {[O[n].pass_index for n in names]}", "Ne modifiez pas les index : le masque en dépend.", 3)
    ng = sc.compositing_node_group
    if not r.check(ng is not None, "Arbre de compositing présent", "Partez du fichier de départ.", 3):
        return r.finish()
    outs = [n for n in ng.nodes if n.bl_idname == "NodeGroupOutput"]
    reach, todo = set(), list(outs)
    while todo:
        n = todo.pop()
        if n in reach:
            continue
        reach.add(n)
        todo += [l.from_node for l in ng.links if l.to_node == n]
    orphans = [n.name for n in ng.nodes if n not in reach]
    has_mask = any(n.bl_idname in ("CompositorNodeIDMask", "CompositorNodeCryptomatteV2", "CompositorNodeCryptomatte") for n in reach)
    r.check(has_mask, "Un nœud de masque (ID Mask ou Cryptomatte) alimente la sortie", "Ajoutez un nœud ID Mask (Index 2) ou Cryptomatte.", 6)
    r.check(not orphans and bool(outs), "Arbre relié, aucun nœud orphelin" if not orphans else f"Nœuds orphelins : {', '.join(orphans)}", "Chaque nœud doit mener à Group Output.", 4)
    r.check(sc.render.use_compositing, f"Compositing de rendu : {'activé' if sc.render.use_compositing else 'désactivé'}", "Output > Post Processing > Pipeline : Compositing.", 3)
    sc.render.engine = "CYCLES"
    sc.cycles.device = "CPU"
    sc.cycles.samples = 16
    sc.cycles.use_denoising = False
    sc.cycles.seed = 0
    sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage = 192, 72, 100
    sc.render.image_settings.file_format = "PNG"
    sc.render.image_settings.color_mode = "RGB"
    p = os.path.join(tempfile.gettempdir(), "bcma_ch1103_val.png")
    sc.render.filepath = p
    bpy.ops.render.render(write_still=True)
    im = bpy.data.images.load(p)
    px = np.array(im.pixels[:], np.float32).reshape(72, 192, 4)[..., :3][::-1].copy()
    bpy.data.images.remove(im)
    s = {"A": sat(px[30:42, 42:54]), "B": sat(px[30:42, 90:102]), "C": sat(px[30:42, 138:150]), "bg": sat(px[2:10, 2:190])}
    r.check(s["B"] >= 0.4, f"Sphere_B garde sa couleur : saturation {s['B']:.2f} (≥ 0,4)", "Le masque doit laisser passer l'image d'origine sur la sphère verte.", 8)
    r.check(s["A"] <= 0.1 and s["C"] <= 0.1, f"Sphere_A et Sphere_C en gris : saturations {s['A']:.2f} et {s['C']:.2f} (≤ 0,1)", "Le fond désaturé doit couvrir les deux autres sphères.", 8)
    r.check(s["bg"] <= 0.1, f"Fond gris : saturation {s['bg']:.2f} (≤ 0,1)", "Le fond est déjà peu saturé : ne le colorez pas.", 4)
    if debug:
        print("[DEBUG]", {k: round(v, 3) for k, v in s.items()}, [n.bl_idname for n in ng.nodes])
    return r.finish()


if __name__ == "__main__":
    L.run(main)
