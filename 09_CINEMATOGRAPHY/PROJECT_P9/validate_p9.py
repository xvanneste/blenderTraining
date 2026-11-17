"""
validate_p9.py — Correcteur du projet P9 « Cinq plans, cinq émotions » (lumière, couleur, cadrage).
Usage : blender -b --factory-startup <fichier.blend> --python-exit-code 1 --python validate_p9.py [-- --debug]
Le fichier contient CINQ SCÈNES : SH_JOY, SH_SADNESS, SH_ANGER, SH_CALM, SH_FEAR. Chacune a sa caméra (scene.camera), au moins une lampe ou un monde éclairant, et l'objet partagé Hero
(cylindre de 1,8 m, couleur d'objet rouge, posé en (0, 6, 0,9), qui ne doit pas bouger). Le correcteur rend chaque scène deux fois (160 × 90) :
  (a) rendu d'ambiance : Cycles CPU, 32 échantillons, sans débruitage, avec la gestion des couleurs de la scène, image affichée : luminance moyenne Y, écart p95 − p5, couleur moyenne (R, G, B) ;
  (b) rendu de cadrage : Workbench plat, couleurs d'objet, monde noir temporaire : hauteur du Hero (rouge) en fraction de l'image et abscisse de son centre.
Critères par plan (valeurs mesurées sur la référence : voir README) :
  JOY     : Y moyen ≥ 0,45 ; chaud (R/B ≥ 1,1) ; Hero sur un tiers vertical (33 % ou 67 %, ± 8) ;
  SADNESS : Y moyen de 0,02 à 0,15 ; froid (B/R ≥ 1,1) ; Hero sur un tiers vertical (± 8) ;
  ANGER   : part de rouge R/(R+G+B) ≥ 0,5 ; écart p95 − p5 ≥ 0,4 ; Hero haut (≥ 60 % de l'image) et centré (50 % ± 10) ;
  CALM    : Y moyen de 0,25 à 0,5 ; écart p95 − p5 ≤ 0,4 ; B ≥ R ; Hero sur un tiers vertical (± 8) ;
  FEAR    : Y moyen de 0,01 à 0,12 ; Hero petit (≤ 35 % de l'image) et excentré (centre hors de 40–60 %).
Ensemble : luminance moyenne des cinq plans étalée d'au moins 0,3 (max − min) ; tailles du Hero étalées d'au moins 0,3.
Planche renders/p9_contact_sheet.png (dossier du .blend) : ≥ 1 600 px de large, non noire et contrastée.
Testé avec : Blender 5.3.0.
"""
import os
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bpy  # noqa: E402
import numpy as np  # noqa: E402
from mathutils import Vector  # noqa: E402

SHOTS = ("JOY", "SADNESS", "ANGER", "CALM", "FEAR")


def _render_png(sc, path, w=160, h=90):
    sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage = w, h, 100
    sc.render.image_settings.file_format = "PNG"
    sc.render.image_settings.color_mode = "RGB"
    sc.render.filepath = path
    bpy.ops.render.render(write_still=True, scene=sc.name)
    im = bpy.data.images.load(path)
    px = np.array(im.pixels[:], np.float32).reshape(h, w, 4)[..., :3][::-1].copy()
    bpy.data.images.remove(im)
    return px


def measure_shot(name):
    """Renvoie les mesures d'ambiance et de cadrage de la scène SH_<name> (modifie temporairement la scène, puis la restaure)."""
    sc = bpy.data.scenes["SH_" + name]
    keep = (sc.render.engine, sc.cycles.samples, sc.cycles.use_denoising, sc.cycles.device, sc.world, sc.display.shading.light, sc.display.shading.color_type)
    sc.render.engine = "CYCLES"
    sc.cycles.device = "CPU"
    sc.cycles.samples = 32
    sc.cycles.use_denoising = False
    px = _render_png(sc, os.path.join(tempfile.gettempdir(), f"bcma_p9_{name}_mood.png"))
    Y = px[..., 0] * 0.2126 + px[..., 1] * 0.7152 + px[..., 2] * 0.0722
    rgb = px.reshape(-1, 3).mean(axis=0)
    out = {"Y": float(Y.mean()), "spread": float(np.percentile(Y, 95) - np.percentile(Y, 5)), "R": float(rgb[0]), "G": float(rgb[1]), "B": float(rgb[2])}
    black = bpy.data.worlds.new("WO_tmp_black")
    black.color = (0, 0, 0)
    sc.world = black
    sc.render.engine = "BLENDER_WORKBENCH"
    sc.display.shading.light, sc.display.shading.color_type = "FLAT", "OBJECT"
    px = _render_png(sc, os.path.join(tempfile.gettempdir(), f"bcma_p9_{name}_frame.png"))
    red = (px[..., 0] > 0.7) & (px[..., 1] < 0.3) & (px[..., 2] < 0.3)
    ys, xs = np.nonzero(red)
    out["hero_px"] = int(red.sum())
    out["h"] = float((ys.max() + 1 - ys.min()) / red.shape[0]) if len(ys) else 0.0
    out["cx"] = float((xs.mean() + 0.5) / red.shape[1]) if len(xs) else -1.0
    sc.render.engine, sc.cycles.samples, sc.cycles.use_denoising, sc.cycles.device, sc.world, sc.display.shading.light, sc.display.shading.color_type = keep
    bpy.data.worlds.remove(black)
    return out


def third(cx):
    return min(abs(cx - 1 / 3), abs(cx - 2 / 3)) <= 0.08


def main():
    debug = L.flag("--debug")
    r = L.Report("P9 — Cinq plans, cinq émotions")
    ok_scenes = all(("SH_" + n) in bpy.data.scenes for n in SHOTS)
    if not r.check(ok_scenes, "Les cinq scènes SH_JOY, SH_SADNESS, SH_ANGER, SH_CALM, SH_FEAR existent", "Une scène par plan (menu des scènes en haut de la fenêtre).", 6):
        return r.finish()
    hero = bpy.data.objects.get("Hero")
    in_all = hero is not None and all(hero.name in bpy.data.scenes["SH_" + n].objects for n in SHOTS)
    r.check(in_all and (hero.matrix_world.translation - Vector((0, 6, 0.9))).length <= 0.01, "Hero présent dans les cinq scènes, à (0, 6, 0,9)", "Le sujet est partagé et ne bouge pas : changez la lumière, la couleur et la caméra.", 6)
    cams = all(bpy.data.scenes["SH_" + n].camera is not None for n in SHOTS)
    r.check(cams, "Chaque scène a sa caméra", "scene.camera doit être défini.", 4)
    if not (in_all and cams):
        return r.finish()
    m = {n: measure_shot(n) for n in SHOTS}
    if debug:
        for n in SHOTS:
            print("[DEBUG]", n, {k: round(v, 3) for k, v in m[n].items()})
    f = lambda n: f"Y {m[n]['Y']:.2f}, R/B {m[n]['R'] / max(m[n]['B'], 1e-6):.2f}, écart {m[n]['spread']:.2f}, Hero {100 * m[n]['h']:.0f} % à {100 * m[n]['cx']:.0f} %"
    j = m["JOY"]
    r.check(j["Y"] >= 0.45 and j["R"] / max(j["B"], 1e-6) >= 1.1 and third(j["cx"]), f"JOY : {f('JOY')} (clair, chaud, sur un tiers)", "Y ≥ 0,45 ; R/B ≥ 1,1 ; Hero à 33 % ou 67 %.", 8)
    s = m["SADNESS"]
    r.check(0.02 <= s["Y"] <= 0.15 and s["B"] / max(s["R"], 1e-6) >= 1.1 and third(s["cx"]), f"SADNESS : {f('SADNESS')} (sombre, froid, sur un tiers)", "0,02 ≤ Y ≤ 0,15 ; B/R ≥ 1,1 ; Hero sur un tiers.", 8)
    a = m["ANGER"]
    share = a["R"] / max(a["R"] + a["G"] + a["B"], 1e-6)
    r.check(share >= 0.5 and a["spread"] >= 0.4 and a["h"] >= 0.6 and abs(a["cx"] - 0.5) <= 0.1, f"ANGER : part de rouge {share:.2f}, {f('ANGER')} (rouge, contrasté, gros plan centré)", "R/(R+G+B) ≥ 0,5 ; écart ≥ 0,4 ; Hero ≥ 60 % et centré.", 8)
    c = m["CALM"]
    r.check(0.25 <= c["Y"] <= 0.5 and c["spread"] <= 0.4 and c["B"] >= c["R"] and third(c["cx"]), f"CALM : {f('CALM')} (moyen, doux, bleuté, sur un tiers)", "0,25 ≤ Y ≤ 0,5 ; écart ≤ 0,4 ; B ≥ R ; Hero sur un tiers.", 8)
    fe = m["FEAR"]
    r.check(0.01 <= fe["Y"] <= 0.12 and fe["h"] <= 0.35 and abs(fe["cx"] - 0.5) > 0.1, f"FEAR : {f('FEAR')} (très sombre, petit, excentré)", "0,01 ≤ Y ≤ 0,12 ; Hero ≤ 35 % ; centre hors de 40–60 %.", 8)
    ys = [m[n]["Y"] for n in SHOTS]
    hs = [m[n]["h"] for n in SHOTS]
    r.check(max(ys) - min(ys) >= 0.3 and max(hs) - min(hs) >= 0.3, f"Contraste entre plans : luminance étalée de {max(ys) - min(ys):.2f} (≥ 0,3), tailles étalées de {max(hs) - min(hs):.2f} (≥ 0,3)", "Les cinq plans doivent différer en lumière et en échelle.", 6)
    sheet = os.path.join(os.path.dirname(bpy.data.filepath), "renders", "p9_contact_sheet.png")
    if os.path.exists(sheet):
        im = bpy.data.images.load(sheet)
        w, h = im.size
        px = np.array(im.pixels[:], np.float32).reshape(h, w, 4)[..., :3]
        bpy.data.images.remove(im)
        Y = px[..., 0] * 0.2126 + px[..., 1] * 0.7152 + px[..., 2] * 0.0722
        r.check(w >= 1600 and Y.mean() > 0.03 and (np.percentile(Y, 95) - np.percentile(Y, 5)) > 0.1, f"Planche : {w} × {h} px, luminance moyenne {Y.mean():.2f}, contraste {np.percentile(Y, 95) - np.percentile(Y, 5):.2f}", "≥ 1 600 px de large, non noire, contrastée.", 6)
    else:
        r.check(False, "Planche renders/p9_contact_sheet.png", "Rendez les cinq plans côte à côte dans renders/.", 6)
    return r.finish()


if __name__ == "__main__":
    L.run(main)
