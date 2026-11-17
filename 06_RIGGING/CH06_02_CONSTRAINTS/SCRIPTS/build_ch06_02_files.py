"""
build_ch06_02_files.py — « Contraintes » (CH06.02).

Un rig de REGARD RIG_Gaze (armature) : un bone « head » qui s'oriente à moitié vers une cible, deux yeux qui visent exactement la cible.
  Bones : head (de (0, 0, 1,70) à (0, −0,15, 1,70), orienté vers l'avant −Y) ; eye.L (0,03 ; −0,09 ; 1,74 -> y −0,14) et eye.R (miroir), enfants de head.
  Cible : l'Empty EMP_Target (par défaut en (0, −2, 1,74)).
  Contraintes (Pose Mode > Bone Constraints) :
    head  : 1. Damped Track vers EMP_Target (Track Axis Y, Influence 0,5) ; 2. Limit Rotation (Z limité à ± 35°, espace Local)
    eye.L / eye.R : Damped Track vers EMP_Target (Track Axis Y, Influence 1)
  STARTER_FILES/ch06_02_constraints_starter.blend : armature et cible, SANS contraintes.
  COMPLETED_EXAMPLES/ch06_02_constraints_solution.blend (+ _reference.png : croquis vue de dessus pour trois positions de la cible)
  COUNTER_EXAMPLES/ : no_constraints, wrong_axis, head_full, no_limit, eye_no_target, order_swapped
Usage : blender -b --factory-startup --python-exit-code 1 --python build_ch06_02_files.py
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
NOTE = """CH06.02 — CONTRAINTES (RIG_Gaze, cible EMP_Target) : un rig de regard
Pose Mode > onglet Bone Constraints :
1. eye.L et eye.R : Damped Track → Target EMP_Target, Track Axis Y (Influence 1) : les yeux visent la cible.
2. head : (a) Damped Track → EMP_Target, Track Axis Y, Influence 0,5 : la tête suit à moitié ; PUIS (b) Limit Rotation, Limit Z (−35° à +35°), Owner Space Local : on ne tourne pas la tête de plus de 35°.
L'ORDRE compte : la pile est évaluée de haut en bas, la limite vient après le suivi.
Le correcteur DÉPLACE la cible (devant, à 45°, presque de côté) et mesure : erreur de visée des yeux ≤ 1°, rotation de la tête ≈ la moitié de l'angle puis plafonnée à 35°.
Vérification : SCRIPTS/validate_ch06_02.py -- --exercise constraints
"""


def make(kind):
    for o in list(bpy.data.objects):                 # L.reset ne purge pas les objets orphelins : sinon EMP_Target.001
        bpy.data.objects.remove(o, do_unlink=True)
    for a in list(bpy.data.armatures):
        bpy.data.armatures.remove(a)
    L.reset("SC_GAZE")
    L.studio(subject_height=1.76)
    st = bpy.data.objects.get("EMP_Target")          # L.studio crée déjà un EMP_Target (visée de la caméra) : on le renomme pour libérer le nom
    if st is not None:
        st.name = "EMP_Studio"
    bpy.ops.object.empty_add(type="SPHERE", radius=0.08, location=(0, -2, 1.74))
    tgt = bpy.context.active_object
    tgt.name = "EMP_Target"
    arm = bpy.data.armatures.new("ARM_Gaze")
    ob = bpy.data.objects.new("RIG_Gaze", arm)
    bpy.context.scene.collection.objects.link(ob)
    bpy.context.view_layer.objects.active = ob
    ob.select_set(True)
    bpy.ops.object.mode_set(mode="EDIT")
    eb = arm.edit_bones
    h = eb.new("head"); h.head, h.tail = Vector((0, 0, 1.70)), Vector((0, -0.15, 1.70))
    for n, sx in (("eye.L", 1), ("eye.R", -1)):
        e = eb.new(n); e.head, e.tail = Vector((0.03 * sx, -0.09, 1.74)), Vector((0.03 * sx, -0.14, 1.74)); e.parent = h
    bpy.ops.object.mode_set(mode="OBJECT")
    ob.show_in_front = True
    if kind != "starter":
        bpy.ops.object.mode_set(mode="POSE")
        axis = "TRACK_X" if kind == "wrong_axis" else "TRACK_Y"
        for n in ("eye.L", "eye.R"):
            if kind == "no_constraints":
                continue
            c = ob.pose.bones[n].constraints.new("DAMPED_TRACK")
            c.target = None if (kind == "eye_no_target" and n == "eye.R") else tgt
            c.track_axis = axis
        if kind != "no_constraints":
            hb = ob.pose.bones["head"]

            def damped():
                c = hb.constraints.new("DAMPED_TRACK")
                c.target = tgt
                c.track_axis = axis
                c.influence = 1.0 if kind == "head_full" else 0.5

            def limit():
                c = hb.constraints.new("LIMIT_ROTATION")
                c.use_limit_z = True
                c.min_z, c.max_z = math.radians(-35), math.radians(35)
                c.owner_space = "LOCAL"
            if kind == "order_swapped":
                limit(); damped()
            elif kind == "no_limit":
                damped()
            else:
                damped(); limit()
        bpy.ops.object.mode_set(mode="OBJECT")
    L.instructions(NOTE)
    return ob, tgt


def sketch(ob, tgt, path):
    """Trois vignettes vue de dessus (x, y) : cible (rouge), tête (jaune), yeux (orange)."""
    S = 220
    tiles = []
    for pos in ((0, -2, 1.74), (1.5, -1.5, 1.74), (3.0, -0.2, 1.74)):
        tgt.location = pos
        bpy.context.view_layer.update()
        ev = ob.evaluated_get(bpy.context.evaluated_depsgraph_get())
        img = np.zeros((S, S, 3), np.float32)
        img[...] = 0.1

        def px(p):
            return int(S / 2 + p[0] * 40), int(S - 30 + p[1] * 40)

        def line(a, b, col, th=1):
            x0, y0 = px(a); x1, y1 = px(b)
            n = max(abs(x1 - x0), abs(y1 - y0)) + 1
            for k in range(n + 1):
                x, y = int(x0 + (x1 - x0) * k / n), int(y0 + (y1 - y0) * k / n)
                if 0 <= x < S and 0 <= y < S:
                    img[max(y - th, 0):y + th + 1, max(x - th, 0):x + th + 1] = col
        for n, col in (("head", (0.95, 0.9, 0.2)), ("eye.L", (0.95, 0.55, 0.15)), ("eye.R", (0.95, 0.55, 0.15))):
            pb = ev.pose.bones[n]
            a = ev.matrix_world @ pb.head
            b = ev.matrix_world @ pb.tail
            line(a, a + (b - a).normalized() * (3.0 if n != "head" else 1.0), col)
        tx, ty = px(tgt.location)
        img[max(ty - 4, 0):ty + 5, max(tx - 4, 0):tx + 5] = (1, 0.2, 0.2)
        tiles.append(img)
    sheet = np.concatenate(tiles, axis=1)
    rgba = np.concatenate([sheet, np.ones(sheet.shape[:2] + (1,), np.float32)], axis=2)
    out = bpy.data.images.new("sk", sheet.shape[1], S)
    out.pixels = rgba[::-1].ravel()
    out.filepath_raw = path
    out.file_format = "PNG"
    out.save()
    tgt.location = (0, -2, 1.74)


def main():
    out = os.path.join(CH, "COMPLETED_EXAMPLES")
    make("starter")
    L.save(os.path.join(CH, "STARTER_FILES", "ch06_02_constraints_starter.blend"))
    for k in ("no_constraints", "wrong_axis", "head_full", "no_limit", "eye_no_target", "order_swapped"):
        make(k)
        L.save(os.path.join(out, "COUNTER_EXAMPLES", f"ch06_02_constraints_{k}.blend"))
    ob, tgt = make("solution")
    L.save(os.path.join(out, "ch06_02_constraints_solution.blend"))
    sketch(ob, tgt, os.path.join(out, "ch06_02_constraints_reference.png"))


if __name__ == "__main__":
    L.run(main)
