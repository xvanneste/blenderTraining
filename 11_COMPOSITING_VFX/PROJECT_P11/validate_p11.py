"""
validate_p11.py — Correcteur du projet P11 « Intégrer un élément 3D dans une prise de vue » (plaque + cube : ombre, sol invisible, exposition, couleur, grain, rapport de contrôle qualité).
Usage : blender -b --factory-startup <fichier.blend> --python-exit-code 1 --python validate_p11.py [-- --debug]
Données : image « plate » (320 × 180 : ciel, sol chaud granuleux, poteau dont l'ombre tombe à DROITE), Cube (0, 0, 0,5), Floor, SUN (4 W/m²), CAM (0, −8, 3), 75°, 35 mm. Le correcteur lit l'arbre de compositing et rend DEUX FOIS (Cycles CPU, 320 × 180, sans débruitage,
échantillons de l'élève, graines 0 et 1, compositing de l'élève), compare à la plaque et contrôle :
  1. scène : Cube, caméra et SUN (4 W/m²) inchangés ; arbre relié à Group Output sans nœud orphelin ; compositing activé ;
  2. intégration (CH11.09) : cube présent (écart moyen à la plaque dans la boîte projetée du cube ≥ 0,008) ; sol lointain = plaque (± 0,03) ; ombre à DROITE du cube (≤ −0,04), côté gauche inchangé (± 0,03) ;
  3. cohérence (CH11.10) : exposition (dessus du cube / sol de la plaque) de 0,85 à 1,15 ; dominante (rouge − bleu) à ± 0,04 de la plaque ; grain (deux rendus) de 0,008 à 0,025 ;
  4. image finale renders/p11_final.png (dossier du .blend) : 320 × 180 ou un multiple entier, luminance moyenne de 0,2 à 0,8, et différente de la plaque (écart moyen ≥ 0,008) dans la boîte du cube ;
  5. rapport renders/p11_qc.json : clés ratio, cast, noise (valeurs relevées par l'élève) cohérentes avec les mesures du correcteur (ratio ± 0,1, cast ± 0,03, noise ± 0,01) et « notes » (au moins 5 phrases de plus de 20 caractères).
Testé avec : Blender 5.3.0.
"""
import json
import math
import os
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bpy  # noqa: E402
import numpy as np  # noqa: E402
from bpy_extras.object_utils import world_to_camera_view  # noqa: E402
from mathutils import Vector  # noqa: E402

W, H = 320, 180


def lum(a):
    return a[..., 0] * 0.2126 + a[..., 1] * 0.7152 + a[..., 2] * 0.0722


def rend(sc, seed, path):
    sc.cycles.seed = seed
    sc.render.filepath = path
    bpy.ops.render.render(write_still=True)
    im = bpy.data.images.load(path)
    w, h = im.size
    px = np.array(im.pixels[:], np.float32).reshape(h, w, 4)[..., :3][::-1].copy()
    bpy.data.images.remove(im)
    return px


def measure(sc):
    """Mesures d'intégration et de cohérence (rend deux fois à 320 × 180)."""
    keep = (sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage)
    sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage = W, H, 100
    a = rend(sc, 0, os.path.join(tempfile.gettempdir(), "bcma_p11_0.png"))
    b = rend(sc, 1, os.path.join(tempfile.gettempdir(), "bcma_p11_1.png"))
    sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage = keep
    pl = np.array(bpy.data.images["plate"].pixels[:], np.float32).reshape(H, W, 4)[..., :3][::-1].copy()
    v = world_to_camera_view(sc, sc.camera, Vector((0, 0, 1.0)))
    tx, ty = int(v.x * W), int((1 - v.y) * H)
    top = (slice(ty - 3, ty + 4), slice(tx - 8, tx + 9))
    gr = (slice(140, 165), slice(40, 90))
    t, t2, g = a[top], b[top], pl[gr]
    # boîte du cube : projection de ses huit coins
    pts = [world_to_camera_view(sc, sc.camera, Vector((x, y, z))) for x in (-0.5, 0.5) for y in (-0.5, 0.5) for z in (0.0, 1.0)]
    x0, x1 = int(min(p.x for p in pts) * W), int(max(p.x for p in pts) * W)
    yt, yb = int((1 - max(p.y for p in pts)) * H), int((1 - min(p.y for p in pts)) * H)
    region = (slice(max(yt, 0), min(yb, H)), slice(max(x0, 0), min(x1, W)))
    out = {"bbox": (max(x0, 0), min(x1, W), max(yt, 0), min(yb, H)), "cube_diff": float(np.abs(a[region] - pl[region]).mean()), "ratio": float(lum(t).mean() / lum(g).mean()), "cast": float((t[..., 0] - t[..., 2]).mean() - (g[..., 0] - g[..., 2]).mean()),
           "noise": float(np.std(lum(t) - lum(t2)) / math.sqrt(2.0)), "far": float((lum(a[140:170, 20:70]) - lum(pl[140:170, 20:70])).mean())}
    y1 = yb
    d = lambda p, q, c, e: float((lum(a[c:e, p:q]) - lum(pl[c:e, p:q])).mean())
    out["right"] = d(x1 + 3, min(x1 + 28, W), y1 - 8, y1 + 4)
    out["left"] = d(max(x0 - 28, 0), max(x0 - 3, 1), y1 - 8, y1 + 4)
    return out


def main():
    debug = L.flag("--debug")
    r = L.Report("P11 — Intégrer un élément 3D dans une prise de vue")
    O = bpy.data.objects
    if not r.check(all(O.get(n) for n in ("Cube", "Floor", "SUN", "CAM")) and bpy.data.images.get("plate") is not None, "Cube, Floor, SUN, CAM et la plaque présents", "Partez de la scène fournie.", 2):
        return r.finish()
    sc = bpy.context.scene
    ok = (O["Cube"].location - Vector((0, 0, 0.5))).length < 1e-3 and abs(O["SUN"].data.energy - 4) < 1e-3 and (O["CAM"].location - Vector((0, -8, 3))).length < 1e-3
    r.check(ok, "Scène inchangée : Cube, caméra, puissance du SUN", "Travaillez le soleil (rotation), le sol, le film, le compositeur et les échantillons.", 3)
    ng = sc.compositing_node_group
    if not r.check(ng is not None, "Arbre de compositing présent", "Partez de la scène fournie.", 3):
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
    sc.render.image_settings.file_format = "PNG"
    sc.render.image_settings.color_mode = "RGB"
    m = measure(sc)
    r.check(m["cube_diff"] >= 0.008, f"Cube présent : écart moyen à la plaque dans sa boîte {m['cube_diff']:.3f} (≥ 0,008)", "Film transparent + Alpha Over : Foreground = Render Layers.", 6)
    r.check(abs(m["far"]) <= 0.03, f"Sol lointain = plaque : différence {m['far']:+.3f} (± 0,03)", "Floor = Shadow Catcher et film transparent.", 8)
    r.check(m.get("right", 0) <= -0.04 and abs(m.get("left", 1)) <= 0.03, f"Ombre à droite : {m.get('right', float('nan')):+.3f} (≤ −0,04) ; côté gauche : {m.get('left', float('nan')):+.3f} (± 0,03)", "SUN : rotation X 50°, Z −50° (soleil à gauche comme dans la plaque).", 8)
    r.check(0.85 <= m["ratio"] <= 1.15, f"Exposition : dessus du cube / sol de la plaque = {m['ratio']:.2f} (0,85–1,15)", "Nœud Exposure sur le rendu seul.", 8)
    r.check(abs(m["cast"]) <= 0.04, f"Dominante : écart {m['cast']:+.3f} (± 0,04)", "Nœud Color Balance (Gain chaud) sur le rendu seul.", 8)
    r.check(0.008 <= m["noise"] <= 0.025, f"Grain : bruit du cube {m['noise']:.4f} (0,008–0,025) avec {sc.cycles.samples} échantillons", "Peu d'échantillons, sans débruitage.", 8)
    here = os.path.dirname(bpy.data.filepath)
    fin = os.path.join(here, "renders", "p11_final.png")
    if os.path.exists(fin):
        im = bpy.data.images.load(fin)
        w, h = im.size
        px = np.array(im.pixels[:], np.float32).reshape(h, w, 4)[..., :3][::-1].copy()
        bpy.data.images.remove(im)
        ym = float(lum(px).mean())
        s = w / float(W)
        pl = np.array(bpy.data.images["plate"].pixels[:], np.float32).reshape(H, W, 4)[..., :3][::-1].copy()
        plr = np.repeat(np.repeat(pl, int(round(s)), axis=0), int(round(s)), axis=1)[:h, :w]
        bx0, bx1, by0, by1 = [int(v * round(s)) for v in m["bbox"]]
        diff = float(np.abs(px[by0:by1, bx0:bx1] - plr[by0:by1, bx0:bx1]).mean()) if by1 > by0 and bx1 > bx0 else 0.0
        r.check(w >= 320 and h >= 180 and w % 320 == 0 and 0.2 <= ym <= 0.8 and diff >= 0.008, f"Image finale : {w} × {h}, luminance moyenne {ym:.2f} (0,2–0,8), écart à la plaque dans la boîte du cube {diff:.3f} (≥ 0,008)", "Rendez 320 × 180 (ou un multiple entier) dans renders/p11_final.png.", 8)
    else:
        r.check(False, "Image finale renders/p11_final.png", "Rendez l'image finale à côté du .blend.", 8)
    rep = os.path.join(here, "renders", "p11_qc.json")
    if os.path.exists(rep):
        try:
            d = json.load(open(rep, encoding="utf-8"))
            ok = abs(d["ratio"] - m["ratio"]) <= 0.1 and abs(d["cast"] - m["cast"]) <= 0.03 and abs(d["noise"] - m["noise"]) <= 0.01
            notes = [n for n in d.get("notes", []) if isinstance(n, str) and len(n) > 20]
            r.check(ok, f"Rapport cohérent : ratio {d['ratio']} (mesuré {m['ratio']:.2f}), dominante {d['cast']} ({m['cast']:+.3f}), grain {d['noise']} ({m['noise']:.4f})", "Reportez les mesures du correcteur dans p11_qc.json.", 6)
            r.check(len(notes) >= 5, f"Notes : {len(notes)} phrase(s) de plus de 20 caractères (≥ 5)", "Au moins 5 observations.", 4)
        except Exception as ex:  # noqa: BLE001
            r.check(False, f"Rapport illisible ({type(ex).__name__})", "JSON avec ratio, cast, noise, notes.", 10)
    else:
        r.check(False, "Rapport renders/p11_qc.json", "Écrivez le rapport de contrôle qualité.", 10)
    if debug:
        print("[DEBUG]", {k: (round(v, 4) if not isinstance(v, tuple) else v) for k, v in m.items()})
    return r.finish()


if __name__ == "__main__":
    L.run(main)
