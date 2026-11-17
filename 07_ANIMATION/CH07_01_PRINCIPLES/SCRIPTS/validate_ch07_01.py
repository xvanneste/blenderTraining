"""
validate_ch07_01.py — Correcteur « Les 12 principes » (CH07.01).
Usage : … --python-exit-code 1 --python validate_ch07_01.py -- --exercise principles [--debug]
Objet : GEO_Ball (animé : position en clés aux images 1, 8, 18, 28, 40 — saut en place, 40 images, 24 i/s).
  Configuration : plage 1–40 à 24 i/s ; courbes d'ÉCHELLE (X, Y et Z) sur GEO_Ball.
  Mesures sur l'animation ÉVALUÉE (échelle et sommets monde, image par image) :
    Contact : le point le plus bas de la balle est à ≤ 3 cm du sol aux images 1, 8 et 28 (la balle se déforme à partir du sol) ;
    Position : sommet du saut à l'image 18 : point le plus haut ≥ 2,9 m (base à 1,9 m ou plus) ;
    Repos : échelle (1, 1, 1) ± 0,03 aux images 1 et 40 ;
    Anticipation : entre les images 2 et 7, l'échelle Z descend à 0,8 ou moins ET l'échelle X monte à 1,1 ou plus ;
    Étirement : entre les images 9 et 26, l'échelle Z atteint 1,25 ou plus, avec une échelle X ≤ 0,95 à cet instant ;
    Volume : |sx·sy·sz − 1| ≤ 0,12 à chaque image de 1 à 40 ;
    Contact écrasé : image 28 : échelle Z ≤ 0,8 et X ≥ 1,1 ;
    Sommet neutre : image 18 : |sz − 1| ≤ 0,12 ;
    Symétrie : sx = sy (± 0,01) à chaque image.
Testé avec : Blender 5.3.0.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bpy  # noqa: E402
import numpy as np  # noqa: E402


def sample(ob):
    sc = bpy.context.scene
    rest = np.array([v.co[:] for v in ob.data.vertices])
    out = {}
    for f in range(1, 41):
        sc.frame_set(f)
        bpy.context.view_layer.update()
        mw = np.array(ob.matrix_world)
        pts = rest @ mw[:3, :3].T + mw[:3, 3]
        out[f] = (tuple(ob.scale), float(pts[:, 2].min()), float(pts[:, 2].max()), float(mw[2, 3]))
    return out


def main():
    debug = L.flag("--debug")
    r = L.Report("CH07.01 — Les 12 principes (squash & stretch, anticipation)")
    ob = bpy.data.objects.get("GEO_Ball")
    if not r.check(ob is not None and ob.animation_data is not None and ob.animation_data.action is not None, "GEO_Ball animée présente", "Partez du fichier de départ.", 2):
        return r.finish()
    sc = bpy.context.scene
    r.check(sc.frame_start == 1 and sc.frame_end == 40 and sc.render.fps == 24, f"Plage {sc.frame_start}–{sc.frame_end} à {sc.render.fps} i/s (1–40 à 24)", "Ne changez pas la plage.", 2)
    act = ob.animation_data.action
    try:
        fcs = list(act.fcurves)
    except AttributeError:
        fcs = [f for l in act.layers for s in l.strips for cb in s.channelbags for f in cb.fcurves]
    sc_idx = {f.array_index for f in fcs if f.data_path == "scale"}
    r.check(sc_idx == {0, 1, 2}, f"Courbes d'échelle X, Y, Z présentes (trouvées : {sorted(sc_idx)})", "Insérez des clés d'échelle (I > Scale).", 5)
    d = sample(ob)
    sc.frame_set(1)
    low = {f: d[f][1] for f in (1, 8, 28)}
    r.check(all(abs(v) <= 0.03 for v in low.values()), f"Contact : point le plus bas aux images 1, 8, 28 = {[round(low[f], 3) for f in (1, 8, 28)]} m (≤ 3 cm)", "L'origine de la balle est à sa base : ne la déplacez pas.", 5)
    r.check(d[18][2] >= 2.9, f"Sommet du saut : point le plus haut à l'image 18 = {d[18][2]:.2f} m", "Ne modifiez pas la position.", 3)
    r.check(all(abs(c - 1) <= 0.03 for f in (1, 40) for c in d[f][0]), f"Repos : échelle {tuple(round(c, 2) for c in d[1][0])} (image 1) et {tuple(round(c, 2) for c in d[40][0])} (image 40) = (1, 1, 1)", "Clés de repos aux images 1 et 40.", 3)
    ant = [d[f][0] for f in range(2, 8)]
    mz, mx = min(a[2] for a in ant), max(a[0] for a in ant)
    r.check(mz <= 0.8 and mx >= 1.1, f"Anticipation (images 2–7) : Scale Z min {mz:.2f} (≤ 0,8), Scale X max {mx:.2f} (≥ 1,1)", "Écrasez la balle avant le départ (image 5).", 6)
    fl = {f: d[f][0] for f in range(9, 27)}
    fmax = max(fl, key=lambda f: fl[f][2])
    r.check(fl[fmax][2] >= 1.25 and fl[fmax][0] <= 0.95, f"Étirement (images 9–26) : Scale Z max {fl[fmax][2]:.2f} à l'image {fmax} (≥ 1,25), Scale X {fl[fmax][0]:.2f} (≤ 0,95)", "Étirez la balle en vol (images 13 et 23).", 6)
    vol = max(abs(d[f][0][0] * d[f][0][1] * d[f][0][2] - 1) for f in d)
    r.check(vol <= 0.12, f"Volume constant : écart maximal {vol:.3f} (≤ 0,12) sur les 40 images", "Scale X = Scale Y = 1 / √(Scale Z).", 6)
    r.check(d[28][0][2] <= 0.8 and d[28][0][0] >= 1.1, f"Contact écrasé (image 28) : Z {d[28][0][2]:.2f} (≤ 0,8), X {d[28][0][0]:.2f} (≥ 1,1)", "Écrasez la balle au contact.", 5)
    r.check(abs(d[18][0][2] - 1) <= 0.12, f"Sommet neutre (image 18) : Scale Z {d[18][0][2]:.2f} (1 ± 0,12)", "La balle reprend sa forme au sommet.", 3)
    sym = max(abs(d[f][0][0] - d[f][0][1]) for f in d)
    r.check(sym <= 0.01, f"Symétrie : écart X/Y maximal {sym:.3f} (≤ 0,01)", "Scale X et Y identiques.", 2)
    if debug:
        print("[DEBUG] low", {f: round(v, 3) for f, v in low.items()}, "apex", d[18], "ant", round(mz, 2), round(mx, 2), "stretch", fmax, d[fmax][0], "vol", round(vol, 3), "sz28", d[28][0], "sym", round(sym, 3))
    return r.finish()


if __name__ == "__main__":
    L.run(main)
