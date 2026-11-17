"""
validate_ch06_03.py — Correcteur « Skinning » (CH06.03).
Usage : … --python-exit-code 1 --python validate_ch06_03.py -- --exercise skinning [--render] [--debug]
CHR_Arm (tube de 60 cm le long de X) lié à RIG_Arm (bones upper 0–0,30 m et fore 0,30–0,60 m) :
  Liaison  : modificateur Armature dont l'objet est RIG_Arm ; groupes de sommets « upper » et « fore » (noms de bones) et aucun autre groupe.
  Poids    : chaque sommet pesé (au moins un poids > 0) ; somme des poids = 1 (± 0,02) ; au plus 4 influences par sommet.
  Pliage   : forearm tourné de 90° autour de Z au coude (0,30 ; 0 ; 0) — la pose est ensuite remise à zéro :
             racine (x < 0,10) déplacée de ≤ 5 mm ; bout (x > 0,55) à ≤ 2 cm de la position d'un solide tournant avec forearm ;
             coude lisse : allongement maximal d'une arête ≤ 2,2 fois sa longueur de repos (une coupure brutale des poids déchire le coude).
Testé avec : Blender 5.3.0.
"""
import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bpy  # noqa: E402
import numpy as np  # noqa: E402
from mathutils import Matrix, Vector  # noqa: E402

ELBOW = Vector((0.30, 0, 0))


def coords(ob):
    ev = ob.evaluated_get(bpy.context.evaluated_depsgraph_get())
    me = ev.to_mesh()
    co = np.array([v.co[:] for v in me.vertices])
    ev.to_mesh_clear()
    return co


def main():
    debug = L.flag("--debug")
    r = L.Report("CH06.03 — Skinning")
    tube, rig = bpy.data.objects.get("CHR_Arm"), bpy.data.objects.get("RIG_Arm")
    if not r.check(tube is not None and rig is not None and rig.type == "ARMATURE", "CHR_Arm et RIG_Arm présents", "Partez du fichier de départ.", 2):
        return r.finish()
    mods = [m for m in tube.modifiers if m.type == "ARMATURE" and m.object == rig]
    r.check(bool(mods), "Modificateur Armature pointant vers RIG_Arm", "Ctrl+P > With Automatic Weights (ajoute le modificateur).", 4)
    names = {g.name for g in tube.vertex_groups}
    bones = {b.name for b in rig.data.bones}
    r.check({"upper", "fore"} <= names, f"Groupes de sommets upper et fore présents ({sorted(names)})", "Un groupe par bone déformant.", 4)
    r.check(names <= bones, f"Aucun groupe sans bone ({sorted(names - bones) or 'aucun'})", "Un groupe qui ne correspond à aucun bone ne déforme rien et gêne.", 2)
    me = tube.data
    n = len(me.vertices)
    sums, infl, unw = np.zeros(n), np.zeros(n, int), 0
    for v in me.vertices:
        ws = [g.weight for g in v.groups if g.weight > 1e-4]
        sums[v.index] = sum(g.weight for g in v.groups)
        infl[v.index] = len(ws)
        if not ws:
            unw += 1
    r.check(unw == 0, f"Sommets sans poids : {unw} sur {n}", "Weight Paint ou Automatic Weights sur tout le maillage.", 4)
    r.check(bool(np.all(np.abs(sums[infl > 0] - 1.0) <= 0.02)), f"Poids normalisés : somme min {float(sums.min()):.2f}, max {float(sums.max()):.2f} (1 ± 0,02)", "Weights > Normalize All.", 3)
    r.check(int(infl.max()) <= 4, f"Au plus 4 influences par sommet (maximum : {int(infl.max())})", "Weights > Limit Total (4).", 3)
    # pliage
    rest = coords(tube)
    pb = rig.pose.bones["fore"]
    pb.rotation_mode = "XYZ"
    pb.rotation_euler = (0, 0, math.radians(90))
    bpy.context.view_layer.update()
    bent = coords(tube)
    pb.rotation_euler = (0, 0, 0)
    bpy.context.view_layer.update()
    root = rest[:, 0] < 0.10
    tip = rest[:, 0] > 0.55
    d_root = float(np.linalg.norm(bent[root] - rest[root], axis=1).max())
    Rm = Matrix.Rotation(math.radians(90), 3, "Z")
    exp_tip = np.array([(Rm @ (Vector(p) - ELBOW)) + ELBOW for p in rest[tip]])
    d_tip = float(np.linalg.norm(bent[tip] - exp_tip, axis=1).max())
    r.check(d_root <= 0.005, f"Racine immobile : déplacement max {1000 * d_root:.1f} mm (≤ 5 mm)", "Les sommets de la racine pèsent 1 sur upper.", 4)
    r.check(d_tip <= 0.02, f"Bout solidaire de forearm : écart max {1000 * d_tip:.1f} mm (≤ 20 mm)", "Les sommets du bout pèsent 1 sur fore.", 4)
    edges = np.array([[e.vertices[0], e.vertices[1]] for e in me.edges])
    l0 = np.linalg.norm(rest[edges[:, 0]] - rest[edges[:, 1]], axis=1)
    l1 = np.linalg.norm(bent[edges[:, 0]] - bent[edges[:, 1]], axis=1)
    ratio = float((l1 / np.maximum(l0, 1e-9)).max())
    r.check(ratio <= 2.2, f"Coude lisse : allongement maximal d'une arête ×{ratio:.2f} (≤ 2,2)", "Adoucir les poids au coude (Smooth, Blur) au lieu d'une coupure nette.", 4)
    if debug:
        print("[DEBUG] unweighted", unw, "sum", round(float(sums.min()), 3), round(float(sums.max()), 3), "infl", int(infl.max()), "d_root", round(d_root, 4), "d_tip", round(d_tip, 4), "stretch", round(ratio, 3))
    if L.flag("--render"):
        lum = L.quick_render(15, 4)
        r.check(lum > 0.05, f"Rendu de contrôle non noir ({lum:.3f})", "", 1)
    return r.finish()


if __name__ == "__main__":
    L.run(main)
