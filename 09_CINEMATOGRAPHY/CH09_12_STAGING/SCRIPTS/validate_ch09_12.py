"""
validate_ch09_12.py — Correcteur « Mise en scène » (CH09.12).
Usage : … --python-exit-code 1 --python validate_ch09_12.py -- --exercise staging [--debug]
Objets : A, B, C (personnages), Table, Cup (tasse), CAM (en (0, −9, 1,6), focale 35 mm : ne doit pas changer). Animation 1–72 ; moment clé = image 36 ; raccord 36 → 37.
Le correcteur évalue la scène image par image (frame_set 1 à 72) et rend l'image 36 (Workbench plat 320 × 180) :
  triangle à l'image 36 : aire ≥ 2 m², angle minimal ≥ 30° ; étagement : distances à la caméra (selon y) étalées sur ≥ 3 m, ≥ 1 m entre deux personnages ;
  visibilité (rendu) : A, B, C ≥ 30 pixels chacun, centres séparés d'au moins 8 % de la largeur ;
  continuité : au raccord 36 → 37 chaque personnage ≤ 0,12 m, la tasse ≤ 1 cm ; ≤ 0,15 m par image pour tout personnage ; jamais deux personnages à moins de 0,6 m.
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
from mathutils import Vector  # noqa: E402


def ang(p, q, r):
    v1, v2 = (q[0] - p[0], q[1] - p[1]), (r[0] - p[0], r[1] - p[1])
    d = (v1[0] * v2[0] + v1[1] * v2[1]) / (math.hypot(*v1) * math.hypot(*v2) + 1e-12)
    return math.degrees(math.acos(max(-1.0, min(1.0, d))))


def main():
    debug = L.flag("--debug")
    r = L.Report("CH09.12 — Mise en scène")
    sc = bpy.context.scene
    obs = {n: bpy.data.objects.get(n) for n in ("A", "B", "C", "Cup", "CAM", "Table")}
    if not r.check(all(obs.values()), "A, B, C, Table, Cup et CAM présents", "Partez du fichier de départ.", 2):
        return r.finish()
    cam = obs["CAM"]
    r.check((cam.matrix_world.translation - Vector((0, -9, 1.6))).length <= 0.01 and abs(cam.data.lens - 35) <= 0.5, "Caméra inchangée : (0, −9, 1,6), 35 mm", "Corrigez le blocking, pas la caméra.", 3)
    pos = {}
    for f in range(1, 73):
        sc.frame_set(f)
        pos[f] = ({n: obs[n].matrix_world.translation.copy() for n in "ABC"}, obs["Cup"].matrix_world.translation.copy())
    sc.frame_set(36)
    P = [obs[n].matrix_world.translation for n in "ABC"]
    a, b, c = [(p.x, p.y) for p in P]
    area = 0.5 * abs((b[0] - a[0]) * (c[1] - a[1]) - (c[0] - a[0]) * (b[1] - a[1]))
    amin = min(ang(a, b, c), ang(b, a, c), ang(c, a, b))
    r.check(area >= 2.0 and amin >= 30.0, f"Triangle de blocking à l'image 36 : aire {area:.1f} m² (≥ 2), angle minimal {amin:.0f}° (≥ 30)", "Disposez A, B, C en triangle autour de la table, pas en ligne.", 8)
    depth = sorted(p.y + 9.0 for p in P)
    spread, gap = depth[-1] - depth[0], min(depth[1] - depth[0], depth[2] - depth[1])
    r.check(spread >= 3.0 and gap >= 1.0, f"Étagement en profondeur : étalement {spread:.1f} m (≥ 3), plus petit écart {gap:.1f} m (≥ 1)", "Premier plan, plan moyen et fond : des distances à la caméra différentes.", 8)
    sc.render.engine = "BLENDER_WORKBENCH"
    sc.view_settings.view_transform = "Standard"
    sc.view_settings.look = "None"
    sh = sc.display.shading
    sh.light, sh.color_type = "FLAT", "OBJECT"
    sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage = 320, 180, 100
    sc.camera = cam
    sc.render.image_settings.file_format = "PNG"
    sc.render.image_settings.color_mode = "RGB"
    path = os.path.join(tempfile.gettempdir(), "bcma_ch0912_val.png")
    sc.render.filepath = path
    bpy.ops.render.render(write_still=True)
    im = bpy.data.images.load(path)
    px = np.array(im.pixels[:], np.float32).reshape(180, 320, 4)[..., :3][::-1].copy()
    bpy.data.images.remove(im)
    R, G, B = px[..., 0], px[..., 1], px[..., 2]
    masks = {"A": (R > 0.7) & (G < 0.3) & (B < 0.3), "B": (B > 0.7) & (R < 0.3) & (G < 0.3), "C": (G > 0.7) & (R < 0.3) & (B < 0.3)}
    cnt = {n: int(m.sum()) for n, m in masks.items()}
    r.check(all(v >= 30 for v in cnt.values()), f"Les trois personnages sont visibles à l'image 36 : A {cnt['A']} px, B {cnt['B']} px, C {cnt['C']} px (≥ 30)", "Un personnage est caché derrière un autre ou hors cadre.", 8)
    cxs = {n: np.nonzero(m)[1].mean() / 320.0 for n, m in masks.items() if m.sum()}
    if len(cxs) == 3:
        sep = min(abs(cxs["A"] - cxs["B"]), abs(cxs["A"] - cxs["C"]), abs(cxs["B"] - cxs["C"]))
        r.check(sep >= 0.08, f"Centres séparés : écart minimal {100 * sep:.0f} % de la largeur (≥ 8 %)", "Écartez-les horizontalement pour qu'ils ne se superposent pas.", 5)
    else:
        r.check(False, "Centres séparés : un personnage n'est pas visible", "Voir le contrôle précédent.", 5)
    jump = max((pos[37][0][n] - pos[36][0][n]).length for n in "ABC")
    cupj = (pos[37][1] - pos[36][1]).length
    r.check(jump <= 0.12, f"Raccord 36 → 37 : plus grand saut d'un personnage {jump:.2f} m (≤ 0,12)", "Un personnage change de place entre deux plans : corrigez la clé de l'image 37.", 8)
    r.check(cupj <= 0.01, f"Raccord 36 → 37 : la tasse bouge de {100 * cupj:.1f} cm (≤ 1)", "La tasse ne doit pas changer de place entre deux plans.", 8)
    step = max((pos[f + 1][0][n] - pos[f][0][n]).length for f in range(1, 72) for n in "ABC")
    r.check(step <= 0.15, f"Vitesse maximale : {step:.2f} m par image (≤ 0,15)", "Un personnage se téléporte : répartissez le déplacement sur plus d'images.", 7)
    dmin = min((pos[f][0][p] - pos[f][0][q]).length for f in pos for p, q in (("A", "B"), ("A", "C"), ("B", "C")))
    r.check(dmin >= 0.6, f"Distance minimale entre personnages : {dmin:.2f} m (≥ 0,6)", "Les personnages ne doivent pas se traverser.", 5)
    if debug:
        print("[DEBUG] area", round(area, 2), "amin", round(amin, 1), "spread", round(spread, 2), "gap", round(gap, 2), "jump", round(jump, 3), "cup", round(cupj, 3), "step", round(step, 3), "dmin", round(dmin, 2), cnt)
    return r.finish()


if __name__ == "__main__":
    L.run(main)
