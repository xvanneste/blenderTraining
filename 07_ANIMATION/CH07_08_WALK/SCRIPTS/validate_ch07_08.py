"""
validate_ch07_08.py — Correcteur « Cycles de marche » (CH07.08).
Usage : … --python-exit-code 1 --python validate_ch07_08.py -- --exercise walk [--debug]
Objets : CHR_Mannequin, RIG_Mannequin (13 bones), animation de marche SUR PLACE, plage 1–25 à 24 i/s ; l'avant est −Y. Mesures sur les positions monde ÉVALUÉES (chevilles = fin de shin, genoux = début de shin, poignets = fin de fore, hanches = début de hips).
  Boucle : l'image 25 reprend l'image 1 (chevilles, genoux, poignets, hanches : écart ≤ 1 cm) ; demi-cycle : à l'image 13, la cheville gauche est où était la droite à l'image 1 (≤ 3 cm) et inversement.
  Pas : à l'image 1, écart des chevilles en Y entre 0,45 et 0,75 m.
  Sol : chaque pied est au sol (z de la cheville ≤ 0,065 m) pendant 9 à 15 des 24 images du cycle ; en ballant, la cheville monte d'au moins 6 cm au-dessus de sa hauteur au sol (0,05 m).
  Glissement : pendant l'appui (plus longue série d'images où la cheville est au sol, première et dernière image écartées), la cheville recule (+Y) de 0,035 à 0,065 m/image, à vitesse constante : écart maximal à la droite ajustée ≤ 3 cm.
  Hanches : amplitude verticale de 0,02 à 0,08 m ; aux contacts (images 1 et 13) plus basses d'au moins 2 cm qu'aux passages (images 7 et 19).
  Bras : opposés aux jambes : si le pied gauche est devant à l'image 1, le poignet gauche est derrière le droit d'au moins 10 cm (et inversement).
Testé avec : Blender 5.3.0.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bpy  # noqa: E402
import numpy as np  # noqa: E402

NAMES = ("hips", "thigh.L", "shin.L", "thigh.R", "shin.R", "fore.L", "fore.R")


def main():
    debug = L.flag("--debug")
    r = L.Report("CH07.08 — Cycles de marche")
    rig = bpy.data.objects.get("RIG_Mannequin")
    if not r.check(rig is not None and rig.type == "ARMATURE" and all(n in rig.pose.bones for n in NAMES) and rig.animation_data is not None and rig.animation_data.action is not None, "RIG_Mannequin animé présent", "Partez du fichier de départ.", 2):
        return r.finish()
    sc = bpy.context.scene
    r.check(sc.frame_start == 1 and sc.frame_end == 25 and sc.render.fps == 24, f"Plage {sc.frame_start}–{sc.frame_end} à {sc.render.fps} i/s (1–25 à 24)", "Ne changez pas la plage.", 1)
    D = {k: [] for k in ("aL", "aR", "kL", "kR", "wL", "wR", "hz")}
    for f in range(1, 26):
        sc.frame_set(f)
        bpy.context.view_layer.update()
        mw = rig.matrix_world
        pb = rig.pose.bones
        D["aL"].append(np.array(mw @ pb["shin.L"].tail))
        D["aR"].append(np.array(mw @ pb["shin.R"].tail))
        D["kL"].append(np.array(mw @ pb["shin.L"].head))
        D["kR"].append(np.array(mw @ pb["shin.R"].head))
        D["wL"].append(np.array(mw @ pb["fore.L"].tail))
        D["wR"].append(np.array(mw @ pb["fore.R"].tail))
        D["hz"].append(float((mw @ pb["hips"].head).z))
    sc.frame_set(1)
    A = {k: np.array(v) for k, v in D.items()}                         # A[k][f - 1]
    loop = max(float(np.linalg.norm(A[k][24] - A[k][0])) for k in ("aL", "aR", "kL", "kR", "wL", "wR")) + abs(A["hz"][24] - A["hz"][0])
    mir = max(abs(A["aL"][12][1] - A["aR"][0][1]), abs(A["aR"][12][1] - A["aL"][0][1]))
    r.check(loop <= 0.01 and mir <= 0.03, f"Boucle : image 25 = image 1 (écart {1000 * loop:.1f} mm ≤ 10) ; demi-cycle : écart {1000 * mir:.1f} mm (≤ 30)", "Dupliquez l'image 1 à l'image 25 ; l'image 13 est l'image 1 inversée gauche/droite.", 8)
    stride = abs(A["aL"][0][1] - A["aR"][0][1])
    r.check(0.45 <= stride <= 0.75, f"Pas : chevilles écartées de {stride:.2f} m au contact (0,45–0,75)", "Jambes écartées de 0,6 m aux contacts.", 5)
    res = {}
    for s in ("L", "R"):
        z = A["a" + s][:24, 2]
        res[s] = (int((z <= 0.065).sum()), float(z.max() - 0.05))
    r.check(all(9 <= res[s][0] <= 15 for s in res) and all(res[s][1] >= 0.06 for s in res), f"Sol : images au sol {res['L'][0]} (G) et {res['R'][0]} (D) sur 24 (9–15) ; levée du pied libre {100 * res['L'][1]:.0f} et {100 * res['R'][1]:.0f} cm (≥ 6)", "Le pied d'appui touche, le pied libre se lève.", 7)
    fits = {}
    for s_ in ("L", "R"):
        z, y = A["a" + s_][:, 2], A["a" + s_][:, 1]
        on = z <= 0.065
        best, i = (0, -1), 0
        while i < 25:
            if on[i]:
                j = i
                while j + 1 < 25 and on[j + 1]:
                    j += 1
                if j - i > best[1] - best[0]:
                    best = (i, j)
                i = j + 1
            else:
                i += 1
        a_, b_ = best[0] + 1, best[1] - 1                                  # on écarte la première et la dernière image de l'appui (transitions du talon et de la pointe)
        if b_ - a_ >= 4:
            xs = np.arange(a_, b_ + 1)
            c = np.polyfit(xs, y[a_:b_ + 1], 1)
            fits[s_] = (float(c[0]), float(np.abs(np.polyval(c, xs) - y[a_:b_ + 1]).max()))
        else:
            fits[s_] = (0.0, 9.0)
    r.check(all(0.035 <= fits[s_][0] <= 0.065 and fits[s_][1] <= 0.03 for s_ in fits), f"Appui sans glissement : la cheville recule de {fits['L'][0]:.3f} (G) et {fits['R'][0]:.3f} (D) m/image (0,035–0,065) ; écart à la droite {1000 * fits['L'][1]:.0f} et {1000 * fits['R'][1]:.0f} mm (≤ 30)", "Pied d'appui à vitesse constante : interpolation Linear, une clé tous les 2 à 3 images.", 8)
    hz = A["hz"][:24]
    rng = float(hz.max() - hz.min())
    low = max(A["hz"][0], A["hz"][12])
    high = min(A["hz"][6], A["hz"][18])
    r.check(0.02 <= rng <= 0.08 and high - low >= 0.02, f"Hanches : amplitude {100 * rng:.1f} cm (2–8) ; contacts {100 * low:.1f} cm, passages {100 * high:.1f} cm (écart ≥ 2 cm)", "Le corps est le plus bas aux contacts, le plus haut aux passages.", 6)
    fwd = "L" if A["aL"][0][1] < A["aR"][0][1] else "R"
    wl, wr = A["wL"][0][1], A["wR"][0][1]
    behind = (wl - wr) if fwd == "L" else (wr - wl)
    r.check(behind >= 0.10, f"Bras opposés aux jambes : pied {fwd} devant, son poignet est derrière l'autre de {100 * behind:.0f} cm (≥ 10)", "Le bras du côté de la jambe avancée recule.", 5)
    if debug:
        print("[DEBUG] loop", round(loop, 4), "mir", round(mir, 4), "stride", round(stride, 3), "res", res, "fits", fits, "rng", round(rng, 3), "low/high", round(low, 3), round(high, 3), "behind", round(behind, 3))
    return r.finish()


if __name__ == "__main__":
    L.run(main)
