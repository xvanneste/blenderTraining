"""
validate_ch07_07.py — Correcteur « Posing et silhouette » (CH07.07).
Usage : … --python-exit-code 1 --python validate_ch07_07.py -- --exercise posing [--debug]
Objets : CHR_Mannequin (corps lié par groupes de sommets) et RIG_Mannequin (hips, spine, chest, neck, head, thigh/shin .L/.R, upper_arm/fore .L/.R). La pose ENREGISTRÉE est mesurée (vue de face : plan X–Z).
  Contrapposto : inclinaison de la ligne des épaules (upper_arm.R → upper_arm.L) et de la ligne des hanches (thigh.R → thigh.L) en sens OPPOSÉS, chacune de 4° à 20°.
  Appui : la jambe d'appui (celle dont le genou est le moins plié) a un genou à ≤ 8° ; sa cheville (fin de shin) est à z ≤ 0,09 m et à ≤ 15 cm (horizontalement) du centre des hanches ;
          la jambe libre a un genou plié d'au moins 15° et une cheville à z ≥ 0,02 m (pas dans le sol).
  Ligne d'action : angle entre la colonne (spine, tête → queue) et le vecteur chest.head → head.tail, dans le plan X–Z, de 8° à 40°.
  Silhouette : rendu Workbench à plat, de face (caméra orthographique) : solidité (aire / aire de l'enveloppe convexe) ≤ 0,50.
Testé avec : Blender 5.3.0.
"""
import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bpy  # noqa: E402
import numpy as np  # noqa: E402

NAMES = ("hips", "spine", "chest", "neck", "head", "thigh.L", "shin.L", "thigh.R", "shin.R", "upper_arm.L", "fore.L", "upper_arm.R", "fore.R")


def silhouette(body, w=240, h=360):
    sc = bpy.context.scene
    cam_d = bpy.data.cameras.new("CAM_Sil")
    cam_d.type = "ORTHO"
    cam_d.ortho_scale = 2.4
    cam = bpy.data.objects.new("CAM_Sil", cam_d)
    sc.collection.objects.link(cam)
    cam.location = (0, -6, 1.0)
    cam.rotation_euler = (math.radians(90), 0, 0)
    sc.camera = cam
    sc.render.engine = "BLENDER_WORKBENCH"
    sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage = w, h, 100
    sc.render.film_transparent = False
    sh = sc.display.shading
    sh.light, sh.color_type, sh.single_color = "FLAT", "SINGLE", (1, 1, 1)
    sh.background_type = "VIEWPORT"
    sh.background_color = (0, 0, 0)
    for o in bpy.data.objects:
        o.hide_render = o != body
    path = os.path.join(bpy.app.tempdir, "sil_p7.png")
    sc.render.filepath = path
    sc.render.image_settings.file_format = "PNG"
    sc.render.image_settings.color_mode = "RGB"
    bpy.ops.render.render(write_still=True)
    img = bpy.data.images.load(path)
    px = np.array(img.pixels[:], np.float32).reshape(img.size[1], img.size[0], 4)[..., 0]
    bpy.data.images.remove(img)
    return px > 0.5


def solidity(mask):
    ys, xs = np.nonzero(mask)
    pts = sorted(set(zip(xs.tolist(), ys.tolist())))
    if len(pts) < 3:
        return 1.0

    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    lo, up = [], []
    for p in pts:
        while len(lo) >= 2 and cross(lo[-2], lo[-1], p) <= 0:
            lo.pop()
        lo.append(p)
    for p in reversed(pts):
        while len(up) >= 2 and cross(up[-2], up[-1], p) <= 0:
            up.pop()
        up.append(p)
    hull = lo[:-1] + up[:-1]
    area = sum(hull[i][0] * hull[(i + 1) % len(hull)][1] - hull[(i + 1) % len(hull)][0] * hull[i][1] for i in range(len(hull)))
    return float(mask.sum()) / max(abs(area) / 2, 1.0)


def main():
    debug = L.flag("--debug")
    r = L.Report("CH07.07 — Posing et silhouette")
    body, rig = bpy.data.objects.get("CHR_Mannequin"), bpy.data.objects.get("RIG_Mannequin")
    if not r.check(body is not None and rig is not None and rig.type == "ARMATURE" and all(n in rig.pose.bones for n in NAMES), "CHR_Mannequin et RIG_Mannequin présents (13 bones)", "Partez du fichier de départ.", 2):
        return r.finish()
    r.check(any(m.type == "ARMATURE" and m.object == rig for m in body.modifiers), "Le mannequin est lié au rig (modificateur Armature)", "Ne défaites pas le lien.", 1)
    bpy.context.view_layer.update()
    P = {n: (np.array(rig.matrix_world @ rig.pose.bones[n].head), np.array(rig.matrix_world @ rig.pose.bones[n].tail)) for n in NAMES}

    def tilt(a, b):
        d = P[b][0] - P[a][0]
        return math.degrees(math.atan2(d[2], d[0]))
    sh, hp = tilt("upper_arm.R", "upper_arm.L"), tilt("thigh.R", "thigh.L")
    ok = sh * hp < 0 and 4 <= abs(sh) <= 20 and 4 <= abs(hp) <= 20
    r.check(ok, f"Contrapposto : épaules {sh:+.1f}°, hanches {hp:+.1f}° (sens opposés, chacune de 4° à 20°)", "Basculez les hanches d'un côté, les épaules de l'autre.", 8)

    def bend(side):
        t = P["thigh." + side][1] - P["thigh." + side][0]
        s = P["shin." + side][1] - P["shin." + side][0]
        return math.degrees(math.acos(max(-1.0, min(1.0, float(np.dot(t, s) / (np.linalg.norm(t) * np.linalg.norm(s)))))))
    bl, br = bend("L"), bend("R")
    sup, free = ("L", "R") if bl <= br else ("R", "L")
    bs, bf = min(bl, br), max(bl, br)
    ank = {s: P["shin." + s][1] for s in ("L", "R")}
    hc = (P["thigh.L"][0] + P["thigh.R"][0]) / 2
    r.check(bs <= 8.0 and bf >= 15.0, f"Appui : jambe {sup} tendue (genou {bs:.1f}° ≤ 8), jambe {free} relâchée (genou {bf:.1f}° ≥ 15)", "Une jambe porte le poids, l'autre est détendue.", 6)
    r.check(ank[sup][2] <= 0.09 and ank[sup][2] >= 0.0 and abs(ank[sup][0] - hc[0]) <= 0.15 and ank[free][2] >= 0.02, f"Équilibre : cheville d'appui à z = {ank[sup][2]:.3f} m (≤ 0,09) et à {abs(ank[sup][0] - hc[0]) * 100:.0f} cm sous les hanches (≤ 15) ; pied libre à z = {ank[free][2]:.3f} m (≥ 0,02)", "Le poids est au-dessus du pied d'appui, pas de pied dans le sol.", 6)
    a = P["spine"][1] - P["spine"][0]
    b = P["head"][1] - P["chest"][0]
    ang = math.degrees(abs(math.atan2(a[2] * b[0] - a[0] * b[2], a[0] * b[0] + a[2] * b[2])))
    r.check(8.0 <= ang <= 40.0, f"Ligne d'action : colonne et haut du corps forment {ang:.1f}° (8°–40°)", "Courbez la colonne : spine, chest, neck, head en cascade.", 6)
    mask = silhouette(body)
    sol = solidity(mask)
    r.check(sol <= 0.50, f"Silhouette de face (rendu Workbench) : solidité {sol:.3f} (≤ 0,50)", "Dégagez les bras du corps : la silhouette doit se lire en un coup d'œil.", 6)
    if debug:
        print("[DEBUG] sh", round(sh, 1), "hp", round(hp, 1), "bends", round(bl, 1), round(br, 1), "ank", [round(float(v), 3) for v in ank[sup]], [round(float(v), 3) for v in ank[free]], "dx", round(abs(ank[sup][0] - hc[0]), 3), "curve", round(ang, 1), "sol", round(sol, 3))
    return r.finish()


if __name__ == "__main__":
    L.run(main)
