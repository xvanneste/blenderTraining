"""
validate_ch06_05.py — Correcteur « Rig humanoïde » (CH06.05, Rigify).
Usage : … --python-exit-code 1 --python validate_ch06_05.py -- --exercise humanoid [--render] [--debug]
Objets : CHR_Hero_Body (corps), META_Hero (méta-rig Rigify) et RIG_Hero (rig GÉNÉRÉ) :
  Rig généré : ≥ 400 bones dont DEF-spine, DEF-thigh.L, ORG-/MCH-, contrôleurs root, torso, foot_ik.L, hand_ik.L ; ≥ 10 collections de bones ; données portant rig_id (Rigify) ;
  Bras : coudes (tête DEF-forearm) et poignets (tête DEF-hand) à ≤ 4 cm du centre local du bras (sommets à < 9 cm).
  Ajustement : sommet du bone DEF le plus haut à 1,76 ± 0,12 m ; pieds au sol (z min des bones DEF ≥ −0,06 m) ; centre en X du rig à ≤ 5 cm de celui du corps ; échelle de l'objet 1.
  Peau : CHR_Hero_Body parenté à RIG_Hero, modificateur Armature → RIG_Hero, groupes DEF-spine et DEF-thigh.L, ≥ 98 % des sommets pesés, somme des poids = 1 (± 0,02), ≤ 4 influences.
  Comportement (le rig est DÉPLACÉ puis remis) : racine +0,5 m en X : les sommets suivent (moyenne 0,5 ± 0,03 m ; ≥ 98 % à plus de 0,4 m) ;
        pied gauche (foot_ik.L) levé de 0,25 m : le pied gauche (x > 0,03 ; z < 0,08) monte de 0,10 à 0,30 m, le pied droit reste (≤ 1 cm), la tête (z > 1,6) reste (≤ 2 cm).
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
    r = L.Report("CH06.05 — Rig humanoïde (Rigify)")
    body, meta, rig = bpy.data.objects.get("CHR_Hero_Body"), bpy.data.objects.get("META_Hero"), bpy.data.objects.get("RIG_Hero")
    if not r.check(body is not None and meta is not None, "CHR_Hero_Body et META_Hero présents", "Partez du fichier de départ.", 2):
        return r.finish()
    gen = rig is not None and rig.type == "ARMATURE" and len(rig.data.bones) >= 400
    r.check(gen, f"Rig généré RIG_Hero : {len(rig.data.bones) if rig is not None and rig.type == 'ARMATURE' else 0} bones (≥ 400)", "Meta-rig > Object Data > Rigify > Generate Rig ; renommer l'objet « rig » en RIG_Hero.", 6)
    if not gen:
        return r.finish()
    names = {b.name for b in rig.data.bones}
    need = ["root", "torso", "foot_ik.L", "hand_ik.L", "DEF-spine", "DEF-thigh.L"]
    miss = [n for n in need if n not in names]
    r.check(not miss and any(n.startswith("ORG-") for n in names) and any(n.startswith("MCH-") for n in names), f"Bones Rigify attendus (manquants : {miss or 'aucun'}) ; ORG-/MCH- présents", "Le rig généré contient DEF-, ORG-, MCH-.", 3)
    r.check(len(rig.data.collections_all) >= 10 and "rig_id" in rig.data, f"{len(rig.data.collections_all)} collections de bones (≥ 10) ; rig_id Rigify : {'oui' if 'rig_id' in rig.data else 'non'}", "", 2)
    # ajustement
    mw = rig.matrix_world
    defs = [b for b in rig.data.bones if b.name.startswith("DEF-")]
    top = max((mw @ b.tail_local).z for b in defs)
    zmin = min(min((mw @ b.head_local).z, (mw @ b.tail_local).z) for b in defs)
    body_co = np.array([body.matrix_world @ v.co for v in body.data.vertices])
    rig_cx = float(np.mean([(mw @ b.head_local).x for b in defs]))
    r.check(abs(top - 1.76) <= 0.12, f"Taille du rig : sommet des bones DEF à {top:.2f} m (1,76 ± 0,12)", "Mettre le méta-rig à l'échelle du corps (≈ 0,89) AVANT de générer.", 5)
    r.check(zmin >= -0.06, f"Pieds au sol : z min des bones DEF = {zmin:+.3f} m (≥ −0,06)", "", 2)
    r.check(abs(rig_cx - float(body_co[:, 0].mean())) <= 0.05, f"Rig centré sous le corps (écart en X {abs(rig_cx - float(body_co[:, 0].mean())) * 100:.1f} cm ≤ 5)", "Pas de décalage en X du méta-rig.", 3)
    r.check(all(abs(s - 1) < 1e-4 for s in rig.scale), "Échelle du rig = 1", "Appliquer l'échelle du méta-rig avant la génération.", 1)
    # bras alignés : coude (tête de DEF-forearm) et poignet (tête de DEF-hand) au centre de la section du bras, des deux côtés
    gaps = {}
    for side in ("L", "R"):
        for bn in (f"DEF-forearm.{side}", f"DEF-hand.{side}"):
            b = rig.data.bones.get(bn)
            if b is None:
                gaps[bn] = 9.0
                continue
            p = np.array((mw @ b.head_local)[:])
            near = body_co[np.linalg.norm(body_co - p, axis=1) < 0.09]
            gaps[bn] = float(np.linalg.norm(p - near.mean(0))) if len(near) >= 10 else 9.0
    worst = max(gaps.values())
    r.check(worst <= 0.04, ("Bras du rig dans les bras du corps : coudes et poignets à " + (f"{100 * worst:.1f} cm au plus du centre de la section (≤ 4)" if worst < 9 else "— au moins une articulation est HORS du bras (aucun sommet à moins de 9 cm)")),
            "Avant de générer, ajuster les bras du méta-rig en Edit Mode : coude et poignet au milieu du bras, vus de face ET de profil.", 4)
    # peau
    mods = [m for m in body.modifiers if m.type == "ARMATURE" and m.object == rig]
    r.check(bool(mods) and body.parent == rig, "Corps parenté à RIG_Hero avec un modificateur Armature", "Ctrl+P > With Automatic Weights.", 5)
    gn = {g.name for g in body.vertex_groups}
    r.check("DEF-spine" in gn and "DEF-thigh.L" in gn, f"Groupes DEF-spine et DEF-thigh.L présents ({len(gn)} groupes)", "", 3)
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
    shift(rig, "foot_ik.L", (0, 0, 0.25))
    lifted = coords(body)
    shift(rig, "foot_ik.L", (0, 0, 0))
    d = lifted - rest
    left = (rest[:, 0] > 0.03) & (rest[:, 2] < 0.08)
    right = (rest[:, 0] < -0.03) & (rest[:, 2] < 0.08)
    head = rest[:, 2] > 1.6
    up_l = float(d[left, 2].mean()) if left.any() else 0.0
    mv_r = float(np.abs(d[right]).max()) if right.any() else 9.0
    mv_h = float(np.abs(d[head]).max()) if head.any() else 9.0
    r.check(0.10 <= up_l <= 0.30, f"Pied gauche levé de 0,25 m : le pied du corps monte de {up_l:.3f} m (0,10–0,30)", "Les sommets du pied pèsent sur les bones du pied gauche.", 4)
    r.check(mv_r <= 0.01 and mv_h <= 0.02, f"Pied droit ({1000 * mv_r:.1f} mm ≤ 10) et tête ({1000 * mv_h:.1f} mm ≤ 20) immobiles", "Pas de poids parasites entre les côtés.", 3)
    if debug:
        print("[DEBUG] gaps", {k: round(v, 3) for k, v in gaps.items()}, "bones", len(rig.data.bones), "top", round(top, 3), "zmin", round(zmin, 3), "cx", round(rig_cx, 3), "frac", round(frac, 4), "dx", round(float(dx.mean()), 3), "up_l", round(up_l, 3), "mv_r", round(mv_r, 4), "mv_h", round(mv_h, 4))
    if L.flag("--render"):
        lum = L.quick_render(15, 4)
        r.check(lum > 0.05, f"Rendu de contrôle non noir ({lum:.3f})", "", 1)
    return r.finish()


if __name__ == "__main__":
    L.run(main)
