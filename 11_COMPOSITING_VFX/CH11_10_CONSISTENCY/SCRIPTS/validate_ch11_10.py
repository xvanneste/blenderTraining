"""
validate_ch11_10.py — Correcteur « Cohérence visuelle » (CH11.10).
Usage : … --python-exit-code 1 --python validate_ch11_10.py -- --exercise consistency [--debug]
Données : plaque « plate » (sol (0,55 ; 0,50 ; 0,42), grain de 0,011 mesuré), Cube gris neutre (0,6) posé sur Floor (shadow catcher), film transparent, SUN (4 W/m²), CAM (0, −8, 3), 75°, 35 mm. Le correcteur lit l'arbre de compositing et rend DEUX FOIS (Cycles CPU, 320 × 180, sans débruitage,
  échantillons de l'élève, graines 0 et 1, compositing de l'élève) puis compare la face du dessus du cube (patch de 7 × 17 pixels au centre projeté du dessus) à un patch de sol de la plaque (rangées 140–164, colonnes 40–89) :
  exposition : luminance du dessus / luminance du sol de la plaque de 0,85 à 1,15 (départ 1,86 ; solution 1,01) ;
  dominante : (rouge − bleu) du dessus moins (rouge − bleu) du sol entre −0,04 et +0,04 (départ −0,20 ; solution +0,007) ;
  grain : écart-type de la différence des deux rendus sur le dessus / √2 de 0,008 à 0,025 (solution 0,012 avec 2 échantillons ; 128 échantillons : 0,002 ; la plaque 0,011) ;
  structure : arbre relié à Group Output, aucun nœud orphelin, compositing activé ; la scène (Cube, caméra, SUN 4 W/m²) n'est pas modifiée.
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
from bpy_extras.object_utils import world_to_camera_view  # noqa: E402
from mathutils import Vector  # noqa: E402

W, H = 320, 180


def lum(a):
    return a[..., 0] * 0.2126 + a[..., 1] * 0.7152 + a[..., 2] * 0.0722


def rend(sc, seed):
    sc.cycles.seed = seed
    p = os.path.join(tempfile.gettempdir(), f"bcma_ch1110_val{seed}.png")
    sc.render.filepath = p
    bpy.ops.render.render(write_still=True)
    im = bpy.data.images.load(p)
    px = np.array(im.pixels[:], np.float32).reshape(H, W, 4)[..., :3][::-1].copy()
    bpy.data.images.remove(im)
    return px


def main():
    debug = L.flag("--debug")
    r = L.Report("CH11.10 — Cohérence visuelle")
    O = bpy.data.objects
    if not r.check(all(O.get(n) for n in ("Cube", "Floor", "SUN", "CAM")) and bpy.data.images.get("plate") is not None, "Cube, Floor, SUN, CAM et la plaque présents", "Partez du fichier de départ.", 2):
        return r.finish()
    sc = bpy.context.scene
    ok = (O["Cube"].location - Vector((0, 0, 0.5))).length < 1e-3 and abs(O["SUN"].data.energy - 4) < 1e-3 and (O["CAM"].location - Vector((0, -8, 3))).length < 1e-3
    r.check(ok, "Scène inchangée : Cube, caméra, puissance du SUN", "Corrigez dans le compositeur (et les échantillons Cycles pour le grain).", 3)
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
    sc.cycles.use_denoising = False
    sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage = W, H, 100
    sc.render.image_settings.file_format = "PNG"
    sc.render.image_settings.color_mode = "RGB"
    a, b = rend(sc, 0), rend(sc, 1)
    pl = np.array(bpy.data.images["plate"].pixels[:], np.float32).reshape(H, W, 4)[..., :3][::-1].copy()
    v = world_to_camera_view(sc, sc.camera, Vector((0, 0, 1.0)))
    tx, ty = int(v.x * W), int((1 - v.y) * H)
    top = (slice(ty - 3, ty + 4), slice(tx - 8, tx + 9))
    gr = (slice(140, 165), slice(40, 90))
    t, t2, g = a[top], b[top], pl[gr]
    ratio = float(lum(t).mean() / lum(g).mean())
    cast = float((t[..., 0] - t[..., 2]).mean() - (g[..., 0] - g[..., 2]).mean())
    noise = float(np.std(lum(t) - lum(t2)) / math.sqrt(2.0))
    r.check(0.85 <= ratio <= 1.15, f"Exposition : dessus du cube / sol de la plaque = {ratio:.2f} (0,85–1,15)", "Nœud Exposure sur le rendu seul (≈ −2 diaphragmes).", 8)
    r.check(abs(cast) <= 0.04, f"Dominante de couleur : écart {cast:+.3f} (± 0,04)", "Nœud Color Balance (Gain chaud) sur le rendu seul.", 8)
    r.check(0.008 <= noise <= 0.025, f"Grain : bruit du cube {noise:.4f} (0,008–0,025 ; plaque 0,011) avec {sc.cycles.samples} échantillons", "La plaque a du grain : baissez les échantillons Cycles (2 à 4), sans débruitage.", 8)
    if debug:
        print("[DEBUG] ratio", round(ratio, 3), "cast", round(cast, 3), "noise", round(noise, 4), "samples", sc.cycles.samples)
    return r.finish()


if __name__ == "__main__":
    L.run(main)
