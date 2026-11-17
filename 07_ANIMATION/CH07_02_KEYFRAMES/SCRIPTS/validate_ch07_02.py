"""
validate_ch07_02.py — Correcteur « Keyframes et timeline » (CH07.02).
Usage : … --python-exit-code 1 --python validate_ch07_02.py -- --exercise keyframes [--debug]
Objet : GEO_Crate.
  Timeline : plage 1–72 à 24 i/s ; image courante 1 ; marqueurs « arrive » (image 24) et « turn_end » (image 48).
  Position X : clés exactement aux images 1, 24, 48, 72 (4 clés) avec les valeurs 0, 4, 4, 0 (± 0,01) ; Y et Z de la position restent à 0.
  Rotation Z : clés aux images 24, 48, 72 : 0°, 90°, 90° (± 0,5°).
  Évalué : repos (X entre 28 et 44 : 4 ± 0,005 ; rotation à l'image 60 = 90°) ; rotation LINÉAIRE : 22,5° ± 2° à l'image 30 et 67,5° ± 2° à l'image 42 ;
           pas de dépassement : X entre −0,01 et 4,01 sur toute la plage ; départ : X = 0 et rotation 0 à l'image 1.
Testé avec : Blender 5.3.0.
"""
import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bpy  # noqa: E402


def fcurves(act):
    try:
        return list(act.fcurves)
    except AttributeError:
        return [f for l in act.layers for st in l.strips for cb in st.channelbags for f in cb.fcurves]


def keys(fcs, path, idx):
    fc = next((f for f in fcs if f.data_path == path and f.array_index == idx), None)
    return [(round(k.co[0]), k.co[1]) for k in fc.keyframe_points] if fc else []


def main():
    debug = L.flag("--debug")
    r = L.Report("CH07.02 — Keyframes et timeline")
    ob = bpy.data.objects.get("GEO_Crate")
    if not r.check(ob is not None and ob.animation_data is not None and ob.animation_data.action is not None, "GEO_Crate animée présente", "Insérez au moins une clé.", 2):
        return r.finish()
    sc = bpy.context.scene
    r.check(sc.frame_start == 1 and sc.frame_end == 72 and sc.render.fps == 24, f"Timeline : plage {sc.frame_start}–{sc.frame_end} à {sc.render.fps} i/s (1–72 à 24)", "Propriétés de sortie / timeline : Start 1, End 72.", 3)
    mk = {m.name: m.frame for m in sc.timeline_markers}
    r.check(mk.get("arrive") == 24 and mk.get("turn_end") == 48, f"Marqueurs : {mk} (arrive = 24, turn_end = 48)", "Timeline : M pour ajouter un marqueur, F2 pour le renommer.", 3)
    fcs = fcurves(ob.animation_data.action)
    kx = keys(fcs, "location", 0)
    r.check([f for f, v in kx] == [1, 24, 48, 72] and all(abs(v - e) <= 0.01 for (f, v), e in zip(kx, (0, 4, 4, 0))), f"Position X : clés {[(f, round(v, 2)) for f, v in kx]} (images 1, 24, 48, 72 ; valeurs 0, 4, 4, 0)", "Quatre clés exactement.", 6)
    r.check(all(abs(v) <= 1e-3 for f, v in keys(fcs, "location", 1) + keys(fcs, "location", 2)), "Position Y et Z restent à 0", "", 1)
    kr = keys(fcs, "rotation_euler", 2)
    r.check([f for f, v in kr] == [24, 48, 72] and all(abs(math.degrees(v) - e) <= 0.5 for (f, v), e in zip(kr, (0, 90, 90))), f"Rotation Z : clés {[(f, round(math.degrees(v), 1)) for f, v in kr]} (images 24, 48, 72 ; 0°, 90°, 90°)", "Clés de rotation Z.", 5)

    def at(f):
        sc.frame_set(f)
        bpy.context.view_layer.update()
        return ob.location.x, math.degrees(ob.rotation_euler.z)
    hold = [at(f)[0] for f in range(28, 45)]
    r.check(max(abs(x - 4) for x in hold) <= 0.005 and abs(at(60)[1] - 90) <= 0.5, f"Repos : X entre 28 et 44 = {min(hold):.3f}–{max(hold):.3f} ; rotation à l'image 60 = {at(60)[1]:.1f}°", "Deux clés de même valeur donnent un maintien.", 4)
    a30, a42 = at(30)[1], at(42)[1]
    r.check(abs(a30 - 22.5) <= 2 and abs(a42 - 67.5) <= 2, f"Rotation linéaire : {a30:.1f}° à l'image 30 (22,5 ± 2), {a42:.1f}° à l'image 42 (67,5 ± 2)", "Interpolation Linear sur les clés de rotation (T > Linear).", 5)
    xs = [at(f)[0] for f in range(1, 73)]
    r.check(min(xs) >= -0.01 and max(xs) <= 4.01, f"Pas de dépassement : X de {min(xs):.3f} à {max(xs):.3f}", "Gardez les poignées Auto Clamped.", 3)
    x1, a1 = at(1)
    r.check(abs(x1) <= 0.01 and abs(a1) <= 0.5, f"Départ : X = {x1:.2f}, rotation = {a1:.1f}° à l'image 1", "", 2)
    sc.frame_set(1)
    if debug:
        print("[DEBUG] kx", kx, "kr", [(f, round(math.degrees(v), 1)) for f, v in kr], "a30", round(a30, 1), "a42", round(a42, 1), "x range", round(min(xs), 3), round(max(xs), 3))
    return r.finish()


if __name__ == "__main__":
    L.run(main)
