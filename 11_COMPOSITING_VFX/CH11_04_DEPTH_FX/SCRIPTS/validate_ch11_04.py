"""
validate_ch11_04.py — Correcteur « Depth, defocus, motion blur » (CH11.04).
Usage : … --python-exit-code 1 --python validate_ch11_04.py -- --exercise depth_fx [--debug]
Objets : Near (fixe, 5 m), Mover (5 m, animée en x de −0,5 à 0,5 entre les images 1 et 21), Far (fixe, 30 m), CAM (135 mm). Le correcteur lit l'arbre de compositing et rend l'IMAGE 10 (Cycles CPU, 320 × 180, 4 échantillons, sans débruitage, sans flou de mouvement de rendu, compositing de l'élève) :
  structure : arbre relié à Group Output, aucun nœud orphelin, compositing de rendu activé ;
  profondeur de champ en post : pic de Near (colonnes 0–99, rangées 80–99 moyennées, moins le fond) ≥ 0,9 ; pic de Far (colonnes 200–319) ≤ 0,5 (départ 0,92 ; solution 0,30) ;
  flou de mouvement en post : largeur de Mover (colonnes 110–199, pixels au-dessus de 0,05 de fond) de 18 à 45 pixels (sans flou : 12 ; solution : 27).
La scène (positions, focale 135 mm) ne doit pas être modifiée.
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
    r = L.Report("CH11.04 — Depth, defocus, motion blur")
    O = bpy.data.objects
    if not r.check(all(O.get(n) for n in ("Near", "Mover", "Far", "CAM")), "Near, Mover, Far et CAM présents", "Partez du fichier de départ.", 2):
        return r.finish()
    sc = bpy.context.scene
    r.check(abs(O["CAM"].data.lens - 135) < 0.5 and abs(O["Far"].location.y - 30) < 1e-3 and abs(O["Near"].location.y - 5) < 1e-3, "Scène inchangée : caméra 135 mm, Near à 5 m, Far à 30 m", "Réglez le compositeur et la mise au point, pas la scène.", 3)
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
    sc.cycles.samples = 4
    sc.cycles.use_denoising = False
    sc.render.use_motion_blur = False
    sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage = 320, 180, 100
    sc.render.image_settings.file_format = "PNG"
    sc.render.image_settings.color_mode = "RGB"
    sc.frame_set(10)
    p = os.path.join(tempfile.gettempdir(), "bcma_ch1104_val.png")
    sc.render.filepath = p
    bpy.ops.render.render(write_still=True)
    im = bpy.data.images.load(p)
    px = np.array(im.pixels[:], np.float32).reshape(180, 320, 4)[..., :3][::-1].copy()
    bpy.data.images.remove(im)
    y = px[..., 0] * 0.2126 + px[..., 1] * 0.7152 + px[..., 2] * 0.0722
    band = y[80:100].mean(axis=0)
    bg = float(np.median(band))
    near, far, w = float(band[:100].max() - bg), float(band[200:].max() - bg), int((band[110:200] - bg > 0.05).sum())
    r.check(near >= 0.9, f"Near nette : pic {near:.2f} (≥ 0,9) ; mise au point de la caméra {O['CAM'].data.dof.focus_distance:.1f} m", "Camera > Depth of Field > Focus Distance : 5 m.", 8)
    r.check(far <= 0.5, f"Far floue : pic {far:.2f} (≤ 0,5)", "Nœud Defocus : Z ← Depth, Use Z-Buffer, F-stop 1.", 8)
    r.check(18 <= w <= 45, f"Mover étalée : {w} pixels de large (18–45 ; sans flou : 12)", "Nœud Vector Blur : Speed ← Vector, Depth ← Depth, Shutter ≥ 0,7.", 8)
    if debug:
        print("[DEBUG] near", round(near, 3), "far", round(far, 3), "w", w)
    return r.finish()


if __name__ == "__main__":
    L.run(main)
