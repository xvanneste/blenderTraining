"""
validate_ch07_15.py — Correcteur « Scène dialoguée » (CH07.15 : blocking, splining).
Usage : … --python-exit-code 1 --python validate_ch07_15.py -- --exercise dialogue [--debug]
Objet : GEO_Head (lacet autour de Z) ; plage 1–73 à 24 i/s ; poses : images 1, 13, 25, 37, 49, 61, 73 : 0°, +40°, +40°, −30°, −30°, 0°, 0°.
  Actions : « BLOCK » (blocking) INTACTE : clés exactement aux 7 images, valeurs des poses (± 0,5°), toutes en interpolation CONSTANT ;
            « FINAL » (splining) ACTIVE sur GEO_Head : contient les 7 images des poses avec les mêmes valeurs (± 0,5°), au moins 2 clés supplémentaires (breakdowns), toutes les clés en BEZIER.
  Évalué (action active) : variation maximale du lacet d'une image à l'autre ≤ 10° ; maintiens plats : lacet à l'image 19 = +40° ± 1,5°, à l'image 43 = −30° ± 1,5°, à l'image 67 = 0° ± 1,5°.
  Marqueurs « beat_1 » à « beat_7 » aux images des poses ; plage de la scène 1–73 à 24 i/s.
Testé avec : Blender 5.3.0.
"""
import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bpy  # noqa: E402

BEATS = [(1, 0.0), (13, 40.0), (25, 40.0), (37, -30.0), (49, -30.0), (61, 0.0), (73, 0.0)]


def fcurves(act):
    try:
        return list(act.fcurves)
    except AttributeError:
        return [f for l in act.layers for st in l.strips for cb in st.channelbags for f in cb.fcurves]


def yaw_curve(act):
    return next((f for f in fcurves(act) if f.data_path == "rotation_euler" and f.array_index == 2), None)


def main():
    debug = L.flag("--debug")
    r = L.Report("CH07.15 — Scène dialoguée (blocking, splining)")
    ob = bpy.data.objects.get("GEO_Head")
    block, final = bpy.data.actions.get("BLOCK"), bpy.data.actions.get("FINAL")
    if not r.check(ob is not None and block is not None and final is not None and ob.animation_data is not None, "GEO_Head et les actions BLOCK et FINAL présentes", "Dupliquez BLOCK en FINAL.", 3):
        return r.finish()
    sc = bpy.context.scene
    r.check(sc.frame_start == 1 and sc.frame_end == 73 and sc.render.fps == 24, f"Plage {sc.frame_start}–{sc.frame_end} à {sc.render.fps} i/s (1–73 à 24)", "Ne changez pas la plage.", 1)
    fb, ff = yaw_curve(block), yaw_curve(final)
    kb = [(round(k.co[0]), math.degrees(k.co[1]), k.interpolation) for k in fb.keyframe_points] if fb else []
    r.check([f for f, v, i in kb] == [f for f, a in BEATS] and all(abs(v - a) <= 0.5 for (f, v, i), (f2, a) in zip(kb, BEATS)) and all(i == "CONSTANT" for f, v, i in kb), f"BLOCK intacte : {len(kb)} clés aux images {[f for f, v, i in kb]}, toutes CONSTANT : {'oui' if kb and all(i == 'CONSTANT' for f, v, i in kb) else 'non'}", "Ne modifiez pas BLOCK : c'est le blocking de référence.", 5)
    r.check(ob.animation_data.action == final, f"FINAL est l'action active (active : {ob.animation_data.action.name if ob.animation_data.action else None})", "Assignez FINAL à GEO_Head.", 3)
    kf = {round(k.co[0]): (math.degrees(k.co[1]), k.interpolation) for k in ff.keyframe_points} if ff else {}
    r.check(all(f in kf and abs(kf[f][0] - a) <= 0.5 for f, a in BEATS), f"FINAL garde les 7 poses (valeurs ± 0,5°) : {'oui' if all(f in kf and abs(kf[f][0] - a) <= 0.5 for f, a in BEATS) else 'non'}", "Splining : les poses ne changent pas.", 5)
    extra = [f for f in kf if f not in [b for b, a in BEATS]]
    r.check(len(extra) >= 2, f"Breakdowns : {len(extra)} clés supplémentaires (≥ 2) aux images {sorted(extra)}", "Ajoutez des clés entre les poses (images 7, 31, 55).", 3)
    r.check(bool(kf) and all(i == "BEZIER" for a, i in kf.values()), "Toutes les clés de FINAL sont en Bezier", "Dope Sheet : T > Bezier.", 4)
    ang = []
    for f in range(1, 74):
        sc.frame_set(f)
        bpy.context.view_layer.update()
        ang.append(math.degrees(ob.rotation_euler.z))
    sc.frame_set(1)
    dmax = max(abs(ang[i + 1] - ang[i]) for i in range(72))
    r.check(dmax <= 10.0, f"Mouvement lisse : variation maximale du lacet {dmax:.1f}°/image (≤ 10)", "Bezier : plus de sauts entre les poses.", 4)
    holds = (abs(ang[18] - 40), abs(ang[42] + 30), abs(ang[66]))
    r.check(max(holds) <= 1.5, f"Maintiens plats : écarts {[round(h, 2) for h in holds]}° aux images 19, 43, 67 (≤ 1,5)", "Poignées Auto Clamped : un maintien entre deux clés égales reste plat ; pas de breakdown dans un maintien.", 5)
    mk = {m.name: m.frame for m in sc.timeline_markers}
    r.check(all(mk.get(f"beat_{i}") == f for i, (f, a) in enumerate(BEATS, 1)), f"Marqueurs beat_1 à beat_7 : {'conformes' if all(mk.get(f'beat_{i}') == f for i, (f, a) in enumerate(BEATS, 1)) else 'manquants ou mal placés'}", "M dans la timeline, nommer chaque marqueur.", 3)
    if debug:
        print("[DEBUG] kb", kb, "kf", sorted(kf.items()), "dmax", round(dmax, 2), "holds", [round(h, 2) for h in holds], "mk", mk)
    return r.finish()


if __name__ == "__main__":
    L.run(main)
