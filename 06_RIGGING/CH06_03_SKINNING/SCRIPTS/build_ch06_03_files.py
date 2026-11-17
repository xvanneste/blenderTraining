"""
build_ch06_03_files.py — « Skinning » (CH06.03).

Un bras-tube CHR_Arm (cylindre de 60 cm le long de X, rayon 5 cm, 31 anneaux de 16 sommets) et son armature RIG_Arm (bones upper de 0 à 0,30 m et fore de 0,30 à 0,60 m, connectés).
  Solution : Automatic Weights (parent_set ARMATURE_AUTO) : groupes de sommets « upper » et « fore », modificateur Armature -> RIG_Arm, poids normalisés.
  STARTER_FILES/ch06_03_skinning_starter.blend : le tube et l'armature, NON liés (pas de groupes, pas de modificateur).
  COMPLETED_EXAMPLES/ch06_03_skinning_solution.blend (+ _reference.png : poids et pose pliée)
  COUNTER_EXAMPLES/ : unweighted, unnormalized, rigid, swapped, too_many, no_modifier
Test de pliage du correcteur : forearm tourné de 90° autour de Z, au coude (0,30 ; 0 ; 0).
Usage : blender -b --factory-startup --python-exit-code 1 --python build_ch06_03_files.py
Testé avec : Blender 5.3.0.
"""
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bmesh  # noqa: E402
import bpy  # noqa: E402
import numpy as np  # noqa: E402
from mathutils import Vector  # noqa: E402

CH = L.chapter_dir(__file__)
NOTE = """CH06.03 — SKINNING (CHR_Arm lié à RIG_Arm) : lier le tube à l'armature avec des poids propres
1. Sélectionnez le tube CHR_Arm, puis l'armature RIG_Arm (active) : Ctrl+P > With Automatic Weights.
2. Résultat attendu : groupes de sommets « upper » et « fore » ; modificateur Armature (objet RIG_Arm) ; chaque sommet pesé ; somme des poids = 1 ; au plus 4 influences par sommet.
3. Pliez le coude (Pose Mode, forearm tourne de 90°) : le bout du bras suit forearm, la racine reste sur upper, le coude se plie sans cassure.
Vérification : SCRIPTS/validate_ch06_03.py -- --exercise skinning
"""
N_RING, N_SEG, LENGTH, RADIUS = 31, 16, 0.6, 0.05


def make_tube():
    bm = bmesh.new()
    rings = []
    for i in range(N_RING):
        x = LENGTH * i / (N_RING - 1)
        rings.append([bm.verts.new((x, RADIUS * math.cos(2 * math.pi * k / N_SEG), RADIUS * math.sin(2 * math.pi * k / N_SEG))) for k in range(N_SEG)])
    for i in range(N_RING - 1):
        for k in range(N_SEG):
            bm.faces.new((rings[i][k], rings[i][(k + 1) % N_SEG], rings[i + 1][(k + 1) % N_SEG], rings[i + 1][k]))
    me = bpy.data.meshes.new("ME_CHR_Arm")
    bm.to_mesh(me)
    bm.free()
    ob = bpy.data.objects.new("CHR_Arm", me)
    bpy.context.scene.collection.objects.link(ob)
    for p in me.polygons:
        p.use_smooth = True
    return ob


def make_rig():
    arm = bpy.data.armatures.new("ARM_Arm")
    ob = bpy.data.objects.new("RIG_Arm", arm)
    bpy.context.scene.collection.objects.link(ob)
    bpy.context.view_layer.objects.active = ob
    for o in bpy.data.objects:
        o.select_set(False)
    ob.select_set(True)
    bpy.ops.object.mode_set(mode="EDIT")
    up = arm.edit_bones.new("upper"); up.head, up.tail = Vector((0, 0, 0)), Vector((0.30, 0, 0))
    fo = arm.edit_bones.new("fore"); fo.head, fo.tail = Vector((0.30, 0, 0)), Vector((0.60, 0, 0))
    fo.parent = up
    fo.use_connect = True
    bpy.ops.object.mode_set(mode="OBJECT")
    ob.show_in_front = True
    return ob


def bend(rig, angle=90.0):
    rig.pose.bones["fore"].rotation_mode = "XYZ"
    rig.pose.bones["fore"].rotation_euler = (0, 0, math.radians(angle))
    bpy.context.view_layer.update()


def evaluated_coords(ob):
    ev = ob.evaluated_get(bpy.context.evaluated_depsgraph_get())
    me = ev.to_mesh()
    co = np.array([v.co[:] for v in me.vertices])
    ev.to_mesh_clear()
    return co


def build(kind):
    L.reset("SC_SKIN")
    L.studio(subject_height=1.0)
    tube = make_tube()
    rig = make_rig()
    if kind != "starter":
        bpy.ops.object.select_all(action="DESELECT")
        tube.select_set(True)
        rig.select_set(True)
        bpy.context.view_layer.objects.active = rig
        r = bpy.ops.object.parent_set(type="ARMATURE_AUTO")
        assert "FINISHED" in r, r
        bpy.context.view_layer.objects.active = tube
        bpy.ops.object.vertex_group_normalize_all(group_select_mode="ALL", lock_active=False)   # Automatic Weights laisse des sommes de 0,978 : on normalise
        me = tube.data
        gu, gf = tube.vertex_groups["upper"], tube.vertex_groups["fore"]
        if kind == "rigid":                               # poids binaires : tout ce qui est avant le coude pèse 1 sur upper, après : 1 sur fore
            for v in me.vertices:
                gu.add([v.index], 1.0 if v.co.x < 0.30 else 0.0, "REPLACE")
                gf.add([v.index], 0.0 if v.co.x < 0.30 else 1.0, "REPLACE")
        elif kind == "unnormalized":
            for v in me.vertices:
                for g in (gu, gf):
                    try:
                        w = g.weight(v.index)
                    except RuntimeError:
                        continue
                    g.add([v.index], w * 0.5, "REPLACE")
        elif kind == "unweighted":
            idx = [v.index for v in me.vertices if v.co.x > 0.54]
            gu.remove(idx)
            gf.remove(idx)
        elif kind == "swapped":
            gu.name, gf.name = "tmp", "upper"
            gu.name = "fore"
        elif kind == "too_many":
            for k in range(3):
                g = tube.vertex_groups.new(name=f"extra.{k}")
                g.add(list(range(len(me.vertices))), 0.01, "REPLACE")
        elif kind == "no_modifier":
            for m in list(tube.modifiers):
                tube.modifiers.remove(m)
    L.instructions(NOTE)
    return tube, rig


def sketch(tube, rig, path):
    """Deux panneaux (x, y) : poids (rouge = upper, bleu = fore) au repos, puis pose pliée."""
    S = 360
    img = np.zeros((S, 2 * S, 3), np.float32)
    img[...] = 0.08
    me = tube.data
    gu = tube.vertex_groups["upper"]
    rest = np.array([v.co[:] for v in me.vertices])
    w = []
    for v in me.vertices:
        try:
            w.append(gu.weight(v.index))
        except RuntimeError:
            w.append(0.0)
    w = np.array(w)
    bend(rig)
    bent = evaluated_coords(tube)
    for off, co in ((0, rest), (S, bent)):
        for p, wu in zip(co, w):
            x, y = int(off + 40 + p[0] * 450), int(S / 2 + 60 - p[1] * 450)
            if 0 <= x < off + S and 0 <= y < S:
                img[max(y - 1, 0):y + 2, max(x - 1, 0):x + 2] = (wu, 0.1, 1 - wu)
    rgba = np.concatenate([img, np.ones(img.shape[:2] + (1,), np.float32)], axis=2)
    out = bpy.data.images.new("sk", 2 * S, S)
    out.pixels = rgba[::-1].ravel()
    out.filepath_raw = path
    out.file_format = "PNG"
    out.save()
    rig.pose.bones["fore"].rotation_euler = (0, 0, 0)


def main():
    out = os.path.join(CH, "COMPLETED_EXAMPLES")
    build("starter")
    L.save(os.path.join(CH, "STARTER_FILES", "ch06_03_skinning_starter.blend"))
    for k in ("unweighted", "unnormalized", "rigid", "swapped", "too_many", "no_modifier"):
        build(k)
        L.save(os.path.join(out, "COUNTER_EXAMPLES", f"ch06_03_skinning_{k}.blend"))
    tube, rig = build("solution")
    L.save(os.path.join(out, "ch06_03_skinning_solution.blend"))
    sketch(tube, rig, os.path.join(out, "ch06_03_skinning_reference.png"))


if __name__ == "__main__":
    L.run(main)
