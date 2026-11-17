"""
validate_ch06_10.py — Correcteur « Contrôleurs et ergonomie » (CH06.10).
Usage : … --python-exit-code 1 --python validate_ch06_10.py -- --exercise controls [--debug]
Objet : RIG_Ctl — bones MCH-pivot ; root, ctl_spine, ctl_arm.L, ctl_arm.R (contrôleurs) ; DEF-spine, DEF-arm.L, DEF-arm.R (déformation).
  Organisation : trois collections de bones « Controls » (root, ctl_*), « Deform » (DEF-*), « Mechanism » (MCH-*) ; Deform et Mechanism masquées, Controls visible ;
                 use_deform vrai pour les DEF-*, faux pour les autres ; aucun nom par défaut (« Bone… ») ; chaque .L a son .R.
  Contrôleurs : forme personnalisée (maillage d'au moins 8 sommets et 8 arêtes) rangée dans une collection masquée ; couleur de palette ≠ DEFAULT, gauche ≠ droite, centre ≠ gauche et droite ;
                ctl_arm.* : Location et Scale verrouillés ; ctl_spine : Scale verrouillé.
  Comportement (les contrôleurs sont tournés puis remis ; mesures sur les bones DEF évalués) :
    ctl_arm.L tourné de 30° : DEF-arm.L tourne de 30° ± 1° ; DEF-arm.R reste (≤ 0,1°) ;
    ctl_spine tourné de 20° : DEF-arm.L et DEF-arm.R tournent chacun de 20° ± 1° (la hiérarchie des contrôleurs est conservée).
Testé avec : Blender 5.3.0.
"""
import math
import os
import re
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bpy  # noqa: E402
from mathutils import Vector  # noqa: E402

CTL = ("root", "ctl_spine", "ctl_arm.L", "ctl_arm.R")
DEF = ("DEF-spine", "DEF-arm.L", "DEF-arm.R")
MCH = ("MCH-pivot",)


def direction(rig, name):
    bpy.context.view_layer.update()
    ev = rig.evaluated_get(bpy.context.evaluated_depsgraph_get())
    b = ev.pose.bones[name]
    return (ev.matrix_world @ b.tail - ev.matrix_world @ b.head).normalized()


def main():
    debug = L.flag("--debug")
    r = L.Report("CH06.10 — Contrôleurs et ergonomie")
    rig = bpy.data.objects.get("RIG_Ctl")
    if not r.check(rig is not None and rig.type == "ARMATURE" and all(n in rig.data.bones for n in CTL + DEF + MCH), "RIG_Ctl présent avec ses 8 bones", "Partez du fichier de départ.", 2):
        return r.finish()
    arm = rig.data
    # collections
    want = {"Controls": set(CTL), "Deform": set(DEF), "Mechanism": set(MCH)}
    got = {c.name: {b.name for b in c.bones} for c in arm.collections_all}
    r.check(got == want, f"Collections de bones : {sorted(got)} — contenu {'conforme' if got == want else 'NON conforme'}", "Controls = root et ctl_* ; Deform = DEF-* ; Mechanism = MCH-*.", 6)
    vis = {c.name: c.is_visible for c in arm.collections_all}
    r.check(vis.get("Controls") is True and vis.get("Deform") is False and vis.get("Mechanism") is False, f"Visibilité : {vis} (Controls visible, Deform et Mechanism masquées)", "Œil des collections.", 4)
    r.check(all(arm.bones[n].use_deform for n in DEF) and not any(arm.bones[n].use_deform for n in CTL + MCH), "use_deform : vrai pour les DEF-*, faux pour les contrôleurs et le mécanisme", "Bone properties > Deform.", 4)
    # formes
    ok_sh, why = True, []
    for n in CTL:
        cs = rig.pose.bones[n].custom_shape
        if cs is None or cs.type != "MESH" or len(cs.data.vertices) < 8 or len(cs.data.edges) < 8:
            ok_sh = False
            why.append(n)
        elif not cs.users_collection or not all(c.hide_viewport for c in cs.users_collection):
            ok_sh = False
            why.append(n + " (forme non masquée)")
    r.check(ok_sh, f"Formes personnalisées sur les 4 contrôleurs, rangées dans une collection masquée (à revoir : {why or 'aucun'})", "Bone properties > Viewport Display > Custom Shape ; collection WIDGETS masquée.", 5)
    # couleurs
    pal = {n: rig.pose.bones[n].color.palette for n in CTL}
    r.check(all(p != "DEFAULT" for p in pal.values()) and pal["ctl_arm.L"] != pal["ctl_arm.R"] and pal["ctl_spine"] not in (pal["ctl_arm.L"], pal["ctl_arm.R"]), f"Couleurs : {pal} (toutes ≠ DEFAULT, gauche ≠ droite, centre distinct)", "Bone properties > Bone Color.", 4)
    # verrous
    pbs = rig.pose.bones
    arms_ok = all(all(pbs[n].lock_location) and all(pbs[n].lock_scale) for n in ("ctl_arm.L", "ctl_arm.R"))
    r.check(arms_ok and all(pbs["ctl_spine"].lock_scale), "Verrous : ctl_arm.* en rotation seule (Location et Scale), ctl_spine sans Scale", "Cases de verrou des Transform.", 4)
    names = [b.name for b in arm.bones]
    pairs = all((n[:-2] + ".R") in names for n in names if n.endswith(".L")) and all((n[:-2] + ".L") in names for n in names if n.endswith(".R"))
    r.check(pairs and not any(re.match(r"^Bone(\.\d+)?$", n) for n in names), "Noms : paires .L/.R complètes, pas de nom par défaut", "Convention de nommage.", 2)
    # comportement
    rest = {n: direction(rig, n) for n in DEF}
    pb = pbs["ctl_arm.L"]
    pb.rotation_euler = (0, 0, math.radians(30))
    dL = math.degrees(rest["DEF-arm.L"].angle(direction(rig, "DEF-arm.L")))
    dR = math.degrees(rest["DEF-arm.R"].angle(direction(rig, "DEF-arm.R")))
    pb.rotation_euler = (0, 0, 0)
    r.check(abs(dL - 30) <= 1.0 and dR <= 0.1, f"ctl_arm.L +30° : DEF-arm.L tourne de {dL:.1f}° (30 ± 1) ; DEF-arm.R de {dR:.2f}° (≤ 0,1)", "Copy Transforms (World → World) de DEF-arm.L vers ctl_arm.L.", 5)
    sp = pbs["ctl_spine"]
    sp.rotation_euler = (0, math.radians(20), 0)
    sL = math.degrees(rest["DEF-arm.L"].angle(direction(rig, "DEF-arm.L")))
    sR = math.degrees(rest["DEF-arm.R"].angle(direction(rig, "DEF-arm.R")))
    sp.rotation_euler = (0, 0, 0)
    r.check(abs(sL - 20) <= 1.0 and abs(sR - 20) <= 1.0, f"ctl_spine +20° : DEF-arm.L {sL:.1f}° et DEF-arm.R {sR:.1f}° (20 ± 1)", "Les contrôleurs des bras sont enfants de ctl_spine ; les DEF-* copient les contrôleurs.", 4)
    if debug:
        print("[DEBUG] dL", round(dL, 2), "dR", round(dR, 3), "sL", round(sL, 2), "sR", round(sR, 2), "pal", pal, "got", got)
    return r.finish()


if __name__ == "__main__":
    L.run(main)
