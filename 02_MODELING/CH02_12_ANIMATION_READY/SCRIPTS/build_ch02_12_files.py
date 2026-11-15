"""
build_ch02_12_files.py — « Le coude qui plie bien » (CH02.12, modélisation pour l'animation).

  STARTER_FILES/ch02_12_arm_starter.blend
      GEO_Arm : bras simplifié (cylindre Ø 10 cm, 60 cm, coude à z = 0,30), 4 segments réguliers ;
      ARM_Arm : armature 2 os (UpperArm, Forearm), modificateur Armature + groupes de sommets ;
      EMP_Elbow : repère du coude.
  COMPLETED_EXAMPLES/ch02_12_arm_solution.blend
      Mêmes objets + 4 boucles ajoutées autour du coude (z = 0,24 / 0,27 / 0,33 / 0,36).
  COMPLETED_EXAMPLES/ch02_12_arm_bent_starter.png et _bent_solution.png : coude plié à 90°.
Usage : blender -b --factory-startup --python build_ch02_12_files.py --python-exit-code 1
Testé avec : Blender 5.3.0.
"""
import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bmesh  # noqa: E402
import bpy  # noqa: E402

CH = L.chapter_dir(__file__)
NOTE = """CH02.12 — LE COUDE QUI PLIE BIEN
GEO_Arm n'a que 4 segments : plié à 90°, le coude s'écrase (12,5 % de volume perdu, mesuré).
1. Edit Mode, Ctrl+R sur le cylindre près du coude (EMP_Elbow, z = 0,30) : ajoutez au moins 3
   boucles entre z = 0,22 et z = 0,38 (par exemple 0,24 / 0,27 / 0,33 / 0,36 : Ctrl+R puis G Z).
   Les poids de déformation sont interpolés automatiquement par Loop Cut.
2. Testez : sélectionnez ARM_Arm, Pose Mode (Ctrl+Tab), os Forearm, R X 90. Comparez. Revenez
   à la pose de repos (Alt+R) avant d'enregistrer.
3. Gardez l'échelle d'objet à 1 et les dimensions réelles (60 cm).
Vérification : SCRIPTS/validate_ch02_12.py -- --exercise arm
"""
ELBOW = 0.30
BASE = [0.0, 0.15, 0.30, 0.45, 0.60]
EXTRA = [0.24, 0.27, 0.33, 0.36]


def arm_mesh(zs):
    bm = bmesh.new()
    rings = []
    for z in zs:
        rings.append([bm.verts.new((0.05 * math.cos(a), 0.05 * math.sin(a), z))
                      for a in [i * 2 * math.pi / 16 for i in range(16)]])
    for r0, r1 in zip(rings, rings[1:]):
        for i in range(16):
            bm.faces.new((r0[i], r0[(i + 1) % 16], r1[(i + 1) % 16], r1[i]))
    bm.faces.new(rings[0][::-1])
    bm.faces.new(rings[-1])
    me = bpy.data.meshes.new("ME_Arm")
    bm.to_mesh(me)
    bm.free()
    return me


def smooth_w(z, width=0.06):
    t = min(1.0, max(0.0, (z - (ELBOW - width / 2)) / width))
    return t * t * (3 - 2 * t)


def build(sol):
    L.reset("SC_Arm")
    L.studio(subject_height=0.7)
    col = L.collection("CHARACTER")
    skin = L.material("MAT_Skin", (0.8, 0.6, 0.5), 0.5)
    me = arm_mesh(sorted(BASE + EXTRA) if sol else BASE)
    arm = bpy.data.objects.new("GEO_Arm", me)
    col.objects.link(arm)
    me.materials.append(skin)
    for p in me.polygons:
        p.use_smooth = True
    # armature
    ad = bpy.data.armatures.new("AR_Arm")
    rig = bpy.data.objects.new("ARM_Arm", ad)
    col.objects.link(rig)
    bpy.context.view_layer.objects.active = rig
    rig.select_set(True)
    bpy.ops.object.mode_set(mode="EDIT")
    up = ad.edit_bones.new("UpperArm")
    up.head, up.tail = (0, 0, 0), (0, 0, ELBOW)
    fo = ad.edit_bones.new("Forearm")
    fo.head, fo.tail = (0, 0, ELBOW), (0, 0, 0.6)
    fo.parent = up
    fo.use_connect = True
    bpy.ops.object.mode_set(mode="OBJECT")
    g_up = arm.vertex_groups.new(name="UpperArm")
    g_fo = arm.vertex_groups.new(name="Forearm")
    for v in me.vertices:
        w = smooth_w(v.co.z)
        g_up.add([v.index], 1 - w, "REPLACE")
        g_fo.add([v.index], w, "REPLACE")
    m = arm.modifiers.new("Armature", "ARMATURE")
    m.object = rig
    arm.parent = rig
    emp = L.empty("EMP_Elbow", col, (0, 0, ELBOW), "SPHERE", 0.07)
    emp.hide_render = True
    cam = L.obj("CAM_Main")
    cam.location = (1.6, -0.9, 0.6)
    cam.data.lens = 50
    L.obj("EMP_Target").location = (0, 0.12, 0.33)
    L.render_defaults("BLENDER_EEVEE", 50)
    L.instructions(NOTE)
    return rig


def bend_and_render(rig, path):
    pb = rig.pose.bones["Forearm"]
    pb.rotation_mode = "XYZ"
    pb.rotation_euler = (math.radians(90), 0, 0)
    bpy.context.view_layer.update()
    bpy.context.scene.render.filepath = path
    bpy.ops.render.render(write_still=True)
    pb.rotation_euler = (0, 0, 0)


def main():
    out = os.path.join(CH, "COMPLETED_EXAMPLES")
    rig = build(False)
    L.save(os.path.join(CH, "STARTER_FILES", "ch02_12_arm_starter.blend"))
    bend_and_render(rig, os.path.join(out, "ch02_12_arm_bent_starter.png"))
    rig = build(True)
    L.save(os.path.join(out, "ch02_12_arm_solution.blend"))
    bend_and_render(rig, os.path.join(out, "ch02_12_arm_bent_solution.png"))


if __name__ == "__main__":
    L.run(main)
