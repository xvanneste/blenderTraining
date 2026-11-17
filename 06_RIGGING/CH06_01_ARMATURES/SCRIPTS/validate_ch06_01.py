"""
validate_ch06_01.py — Correcteur « Armatures et bones » (CH06.01).
Usage : … --python-exit-code 1 --python validate_ch06_01.py -- --exercise armature [--render] [--debug]
RIG_Hero (données ARM_Hero) :
  Objet    : échelle 1, rotation 0, position (0, 0, 0) ; données nommées ARM_Hero.
  Noms     : les 25 bones attendus (root, pelvis, spine.001–003, neck, head ; shoulder, upper_arm, forearm, hand, thigh, shin, foot, toe en .L et .R) ; aucun nom du type « Bone.001 » ; pas de bone en trop.
  Côtés    : chaque bone .L a son .R et réciproquement.
  Hiérarchie : parent de chaque bone conforme (root > pelvis > spine… ; spine.003 > shoulder > upper_arm > forearm > hand ; pelvis > thigh > shin > foot > toe).
  Connexions : colonne, cou, tête, forearm, hand, shin, foot, toe connectés (use_connect) ; shoulder et thigh NON connectés.
  Symétrie : tête et queue de chaque .R = miroir (X → −X) du .L à 2 mm ; roll opposé à 0,001 rad près ; roll nul.
  Géométrie : taille 1,76 m ± 5 cm (queue de head) ; pieds au sol (z de la queue de toe ≤ 2 cm) ; aucun bone de moins de 2 cm ; bras en pose A (hand.L plus bas et plus loin que shoulder.L).
  Déformation : root ne déforme pas (use_deform = False) ; tous les autres déforment.
  Pose de repos : aucune transformation en Pose Mode (position, rotation, échelle identité).
Testé avec : Blender 5.3.0.
"""
import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bpy  # noqa: E402

PARENT = {"root": None, "pelvis": "root", "spine.001": "pelvis", "spine.002": "spine.001", "spine.003": "spine.002", "neck": "spine.003", "head": "neck"}
SIDE_PARENT = {"shoulder": "spine.003", "upper_arm": "shoulder", "forearm": "upper_arm", "hand": "forearm", "thigh": "pelvis", "shin": "thigh", "foot": "shin", "toe": "foot"}
CONNECTED = {"spine.001", "spine.002", "spine.003", "neck", "head", "upper_arm", "forearm", "hand", "shin", "foot", "toe"}
EXPECT = dict(PARENT)
for s in (".L", ".R"):
    for n, p in SIDE_PARENT.items():
        EXPECT[n + s] = p if p in ("spine.003", "pelvis") else p + s


def main():
    debug = L.flag("--debug")
    r = L.Report("CH06.01 — Armatures et bones")
    ob = bpy.data.objects.get("RIG_Hero")
    if not r.check(ob is not None and ob.type == "ARMATURE", "Objet armature RIG_Hero", "Renommez l'objet armature RIG_Hero.", 4):
        return r.finish()
    arm = ob.data
    r.check(arm.name == "ARM_Hero", f"Données nommées ARM_Hero (actuel : {arm.name})", "Renommez les données de l'armature.", 1)
    tr_ok = all(abs(s - 1) < 1e-4 for s in ob.scale) and all(abs(a) < 1e-4 for a in ob.rotation_euler) and ob.location.length < 1e-4
    r.check(tr_ok, "Objet : échelle 1, rotation 0, position (0, 0, 0)", "Object > Apply > All Transforms.", 2)
    names = set(b.name for b in arm.bones)
    missing = sorted(set(EXPECT) - names)
    extra = sorted(names - set(EXPECT))
    r.check(not missing, f"Bones attendus présents (manquants : {missing[:6] or 'aucun'})", "Créez tous les bones de la liste.", 5)
    r.check(not extra, f"Aucun bone en trop ou mal nommé (en trop : {extra[:6] or 'aucun'})", "Nommez : root, pelvis, spine.001…, upper_arm.L…", 4)
    sides = [n for n in names if n.endswith(".L")]
    r.check(all(n[:-2] + ".R" in names for n in sides) and all(n[:-2] + ".L" in names for n in names if n.endswith(".R")), "Chaque bone .L a son .R et réciproquement", "Symétrie : Symmetrize ou construire les deux côtés.", 4)
    bones = arm.bones
    bad_par = [n for n, p in EXPECT.items() if n in bones and ((bones[n].parent.name if bones[n].parent else None) != p)]
    r.check(not bad_par, f"Hiérarchie conforme (erreurs : {bad_par[:5] or 'aucune'})", "Ctrl+P > Keep Offset ou parent dans Bone Properties > Relations.", 4)
    bad_conn = [n for n in EXPECT if n in bones and (bones[n].use_connect != ((n[:-2] if n[-2:] in (".L", ".R") else n) in CONNECTED))]
    r.check(not bad_conn, f"Connexions conformes (erreurs : {bad_conn[:5] or 'aucune'})", "Connected : chaînes oui ; shoulder et thigh non.", 3)
    # édition : roll et miroirs
    bpy.context.view_layer.objects.active = ob
    bpy.ops.object.mode_set(mode="EDIT")
    eb = arm.edit_bones
    asym, rolls, short = [], [], []
    for n in sides:
        a, b = eb.get(n), eb.get(n[:-2] + ".R")
        if a is None or b is None:
            continue
        d = max((a.head - b.head * __import__("mathutils").Vector((-1, 1, 1))).length, (a.tail - b.tail * __import__("mathutils").Vector((-1, 1, 1))).length)
        if d > 0.002:
            asym.append((n, round(d, 4)))
        if abs(a.roll + b.roll) > 1e-3 or abs(a.roll) > 1e-3:
            rolls.append(n)
    for b in eb:
        if b.length < 0.02:
            short.append(b.name)
    top = eb["head"].tail.z if "head" in eb else 0.0
    toe = eb["toe.L"].tail.z if "toe.L" in eb else 9.0
    arm_pose = "hand.L" in eb and "shoulder.L" in eb and eb["hand.L"].tail.z < eb["shoulder.L"].head.z - 0.3 and eb["hand.L"].tail.x > eb["shoulder.L"].tail.x + 0.2
    bpy.ops.object.mode_set(mode="OBJECT")
    r.check(not asym, f"Symétrie X des bones .R (écarts > 2 mm : {asym[:4] or 'aucun'})", "Symmetrize (Armature > Symmetrize) depuis le côté .L.", 5)
    r.check(not rolls, f"Roll nul et opposé entre .L et .R (erreurs : {rolls[:4] or 'aucune'})", "Armature > Bone Roll > Clear Roll ou Recalculate.", 2)
    r.check(abs(top - 1.76) <= 0.05, f"Taille : sommet de head à {top:.2f} m (1,76 ± 0,05)", "Le squelette doit épouser le mannequin.", 3)
    r.check(abs(toe) <= 0.02, f"Pieds au sol : queue de toe à z = {toe:+.3f} m", "", 2)
    r.check(not short, f"Aucun bone de moins de 2 cm ({short[:4] or 'aucun'})", "", 2)
    r.check(arm_pose, "Bras en pose A : hand.L plus bas et plus loin que shoulder.L", "Les bras s'écartent d'environ 40° de la verticale.", 2)
    deform_bad = [b.name for b in arm.bones if b.use_deform == (b.name == "root")]
    r.check(not deform_bad, f"Déformation : root non, les autres oui (erreurs : {deform_bad[:5] or 'aucune'})", "Bone Properties > Deform.", 2)
    dirty = [pb.name for pb in ob.pose.bones if pb.location.length > 1e-5 or any(abs(a) > 1e-5 for a in pb.rotation_euler) or abs(pb.rotation_quaternion.w - 1) > 1e-5 or any(abs(s - 1) > 1e-5 for s in pb.scale)]
    r.check(not dirty, f"Pose de repos propre (bones transformés : {dirty[:4] or 'aucun'})", "Pose > Clear Transform > All sur tous les bones.", 3)
    if debug:
        print("[DEBUG] missing", missing, "extra", extra, "asym", asym, "rolls", rolls, "top", round(top, 3), "toe", round(toe, 3), "dirty", dirty)
    if L.flag("--render"):
        lum = L.quick_render(15, 4)
        r.check(lum > 0.05, f"Rendu de contrôle non noir ({lum:.3f})", "", 1)
    return r.finish()


if __name__ == "__main__":
    L.run(main)
