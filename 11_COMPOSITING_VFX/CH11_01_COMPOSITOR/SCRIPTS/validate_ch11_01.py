"""
validate_ch11_01.py — Correcteur « Compositor » (CH11.01).
Usage : … --python-exit-code 1 --python validate_ch11_01.py -- --exercise compositor [--debug]
Objets : Ball, Floor, SUN (0,6 W/m²), CAM. Le correcteur lit l'ARBRE de compositing (scene.compositing_node_group) et RENDU (Cycles CPU, 128 × 72, 2 échantillons, sans débruitage, compositing de l'élève ; graines 0 et 1) :
  structure : arbre présent avec un nœud Render Layers, un nœud Group Output relié, et AUCUN nœud orphelin (tout nœud mène à la sortie) ; Render Properties : use_compositing activé ;
  luminance moyenne de l'image finale de 0,35 à 0,65 (départ 0,277 ; solution 0,459) ;
  bruit : écart-type de la différence des deux rendus (graines 0 et 1) sur le sol (rangées 52–69, colonnes 5–39) / √2 ≤ 0,012 (exposition seule 0,029 ; solution 0,0063) ;
  lisibilité : (luminance du centre de la sphère − luminance du coin haut gauche) / luminance moyenne ≥ 0,65 (solution 0,81 ; Blur de 60 pixels 0,47).
La scène (SUN 0,6 W/m²) ne doit pas être modifiée.
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
    p = os.path.join(tempfile.gettempdir(), f"bcma_ch1101_val{seed}.png")
    sc.render.filepath = p
    bpy.ops.render.render(write_still=True)
    im = bpy.data.images.load(p)
    px = np.array(im.pixels[:], np.float32).reshape(72, 128, 4)[..., :3][::-1].copy()
    bpy.data.images.remove(im)
    return px[..., 0] * 0.2126 + px[..., 1] * 0.7152 + px[..., 2] * 0.0722


def main():
    debug = L.flag("--debug")
    r = L.Report("CH11.01 — Compositor")
    if not r.check(all(bpy.data.objects.get(n) for n in ("Ball", "Floor", "SUN", "CAM")), "Ball, Floor, SUN et CAM présents", "Partez du fichier de départ.", 2):
        return r.finish()
    sc = bpy.context.scene
    r.check(abs(bpy.data.objects["SUN"].data.energy - 0.6) < 1e-3, "Scène inchangée : SUN 0,6 W/m²", "Travaillez dans le compositeur, pas dans la scène.", 3)
    ng = sc.compositing_node_group
    if not r.check(ng is not None, "Arbre de compositing présent (scene.compositing_node_group)", "Compositing : New dans l'éditeur Compositor.", 4):
        return r.finish()
    rls = [n for n in ng.nodes if n.bl_idname == "CompositorNodeRLayers"]
    outs = [n for n in ng.nodes if n.bl_idname == "NodeGroupOutput"]
    linked_out = bool(outs) and any(l.to_node == outs[0] for l in ng.links)
    r.check(bool(rls) and linked_out, f"Render Layers : {len(rls)} ; Group Output relié : {'oui' if linked_out else 'non'}", "Render Layers → … → Group Output.", 5)
    reach, todo = set(), list(outs)
    while todo:
        n = todo.pop()
        if n in reach:
            continue
        reach.add(n)
        todo += [l.from_node for l in ng.links if l.to_node == n]
    orphans = [n.name for n in ng.nodes if n not in reach]
    r.check(not orphans, "Aucun nœud orphelin" if not orphans else f"Nœuds orphelins : {', '.join(orphans)}", "Supprimez ou reliez les nœuds qui ne mènent pas à la sortie.", 5)
    r.check(sc.render.use_compositing, f"Compositing de rendu : {'activé' if sc.render.use_compositing else 'désactivé'}", "Render Properties / Output : activez Compositing.", 4)
    sc.render.engine = "CYCLES"
    sc.cycles.device = "CPU"
    sc.cycles.samples = 2
    sc.cycles.use_denoising = False
    sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage = 128, 72, 100
    sc.render.image_settings.file_format = "PNG"
    sc.render.image_settings.color_mode = "RGB"
    a, b = lum(sc, 0), lum(sc, 1)
    mean = float(a.mean())
    flat = (slice(52, 70), slice(5, 40))
    noise = float(np.std(a[flat] - b[flat]) / math.sqrt(2.0))
    rel = float((a[32:40, 60:68].mean() - a[2:10, 2:10].mean()) / max(mean, 1e-6))
    r.check(0.35 <= mean <= 0.65, f"Luminance moyenne : {mean:.3f} (0,35–0,65)", "Nœud Exposure : augmentez la prise Exposure (diaphragmes).", 8)
    r.check(noise <= 0.012, f"Bruit : {noise:.4f} (≤ 0,012)", "Nœud Blur : prise Size (pixels).", 8)
    r.check(rel >= 0.65, f"Lisibilité de la sphère : (centre − coin) / moyenne = {rel:.2f} (≥ 0,65)", "Un flou trop fort efface la sphère : réduisez Size.", 6)
    if debug:
        print("[DEBUG] mean", round(mean, 3), "noise", round(noise, 4), "rel", round(rel, 3), "nodes", [n.bl_idname for n in ng.nodes])
    return r.finish()


if __name__ == "__main__":
    L.run(main)
