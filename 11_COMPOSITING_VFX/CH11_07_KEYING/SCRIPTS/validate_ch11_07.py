"""
validate_ch11_07.py — Correcteur « Keying » (CH11.07).
Usage : … --python-exit-code 1 --python validate_ch11_07.py -- --exercise keying [--debug]
Données : l'image « greenscreen » (160 × 90, empaquetée dans le .blend : fond vert (0,10 ; 0,80 ; 0,15) avec grain, sujet elliptique (0,75 ; 0,35 ; 0,30) centré en (80, 45), bord doux et contaminé de vert), CAM. Le correcteur lit l'arbre de compositing et rend (Workbench, 160 × 90, Standard, compositing de l'élève) :
  structure : arbre relié à Group Output, aucun nœud orphelin, compositing de rendu activé ;
  fond remplacé : écart moyen des couleurs AFFICHÉES des quatre coins à la valeur affichée du bleu (0,10 ; 0,20 ; 0,80 linéaire = (0,35 ; 0,48 ; 0,91) en sRGB) ≤ 0,08 (départ 0,44 ; solution 0,006) ;
  sujet conservé : écart du centre du sujet (rangées 40–49, colonnes 75–84) à (0,75 ; 0,35 ; 0,30) ≤ 0,1 ;
  contamination : sur l'anneau du sujet (d normalisé de 0,86 à 0,95), vert − (rouge + bleu)/2 ≤ 0,06 (image brute 0,130 ; solution −0,028 ; Chroma Matte seul 0,130).
Testé avec : Blender 5.3.0.
"""
import os
import sys
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bpy  # noqa: E402
import numpy as np  # noqa: E402

BLUE = (0.10, 0.20, 0.80)
SBLUE = tuple((c * 12.92 if c <= 0.0031308 else 1.055 * c ** (1 / 2.4) - 0.055) for c in BLUE)
SUBJ = (0.75, 0.35, 0.30)


def main():
    debug = L.flag("--debug")
    r = L.Report("CH11.07 — Keying")
    if not r.check(bpy.data.images.get("greenscreen") is not None, "Image « greenscreen » présente", "Partez du fichier de départ.", 2):
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
    sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage = 160, 90, 100
    sc.view_settings.view_transform = "Standard"
    sc.render.image_settings.file_format = "PNG"
    sc.render.image_settings.color_mode = "RGB"
    p = os.path.join(tempfile.gettempdir(), "bcma_ch1107_val.png")
    sc.render.filepath = p
    bpy.ops.render.render(write_still=True)
    im = bpy.data.images.load(p)
    px = np.array(im.pixels[:], np.float32).reshape(90, 160, 4)[..., :3][::-1].copy()
    bpy.data.images.remove(im)
    corners = np.concatenate([px[2:10, 2:10].reshape(-1, 3), px[2:10, 150:158].reshape(-1, 3), px[80:88, 2:10].reshape(-1, 3), px[80:88, 150:158].reshape(-1, 3)])
    bg_err = float(np.abs(corners.mean(axis=0) - np.array(SBLUE)).mean())
    subj_err = float(np.abs(px[40:50, 75:85].reshape(-1, 3).mean(axis=0) - np.array(SUBJ)).mean())
    yy, xx = np.mgrid[0:90, 0:160].astype(np.float32)
    d = np.sqrt(((xx - 80) / 30.0) ** 2 + ((yy - 45) / 28.0) ** 2)
    rp = px[(d > 0.86) & (d < 0.95)]
    spill = float((rp[:, 1] - (rp[:, 0] + rp[:, 2]) / 2).mean())
    r.check(bg_err <= 0.08, f"Fond remplacé par le bleu : écart des coins {bg_err:.3f} (≤ 0,08)", "Keying (Key Color = le vert du fond) puis Alpha Over avec un nœud RGB bleu en Background.", 8)
    r.check(subj_err <= 0.1, f"Sujet conservé : écart du centre {subj_err:.3f} (≤ 0,1)", "Le sujet doit passer en Foreground de l'Alpha Over.", 6)
    r.check(spill <= 0.06, f"Contamination retirée : vert − (rouge + bleu)/2 = {spill:+.3f} (≤ 0,06)", "Nœud Color Spill (canal G) sur le sujet détouré.", 8)
    if debug:
        print("[DEBUG] bg", round(bg_err, 4), "subj", round(subj_err, 4), "spill", round(spill, 4), [n.bl_idname for n in ng.nodes])
    return r.finish()


if __name__ == "__main__":
    L.run(main)
