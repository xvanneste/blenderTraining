"""
validate_ch06_06.py — Correcteur « Rig quadrupède » (CH06.06, Rigify Basic Quadruped).
Usage : … --python-exit-code 1 --python validate_ch06_05.py -- --exercise quadruped [--render] [--debug]
Objets : CHR_Quad (créature), META_Quad (méta-rig) et RIG_Quad (rig GÉNÉRÉ) :
  Rig généré : ≥ 200 bones dont DEF-spine, DEF-front_thigh.L, ORG-/MCH-, contrôleurs root, torso, foot_ik.L, front_foot_ik.L ; ≥ 10 collections ; rig_id Rigify ; échelle 1.
  Ajustement : étendues Y des bones DEF et du maillage à ≤ 12 cm près (début et fin), sommet à ≤ 12 cm, pattes au sol (z min des DEF ≥ −0,06) ; centre en X à ≤ 5 cm.
  Peau : CHR_Quad parenté à RIG_Quad, modificateur Armature, groupes DEF-spine et DEF-front_thigh.L, ≥ 98 % des sommets pesés, somme 1 (± 0,02), ≤ 4 influences.
  Comportement (le rig est DÉPLACÉ puis remis) : racine +0,5 m en X (moyenne 0,5 ± 0,03 m ; ≥ 98 % à plus de 0,4 m) ;
        patte avant gauche (front_foot_ik.L) levée de 0,15 m : sa patte monte de 0,08 à 0,18 m, les trois autres pattes restent (≤ 1 cm).
Testé avec : Blender 5.3.0.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bpy  # noqa: E402
import numpy as np  # noqa: E402
from mathutils import Vector  # noqa: E402


def coords(ob):
    ev = ob.evaluated_get(bpy.context.evaluated_depsgraph_get())
    me = ev.to_mesh()
    co = np.array([v.co[:] for v in me.vertices])
    ev.to_mesh_clear()
    return co


def shift(rig, name, delta):
    pb = rig.pose.bones[name]
    pb.location = pb.bone.matrix_local.to_3x3().inverted() @ Vector(delta)
    bpy.context.view_layer.update()


def main():
    debug = L.flag("--debug")
    r = L.Report("CH06.06 — Rig quadrupède (Rigify)")
    body, meta, rig = bpy.data.objects.get("CHR_Quad"), bpy.data.objects.get("META_Quad"), bpy.data.objects.get("RIG_Quad")
    if not r.check(body is not None and meta is not None, "CHR_Quad et META_Quad présents", "Partez du fichier de départ.", 2):
        return r.finish()
    gen = rig is not None and rig.type == "ARMATURE" and len(rig.data.bones) >= 200
    r.check(gen, f"Rig généré RIG_Quad : {len(rig.data.bones) if rig is not None and rig.type == 'ARMATURE' else 0} bones (≥ 200)", "Meta-rig > Object Data > Rigify > Generate Rig ; renommer l'objet « rig » en RIG_Quad.", 6)
    if not gen:
        return r.finish()
    names = {b.name for b in rig.data.bones}
    need = ["root", "torso", "foot_ik.L", "front_foot_ik.L", "DEF-spine", "DEF-front_thigh.L"]
    miss = [n for n in need if n not in names]
    r.check(not miss and any(n.startswith("ORG-") for n in names) and any(n.startswith("MCH-") for n in names), f"Bones Rigify attendus (manquants : {miss or 'aucun'}) ; ORG-/MCH- présents", "Le rig généré contient DEF-, ORG-, MCH-.", 3)
    r.check(len(rig.data.collections_all) >= 10 and "rig_id" in rig.data, f"{len(rig.data.collections_all)} collections de bones (≥ 10) ; rig_id Rigify : {'oui' if 'rig_id' in rig.data else 'non'}", "", 2)
    # ajustement
    mw = rig.matrix_world
    defs = [b for b in rig.data.bones if b.name.startswith("DEF-")]
    ys = [(mw @ b.head_local).y for b in defs] + [(mw @ b.tail_local).y for b in defs]
    zs_top = max((mw @ b.tail_local).z for b in defs)
    zmin = min(min((mw @ b.head_local).z, (mw @ b.tail_local).z) for b in defs)
    body_co = np.array([body.matrix_world @ v.co for v in body.data.vertices])
    rig_cx = float(np.mean([(mw @ b.head_local).x for b in defs]))
    dy0, dy1, dz = abs(min(ys) - float(body_co[:, 1].min())), abs(max(ys) - float(body_co[:, 1].max())), abs(zs_top - float(body_co[:, 2].max()))
    r.check(dy0 <= 0.12 and dy1 <= 0.12 and dz <= 0.12, f"Ajustement : écarts rig/créature en Y {100 * dy0:.0f} et {100 * dy1:.0f} cm, en hauteur {100 * dz:.0f} cm (≤ 12)", "Le méta-rig doit être sur la créature : échelle 1, position 0.", 6)
    r.check(zmin >= -0.06, f"Pattes au sol : z min des bones DEF = {zmin:+.3f} m (≥ −0,06)", "", 2)
    r.check(abs(rig_cx - float(body_co[:, 0].mean())) <= 0.05, f"Rig centré sur la créature (écart en X {abs(rig_cx - float(body_co[:, 0].mean())) * 100:.1f} cm ≤ 5)", "Pas de décalage en X.", 3)
    r.check(all(abs(s - 1) < 1e-4 for s in rig.scale), "Échelle du rig = 1", "Appliquer l'échelle du méta-rig avant la génération.", 1)
    # peau
    mods = [m for m in body.modifiers if m.type == "ARMATURE" and m.object == rig]
    r.check(bool(mods) and body.parent == rig, "Corps parenté à RIG_Quad avec un modificateur Armature", "Ctrl+P > With Automatic Weights.", 5)
    gn = {g.name for g in body.vertex_groups}
    r.check("DEF-spine" in gn and "DEF-front_thigh.L" in gn, f"Groupes DEF-spine et DEF-front_thigh.L présents ({len(gn)} groupes)", "", 3)
    n = len(body.data.vertices)
    sums, infl = np.zeros(n), np.zeros(n, int)
    for v in body.data.vertices:
        ws = [g.weight for g in v.groups if g.weight > 1e-4]
        sums[v.index] = sum(g.weight for g in v.groups)
        infl[v.index] = len(ws)
    frac = float((infl > 0).mean())
    r.check(frac >= 0.98, f"Sommets pesés : {100 * frac:.1f} % (≥ 98)", "Automatic Weights sur tout le maillage.", 4)
    r.check(frac > 0 and bool(np.all(np.abs(sums[infl > 0] - 1) <= 0.02)) and int(infl.max()) <= 4, f"Poids normalisés ({float(sums.min()):.2f}–{float(sums.max()):.2f}) et ≤ 4 influences (max {int(infl.max())})", "Normalize All ; Limit Total 4.", 3)
    # mouvement
    rest = coords(body)
    shift(rig, "root", (0.5, 0, 0))
    moved = coords(body)
    dx = moved[:, 0] - rest[:, 0]
    shift(rig, "root", (0, 0, 0))
    r.check(abs(float(dx.mean()) - 0.5) <= 0.03 and float((dx > 0.4).mean()) >= 0.98, f"Racine +0,5 m : déplacement moyen {float(dx.mean()):.3f} m, {100 * float((dx > 0.4).mean()):.0f} % des sommets à > 0,4 m", "Peau complète et rig sans décalage.", 4)
    shift(rig, "front_foot_ik.L", (0, 0, 0.15))
    lifted = coords(body)
    shift(rig, "front_foot_ik.L", (0, 0, 0))
    d = lifted - rest
    fl = (rest[:, 0] > 0.03) & (rest[:, 1] < -0.15) & (rest[:, 2] < 0.10)
    others = ((rest[:, 0] < -0.03) & (rest[:, 1] < -0.15) & (rest[:, 2] < 0.10)) | ((rest[:, 1] > 0.15) & (rest[:, 2] < 0.12))
    up_l = float(d[fl, 2].mean()) if fl.any() else 0.0
    mv_o = float(np.abs(d[others]).max()) if others.any() else 9.0
    r.check(0.08 <= up_l <= 0.18, f"Patte avant gauche levée de 0,15 m : la patte monte de {up_l:.3f} m (0,08–0,18)", "Les sommets de la patte pèsent sur les bones de la patte avant gauche.", 4)
    r.check(mv_o <= 0.01, f"Les trois autres pattes restent ({1000 * mv_o:.1f} mm ≤ 10)", "Pas de poids parasites entre les pattes.", 3)
    if debug:
        print("[DEBUG] bones", len(rig.data.bones), "dy", round(dy0, 3), round(dy1, 3), "dz", round(dz, 3), "zmin", round(zmin, 3), "cx", round(rig_cx, 3), "frac", round(frac, 4), "dx", round(float(dx.mean()), 3), "up_l", round(up_l, 3), "mv_o", round(mv_o, 4))
    if L.flag("--render"):
        lum = L.quick_render(15, 4)
        r.check(lum > 0.05, f"Rendu de contrôle non noir ({lum:.3f})", "", 1)
    return r.finish()


if __name__ == "__main__":
    L.run(main)
