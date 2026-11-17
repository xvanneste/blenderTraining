"""
build_ch06_08_files.py — « Shape keys et drivers » (CH06.08 : un shape key correctif de coude, piloté par un driver).

Le bras-tube CHR_Arm (60 cm le long de X, rayon 5 cm, 31 anneaux de 16 sommets) lié à RIG_Arm (upper 0 → 0,30 m, fore 0,30 → 0,60 m) par Automatic Weights (comme CH06.03).
Quand le coude plie de 90°, le skinning linéaire écrase le coude (rayon moyen de l'anneau du coude : 4,08 cm au lieu de 5,00 cm ; côté intérieur : 2,5 cm).
  Solution : shape key « elbow_fix » (relatif à Basis, curseur 0–1) qui gonfle radialement les sommets du coude ; limité par le groupe de sommets « elbow » (poids 1 − ((x−0,30)/0,12)², nul au-delà de 12 cm) ;
             DRIVER sur sa valeur : expression « a / 1.5708 », variable a = Transform Channel du bone fore, Rotation Z, Local Space (fore en Rotation Mode XYZ Euler) : 0 au repos, 1 à 90°.
  Le coefficient de gonflage est CALIBRÉ par le script (rayon moyen de l'anneau du coude = 5,0 cm à 90°).
  STARTER_FILES/ch06_08_shapekeys_starter.blend : bras lié, SANS shape key ni driver.
  COMPLETED_EXAMPLES/ch06_08_shapekeys_solution.blend (+ _reference.png : silhouette vue de dessus à 90°, sans puis avec le shape key)
  COUNTER_EXAMPLES/ : no_key, no_driver, always_on, weak, no_group, wrong_bone
Usage : blender -b --factory-startup --python-exit-code 1 --python build_ch06_08_files.py
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
N_RING, N_SEG, LENGTH, RADIUS = 31, 16, 0.6, 0.05
NOTE = """CH06.08 — SHAPE KEYS ET DRIVERS (CHR_Arm, RIG_Arm)
Le coude plié à 90° s'écrase (skinning linéaire). Corrigez-le par un shape key piloté par la pose :
1. CHR_Arm > Object Data > Shape Keys : ajoutez « Basis » puis un second shape key nommé elbow_fix ; Value de 0 à 1.
2. Groupe de sommets « elbow » (poids 1 au coude, 0 au-delà de 12 cm) ; dans le shape key : Vertex Group = elbow.
3. En Edit Mode du shape key elbow_fix, gonflez radialement les sommets du coude (Scale en pivot sur l'axe) : rayon ≈ +22 % au centre.
4. Driver sur la Value : Scripted Expression « a / 1.5708 » ; variable a = Transform Channel, objet RIG_Arm, bone fore, Z Rotation, Local Space.
   (bone fore en Rotation Mode XYZ Euler.)
Le correcteur plie fore de 45° puis 90° : valeur du shape key 0,5 puis 1 ; rayon du coude restauré ; sommets loin du coude inchangés ; repos identique à Basis.
Vérification : SCRIPTS/validate_ch06_08.py -- --exercise shapekeys
"""


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


def coords(ob):
    bpy.context.view_layer.update()
    ev = ob.evaluated_get(bpy.context.evaluated_depsgraph_get())
    me = ev.to_mesh()
    co = np.array([v.co[:] for v in me.vertices])
    ev.to_mesh_clear()
    return co


def dist_centerline(p):
    best = 9.0
    for a, b in (((0, 0, 0), (0.3, 0, 0)), ((0.3, 0, 0), (0.3, 0.3, 0))):
        a, b = Vector(a), Vector(b)
        d = b - a
        t = max(0.0, min(1.0, (Vector(p) - a).dot(d) / d.length_squared))
        best = min(best, (Vector(p) - (a + d * t)).length)
    return best


def ring_mean(co, rest, x=0.30):
    idx = [i for i in range(len(rest)) if abs(rest[i][0] - x) < 1e-3]
    return float(np.mean([dist_centerline(co[i]) for i in idx]))


def add_key(tube, scale):
    sk_basis = tube.shape_key_add(name="Basis", from_mix=False)
    sk = tube.shape_key_add(name="elbow_fix", from_mix=False)
    sk.slider_min, sk.slider_max = 0.0, 1.0
    g = tube.vertex_groups.new(name="elbow")
    for v in tube.data.vertices:
        w = max(0.0, 1.0 - ((v.co.x - 0.30) / 0.12) ** 2)
        if w > 0:
            g.add([v.index], w, "REPLACE")
    for i, v in enumerate(tube.data.vertices):
        sk.data[i].co = Vector((v.co.x, v.co.y * (1 + scale), v.co.z * (1 + scale)))
    return sk


def add_driver(tube, rig, bone="fore", div=1.5708):
    fc = tube.data.shape_keys.driver_add('key_blocks["elbow_fix"].value')
    d = fc.driver
    d.type = "SCRIPTED"
    d.expression = f"a / {div}"
    v = d.variables.new()
    v.name = "a"
    v.type = "TRANSFORMS"
    v.targets[0].id = rig
    v.targets[0].bone_target = bone
    v.targets[0].transform_type = "ROT_Z"
    v.targets[0].transform_space = "LOCAL_SPACE"


def bend(rig, angle):
    rig.pose.bones["fore"].rotation_euler = (0, 0, math.radians(angle))
    bpy.context.view_layer.update()


def skinned(kind_scale=None):
    L.reset("SC_SHAPE")
    tube = make_tube()
    rig = make_rig()
    bpy.ops.object.select_all(action="DESELECT")
    tube.select_set(True)
    rig.select_set(True)
    bpy.context.view_layer.objects.active = rig
    assert "FINISHED" in bpy.ops.object.parent_set(type="ARMATURE_AUTO")
    bpy.context.view_layer.objects.active = tube
    bpy.ops.object.vertex_group_normalize_all(group_select_mode="ALL", lock_active=False)
    rig.pose.bones["fore"].rotation_mode = "XYZ"
    return tube, rig


def calibrate():
    best = None
    for s in np.arange(0.10, 0.50, 0.02):
        tube, rig = skinned()
        rest = np.array([v.co[:] for v in tube.data.vertices])
        sk = add_key(tube, float(s))
        sk.value = 1.0
        bend(rig, 90)
        m = ring_mean(coords(tube), rest)
        print(f"[calib] scale {s:.2f} -> anneau {m:.4f}")
        if best is None or abs(m - 0.05) < best[0]:
            best = (abs(m - 0.05), float(s), m)
    print("[calib] retenu", best)
    return best[1]


def build(kind, scale):
    tube, rig = skinned()
    if kind not in ("starter", "no_key"):
        sk = add_key(tube, 0.05 if kind == "weak" else scale)
        if kind == "no_group":
            sk.vertex_group = ""
        else:
            sk.vertex_group = "elbow"
        if kind == "no_driver":
            sk.value = 0.0
        elif kind == "always_on":
            sk.value = 1.0
        else:
            add_driver(tube, rig, "upper" if kind == "wrong_bone" else "fore")
        if kind == "no_group":
            sk.vertex_group = ""
    L.instructions(NOTE)
    return tube, rig


def sketch(tube, rig, path):
    """Vue de dessus (x, y) : coude à 90°, sans puis avec shape key ; points du maillage + axe des bones."""
    W = 300
    img = np.full((W, 2 * W, 3), 0.08, np.float32)
    sk = tube.data.shape_keys.key_blocks["elbow_fix"]
    bend(rig, 90)
    for panel, muted in enumerate((True, False)):
        sk.mute = muted
        co = coords(tube)
        col = (0.9, 0.55, 0.2) if panel == 0 else (0.3, 0.8, 0.5)
        for e in tube.data.edges:
            a, b = co[e.vertices[0]], co[e.vertices[1]]
            x0, y0 = panel * W + 40 + a[0] * 420, W - 40 - a[1] * 420
            x1, y1 = panel * W + 40 + b[0] * 420, W - 40 - b[1] * 420
            n = int(max(abs(x1 - x0), abs(y1 - y0))) + 1
            for k in range(n + 1):
                x, y = int(x0 + (x1 - x0) * k / n), int(y0 + (y1 - y0) * k / n)
                if 0 <= x < 2 * W and 0 <= y < W:
                    img[y, x] = col
        for a, b in (((0, 0), (0.3, 0)), ((0.3, 0), (0.3, 0.3))):
            for t in np.linspace(0, 1, 200):
                x, y = int(panel * W + 40 + (a[0] + (b[0] - a[0]) * t) * 420), int(W - 40 - (a[1] + (b[1] - a[1]) * t) * 420)
                if 0 <= y < W:
                    img[y, x] = (0.3, 0.7, 1.0)
    sk.mute = False
    rgba = np.concatenate([img, np.ones(img.shape[:2] + (1,), np.float32)], axis=2)
    out = bpy.data.images.new("sk", 2 * W, W)
    out.pixels = rgba[::-1].ravel()
    out.filepath_raw = path
    out.file_format = "PNG"
    out.save()
    bend(rig, 0)


def main():
    out = os.path.join(CH, "COMPLETED_EXAMPLES")
    scale = calibrate()
    build("starter", scale)
    L.save(os.path.join(CH, "STARTER_FILES", "ch06_08_shapekeys_starter.blend"))
    for k in ("no_key", "no_driver", "always_on", "weak", "no_group", "wrong_bone"):
        build(k, scale)
        L.save(os.path.join(out, "COUNTER_EXAMPLES", f"ch06_08_shapekeys_{k}.blend"))
    tube, rig = build("solution", scale)
    L.save(os.path.join(out, "ch06_08_shapekeys_solution.blend"))
    sketch(tube, rig, os.path.join(out, "ch06_08_shapekeys_reference.png"))


if __name__ == "__main__":
    L.run(main)
