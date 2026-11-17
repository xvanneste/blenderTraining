"""
validate_ch06_04.py — Correcteur « IK/FK » (CH06.04).
Usage : … --python-exit-code 1 --python validate_ch06_04.py -- --exercise ikfk [--render] [--debug]
RIG_ArmIK : bones upper, fore, ik_hand, ik_pole, switch (propriété « ik_fk » : 1 = IK, 0 = FK) :
  Configuration : contrainte IK sur fore (Target RIG_ArmIK/ik_hand, Pole Target RIG_ArmIK/ik_pole, Chain Length 2) ; driver sur l'influence de cette contrainte,
                  lu dans pose.bones["switch"]["ik_fk"] ; aucun étirement (ik_stretch = 0 sur upper et fore).
  Comportement (les contrôleurs sont DÉPLACÉS ; le correcteur les remet ensuite) :
    IK, cible (0,45 ; 0 ; 0,25) atteignable : le bout de fore est à ≤ 1 cm de la cible ; longueurs upper et fore = 0,300 m ± 1 mm ;
    pôle en haut (z = +0,5) : coude à plus de 5 cm AU-DESSUS de la droite épaule–bout ; pôle en bas (z = −0,5) : à plus de 5 cm au-dessous ;
    cible hors de portée (0,9 ; 0 ; 0) : longueurs conservées (± 1 mm), bras tendu (le bout à 0,59–0,60 m de l'épaule) ;
    FK (ik_fk = 0) : la contrainte n'agit plus : tourner upper de 40° entraîne fore (bout à ≤ 5 mm de la position d'un solide), et le bout reste à ≥ 10 cm de la cible.
Testé avec : Blender 5.3.0.
"""
import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bpy  # noqa: E402
from mathutils import Matrix, Vector  # noqa: E402


def put(ob, name, world_head):
    b = ob.pose.bones[name]
    b.location = b.bone.matrix_local.to_3x3().inverted() @ (Vector(world_head) - b.bone.head_local)


def side(el, tip):
    """Distance signée du coude à la droite épaule → bout, dans le plan XZ (positif : au-dessus)."""
    return (tip.x * el.z - tip.z * el.x) / max(tip.length, 1e-9)


def state(ob):
    bpy.context.view_layer.update()
    ev = ob.evaluated_get(bpy.context.evaluated_depsgraph_get())
    mw = ev.matrix_world
    u, f = ev.pose.bones["upper"], ev.pose.bones["fore"]
    el, tip = mw @ u.tail, mw @ f.tail
    return el, tip, (mw @ u.tail - mw @ u.head).length, (mw @ f.tail - mw @ f.head).length


def main():
    debug = L.flag("--debug")
    r = L.Report("CH06.04 — IK/FK")
    ob = bpy.data.objects.get("RIG_ArmIK")
    if not r.check(ob is not None and ob.type == "ARMATURE" and all(n in ob.pose.bones for n in ("upper", "fore", "ik_hand", "ik_pole", "switch")), "RIG_ArmIK (bones upper, fore, ik_hand, ik_pole, switch)", "Partez du fichier de départ.", 2):
        return r.finish()
    pb = ob.pose.bones
    ik = next((c for c in pb["fore"].constraints if c.type == "IK"), None)
    r.check(ik is not None and ik.target == ob and ik.subtarget == "ik_hand", "fore : contrainte IK vers ik_hand", "Bone Constraints > Inverse Kinematics : Target RIG_ArmIK, Bone ik_hand.", 4)
    r.check(ik is not None and ik.pole_target == ob and ik.pole_subtarget == "ik_pole" and ik.chain_count == 2, "IK : Pole Target ik_pole ; Chain Length 2", "Pole Target RIG_ArmIK / ik_pole ; Chain Length 2.", 4)
    r.check(pb["upper"].ik_stretch == 0 and pb["fore"].ik_stretch == 0, "Aucun étirement IK (ik_stretch = 0)", "Bone Properties > Inverse Kinematics > Stretch = 0.", 2)
    anim = ob.animation_data
    drv = None
    if anim:
        for fc in anim.drivers:
            if 'constraints["IK"].influence' in fc.data_path or (ik and f'constraints["{ik.name}"].influence' in fc.data_path):
                drv = fc
    ok_d = drv is not None and any('"switch"' in t.data_path and "ik_fk" in t.data_path for v in drv.driver.variables for t in v.targets)
    r.check(ok_d, "Driver : influence de l'IK ← pose.bones[\"switch\"][\"ik_fk\"]", "Clic droit sur Influence > Add Driver ; variable Single Property.", 4)
    pb["switch"]["ik_fk"] = 1.0
    T1, POLE_UP, POLE_DN = (0.45, 0, 0.25), (0.30, 0, 0.50), (0.30, 0, -0.50)
    bpy.ops.object.mode_set(mode="POSE") if bpy.context.object is ob else None
    put(ob, "ik_hand", T1)
    put(ob, "ik_pole", POLE_UP)
    el_up, tip, lu, lf = state(ob)
    d = (tip - Vector(T1)).length
    r.check(d <= 0.01, f"IK : le bout de fore est à {1000 * d:.1f} mm de la cible (≤ 10)", "Contrainte IK active (influence 1, Pole Angle réglé).", 5)
    r.check(abs(lu - 0.30) <= 0.001 and abs(lf - 0.30) <= 0.001, f"Longueurs conservées : upper {lu:.4f}, fore {lf:.4f} (0,300 ± 0,001)", "", 3)
    s_up = side(el_up, tip)
    r.check(s_up > 0.05, f"Pôle en haut : coude à {100 * s_up:+.0f} cm de la droite épaule–bout (> +5 cm : au-dessus)", "Pole Target ik_pole ; Pole Angle (90° ici).", 4)
    put(ob, "ik_pole", POLE_DN)
    el_dn, tip_dn, _, _ = state(ob)
    s_dn = side(el_dn, tip_dn)
    r.check(s_dn < -0.05, f"Pôle en bas : coude à {100 * s_dn:+.0f} cm de la droite (< −5 cm : au-dessous)", "Le coude suit le pôle.", 4)
    put(ob, "ik_pole", POLE_UP)
    put(ob, "ik_hand", (0.9, 0, 0))
    _, tip2, lu2, lf2 = state(ob)
    reach = tip2.length
    r.check(abs(lu2 - 0.30) <= 0.001 and abs(lf2 - 0.30) <= 0.001 and 0.59 <= reach <= 0.60, f"Cible hors de portée : longueurs {lu2:.3f}/{lf2:.3f}, bras tendu à {reach:.3f} m (0,59–0,60)", "Pas d'étirement : le bras se tend sans s'allonger.", 3)
    # FK
    put(ob, "ik_hand", T1)
    pb["switch"]["ik_fk"] = 0.0
    _, tip_rest, _, _ = state(ob)
    R = Matrix.Rotation(math.radians(40), 4, "Y")
    pb["upper"].matrix = R @ pb["upper"].bone.matrix_local
    _, tip_fk, _, _ = state(ob)
    exp = R @ tip_rest
    dfk = (tip_fk - exp).length
    dt = (tip_fk - Vector(T1)).length
    r.check(dfk <= 0.005 and dt >= 0.10, f"FK (ik_fk = 0) : fore suit upper (écart {1000 * dfk:.1f} mm ≤ 5), bout à {100 * dt:.0f} cm de la cible (≥ 10)", "Le driver doit couper l'IK quand ik_fk = 0.", 5)
    pb["upper"].matrix = pb["upper"].bone.matrix_local
    pb["switch"]["ik_fk"] = 1.0
    put(ob, "ik_hand", (0.5954, 0, -0.0521))
    put(ob, "ik_pole", (0.30, 0, 0.50))
    if debug:
        print("[DEBUG] d", round(d, 4), "lu/lf", round(lu, 4), round(lf, 4), "side", round(s_up, 3), round(s_dn, 3), "reach", round(reach, 4), "fk", round(dfk, 4), round(dt, 3), "driver", ok_d)
    if L.flag("--render"):
        lum = L.quick_render(15, 4)
        r.check(lum > 0.05, f"Rendu de contrôle non noir ({lum:.3f})", "", 1)
    return r.finish()


if __name__ == "__main__":
    L.run(main)
