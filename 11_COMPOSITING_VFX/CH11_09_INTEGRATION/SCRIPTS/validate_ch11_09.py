"""
validate_ch11_09.py — Correcteur « Intégration 3D/réel » (CH11.09).
Usage : … --python-exit-code 1 --python validate_ch11_09.py -- --exercise integration [--debug]
Données : image « plate » (320 × 180 : ciel, sol gris 0,55, poteau réel dont l'ombre tombe vers la DROITE), Cube (rouge, (0, 0, 0,5)), Floor, SUN (4 W/m²), CAM (0, −8, 3), 75°, 35 mm. Le correcteur lit l'arbre de compositing et rend (Cycles CPU, 320 × 180, 32 échantillons, sans débruitage, compositing de l'élève), puis compare l'image composée à la plaque :
  structure : arbre relié à Group Output, aucun nœud orphelin, compositing activé ;
  cube visible : au moins 500 pixels rouges (rouge − max(vert, bleu) ≥ 0,3), de couleur proche de (1 ; 0,42 ; 0,42) (écart moyen ≤ 0,15) ;
  ombre à DROITE : différence de luminance (image − plaque) du sol juste à droite du cube (colonnes x1 + 3 à x1 + 27, rangées de la base ± ) ≤ −0,04 (solution −0,067 ; ombre à gauche −0,004) ;
  côté GAUCHE inchangé : différence entre −0,03 et +0,03 (solution −0,003 ; ombre à gauche −0,062) ;
  sol lointain = plaque : différence (colonnes 20–69, rangées 140–169) entre −0,03 et +0,03 (solution 0,0 ; sol opaque +0,33).
La scène (position du Cube, SUN 4 W/m², caméra) ne doit pas être modifiée, sauf la rotation du SUN.
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

W, H = 320, 180


def lum(a):
    return a[..., 0] * 0.2126 + a[..., 1] * 0.7152 + a[..., 2] * 0.0722


def main():
    debug = L.flag("--debug")
    r = L.Report("CH11.09 — Intégration 3D/réel")
    O = bpy.data.objects
    if not r.check(all(O.get(n) for n in ("Cube", "Floor", "SUN", "CAM")) and bpy.data.images.get("plate") is not None, "Cube, Floor, SUN, CAM et la plaque présents", "Partez du fichier de départ.", 2):
        return r.finish()
    sc = bpy.context.scene
    ok = (O["Cube"].location - Vector((0, 0, 0.5))).length < 1e-3 and abs(O["SUN"].data.energy - 4) < 1e-3 and (O["CAM"].location - Vector((0, -8, 3))).length < 1e-3
    r.check(ok, "Scène inchangée : Cube, caméra, puissance du SUN", "Réglez le soleil (rotation), le sol, le film et le compositeur.", 3)
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
    sc.cycles.samples = 32
    sc.cycles.use_denoising = False
    sc.cycles.seed = 0
    sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage = W, H, 100
    sc.render.image_settings.file_format = "PNG"
    sc.render.image_settings.color_mode = "RGB"
    p = os.path.join(tempfile.gettempdir(), "bcma_ch1109_val.png")
    sc.render.filepath = p
    bpy.ops.render.render(write_still=True)
    im = bpy.data.images.load(p)
    px = np.array(im.pixels[:], np.float32).reshape(H, W, 4)[..., :3][::-1].copy()
    bpy.data.images.remove(im)
    pl = np.array(bpy.data.images["plate"].pixels[:], np.float32).reshape(H, W, 4)[..., :3][::-1].copy()
    red = (px[..., 0] - np.maximum(px[..., 1], px[..., 2])) >= 0.3
    ys, xs = np.nonzero(red)
    if not r.check(len(xs) >= 500, f"Cube visible : {len(xs)} pixels rouges (≥ 500)", "Le rendu doit montrer le cube (film transparent + Alpha Over : Foreground = Render Layers).", 8):
        return r.finish()
    col = float(np.abs(px[ys, xs].mean(axis=0) - np.array([1.0, 0.42, 0.42])).mean())
    r.check(col <= 0.15, f"Couleur du cube conservée : écart {col:.3f} (≤ 0,15)", "Ne modifiez pas la couleur du cube.", 4)
    x0, x1, y1 = int(xs.min()), int(xs.max()), int(ys.max())
    d = lambda a, b, c, e: float((lum(px[c:e, a:b]) - lum(pl[c:e, a:b])).mean())
    right, left, far = d(x1 + 3, min(x1 + 28, W), y1 - 8, y1 + 4), d(max(x0 - 28, 0), x0 - 3, y1 - 8, y1 + 4), d(20, 70, 140, 170)
    r.check(far >= -0.03 and far <= 0.03, f"Sol lointain = plaque : différence {far:+.3f} (± 0,03)", "Floor doit être un Shadow Catcher et le film transparent : le sol 3D ne doit pas se voir.", 8)
    r.check(right <= -0.04, f"Ombre à DROITE du cube : différence {right:+.3f} (≤ −0,04)", "SUN : rotation X 50°, Z −50° (soleil à gauche, comme le poteau de la plaque).", 8)
    r.check(-0.03 <= left <= 0.03, f"Côté GAUCHE inchangé : différence {left:+.3f} (± 0,03)", "Pas d'ombre à gauche : le soleil est à gauche dans la plaque.", 6)
    if debug:
        print("[DEBUG] right", round(right, 3), "left", round(left, 3), "far", round(far, 3), "cube", len(xs), round(col, 3))
    return r.finish()


if __name__ == "__main__":
    L.run(main)
