"""
validate_ch11_05.py — Correcteur « Glare et effets » (CH11.05).
Usage : … --python-exit-code 1 --python validate_ch11_05.py -- --exercise glare [--debug]
Objets : Lamp (disque émissif de force 30), Line (barre émissive de force 1), CAM (35 mm). Le correcteur lit l'arbre de compositing et rend (Cycles CPU, 160 × 90, 4 échantillons, sans débruitage, compositing de l'élève) :
  structure : arbre relié à Group Output, aucun nœud orphelin, compositing de rendu activé ;
  Glare : anneau (rayon 20–30 pixels autour du centre (80, 45), rangées ≥ 25) de 0,002 à 0,1 ; champ lointain (rayon 40–60, rangées ≥ 25) ≤ 0,1 ; cœur (rayon < 5) ≥ 0,95 (solution : 0,0066 ; 0,001 ; 1,0) ;
  Lens Distortion : courbure de la barre : (moyenne des rangées de la barre aux colonnes 10 et 150) − (rangée au centre, colonne 80), la barre cherchée dans les rangées 0–26 : de +4 à +12 pixels (solution : +7 ; sans distorsion : 0).
La scène (Lamp force 30, Line force 1, CAM 35 mm) ne doit pas être modifiée.
Testé avec : Blender 5.3.0.
"""
import os
import sys
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bpy  # noqa: E402
import numpy as np  # noqa: E402


def strength(o):
    return o.data.materials[0].node_tree.nodes["Emission"].inputs["Strength"].default_value


def main():
    debug = L.flag("--debug")
    r = L.Report("CH11.05 — Glare et effets")
    O = bpy.data.objects
    if not r.check(all(O.get(n) for n in ("Lamp", "Line", "CAM")), "Lamp, Line et CAM présents", "Partez du fichier de départ.", 2):
        return r.finish()
    sc = bpy.context.scene
    r.check(abs(strength(O["Lamp"]) - 30) < 1e-3 and abs(strength(O["Line"]) - 1) < 1e-3 and abs(O["CAM"].data.lens - 35) < 0.5, "Scène inchangée : Lamp 30, Line 1, caméra 35 mm", "Travaillez dans le compositeur.", 3)
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
    sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage = 160, 90, 100
    sc.render.image_settings.file_format = "PNG"
    sc.render.image_settings.color_mode = "RGB"
    p = os.path.join(tempfile.gettempdir(), "bcma_ch1105_val.png")
    sc.render.filepath = p
    bpy.ops.render.render(write_still=True)
    im = bpy.data.images.load(p)
    px = np.array(im.pixels[:], np.float32).reshape(90, 160, 4)[..., :3][::-1].copy()
    bpy.data.images.remove(im)
    y = px[..., 0] * 0.2126 + px[..., 1] * 0.7152 + px[..., 2] * 0.0722
    yy, xx = np.mgrid[0:90, 0:160]
    rr = np.hypot(xx - 80, yy - 45)
    low = yy >= 25
    ring, far, core = float(y[(rr > 20) & (rr < 30) & low].mean()), float(y[(rr > 40) & (rr < 60) & low].mean()), float(y[rr < 5].mean())

    def row(c):
        col = y[:27, c]
        return int(np.argmax(col)) if col.max() > 0.2 else -1
    e, c = (row(10) + row(150)) / 2.0, row(80)
    curv = (e - c) if e >= 0 and c >= 0 else 99.0
    r.check(0.002 <= ring <= 0.1, f"Halo : anneau {ring:.4f} (0,002–0,1)", "Nœud Glare : type Fog Glow (Bloom, Streaks, Ghosts sont trop forts ici).", 8)
    r.check(far <= 0.1 and core >= 0.95, f"Halo contenu : champ lointain {far:.3f} (≤ 0,1), cœur {core:.2f} (≥ 0,95)", "Le halo doit rester autour de la lampe.", 6)
    r.check(4 <= curv <= 12, f"Courbure de la barre : {curv:+.0f} pixels (+4 à +12)", "Nœud Lens Distortion : Distortion entre 0,15 et 0,4.", 8)
    if debug:
        print("[DEBUG] ring", round(ring, 4), "far", round(far, 4), "core", round(core, 3), "curv", curv)
    return r.finish()


if __name__ == "__main__":
    L.run(main)
