"""
validate_ch11_06.py — Correcteur « Color grading » (CH11.06).
Usage : … --python-exit-code 1 --python validate_ch11_06.py -- --exercise grading [--debug]
Objets : Chart (rampe de gris 0 → 1, émissive), CAM (orthographique). Le correcteur lit l'arbre de compositing et rend l'image deux fois (Cycles CPU, 160 × 90, 1 échantillon, Standard) : avec le compositing de l'élève et avec le compositing désactivé (référence non étalonnée) ; il mesure :
  structure : arbre relié à Group Output, aucun nœud orphelin, compositing de rendu activé ;
  ombres (colonnes 4–31) : bleu − rouge ≥ 0,05 (solution 0,11 ; départ 0) ; hautes lumières (colonnes 128–155) : rouge − bleu ≥ 0,03 (solution 0,060) ;
  exposition : |luminance moyenne étalonnée − luminance moyenne de la référence| ≤ 0,08 (solution −0,001 ; Gain trop fort : +0,12).
Testé avec : Blender 5.3.0.
"""
import os
import sys
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bpy  # noqa: E402
import numpy as np  # noqa: E402


def render(sc, compositing, tag):
    keep = sc.render.use_compositing
    sc.render.use_compositing = compositing
    p = os.path.join(tempfile.gettempdir(), f"bcma_ch1106_val_{tag}.png")
    sc.render.filepath = p
    bpy.ops.render.render(write_still=True)
    sc.render.use_compositing = keep
    im = bpy.data.images.load(p)
    px = np.array(im.pixels[:], np.float32).reshape(90, 160, 4)[..., :3][::-1].copy()
    bpy.data.images.remove(im)
    return px


def main():
    debug = L.flag("--debug")
    r = L.Report("CH11.06 — Color grading")
    O = bpy.data.objects
    if not r.check(O.get("Chart") is not None and O.get("CAM") is not None, "Chart et CAM présents", "Partez du fichier de départ.", 2):
        return r.finish()
    sc = bpy.context.scene
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
    r.check(not orphans and bool(outs) and any(l.to_node == outs[0] for l in ng.links), "Arbre relié, aucun nœud orphelin" if not orphans else f"Nœuds orphelins : {', '.join(orphans)}", "Chaque nœud doit mener à Group Output.", 4)
    r.check(sc.render.use_compositing, f"Compositing de rendu : {'activé' if sc.render.use_compositing else 'désactivé'}", "Output > Post Processing > Pipeline : Compositing.", 3)
    sc.render.engine = "CYCLES"
    sc.cycles.device = "CPU"
    sc.cycles.samples = 1
    sc.cycles.use_denoising = False
    sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage = 160, 90, 100
    sc.render.image_settings.file_format = "PNG"
    sc.render.image_settings.color_mode = "RGB"
    graded, ref = render(sc, True, "g"), render(sc, False, "r")
    ymean = lambda a: float((a[..., 0] * 0.2126 + a[..., 1] * 0.7152 + a[..., 2] * 0.0722).mean())
    sh, hl = graded[:, 4:32].reshape(-1, 3).mean(axis=0), graded[:, 128:156].reshape(-1, 3).mean(axis=0)
    cool, warm, dy = float(sh[2] - sh[0]), float(hl[0] - hl[2]), ymean(graded) - ymean(ref)
    r.check(cool >= 0.05, f"Ombres froides : bleu − rouge = {cool:+.3f} (≥ 0,05)", "Couleur de Lift vers le bleu (Color Balance, Lift/Gamma/Gain).", 8)
    r.check(warm >= 0.03, f"Hautes lumières chaudes : rouge − bleu = {warm:+.3f} (≥ 0,03)", "Couleur de Gain vers l'orange.", 8)
    r.check(abs(dy) <= 0.08, f"Exposition préservée : écart de luminance moyenne {dy:+.3f} (± 0,08)", "Ne changez pas la luminosité globale : Gain proche de 1 en moyenne.", 8)
    if debug:
        print("[DEBUG] cool", round(cool, 4), "warm", round(warm, 4), "dY", round(dy, 4))
    return r.finish()


if __name__ == "__main__":
    L.run(main)
