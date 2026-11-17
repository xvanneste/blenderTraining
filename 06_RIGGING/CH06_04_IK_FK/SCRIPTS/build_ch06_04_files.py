"""
build_ch06_04_files.py — « IK/FK » (CH06.04).

Un bras RIG_ArmIK : bones upper (0 → 0,30 m) et fore (0,30 m → (0,595 ; 0 ; −0,052), pré-fléchi de 10°) ; contrôleurs ik_hand (cible IK, à l'extrémité de fore),
ik_pole (cible de pôle, (0,30 ; 0 ; 0,50)) et switch (porte la propriété personnalisée « ik_fk » : 1 = IK, 0 = FK).
  Contrainte IK sur fore : Target RIG_ArmIK / ik_hand ; Pole Target RIG_ArmIK / ik_pole ; Chain Length 2 ; Pole Angle réglé pour que le coude se plie VERS le pôle.
  Driver : influence de la contrainte IK ← pose.bones["switch"]["ik_fk"]  (Averaged Value, une variable).
  STARTER_FILES/ch06_04_ikfk_starter.blend : bras et contrôleurs, SANS IK ni driver (la propriété ik_fk existe).
  COMPLETED_EXAMPLES/ch06_04_ikfk_solution.blend (+ _reference.png : croquis du bras en IK, pôle haut/bas, puis en FK)
  COUNTER_EXAMPLES/ : no_pole, no_driver, stretch, chain_one, no_ik
Usage : blender -b --factory-startup --python-exit-code 1 --python build_ch06_04_files.py
Testé avec : Blender 5.3.0.
"""
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bpy  # noqa: E402
import numpy as np  # noqa: E402
from mathutils import Vector  # noqa: E402

CH = L.chapter_dir(__file__)
FORE_TAIL = (0.30 + 0.30 * math.cos(math.radians(10)), 0.0, -0.30 * math.sin(math.radians(10)))   # PRÉ-FLEXION de 10° : un bras parfaitement droit est une singularité de l'IK (le coude ne sait pas de quel côté plier)
NOTE = """CH06.04 — IK/FK (RIG_ArmIK) : un bras à cinématique inverse (IK) et directe (FK) commutables
Pose Mode, bone fore > Bone Constraints > Inverse Kinematics : Target RIG_ArmIK / Bone ik_hand ; Pole Target RIG_ArmIK / Bone ik_pole ; Chain Length 2 ; Pole Angle réglé pour que le coude se plie vers le pôle.
Interrupteur : propriété personnalisée « ik_fk » du bone switch (1 = IK, 0 = FK) ; elle pilote l'Influence de la contrainte IK par un DRIVER (variable Single Property : pose.bones["switch"]["ik_fk"]).
Le correcteur teste : (1) IK : le bout de fore atteint ik_hand à 1 cm ; (2) longueurs de bones conservées ; (3) le pôle choisit le côté du coude ; (4) cible hors de portée : bras tendu sans étirement ;
(5) ik_fk = 0 : le bras redevient FK (la contrainte n'agit plus ; tourner upper entraîne fore) ; (6) le driver existe.
Vérification : SCRIPTS/validate_ch06_04.py -- --exercise ikfk
"""


def make(kind):
    for o in list(bpy.data.objects):
        bpy.data.objects.remove(o, do_unlink=True)
    for a in list(bpy.data.armatures):
        bpy.data.armatures.remove(a)
    L.reset("SC_IKFK")
    arm = bpy.data.armatures.new("ARM_ArmIK")
    ob = bpy.data.objects.new("RIG_ArmIK", arm)
    bpy.context.scene.collection.objects.link(ob)
    bpy.context.view_layer.objects.active = ob
    ob.select_set(True)
    bpy.ops.object.mode_set(mode="EDIT")
    E = arm.edit_bones
    up = E.new("upper"); up.head, up.tail = Vector((0, 0, 0)), Vector((0.30, 0, 0))
    fo = E.new("fore"); fo.head, fo.tail = Vector((0.30, 0, 0)), Vector(FORE_TAIL); fo.parent = up; fo.use_connect = True
    ik = E.new("ik_hand"); ik.head, ik.tail = Vector(FORE_TAIL), Vector((FORE_TAIL[0] + 0.10, 0, FORE_TAIL[2]))
    pl = E.new("ik_pole"); pl.head, pl.tail = Vector((0.30, 0, 0.50)), Vector((0.30, 0, 0.60))
    sw = E.new("switch"); sw.head, sw.tail = Vector((0, 0, 0.30)), Vector((0, 0, 0.40))
    bpy.ops.object.mode_set(mode="POSE")
    ob.pose.bones["switch"]["ik_fk"] = 1.0
    if kind != "starter" and kind != "no_ik":
        c = ob.pose.bones["fore"].constraints.new("IK")
        c.name = "IK"
        c.target, c.subtarget = ob, "ik_hand"
        if kind != "no_pole":
            c.pole_target, c.pole_subtarget = ob, "ik_pole"
            c.pole_angle = math.radians(POLE_ANGLE)
        c.chain_count = 1 if kind == "chain_one" else 2
        if kind == "stretch":
            ob.pose.bones["fore"].ik_stretch = 0.1
            ob.pose.bones["upper"].ik_stretch = 0.1
            c.use_stretch = True
        if kind != "no_driver":
            fc = ob.driver_add('pose.bones["fore"].constraints["IK"].influence')
            d = fc.driver
            d.type = "AVERAGE"
            var = d.variables.new()
            var.name = "ik_fk"
            var.type = "SINGLE_PROP"
            var.targets[0].id = ob
            var.targets[0].data_path = 'pose.bones["switch"]["ik_fk"]'
    bpy.ops.object.mode_set(mode="OBJECT")
    ob.show_in_front = True
    L.instructions(NOTE)
    return ob


POLE_ANGLE = 0.0


def put(ob, name, world_head):
    """Place la tête d'un bone sans parent à une position MONDE (la location d'un bone est exprimée dans son repère de repos)."""
    b = ob.pose.bones[name]
    delta = Vector(world_head) - b.bone.head_local
    b.location = b.bone.matrix_local.to_3x3().inverted() @ delta


def elbow(ob):
    bpy.context.view_layer.update()
    ev = ob.evaluated_get(bpy.context.evaluated_depsgraph_get())
    mw = ev.matrix_world
    pbu, pbf = ev.pose.bones["upper"], ev.pose.bones["fore"]
    return mw @ pbu.tail, mw @ pbf.tail


def calibrate():
    """Choisit le Pole Angle pour que le coude se plie vers le pôle (haut) puis vers le bas quand le pôle descend."""
    global POLE_ANGLE
    for ang in (0, 90, -90, 180):
        POLE_ANGLE = ang
        ob = make("solution")
        bpy.ops.object.mode_set(mode="POSE")
        put(ob, "ik_hand", (0.40, 0, 0))                          # à 0,40 m de l'épaule : le coude doit se plier
        put(ob, "ik_pole", (0.30, 0, 0.50))
        el_up, _ = elbow(ob)
        put(ob, "ik_pole", (0.30, 0, -0.50))                      # pôle de l'autre côté
        el_dn, _ = elbow(ob)
        bpy.ops.object.mode_set(mode="OBJECT")
        print(f"[calib] pole_angle {ang} : coude z haut {el_up.z:+.3f} / bas {el_dn.z:+.3f}")
        if el_up.z > 0.05 and el_dn.z < -0.05:
            return ang
    raise RuntimeError("aucun Pole Angle ne convient")


def sketch(path):
    S = 300
    img = np.zeros((S, 4 * S, 3), np.float32)
    img[...] = 0.08
    panels = []
    ob = make("solution")
    bpy.ops.object.mode_set(mode="POSE")
    pb = ob.pose.bones

    def draw(i, pts, col):
        def px(p):
            return int(i * S + 40 + p[0] * 360), int(S / 2 + 40 - p[2] * 360)
        for a, b in zip(pts, pts[1:]):
            x0, y0 = px(a); x1, y1 = px(b)
            n = max(abs(x1 - x0), abs(y1 - y0)) + 1
            for k in range(n + 1):
                x, y = int(x0 + (x1 - x0) * k / n), int(y0 + (y1 - y0) * k / n)
                if 0 <= x < 4 * S and 0 <= y < S:
                    img[max(y - 2, 0):y + 3, max(x - 2, 0):x + 3] = col
    setups = [((0.45, 0, 0.25), (0.3, 0, 0.5), 1.0, "IK, pôle en haut"), ((0.45, 0, 0.25), (0.3, 0, -0.5), 1.0, "IK, pôle en bas"), ((0.9, 0, 0.0), (0.3, 0, 0.5), 1.0, "IK hors de portée"), ((0.6, 0, 0), (0.3, 0, 0.5), 0.0, "FK")]
    for i, (hand, pole, sw, _) in enumerate(setups):
        put(ob, "ik_hand", hand)
        put(ob, "ik_pole", pole)
        pb["switch"]["ik_fk"] = sw
        from mathutils import Matrix
        pb["upper"].matrix = (Matrix.Rotation(math.radians(40), 4, "Y") @ pb["upper"].bone.matrix_local) if sw == 0.0 else pb["upper"].bone.matrix_local
        e, t = elbow(ob)
        draw(i, [Vector((0, 0, 0)), e, t], (0.95, 0.8, 0.2))
        h = ob.matrix_world @ pb["ik_hand"].tail
        hh = ob.matrix_world @ pb["ik_hand"].head
        draw(i, [hh, h], (0.3, 0.7, 1.0))
        pp = ob.matrix_world @ pb["ik_pole"].head
        x, y = int(i * S + 40 + pp[0] * 360), int(S / 2 + 40 - pp[2] * 360)
        if 0 <= y < S:
            img[max(y - 4, 0):y + 5, max(x - 4, 0):x + 5] = (1, 0.2, 0.2)
    rgba = np.concatenate([img, np.ones(img.shape[:2] + (1,), np.float32)], axis=2)
    out = bpy.data.images.new("sk", 4 * S, S)
    out.pixels = rgba[::-1].ravel()
    out.filepath_raw = path
    out.file_format = "PNG"
    out.save()


def main():
    global POLE_ANGLE
    out = os.path.join(CH, "COMPLETED_EXAMPLES")
    POLE_ANGLE = calibrate()
    print("[calib] retenu :", POLE_ANGLE)
    make("starter")
    L.save(os.path.join(CH, "STARTER_FILES", "ch06_04_ikfk_starter.blend"))
    for k in ("no_pole", "no_driver", "stretch", "chain_one", "no_ik"):
        make(k)
        L.save(os.path.join(out, "COUNTER_EXAMPLES", f"ch06_04_ikfk_{k}.blend"))
    make("solution")
    L.save(os.path.join(out, "ch06_04_ikfk_solution.blend"))
    sketch(os.path.join(out, "ch06_04_ikfk_reference.png"))


if __name__ == "__main__":
    L.run(main)
