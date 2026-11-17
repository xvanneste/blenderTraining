"""
validate_ch07_11.py — Correcteur « Animation faciale et lip sync » (CH07.11).
Usage : … --python-exit-code 1 --python validate_ch07_11.py -- --exercise lipsync [--debug]
Objets : GEO_Face, RIG_Face (bones jaw, ctl_smile, ctl_blink) ; plage 1–48 à 24 i/s ; piste de phonèmes : 1 M, 7 A, 13 O, 19 E, 25 M, 31 A, 37 E, 43 M.
  Mesures sur les valeurs ÉVALUÉES : angle de jaw (rotation X, degrés), position X de ctl_smile et de ctl_blink (mètres).
  Visèmes : M : jaw 0° ; A : −12° ; O : −7° ; E : −4° avec ctl_smile à 0,04 m (autres visèmes : sourire 0) ; tolérances ± 1,5° et ± 0,008 m ; vérifiés aux images f − 1 et f (l'image 1 compte seule).
  Bouche fermée sur M : mâchoire à moins de 1,5° (compris dans les visèmes) ; variété : les trois ouvertures (A, O, E) diffèrent d'au moins 2° deux à deux.
  Continuité : la mâchoire ne change jamais de plus de 6° d'une image à l'autre ; le sourire ne change jamais de plus de 0,03 m d'une image à l'autre.
  Clignement : ctl_blink atteint 0,045 m ou plus ; l'intervalle où il dépasse 0,005 m dure de 3 à 8 images et commence entre les images 17 et 21 ; il vaut 0 (± 0,005 m) avant l'image 16 et après l'image 26.
Testé avec : Blender 5.3.0.
"""
import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bpy  # noqa: E402
import numpy as np  # noqa: E402

PHON = [(1, "M"), (7, "A"), (13, "O"), (19, "E"), (25, "M"), (31, "A"), (37, "E"), (43, "M")]
VISEME = {"M": (0.0, 0.0), "A": (-12.0, 0.0), "O": (-7.0, 0.0), "E": (-4.0, 0.04)}


def main():
    debug = L.flag("--debug")
    r = L.Report("CH07.11 — Lip sync (visèmes, continuité, clignement)")
    rig = bpy.data.objects.get("RIG_Face")
    if not r.check(rig is not None and all(n in rig.pose.bones for n in ("jaw", "ctl_smile", "ctl_blink")) and rig.animation_data is not None and rig.animation_data.action is not None, "RIG_Face animé présent (jaw, ctl_smile, ctl_blink)", "Partez du fichier de départ.", 2):
        return r.finish()
    sc = bpy.context.scene
    r.check(sc.frame_start == 1 and sc.frame_end == 48 and sc.render.fps == 24, f"Plage {sc.frame_start}–{sc.frame_end} à {sc.render.fps} i/s (1–48 à 24)", "Ne changez pas la plage.", 1)
    jaw, smile, blink = np.zeros(49), np.zeros(49), np.zeros(49)
    pb = rig.pose.bones
    for f in range(1, 49):
        sc.frame_set(f)
        bpy.context.view_layer.update()
        jaw[f] = math.degrees(pb["jaw"].rotation_euler.x)
        smile[f] = pb["ctl_smile"].location.x
        blink[f] = pb["ctl_blink"].location.x
    sc.frame_set(1)
    bad = []
    for f, p in PHON:
        tj, ts = VISEME[p]
        for ff in (f - 1, f):
            if ff >= 1 and (abs(jaw[ff] - tj) > 1.5 or abs(smile[ff] - ts) > 0.008):
                bad.append((ff, p, round(float(jaw[ff]), 1), round(float(smile[ff]), 3)))
    r.check(not bad, f"Visèmes : {'tous justes' if not bad else 'faux à ' + str(bad[:3])} (images f − 1 et f de chaque phonème)", "Mâchoire A −12°, O −7°, E −4° et sourire 0,04 ; M fermée ; forme atteinte une image avant le son.", 14)
    ops = [float(jaw[7]), float(jaw[13]), float(jaw[19])]                  # A, O, E
    gap = min(abs(ops[0] - ops[1]), abs(ops[0] - ops[2]), abs(ops[1] - ops[2]))
    r.check(gap >= 2.0, f"Variété : ouvertures A, O, E = {[round(o, 1) for o in ops]}° (différentes d'au moins 2° deux à deux ; écart minimal {gap:.1f}°)", "Chaque voyelle a sa forme.", 4)
    dj = float(np.abs(np.diff(jaw[1:])).max())
    ds = float(np.abs(np.diff(smile[1:])).max())
    r.check(dj <= 6.0 and ds <= 0.03, f"Continuité : saut maximal de la mâchoire {dj:.1f}° (≤ 6), du sourire {1000 * ds:.0f} mm (≤ 30)", "Pas de saut : interpolation Bezier ou Linear, pas Constant.", 6)
    on = [f for f in range(1, 49) if blink[f] > 0.005]
    dur = (on[-1] - on[0] + 1) if on else 0
    st = on[0] if on else 0
    ok = bool(on) and float(blink.max()) >= 0.045 and 3 <= dur <= 8 and 17 <= st <= 21 and float(np.abs(blink[1:16]).max()) <= 0.005 and float(np.abs(blink[27:49]).max()) <= 0.005
    r.check(ok, f"Clignement : maximum {1000 * float(blink.max()):.0f} mm (≥ 45), durée {dur} images (3–8), départ à l'image {st} (17–21)", "ctl_blink : 0 → 0,05 → 0 en 4 images environ, vers l'image 19.", 8)
    if debug:
        print("[DEBUG] bad", bad, "ops", [round(o, 1) for o in ops], "dj", round(dj, 2), "ds", round(ds, 4), "blink", on[:1], on[-1:], round(float(blink.max()), 3))
    return r.finish()


if __name__ == "__main__":
    L.run(main)
