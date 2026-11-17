"""
validate_ch07_14.py — Correcteur « Motion capture » (CH07.14).
Usage : … --python-exit-code 1 --python validate_ch07_14.py -- --exercise mocap [--debug]
Objet : RIG_Mocap (BVH importé : Hips, Spine, Head, Arm_L ; 15 courbes), actions « MOCAP » (à nettoyer, ACTIVE) et « MOCAP_RAW » (référence brute, intacte) ; plage 1–96 à 24 i/s.
  Pour chaque courbe de « MOCAP » (comparée à la courbe de même chemin de « MOCAP_RAW », toutes deux évaluées aux images 1 à 96) :
    référence = médiane glissante (5 images) puis lissage gaussien (σ = 1,5 image) de la courbe brute ; amplitude = max − min de la référence ; les courbes dont l'amplitude est inférieure à 0,05 rad (rotations) ou 0,02 m (positions) ne contiennent que du bruit : on y contrôle seulement la rugosité, le nombre de clés et l'interpolation ;
    rugosité (écart quadratique moyen de la différence seconde) ≤ 50 % de celle de la courbe brute ;
    fidélité : écart quadratique moyen à la référence ≤ 8 % de l amplitude ;
    amplitude conservée : max − min de la courbe nettoyée ≥ 90 % de l'amplitude de la référence ;
    glitches supprimés : écart maximal à la référence ≤ 15 % de l'amplitude ;
    au plus 38 clés (96 au départ) ; toutes les clés en interpolation Bezier.
  « MOCAP_RAW » intacte : 15 courbes de 96 clés chacune, avec ses glitches (écart maximal à la référence ≥ 15 % de l'amplitude sur Spine Z).
Testé avec : Blender 5.3.0.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bpy  # noqa: E402
import numpy as np  # noqa: E402


def fcurves(act):
    try:
        return list(act.fcurves)
    except AttributeError:
        return [f for l in act.layers for st in l.strips for cb in st.channelbags for f in cb.fcurves]


def values(fc):
    return np.array([fc.evaluate(f) for f in range(1, 97)])


def floor(fc):
    return 0.05 if fc.data_path.endswith("rotation_euler") else 0.02


def median5(y):
    pad = np.pad(y, 2, mode="edge")
    return np.array([np.median(pad[i:i + 5]) for i in range(len(y))])


def gauss(y, sigma):
    r = max(1, int(round(3 * sigma)))
    k = np.exp(-0.5 * (np.arange(-r, r + 1) / sigma) ** 2)
    k /= k.sum()
    return np.convolve(np.pad(y, r, mode="edge"), k, mode="valid")


def rough(y):
    d = y[2:] - 2 * y[1:-1] + y[:-2]
    return float(np.sqrt(np.mean(d * d)))


def main():
    debug = L.flag("--debug")
    r = L.Report("CH07.14 — Motion capture (nettoyage d'un BVH)")
    rig = bpy.data.objects.get("RIG_Mocap")
    act, raw = bpy.data.actions.get("MOCAP"), bpy.data.actions.get("MOCAP_RAW")
    if not r.check(rig is not None and act is not None and raw is not None and rig.animation_data is not None and rig.animation_data.action == act, "RIG_Mocap avec l'action active « MOCAP » et la référence « MOCAP_RAW »", "Partez du fichier de départ.", 2):
        return r.finish()
    sc = bpy.context.scene
    r.check(sc.frame_start == 1 and sc.frame_end == 96 and sc.render.fps == 24, f"Plage {sc.frame_start}–{sc.frame_end} à {sc.render.fps} i/s (1–96 à 24)", "Ne changez pas la plage.", 1)
    fa = {(f.data_path, f.array_index): f for f in fcurves(act)}
    fr = {(f.data_path, f.array_index): f for f in fcurves(raw)}
    r.check(len(fr) == 15 and all(len(f.keyframe_points) == 96 for f in fr.values()), f"MOCAP_RAW intacte : {len(fr)} courbes de {sorted({len(f.keyframe_points) for f in fr.values()})} clés (15 courbes de 96)", "N'éditez pas MOCAP_RAW : c'est la référence.", 3)
    r.check(set(fa) == set(fr), f"MOCAP a les mêmes 15 courbes que la référence ({len(fa)})", "Ne supprimez aucune courbe.", 2)
    worst = {"rough": 0.0, "fit": 0.0, "amp": 9.0, "spike": 0.0, "keys": 0}
    interp_ok = True
    for key, fcr in fr.items():
        if key not in fa:
            continue
        yr = values(fcr)
        ref = gauss(median5(yr), 1.5)
        amp0 = float(np.ptp(ref))
        yc = values(fa[key])
        if rough(yr) > 1e-9:
            worst["rough"] = max(worst["rough"], rough(yc) / rough(yr))
        worst["keys"] = max(worst["keys"], len(fa[key].keyframe_points))
        if amp0 < floor(fcr):                                         # courbe de pur bruit (aucun mouvement utile) : on ne contrôle que la rugosité et le nombre de clés
            continue
        worst["fit"] = max(worst["fit"], float(np.sqrt(np.mean((yc - ref) ** 2))) / amp0)
        worst["amp"] = min(worst["amp"], float(np.ptp(yc)) / amp0)
        worst["spike"] = max(worst["spike"], float(np.abs(yc - ref).max()) / amp0)
        if any(k.interpolation != "BEZIER" for k in fa[key].keyframe_points):
            interp_ok = False
    r.check(worst["rough"] <= 0.5, f"Bruit supprimé : rugosité maximale {100 * worst['rough']:.0f} % de celle du brut (≤ 50)", "Lissez (Smooth) les courbes.", 7)
    r.check(worst["fit"] <= 0.08 and worst["amp"] >= 0.90, f"Forme conservée : écart à la référence {100 * worst['fit']:.1f} % de l'amplitude (≤ 8) ; amplitude minimale {100 * worst['amp']:.0f} % (≥ 90)", "Ne lissez pas trop : le mouvement doit garder son amplitude.", 7)
    r.check(worst["spike"] <= 0.15, f"Glitches supprimés : écart maximal {100 * worst['spike']:.0f} % de l'amplitude (≤ 15)", "Supprimez les valeurs aberrantes avant de lisser.", 6)
    r.check(worst["keys"] <= 38, f"Clés décimées : {worst['keys']} clés au plus par courbe (≤ 38 ; 96 au départ)", "Decimate (Allowed Change) puis Clean Keyframes.", 5)
    r.check(interp_ok, "Toutes les clés restantes sont en interpolation Bezier", "T > Bezier.", 3)
    sp = next((f for k, f in fr.items() if k == ('pose.bones["Spine"].rotation_euler', 2)), None)
    if sp is not None:
        y = values(sp)
        ref = gauss(median5(y), 1.5)
        glitch = float(np.abs(y - ref).max()) / float(np.ptp(ref))
        r.check(glitch >= 0.15, f"MOCAP_RAW garde ses glitches (écart maximal {100 * glitch:.0f} % ≥ 15)", "MOCAP_RAW ne doit pas être nettoyée.", 2)
    if debug:
        print("[DEBUG]", {k: round(v, 3) for k, v in worst.items()}, "interp", interp_ok)
    return r.finish()


if __name__ == "__main__":
    L.run(main)
