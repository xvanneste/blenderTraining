"""
validate_ch06_02.py — Correcteur « Contraintes » (CH06.02).
Usage : … --python-exit-code 1 --python validate_ch06_02.py -- --exercise constraints [--render] [--debug]
RIG_Gaze / EMP_Target :
  Configuration : eye.L et eye.R portent un Damped Track (ou Track To) vers EMP_Target, Track Axis Y ; head porte un Damped Track vers EMP_Target (Track Axis Y, Influence 0,3–0,7)
                  PUIS un Limit Rotation (Z limité à ± 25–45°, espace Local), dans cet ordre.
  Comportement (la cible est DÉPLACÉE) : T1 (0 ; −2 ; 1,74) : yeux à ≤ 1° de la cible, tête sans rotation (< 1°) ;
                  T2 (1,5 ; −1,5 ; 1,74) : yeux à ≤ 1°, rotation de tête entre 15 % et 70 % de l'angle de la cible (≈ 22°) ;
                  T3 (3 ; −0,2 ; 1,74), presque de côté : yeux à ≤ 1° (tant que la tête plafonne), rotation de tête plafonnée (≤ 36°).
Testé avec : Blender 5.3.0.
"""
import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bpy  # noqa: E402
from mathutils import Vector  # noqa: E402


def tracking(c):
    return c.type in ("DAMPED_TRACK", "TRACK_TO") and c.track_axis == "TRACK_Y"


def measure(ob, tgt, pos):
    tgt.location = pos
    bpy.context.view_layer.update()
    ev = ob.evaluated_get(bpy.context.evaluated_depsgraph_get())
    mw = ev.matrix_world
    out = {}
    for n in ("eye.L", "eye.R"):
        pb = ev.pose.bones[n]
        a, b = mw @ pb.head, mw @ pb.tail
        d = (b - a).normalized()
        to = (tgt.matrix_world.translation - a).normalized()
        out[n] = math.degrees(d.angle(to))
    pb = ev.pose.bones["head"]
    f = ((mw @ pb.tail) - (mw @ pb.head)).normalized()
    out["yaw"] = math.degrees(math.atan2(f.x, -f.y))
    h = mw @ pb.head
    t = tgt.matrix_world.translation - h
    out["target"] = math.degrees(math.atan2(t.x, -t.y))
    return out


def main():
    debug = L.flag("--debug")
    r = L.Report("CH06.02 — Contraintes")
    ob, tgt = bpy.data.objects.get("RIG_Gaze"), bpy.data.objects.get("EMP_Target")
    if not r.check(ob is not None and ob.type == "ARMATURE" and tgt is not None and all(n in ob.pose.bones for n in ("head", "eye.L", "eye.R")), "RIG_Gaze (bones head, eye.L, eye.R) et EMP_Target présents", "Partez du fichier de départ.", 3):
        return r.finish()
    pbs = ob.pose.bones
    for n in ("eye.L", "eye.R"):
        cs = [c for c in pbs[n].constraints if tracking(c) and c.target == tgt]
        r.check(bool(cs), f"{n} : Damped Track / Track To vers EMP_Target, axe Y", "Bone Constraints > Add > Damped Track ; Target EMP_Target ; Track Axis Y.", 3)
    hc = list(pbs["head"].constraints)
    idx_t = next((i for i, c in enumerate(hc) if c.type == "DAMPED_TRACK" and c.target == tgt and c.track_axis == "TRACK_Y"), None)
    r.check(idx_t is not None and 0.3 <= hc[idx_t].influence <= 0.7, f"head : Damped Track vers EMP_Target, Influence {hc[idx_t].influence if idx_t is not None else '—'} (0,3–0,7)", "Influence 0,5 : la tête suit à moitié.", 3)
    idx_l = next((i for i, c in enumerate(hc) if c.type == "LIMIT_ROTATION" and c.use_limit_z and c.owner_space == "LOCAL" and 25 <= math.degrees(c.max_z) <= 45 and 25 <= -math.degrees(c.min_z) <= 45), None)
    r.check(idx_l is not None, "head : Limit Rotation (Z ± 25–45°, espace Local)", "Limit Rotation : Limit Z, Owner Space Local.", 3)
    r.check(idx_t is not None and idx_l is not None and idx_t < idx_l, "Ordre de la pile : le suivi AVANT la limite", "La limite se place après le suivi (la pile s'évalue de haut en bas).", 3)
    m1 = measure(ob, tgt, (0, -2, 1.74))
    m2 = measure(ob, tgt, (1.5, -1.5, 1.74))
    m3 = measure(ob, tgt, (3.0, -0.2, 1.74))
    tgt.location = (0, -2, 1.74)
    err = lambda m: max(m["eye.L"], m["eye.R"])  # noqa: E731
    r.check(err(m1) <= 1 and abs(m1["yaw"]) < 1, f"T1 (devant) : erreur des yeux {err(m1):.2f}°, rotation de tête {m1['yaw']:.1f}° (≤ 1° ; < 1°)", "", 2)
    r.check(err(m2) <= 1, f"T2 (45°) : erreur des yeux {err(m2):.2f}° (≤ 1°)", "Les yeux visent la cible quelle que soit la tête.", 3)
    ratio = abs(m2["yaw"]) / max(abs(m2["target"]), 1e-6)
    r.check(0.15 <= ratio <= 0.70, f"T2 : la tête tourne de {m2['yaw']:.1f}° sur {m2['target']:.1f}° (rapport {ratio:.2f}, 0,15–0,70)", "Influence du Damped Track de la tête.", 3)
    r.check(abs(m3["yaw"]) <= 36 and abs(m3["target"]) > 70, f"T3 (de côté, {m3['target']:.0f}°) : rotation de tête plafonnée à {m3['yaw']:.1f}° (≤ 36°)", "Limit Rotation après le suivi.", 3)
    r.check(err(m3) <= 1, f"T3 : erreur des yeux {err(m3):.2f}° (≤ 1°)", "", 2)
    if debug:
        print("[DEBUG]", {k: round(v, 2) for k, v in m1.items()}, {k: round(v, 2) for k, v in m2.items()}, {k: round(v, 2) for k, v in m3.items()})
    if L.flag("--render"):
        lum = L.quick_render(15, 4)
        r.check(lum > 0.05, f"Rendu de contrôle non noir ({lum:.3f})", "", 1)
    return r.finish()


if __name__ == "__main__":
    L.run(main)
