"""
validate_ch07_06.py — Correcteur « Arcs, overlap, follow-through » (CH07.06).
Usage : … --python-exit-code 1 --python validate_ch07_06.py -- --exercise overlap [--debug]
Objet : RIG_Antenna (bones base, tail_1, tail_2, tail_3 en chaîne ; rotation X locale animée ; plage 1–48 à 24 i/s).
  Mesures sur la rotation X ÉVALUÉE de chaque bone (degrés), images 1 à 48 :
    Base : maximum à l'image 13 (± 1) et d'au moins 20° ; de retour à ≤ 1° à l'image 26.
    Overlap : le maximum de chaque bone de queue (images 1 à 40) survient APRÈS celui de son parent, avec un retard de 1 à 4 images ; amplitude d'au moins 5° pour chaque bone de queue.
    Follow-through : à l'image 26 (la base est arrêtée) tail_3 est encore à 3° ou plus ; OVERSHOOT : tail_3 descend à −3° ou moins entre les images 31 et 44.
    Repos : tous les bones à ≤ 1° aux images 46 à 48.
    Arc : la pointe de tail_3 (images 1 à 30) s écarte d au moins 8 cm de la droite qui joint ses positions aux images 1 et 30 (trajectoire courbe).
Testé avec : Blender 5.3.0.
"""
import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bpy  # noqa: E402
import numpy as np  # noqa: E402

NAMES = ("base", "tail_1", "tail_2", "tail_3")


def main():
    debug = L.flag("--debug")
    r = L.Report("CH07.06 — Arcs, overlap, follow-through")
    rig = bpy.data.objects.get("RIG_Antenna")
    if not r.check(rig is not None and rig.type == "ARMATURE" and all(n in rig.pose.bones for n in NAMES) and rig.animation_data is not None and rig.animation_data.action is not None, "RIG_Antenna animé présent (base, tail_1, tail_2, tail_3)", "Partez du fichier de départ.", 2):
        return r.finish()
    sc = bpy.context.scene
    r.check(sc.frame_start == 1 and sc.frame_end == 48 and sc.render.fps == 24, f"Plage {sc.frame_start}–{sc.frame_end} à {sc.render.fps} i/s (1–48 à 24)", "Ne changez pas la plage.", 1)
    ang = {n: [] for n in NAMES}
    tip = []
    for f in range(1, 49):
        sc.frame_set(f)
        bpy.context.view_layer.update()
        for n in NAMES:
            ang[n].append(math.degrees(rig.pose.bones[n].rotation_euler.x))
        tip.append(np.array(rig.matrix_world @ rig.pose.bones["tail_3"].tail))
    sc.frame_set(1)
    A = {n: np.array(v) for n, v in ang.items()}                       # A[n][f - 1]
    pk = {n: int(np.argmax(A[n][:40])) + 1 for n in NAMES}
    r.check(abs(pk["base"] - 13) <= 1 and A["base"].max() >= 20 and abs(A["base"][25]) <= 1.0, f"Base : maximum {A['base'].max():.1f}° à l'image {pk['base']} (13 ± 1, ≥ 20°) ; image 26 : {A['base'][25]:.1f}° (≤ 1)", "Ne modifiez pas la base.", 3)
    lags = [pk[NAMES[i + 1]] - pk[NAMES[i]] for i in range(3)]
    amp = [float(A[n][:40].max()) for n in NAMES[1:]]
    r.check(all(1 <= l <= 4 for l in lags) and all(a >= 5 for a in amp), f"Overlap : maxima aux images {[pk[n] for n in NAMES]} (retards {lags}, attendus 1 à 4 images) ; amplitudes {[round(a, 1) for a in amp]}° (≥ 5)", "Chaque bone atteint son maximum 2 images après son parent.", 7)
    t3 = A["tail_3"]
    r.check(t3[25] >= 3.0, f"Follow-through : à l'image 26, tail_3 est encore à {t3[25]:.1f}° (≥ 3) alors que la base est arrêtée", "La queue continue quand la base s'arrête.", 5)
    r.check(float(t3[30:44].min()) <= -3.0, f"Overshoot : tail_3 descend à {t3[30:44].min():.1f}° entre les images 31 et 44 (≤ −3)", "La pointe dépasse le repos avant de se stabiliser.", 4)
    r.check(all(float(np.abs(A[n][45:48]).max()) <= 1.0 for n in NAMES), f"Repos : tous les bones à ≤ 1° aux images 46–48 (max {max(float(np.abs(A[n][45:48]).max()) for n in NAMES):.1f}°)", "Terminez au repos.", 3)
    p0, p1 = tip[0], tip[29]
    d = p1 - p0
    dev = 0.0
    for p in tip[:30]:
        t = float(np.dot(p - p0, d) / max(float(np.dot(d, d)), 1e-9))
        dev = max(dev, float(np.linalg.norm(p - (p0 + d * t))))
    r.check(dev >= 0.08, f"Arc : la pointe s'écarte de {100 * dev:.1f} cm de la droite entre ses positions aux images 1 et 30 (≥ 8 cm)", "Une chaîne animée avec retard décrit une courbe.", 3)
    if debug:
        print("[DEBUG] peaks", pk, "lags", lags, "amp", [round(a, 1) for a in amp], "t3_26", round(float(t3[25]), 2), "t3 min", round(float(t3[30:44].min()), 2), "dev", round(dev, 3), "rest", [round(float(np.abs(A[n][45:48]).max()), 2) for n in NAMES])
    return r.finish()


if __name__ == "__main__":
    L.run(main)
