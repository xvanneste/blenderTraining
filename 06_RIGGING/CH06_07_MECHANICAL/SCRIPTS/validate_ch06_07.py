"""
validate_ch06_07.py — Correcteur « Rig mécanique » (CH06.07).
Usage : … --python-exit-code 1 --python validate_ch06_07.py -- --exercise truck [--debug]
Objets : GEO_Truck (maillage, groupes de sommets = bones, modificateur Armature) et RIG_Truck (root, body, wheel_FL/FR/RL/RR, bed, bed_pt, anchor, cyl, rod).
  Configuration : 4 drivers (un par roue) ; roues enfants de root ; Damped Track sur cyl (cible bed_pt) et rod (cible anchor) ; Limit Rotation sur bed ; modificateur Armature → RIG_Truck.
  Comportement (le rig est DÉPLACÉ puis remis ; mesures sur les SOMMETS évalués) :
    Roues : root avance de 0,5 m puis de 0,2 m (Location Y) : chaque roue avance de la même distance ; le repère de la roue tourne de −d/0,30 rad (± 0,05 rad) autour de l'axe X ;
            le repère reste dans le plan de la roue (écart en X ≤ 5 mm) ; les roues ne glissent pas (la distance parcourue = rayon × angle, ± 2 cm).
    Vérin : benne levée de 30° : cyl part de anchor et vise bed_pt (écart ≤ 1,5°) ; rod part de bed_pt et vise anchor (≤ 1,5°) ; tête de rod à ≤ 1 mm de bed_pt ;
            les deux se recouvrent d'au moins 10 cm ; le bout avant de la benne monte à 1,235 m (± 2 cm : charnière 0,6 + 1,2·sin 30° + demi-épaisseur 4 cm·cos 30°).
    Limite : benne demandée à 80° : elle s'arrête à 45° (bout avant à 1,477 m ± 2 cm).
Testé avec : Blender 5.3.0.
"""
import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bpy  # noqa: E402
import numpy as np  # noqa: E402
from mathutils import Vector  # noqa: E402

WHEELS = ("wheel_FL", "wheel_FR", "wheel_RL", "wheel_RR")
R = 0.30


def verts(geo):
    bpy.context.view_layer.update()
    ev = geo.evaluated_get(bpy.context.evaluated_depsgraph_get())
    me = ev.to_mesh()
    co = np.array([v.co[:] for v in me.vertices])
    ev.to_mesh_clear()
    return co


def group_idx(geo):
    idx = {}
    for v in geo.data.vertices:
        for g in v.groups:
            if g.weight > 0.5:
                idx.setdefault(geo.vertex_groups[g.group].name, []).append(v.index)
    return idx


def split_wheel(rest, ids):
    """Sépare les sommets du cylindre (rayon ≥ 0,28 m autour de l'axe) de ceux du repère (rayon < 0,27), d'après la pose de repos."""
    pts = rest[ids]
    c0 = (pts.min(axis=0) + pts.max(axis=0)) / 2
    rad = np.hypot(pts[:, 1] - c0[1], pts[:, 2] - c0[2])
    ids = np.array(ids)
    return ids[rad >= 0.28], ids[rad < 0.27]


def wheel_state(co, parts):
    """Centre (milieu de la boîte du cylindre), angle du repère autour de X, position en X du repère."""
    cyl, mk = parts
    pc = co[cyl]
    c = (pc.min(axis=0) + pc.max(axis=0)) / 2
    rel = co[mk].mean(axis=0) - c
    return c, math.atan2(rel[2], rel[1]), float(rel[0])


def wrap(a):
    return (a + math.pi) % (2 * math.pi) - math.pi


def main():
    debug = L.flag("--debug")
    r = L.Report("CH06.07 — Rig mécanique (roues, vérin, benne)")
    geo, rig = bpy.data.objects.get("GEO_Truck"), bpy.data.objects.get("RIG_Truck")
    if not r.check(geo is not None and rig is not None and rig.type == "ARMATURE", "GEO_Truck et RIG_Truck présents", "Partez du fichier de départ.", 2):
        return r.finish()
    names = {b.name for b in rig.data.bones}
    need = ["root", "body", "bed", "bed_pt", "anchor", "cyl", "rod"] + list(WHEELS)
    if not r.check(all(n in names for n in need), "Bones attendus présents", "Ne renommez pas les bones.", 2):
        return r.finish()
    pb = rig.pose.bones
    # configuration
    ndrv = 0
    if rig.animation_data:
        ndrv = sum(1 for f in rig.animation_data.drivers if "wheel_" in f.data_path and "rotation_euler" in f.data_path)
    r.check(ndrv >= 4, f"{ndrv} driver(s) sur la rotation des roues (≥ 4)", "Clic droit sur la rotation > Add Driver, une fois par roue.", 4)
    r.check(all(rig.data.bones[w].parent is not None and rig.data.bones[w].parent.name == "root" for w in WHEELS), "Les quatre roues sont enfants de root", "Parentez les roues à root (Ctrl+P > Keep Offset / champ Parent).", 3)

    def has(bone, typ, sub=None):
        return any(c.type == typ and (sub is None or c.subtarget == sub) and c.target == rig for c in pb[bone].constraints)
    r.check(has("cyl", "DAMPED_TRACK", "bed_pt") and has("rod", "DAMPED_TRACK", "anchor"), "Damped Track : cyl → bed_pt et rod → anchor", "Bone Constraints > Damped Track.", 4)
    lim = [c for c in pb["bed"].constraints if c.type == "LIMIT_ROTATION"]
    r.check(bool(lim) and lim[0].use_limit_x, "Limit Rotation sur la benne", "Bone Constraints > Limit Rotation (X de 0 à 45°).", 3)
    r.check(any(m.type == "ARMATURE" and m.object == rig for m in geo.modifiers), "Modificateur Armature → RIG_Truck", "", 2)
    ids = group_idx(geo)
    rest = verts(geo)
    parts = {w: split_wheel(rest, ids[w]) for w in WHEELS}
    centers = {w: wheel_state(rest, parts[w]) for w in WHEELS}
    # roues
    pb["root"].rotation_mode = "XYZ"
    out = {}
    for fwd in (0.5, 0.2):
        pb["root"].location = Vector((0, fwd, 0))
        co = verts(geo)
        res = []
        for w in WHEELS:
            c, ang, xk = wheel_state(co, parts[w])
            c0, a0, xk0 = centers[w]
            res.append((c[1] - c0[1], wrap(ang - a0), xk - xk0))
        out[fwd] = res
    pb["root"].location = (0, 0, 0)
    for fwd in (0.5, 0.2):
        adv = [x[0] for x in out[fwd]]
        r.check(all(abs(a - fwd) <= 0.01 for a in adv), f"Root +{fwd} m : les quatre roues avancent de {min(adv):.3f}–{max(adv):.3f} m", "Les roues doivent suivre root.", 3)
        exp = wrap(-fwd / R)
        angs = [x[1] for x in out[fwd]]
        r.check(all(abs(wrap(a - exp)) <= 0.05 for a in angs), f"Root +{fwd} m : le repère de chaque roue tourne de {min(angs):+.2f} à {max(angs):+.2f} rad (attendu {exp:+.2f})", "Expression « -d / 0.3 » sur la rotation Y du bone.", 4)
        xs = [abs(x[2]) for x in out[fwd]]
        r.check(max(xs) <= 0.005, f"Le repère reste dans le plan de la roue (écart X max {1000 * max(xs):.1f} mm ≤ 5)", "Tourner autour de l'AXE du bone (rotation Y), pas autour de X ou Z.", 3)
    # roulement sans glissement (déduit des deux essais)
    a5 = out[0.5][0][1]
    a2 = out[0.2][0][1]
    r.check(abs(wrap(a5) / 0.5 - wrap(a2) / 0.2) <= 0.2, "Rotation proportionnelle à la distance (0,5 m et 0,2 m)", "Le driver doit être linéaire : −d / rayon.", 2)
    # benne et vérin
    pb["bed"].rotation_mode = "XYZ"
    pb["bed"].rotation_euler = (math.radians(30), 0, 0)
    co = verts(geo)
    bpy.context.view_layer.update()
    ev = rig.evaluated_get(bpy.context.evaluated_depsgraph_get())
    mw = ev.matrix_world
    P = ev.pose.bones
    A, B = mw @ P["anchor"].head, mw @ P["bed_pt"].head
    cyl_h, cyl_t = mw @ P["cyl"].head, mw @ P["cyl"].tail
    rod_h, rod_t = mw @ P["rod"].head, mw @ P["rod"].tail

    def ang(u, v):
        return math.degrees(u.normalized().angle(v.normalized()))
    e1 = ang(cyl_t - cyl_h, B - A)
    e2 = ang(rod_t - rod_h, A - B)
    r.check(e1 <= 1.5 and (cyl_h - A).length <= 1e-3, f"Benne 30° : cyl part de anchor et vise bed_pt (écart {e1:.1f}°)", "Damped Track de cyl vers bed_pt.", 4)
    r.check(e2 <= 1.5 and (rod_h - B).length <= 1e-3, f"Benne 30° : rod part de bed_pt et vise anchor (écart {e2:.1f}°)", "Damped Track de rod vers anchor.", 4)
    # recouvrement des deux tubes le long de l'axe A→B
    ax = (B - A).normalized()
    d = (B - A).length
    cyl_end = (cyl_t - A).dot(ax)
    rod_end = d - (rod_t - rod_h).length * 1.0 if False else (rod_t - A).dot(ax)
    overlap = cyl_end - rod_end
    r.check(overlap >= 0.10, f"Cylindre et tige se recouvrent de {overlap:.2f} m (≥ 0,10)", "Les deux bones restent emboîtés.", 2)
    bed_ids = ids["bed"]
    tip = float(co[bed_ids][:, 2].max())
    r.check(abs(tip - 1.235) <= 0.02, f"Benne 30° : bout avant à z = {tip:.2f} m (1,235 ± 0,02)", "Rotation X de la benne.", 3)
    pb["bed"].rotation_euler = (math.radians(80), 0, 0)
    co = verts(geo)
    tip2 = float(co[bed_ids][:, 2].max())
    pb["bed"].rotation_euler = (0, 0, 0)
    r.check(abs(tip2 - 1.477) <= 0.02, f"Benne demandée à 80° : bout à z = {tip2:.2f} m (limite 45° → 1,477 ± 0,02)", "Limit Rotation X max 45°, Owner Space Local.", 4)
    if debug:
        print("[DEBUG] fwd", {k: [(round(a, 3), round(b, 3), round(c, 4)) for a, b, c in v] for k, v in out.items()}, "e1", round(e1, 2), "e2", round(e2, 2), "overlap", round(overlap, 3), "tip", round(tip, 3), round(tip2, 3))
    return r.finish()


if __name__ == "__main__":
    L.run(main)
