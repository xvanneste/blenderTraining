"""
validate_ch07_10.py — Correcteur « Acting » (CH07.10 : plan d'acting muet).
Usage : … --python-exit-code 1 --python validate_ch07_10.py -- --exercise acting [--debug]
Objets : CHR_Mannequin, RIG_Mannequin (13 bones) ; plage 1–72 à 24 i/s. Mesures sur la pose ÉVALUÉE de chaque image :
  lacet d'un bone = rotation de son axe X (monde) autour de Z, en degrés, par rapport au repos ; inclinaison de la colonne = angle du bone spine par rapport à la verticale dans le plan Y–Z (positif : vers l'avant, −Y).
  Idle : tête, buste (chest) et hanches immobiles (lacet ≤ 2°, inclinaison ≤ 2°) de l'image 1 à 18.
  Remarque : début du mouvement de la tête = première image où son lacet dépasse 3° ; elle atteint 90 % de son maximum en 10 images ou moins ; maximum de 40° à 70° (en valeur absolue).
  Retard du corps : le buste commence (lacet > 3°) 2 à 8 images après la tête ; les hanches commencent (lacet > 3°) au moins 2 images après le buste ; lacet final du buste (image 45) d'au moins 20°.
  Temps de pensée : le lacet de la tête varie d'au plus 3° entre l'image 28 et l'image 45.
  Anticipation : inclinaison de la colonne ≤ −5° (en arrière) quelque part entre les images 45 et 55, puis ≥ +8° (en avant) entre les images 56 et 72.
Testé avec : Blender 5.3.0.
"""
import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bpy  # noqa: E402
import numpy as np  # noqa: E402

NAMES = ("hips", "spine", "chest", "head")


def main():
    debug = L.flag("--debug")
    r = L.Report("CH07.10 — Acting muet (intention, maintien, anticipation)")
    rig = bpy.data.objects.get("RIG_Mannequin")
    if not r.check(rig is not None and rig.type == "ARMATURE" and all(n in rig.pose.bones for n in NAMES) and rig.animation_data is not None and rig.animation_data.action is not None, "RIG_Mannequin animé présent", "Partez du fichier de départ.", 2):
        return r.finish()
    sc = bpy.context.scene
    r.check(sc.frame_start == 1 and sc.frame_end == 72 and sc.render.fps == 24, f"Plage {sc.frame_start}–{sc.frame_end} à {sc.render.fps} i/s (1–72 à 24)", "Ne changez pas la plage.", 1)
    rest = {n: math.atan2(rig.data.bones[n].matrix_local[1][0], rig.data.bones[n].matrix_local[0][0]) for n in NAMES}
    yaw = {n: np.zeros(73) for n in ("hips", "chest", "head")}
    pitch = np.zeros(73)
    for f in range(1, 73):
        sc.frame_set(f)
        bpy.context.view_layer.update()
        mw = rig.matrix_world
        for n in yaw:
            m = mw @ rig.pose.bones[n].matrix
            d = math.degrees(math.atan2(m[1][0], m[0][0]) - rest[n])
            yaw[n][f] = (d + 180) % 360 - 180
        s = rig.pose.bones["spine"]
        v = (mw @ s.tail) - (mw @ s.head)
        pitch[f] = math.degrees(math.atan2(-v.y, v.z))
    sc.frame_set(1)

    def first(a, thr=3.0):
        idx = [f for f in range(1, 73) if abs(a[f]) > thr]
        return idx[0] if idx else None
    idle = max(max(float(np.abs(yaw[n][1:19]).max()) for n in yaw), float(np.abs(pitch[1:19]).max()))
    r.check(idle <= 2.0, f"Idle : mouvement maximal de {idle:.1f}° de l'image 1 à 18 (≤ 2)", "Laissez le personnage immobile avant la remarque.", 5)
    th = first(yaw["head"])
    peak = float(np.abs(yaw["head"][1:73]).max())
    quick = None
    if th is not None:
        reach = [f for f in range(th, 73) if abs(yaw["head"][f]) >= 0.9 * peak]
        quick = (reach[0] - th) if reach else None
    r.check(th is not None and quick is not None and quick <= 10 and 40 <= peak <= 70, f"Remarque : la tête démarre à l'image {th}, atteint 90 % en {quick} images (≤ 10), maximum {peak:.0f}° (40–70)", "Une remarque est rapide : 6 à 8 images pour tourner la tête.", 8)
    tc, tw = first(yaw["chest"]), first(yaw["hips"])
    lag1 = (tc - th) if (tc and th) else None
    lag2 = (tw - tc) if (tw and tc) else None
    r.check(lag1 is not None and 2 <= lag1 <= 8 and lag2 is not None and lag2 >= 2 and abs(yaw["chest"][45]) >= 20, f"Retard du corps : buste {lag1} images après la tête (2–8), hanches {lag2} images après le buste (≥ 2) ; buste final {abs(yaw['chest'][45]):.0f}° (≥ 20)", "La tête mène, le buste suit, les hanches ensuite.", 8)
    hold = float(np.ptp(yaw["head"][28:46]))
    r.check(hold <= 3.0, f"Temps de pensée : la tête varie de {hold:.1f}° entre les images 28 et 45 (≤ 3)", "Maintenez la tête : la pensée se lit dans l'immobilité.", 7)
    back, fwd = float(pitch[45:56].min()), float(pitch[56:73].max())
    r.check(back <= -5.0 and fwd >= 8.0, f"Anticipation : colonne à {back:.1f}° en arrière (≤ −5) puis {fwd:.1f}° en avant (≥ 8)", "Reculez avant d'avancer : l'anticipation prépare l'action.", 8)
    if debug:
        print("[DEBUG] idle", round(idle, 2), "th", th, "quick", quick, "peak", round(peak, 1), "tc", tc, "tw", tw, "lag", lag1, lag2, "chest45", round(float(yaw["chest"][45]), 1), "hold", round(hold, 2), "back/fwd", round(back, 1), round(fwd, 1))
    return r.finish()


if __name__ == "__main__":
    L.run(main)
