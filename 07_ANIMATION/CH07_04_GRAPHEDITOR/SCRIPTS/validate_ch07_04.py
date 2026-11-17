"""
validate_ch07_04.py — Correcteur « Graph Editor » (CH07.04).
Usage : … --python-exit-code 1 --python validate_ch07_04.py -- --exercise graph [--debug]
Objet : GEO_Pendulum (rotation Y et position Z animées).
  Clés : rotation Y aux images 1, 13, 25 : −30°, +30°, −30° (± 0,5°) ; position Z aux images 1 et 25.
  Courbe de rotation Y — mesures sur l'animation ÉVALUÉE :
    ralentis : vitesse à l'extrémité (image 13, pente à ± 0,25 image) ≤ 1 °/image ; vitesse maximale entre les images 1 et 13 ≥ 6 °/image (un aller-retour linéaire donne 5 °/image partout) ;
    pas de dépassement : la rotation reste entre −30,5° et +30,5° sur les images 1 à 25 ;
    modificateur Cycles présent ; répétition : image 37 = +30° (± 1°), image 49 = −30°, image 61 = +30°.
  Courbe de position Z : modificateur Noise présent avec Strength entre 0,02 et 0,15 ; frémissement évalué (images 1 à 48) : écart-type de Z entre 0,003 et 0,03 m, amplitude crête à crête ≤ 0,1 m.
  Scène : plage 1–48.
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


def main():
    debug = L.flag("--debug")
    r = L.Report("CH07.04 — Graph Editor (courbes polies)")
    ob = bpy.data.objects.get("GEO_Pendulum")
    if not r.check(ob is not None and ob.animation_data is not None and ob.animation_data.action is not None, "GEO_Pendulum animé présent", "Partez du fichier de départ.", 2):
        return r.finish()
    sc = bpy.context.scene
    fcs = {(f.data_path, f.array_index): f for f in fcurves(ob.animation_data.action)}
    rot, locz = fcs.get(("rotation_euler", 1)), fcs.get(("location", 2))
    if not r.check(rot is not None and locz is not None, "Courbes Y Euler Rotation et Z Location présentes", "Ne supprimez pas de courbe.", 2):
        return r.finish()
    ks = [(round(k.co[0]), math.degrees(k.co[1])) for k in rot.keyframe_points]
    r.check([f for f, v in ks] == [1, 13, 25] and all(abs(v - e) <= 0.5 for (f, v), e in zip(ks, (-30, 30, -30))), f"Clés de rotation Y : {[(f, round(v, 1)) for f, v in ks]} (images 1, 13, 25 ; −30°, +30°, −30°)", "Ne changez pas les clés : polissez les courbes.", 4)
    r.check(sc.frame_start == 1 and sc.frame_end == 48, f"Plage de la scène : {sc.frame_start}–{sc.frame_end} (1–48)", "End = 48.", 2)

    def val(f):
        sc.frame_set(int(math.floor(f)), subframe=f - math.floor(f))
        bpy.context.view_layer.update()
        return math.degrees(ob.rotation_euler.y)
    slope = abs(val(13.25) - val(13.0)) / 0.25
    vmax = max(abs(val(f + 0.5) - val(f)) / 0.5 for f in range(1, 13))
    r.check(slope <= 1.0 and vmax >= 6.0, f"Ralentis : vitesse à l'extrémité {slope:.2f} °/image (≤ 1), vitesse maximale {vmax:.1f} °/image (≥ 6)", "Interpolation Bezier + poignées Auto Clamped (T, V).", 6)
    vs = [val(f) for f in range(1, 26)]
    r.check(min(vs) >= -30.5 and max(vs) <= 30.5, f"Pas de dépassement : rotation de {min(vs):.1f}° à {max(vs):.1f}° (images 1–25)", "Poignées Auto Clamped.", 3)
    cyc = any(m.type == "CYCLES" for m in rot.modifiers)
    rep = (val(37), val(49), val(61))
    r.check(cyc and abs(rep[0] - 30) <= 1 and abs(rep[1] + 30) <= 1 and abs(rep[2] - 30) <= 1, f"Cycles : image 37 = {rep[0]:.1f}°, 49 = {rep[1]:.1f}°, 61 = {rep[2]:.1f}° (30°, −30°, 30°) ; modificateur : {'oui' if cyc else 'non'}", "Barre latérale > Modifiers > Add Modifier > Cycles.", 6)
    nz = [m for m in locz.modifiers if m.type == "NOISE"]
    r.check(bool(nz) and 0.02 <= nz[0].strength <= 0.15, f"Noise sur Z : {'Strength ' + str(round(nz[0].strength, 3)) if nz else 'absent'} (0,02 à 0,15)", "Modificateur Noise : Strength 0,06.", 4)
    zs = []
    for f in range(1, 49):
        sc.frame_set(f)
        bpy.context.view_layer.update()
        zs.append(ob.location.z)
    sd, pp = float(np.std(zs)), float(max(zs) - min(zs))
    r.check(0.003 <= sd <= 0.03 and pp <= 0.1, f"Frémissement : écart-type de Z {1000 * sd:.1f} mm (3–30), amplitude {1000 * pp:.0f} mm (≤ 100)", "Strength 0,06, Scale 6.", 4)
    sc.frame_set(1)
    if debug:
        print("[DEBUG] slope", round(slope, 2), "vmax", round(vmax, 1), "range", round(min(vs), 1), round(max(vs), 1), "rep", [round(x, 1) for x in rep], "sd", round(sd, 4), "pp", round(pp, 3))
    return r.finish()


if __name__ == "__main__":
    L.run(main)
