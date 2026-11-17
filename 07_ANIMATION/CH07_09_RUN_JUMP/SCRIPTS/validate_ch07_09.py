"""
validate_ch07_09.py — Correcteur « Course, saut, interactions » (CH07.09 : le saut).
Usage : … --python-exit-code 1 --python validate_ch07_09.py -- --exercise jump [--debug]
Objets : CHR_Mannequin, RIG_Mannequin (13 bones) ; saut sur place, plage 1–40 à 24 i/s. Mesures sur les positions monde ÉVALUÉES : hanches = début du bone hips, chevilles = fin de shin.L et shin.R.
  Hauteur debout : 0,95 m (image 1).
  Anticipation : les hanches descendent à 0,78 m ou moins avant le décollage (images 2 à 9).
  Vol : la plus longue série d'images où les DEUX chevilles sont à plus de 0,07 m du sol dure de 10 à 18 images ; les hanches montent d'au moins 0,30 m et d'au plus 0,55 m au-dessus de 0,95 m.
  Gravité : accélération médiane (différence seconde de z des hanches) pendant le vol (bords exclus) entre −0,0221 et −0,0119 m/image² (g = 0,01703) ; accélération déduite 8·h/T² (h = hauteur, T = durée du vol) entre 0,0119 et 0,0221.
  Réception : dans les 8 images après l'atterrissage, les hanches descendent à 0,80 m ou moins (amortissement).
  Pieds plantés : hors du vol (images 1 à 9 et après la réception), chevilles à z ≤ 0,065 m et déplacement horizontal ≤ 2 cm par rapport à l'image 1.
  Retour : à l'image 40, hanches à 0,95 ± 0,03 m et chevilles au sol.
  Sol : cheville jamais sous 0,04 m.
Testé avec : Blender 5.3.0.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bpy  # noqa: E402
import numpy as np  # noqa: E402

NAMES = ("hips", "shin.L", "shin.R")


def main():
    debug = L.flag("--debug")
    r = L.Report("CH07.09 — Le saut (anticipation, vol, réception)")
    rig = bpy.data.objects.get("RIG_Mannequin")
    if not r.check(rig is not None and rig.type == "ARMATURE" and all(n in rig.pose.bones for n in NAMES) and rig.animation_data is not None and rig.animation_data.action is not None, "RIG_Mannequin animé présent", "Partez du fichier de départ.", 2):
        return r.finish()
    sc = bpy.context.scene
    r.check(sc.frame_start == 1 and sc.frame_end == 40 and sc.render.fps == 24, f"Plage {sc.frame_start}–{sc.frame_end} à {sc.render.fps} i/s (1–40 à 24)", "Ne changez pas la plage.", 1)
    hz, aL, aR = np.zeros(41), np.zeros((41, 3)), np.zeros((41, 3))
    for f in range(1, 41):
        sc.frame_set(f)
        bpy.context.view_layer.update()
        mw = rig.matrix_world
        hz[f] = (mw @ rig.pose.bones["hips"].head).z
        aL[f] = np.array(mw @ rig.pose.bones["shin.L"].tail)
        aR[f] = np.array(mw @ rig.pose.bones["shin.R"].tail)
    sc.frame_set(1)
    r.check(abs(hz[1] - 0.95) <= 0.03, f"Debout : hanches à {hz[1]:.3f} m à l'image 1 (0,95 ± 0,03)", "Départ debout.", 2)
    r.check(float(hz[2:10].min()) <= 0.78, f"Anticipation : hanches à {float(hz[2:10].min()):.2f} m avant le décollage (≤ 0,78)", "Fléchissez avant de sauter.", 6)
    air = np.array([min(aL[f][2], aR[f][2]) > 0.07 for f in range(1, 41)])
    best, i = (0, -1), 0
    while i < 40:
        if air[i]:
            j = i
            while j + 1 < 40 and air[j + 1]:
                j += 1
            if j - i > best[1] - best[0]:
                best = (i, j)
            i = j + 1
        else:
            i += 1
    t0, t1 = best[0] + 1, best[1] + 1
    T = t1 - t0 + 1 if best[1] >= 0 else 0
    h = float(hz[t0:t1 + 1].max() - 0.95) if T else 0.0
    r.check(10 <= T <= 18 and 0.30 <= h <= 0.55, f"Vol : {T} images (images {t0} à {t1} ; 10–18), hauteur {h:.2f} m au-dessus de 0,95 (0,30–0,55)", "Les deux pieds quittent le sol 10 à 18 images ; apex à 0,3–0,55 m.", 7)
    d2 = hz[2:] - 2 * hz[1:-1] + hz[:-2]                              # d2[i] ↔ image i + 2
    inner = [f for f in range(t0 + 2, t1 - 1) if 2 <= f <= 40]
    med = float(np.median([d2[f - 2] for f in inner])) if len(inner) >= 3 else 0.0
    ag = 8 * h / (max(T + 1, 1) ** 2) if T else 0.0
    r.check(-0.0221 <= med <= -0.0119 and 0.0119 <= ag <= 0.0221, f"Gravité : accélération médiane {med:.4f} m/image² (−0,0221 à −0,0119) ; 8·h/T² = {ag:.4f} (0,0119–0,0221 ; g = 0,0170)", "Parabole : hauteur et durée du vol liées par h = g·T²/8.", 7)
    land = t1 + 1
    after = hz[land:min(land + 9, 41)]
    r.check(len(after) > 0 and float(after.min()) <= 0.80, f"Réception : hanches à {float(after.min()) if len(after) else 9:.2f} m après l'atterrissage (≤ 0,80)", "Amortissez la réception.", 6)
    planted = [f for f in range(1, 41) if f < t0 - 1 or f > land + 8]
    zmax = max(max(aL[f][2], aR[f][2]) for f in planted) if planted else 9
    drift = max(max(np.linalg.norm(aL[f][:2] - aL[1][:2]), np.linalg.norm(aR[f][:2] - aR[1][:2])) for f in planted) if planted else 9
    r.check(zmax <= 0.065 and drift <= 0.02, f"Pieds plantés hors du vol : z max {zmax:.3f} m (≤ 0,065), glissement {1000 * drift:.0f} mm (≤ 20)", "Pieds au sol et immobiles avant et après le saut.", 6)
    r.check(abs(hz[40] - 0.95) <= 0.03 and max(aL[40][2], aR[40][2]) <= 0.065, f"Retour debout : hanches à {hz[40]:.3f} m à l'image 40 (0,95 ± 0,03), chevilles au sol", "Revenez debout avant la fin.", 4)
    zmin = float(min(aL[1:, 2].min(), aR[1:, 2].min()))
    r.check(zmin >= 0.04, f"Sol : cheville la plus basse à {zmin:.3f} m (≥ 0,04)", "Les pieds ne traversent pas le sol.", 2)
    if debug:
        print("[DEBUG] hz1", round(hz[1], 3), "crouch", round(float(hz[2:10].min()), 3), "flight", t0, t1, T, "h", round(h, 3), "med", round(med, 4), "ag", round(ag, 4), "land", round(float(after.min()), 3), "zmax", round(zmax, 3), "drift", round(float(drift), 3), "hz40", round(hz[40], 3))
    return r.finish()


if __name__ == "__main__":
    L.run(main)
