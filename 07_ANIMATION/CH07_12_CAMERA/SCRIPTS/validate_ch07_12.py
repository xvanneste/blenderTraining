"""
validate_ch07_12.py — Correcteur « Animation de caméra » (CH07.12).
Usage : … --python-exit-code 1 --python validate_ch07_12.py -- --exercise camera [--debug]
Objets : CAM_Main (caméra de la scène) et EMP_Subject (sujet animé : X de −1 à +1) ; plage 1–72 à 24 i/s. Mesures sur la caméra ÉVALUÉE (position et orientation mondes) :
  Travelling : Y de −8,00 m à l'image 1 et de −4,00 m à l'image 72 (± 0,10 m, en lissant le tremblé par une moyenne glissante de 9 images) ; hauteur moyenne 1,6 m (± 0,1) ;
               départ et arrivée doux : vitesse moyenne de la trajectoire lissée sur les 3 premières et les 3 dernières images ≤ 25 % de sa vitesse maximale ; trajet monotone (jamais de recul de plus de 5 cm).
  Suivi : une contrainte de visée (Track To, Damped Track ou Locked Track) cible EMP_Subject ; à chaque image l'axe de visée de la caméra (−Z) fait au plus 1° avec la direction caméra → sujet.
  Tremblé : modificateur Noise sur au moins deux courbes de position (X et Z) avec Strength de 0,02 à 0,2 ; résidu de position (position moins moyenne glissante de 9 images, X et Z) : écart-type de 3 à 25 mm et valeur maximale ≤ 0,08 m ; aucun Noise sur la courbe Y.
  Horizon : roulis (inclinaison de l'axe X de la caméra par rapport à l'horizontale) ≤ 1° à chaque image.
Testé avec : Blender 5.3.0.
"""
import math
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


def smooth(a, w=9):
    k = np.ones(w) / w
    pad = np.pad(a, (w // 2, w // 2), mode="edge")
    return np.convolve(pad, k, mode="valid")


def main():
    debug = L.flag("--debug")
    r = L.Report("CH07.12 — Animation de caméra (travelling, suivi, épaule)")
    cam, sub = bpy.data.objects.get("CAM_Main"), bpy.data.objects.get("EMP_Subject")
    if not r.check(cam is not None and sub is not None and cam.type == "CAMERA" and bpy.context.scene.camera == cam, "CAM_Main (caméra de la scène) et EMP_Subject présents", "Partez du fichier de départ.", 2):
        return r.finish()
    sc = bpy.context.scene
    r.check(sc.frame_start == 1 and sc.frame_end == 72 and sc.render.fps == 24, f"Plage {sc.frame_start}–{sc.frame_end} à {sc.render.fps} i/s (1–72 à 24)", "Ne changez pas la plage.", 1)
    P = np.zeros((73, 3))
    err = np.zeros(73)
    roll = np.zeros(73)
    for f in range(1, 73):
        sc.frame_set(f)
        bpy.context.view_layer.update()
        m = cam.matrix_world
        p = np.array(m.translation)
        P[f] = p
        fwd = -np.array([m[0][2], m[1][2], m[2][2]])
        d = np.array(sub.matrix_world.translation) - p
        err[f] = math.degrees(math.acos(max(-1.0, min(1.0, float(np.dot(fwd / np.linalg.norm(fwd), d / np.linalg.norm(d)))))))
        xaxis = np.array([m[0][0], m[1][0], m[2][0]])
        roll[f] = math.degrees(math.asin(max(-1.0, min(1.0, float(xaxis[2] / np.linalg.norm(xaxis))))))
    sc.frame_set(1)
    ys = smooth(P[1:, 1])
    zs = smooth(P[1:, 2])
    r.check(abs(ys[0] + 8) <= 0.10 and abs(ys[-1] + 4) <= 0.10 and abs(float(P[1:, 2].mean()) - 1.6) <= 0.1, f"Travelling : Y de {ys[0]:.2f} m à {ys[-1]:.2f} m (−8 → −4 ± 0,1) ; hauteur moyenne {float(P[1:, 2].mean()):.2f} m (1,6 ± 0,1)", "Clés de position Y aux images 1 (−8) et 72 (−4).", 6)
    v = np.diff(ys)
    vmax = float(np.abs(v).max())
    ends = max(float(np.abs(v[:3]).mean()), float(np.abs(v[-3:]).mean()))
    back = float(max(0.0, -(np.diff(ys)).min() * 0)) if False else float(max(0.0, (ys[:-1] - ys[1:]).max()))
    r.check(vmax > 0 and ends <= 0.25 * vmax and back <= 0.05, f"Départ et arrivée doux : vitesse aux extrémités {1000 * ends:.0f} mm/image pour un maximum de {1000 * vmax:.0f} (≤ 25 %) ; recul maximal {1000 * back:.0f} mm (≤ 50)", "Interpolation Bezier sur la courbe Y (pas Linear).", 6)
    tr = [c for c in cam.constraints if c.type in ("TRACK_TO", "DAMPED_TRACK", "LOCKED_TRACK") and c.target == sub]
    e = float(err[1:].max())
    r.check(bool(tr) and e <= 1.0, f"Suivi : contrainte de visée sur EMP_Subject : {'oui' if tr else 'non'} ; écart maximal de visée {e:.2f}° (≤ 1)", "Contrainte Track To vers EMP_Subject (Track Axis −Z, Up Y).", 8)
    fcs = {(f.data_path, f.array_index): f for f in fcurves(cam.animation_data.action)} if cam.animation_data and cam.animation_data.action else {}
    nz = {i: [m for m in fcs[("location", i)].modifiers if m.type == "NOISE"] for i in (0, 1, 2) if ("location", i) in fcs}
    okn = all(nz.get(i) and 0.02 <= nz[i][0].strength <= 0.2 for i in (0, 2)) and not nz.get(1)
    r.check(okn, f"Tremblé : Noise sur X et Z (Strength {[round(nz[i][0].strength, 3) if nz.get(i) else None for i in (0, 2)]}, 0,02–0,2) ; aucun sur Y : {'oui' if not nz.get(1) else 'NON'}", "Graph Editor : modificateur Noise sur X et Z Location de la caméra.", 5)
    resid = np.concatenate([P[1:, 0] - smooth(P[1:, 0]), P[1:, 2] - zs])
    sd, mx = float(resid.std()), float(np.abs(resid).max())
    r.check(0.003 <= sd <= 0.025 and mx <= 0.08, f"Tremblé mesuré : écart-type {1000 * sd:.1f} mm (3–25), maximum {1000 * mx:.0f} mm (≤ 80)", "Strength 0,1, Scale 8 : assez pour se sentir, pas pour gêner.", 5)
    rl = float(np.abs(roll[1:]).max())
    r.check(rl <= 1.0, f"Horizon : roulis maximal {rl:.2f}° (≤ 1)", "L'horizon doit rester horizontal (Track To, Up Y).", 4)
    if debug:
        print("[DEBUG] y", round(float(ys[0]), 3), round(float(ys[-1]), 3), "zmean", round(float(P[1:, 2].mean()), 3), "ends", round(ends, 4), "vmax", round(vmax, 4), "back", round(back, 4), "err", round(e, 3), "sd", round(sd, 4), "mx", round(mx, 3), "roll", round(rl, 2))
    return r.finish()


if __name__ == "__main__":
    L.run(main)
