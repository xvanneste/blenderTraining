"""
build_ch06_07_files.py — « Rig mécanique » (CH06.07 : camion-benne, roues pilotées par drivers, vérin hydraulique par Damped Track).

Le camion GEO_Truck (un seul maillage, groupes de sommets = bones) et son armature RIG_Truck. AVANT = +Y ; roues de rayon 0,30 m.
  Bones : root (déplacement du camion), body (châssis + cabine), wheel_FL/FR/RL/RR (axe = axe du bone, dirigé vers +X), bed (benne, charnière arrière y = −1,0, axe X),
          bed_pt (point d'attache du vérin, enfant de bed), anchor (point d'attache sur le châssis), cyl (corps du vérin, longueur 0,6), rod (tige, longueur 0,6, enfant de bed_pt).
  Solution : (1) roues : un DRIVER sur rotation_euler[1] (axe du bone) de chaque roue : expression « -d / 0.3 », variable d = Transform Channel de root (Location Y, Local Space) ;
             (2) vérin : Damped Track de cyl vers bed_pt et de rod vers anchor ; (3) benne : Limit Rotation (X de 0 à 45°, Y et Z bloqués), repère Local.
  STARTER_FILES/ch06_07_truck_starter.blend : camion et armature SANS driver ni contrainte.
  COMPLETED_EXAMPLES/ch06_07_truck_solution.blend (+ _reference.png : croquis de profil : repos, camion avancé de 0,5 m, benne levée de 35°)
  COUNTER_EXAMPLES/ : no_drivers, wrong_radius, wrong_axis, unparented_wheels, no_track, no_limit
Usage : blender -b --factory-startup --python-exit-code 1 --python build_ch06_07_files.py
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
from mathutils import Matrix, Vector  # noqa: E402

CH = L.chapter_dir(__file__)
R = 0.30
WHEELS = {"wheel_FL": (-0.55, 0.9), "wheel_FR": (0.55, 0.9), "wheel_RL": (-0.55, -0.7), "wheel_RR": (0.55, -0.7)}
HINGE = Vector((0, -1.0, 0.6))
BED_PT = Vector((0, -0.3, 0.6))
ANCHOR = Vector((0, 0.2, 0.52))
CYL_LEN = 0.6
NOTE = """CH06.07 — RIG MÉCANIQUE (RIG_Truck / GEO_Truck)
1. Roues : sélectionnez RIG_Truck, Pose Mode, chaque bone wheel_* : Rotation Mode = XYZ Euler ; clic droit sur la Rotation Y > Add Driver. Type Scripted Expression « -d / 0.3 » ;
   variable d : Transform Channel, objet RIG_Truck, bone root, Location Y, espace Local Space. L'axe du bone est son axe Y : c'est autour de lui que la roue tourne.
2. Vérin : bone cyl > Bone Constraints > Damped Track vers RIG_Truck / bed_pt ; bone rod > Damped Track vers RIG_Truck / anchor.
3. Benne : bone bed > Bone Constraints > Limit Rotation : Limit X de 0 à 45°, Limit Y et Limit Z à 0, Owner Space Local Space.
Le correcteur AVANCE le camion (root), LÈVE la benne et regarde ce que font les sommets : rotation des roues (rayon 0,30 m), vérin aligné, benne limitée.
Vérification : SCRIPTS/validate_ch06_07.py -- --exercise truck
"""


def box(bm, c, s):
    ret = bmesh.ops.create_cube(bm, size=1.0)
    for v in ret["verts"]:
        v.co = Vector((v.co.x * s[0] + c[0], v.co.y * s[1] + c[1], v.co.z * s[2] + c[2]))
    return ret["verts"]


def capsule(bm, a, b, r):
    d = b - a
    ret = bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=12, radius1=r, radius2=r, depth=d.length)
    rot = Vector((0, 0, 1)).rotation_difference(d.normalized()).to_matrix().to_4x4()
    for v in ret["verts"]:
        v.co = rot @ v.co + (a + b) / 2
    return ret["verts"]


def wheel(bm, cx, cy):
    ret = bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=24, radius1=R, radius2=R, depth=0.2)
    rot = Matrix.Rotation(math.radians(90), 4, "Y")
    verts = list(ret["verts"])
    for v in verts:
        v.co = rot @ v.co + Vector((cx, cy, R))
    mk = box(bm, (cx, cy, R + 0.17), (0.24, 0.06, 0.16))          # repère : boîte à z ≈ 0,17–0,33 au-dessus de l'axe, dépasse de 2 cm
    return verts + mk


def bones_def():
    return {
        "root": ((0, 0, 0), (0, 0.4, 0), None),
        "body": ((0, -1.0, 0.35), (0, 1.2, 0.35), "root"),
        **{n: ((x, y, R), (x + 0.15, y, R), "root") for n, (x, y) in WHEELS.items()},
        "bed": (tuple(HINGE), (0, 0.2, 0.6), "body"),
        "bed_pt": (tuple(BED_PT), (BED_PT.x, BED_PT.y, BED_PT.z + 0.1), "bed"),
        "anchor": (tuple(ANCHOR), (ANCHOR.x, ANCHOR.y, ANCHOR.z + 0.1), "body"),
        "cyl": (tuple(ANCHOR), tuple(ANCHOR + (BED_PT - ANCHOR).normalized() * CYL_LEN), "body"),
        "rod": (tuple(BED_PT), tuple(BED_PT + (ANCHOR - BED_PT).normalized() * CYL_LEN), "bed_pt"),
    }


def make_mesh():
    bm = bmesh.new()
    parts = {}
    parts["body"] = box(bm, (0, -0.2, 0.35), (0.9, 2.2, 0.3)) + box(bm, (0, 0.75, 0.75), (0.9, 0.9, 0.5))
    parts["bed"] = box(bm, (0, -0.4, 0.6), (0.9, 1.2, 0.08))
    for n, (x, y) in WHEELS.items():
        parts[n] = wheel(bm, x, y)
    parts["cyl"] = capsule(bm, ANCHOR, ANCHOR + (BED_PT - ANCHOR).normalized() * CYL_LEN, 0.05)
    parts["rod"] = capsule(bm, BED_PT, BED_PT + (ANCHOR - BED_PT).normalized() * CYL_LEN, 0.03)
    idx = {k: [v.index for v in vs] for k, vs in parts.items()}
    me = bpy.data.meshes.new("ME_Truck")
    bm.to_mesh(me)
    bm.free()
    ob = bpy.data.objects.new("GEO_Truck", me)
    bpy.context.scene.collection.objects.link(ob)
    for k, ids in idx.items():
        g = ob.vertex_groups.new(name=k)
        g.add(ids, 1.0, "REPLACE")
    return ob


def make(kind):
    for o in list(bpy.data.objects):
        bpy.data.objects.remove(o, do_unlink=True)
    for a in list(bpy.data.armatures):
        bpy.data.armatures.remove(a)
    L.reset("SC_TRUCK")
    geo = make_mesh()
    arm = bpy.data.armatures.new("ARM_Truck")
    rig = bpy.data.objects.new("RIG_Truck", arm)
    bpy.context.scene.collection.objects.link(rig)
    bpy.context.view_layer.objects.active = rig
    rig.select_set(True)
    bpy.ops.object.mode_set(mode="EDIT")
    E = arm.edit_bones
    for n, (h, t, p) in bones_def().items():
        b = E.new(n)
        b.head, b.tail = Vector(h), Vector(t)
        if p and not (kind == "unparented_wheels" and n.startswith("wheel_")):
            b.parent = E[p]
    bpy.ops.object.mode_set(mode="POSE")
    pb = rig.pose.bones
    for n in WHEELS:
        pb[n].rotation_mode = "XYZ"
    if kind != "starter":
        radius = 0.15 if kind == "wrong_radius" else 0.3
        axis = 0 if kind == "wrong_axis" else 1
        if kind not in ("no_drivers",):
            for n in WHEELS:
                fc = rig.driver_add(f'pose.bones["{n}"].rotation_euler', axis)
                d = fc.driver
                d.type = "SCRIPTED"
                d.expression = f"-d / {radius}"
                v = d.variables.new()
                v.name = "d"
                v.type = "TRANSFORMS"
                v.targets[0].id = rig
                v.targets[0].bone_target = "root"
                v.targets[0].transform_type = "LOC_Y"
                v.targets[0].transform_space = "LOCAL_SPACE"
        if kind != "no_track":
            c = pb["cyl"].constraints.new("DAMPED_TRACK")
            c.target, c.subtarget = rig, "bed_pt"
            c = pb["rod"].constraints.new("DAMPED_TRACK")
            c.target, c.subtarget = rig, "anchor"
        if kind != "no_limit":
            c = pb["bed"].constraints.new("LIMIT_ROTATION")
            c.use_limit_x = True
            c.min_x, c.max_x = 0.0, math.radians(45)
            c.use_limit_y = c.use_limit_z = True
            c.min_y = c.max_y = c.min_z = c.max_z = 0.0
            c.owner_space = "LOCAL"
    bpy.ops.object.mode_set(mode="OBJECT")
    m = geo.modifiers.new("Armature", "ARMATURE")
    m.object = rig
    geo.parent = rig
    rig.show_in_front = True
    L.instructions(NOTE)
    return geo, rig


def sketch(geo, rig, path):
    W, H = 420, 300
    tiles = []
    pb = rig.pose.bones
    setups = [(0.0, 0.0), (0.5, 0.0), (0.0, 35.0)]
    for fwd, lift in setups:
        pb["root"].location = Vector((0, fwd, 0))
        pb["bed"].rotation_mode = "XYZ"
        pb["bed"].rotation_euler = (math.radians(lift), 0, 0)
        bpy.context.view_layer.update()
        dg = bpy.context.evaluated_depsgraph_get()
        ev = geo.evaluated_get(dg)
        me = ev.to_mesh()
        V = np.array([v.co[:] for v in me.vertices])
        edges = [e.vertices[:] for e in me.edges]
        ev.to_mesh_clear()
        img = np.full((H, W, 3), 0.08, np.float32)

        def px(y, z):
            return int(W / 2 + y * 105), int(H - 40 - z * 105)

        def line(a, b, col):
            x0, y0 = px(*a); x1, y1 = px(*b)
            n = max(abs(x1 - x0), abs(y1 - y0)) + 1
            for k in range(n + 1):
                x, y = int(x0 + (x1 - x0) * k / n), int(y0 + (y1 - y0) * k / n)
                if 0 <= x < W and 0 <= y < H:
                    img[y, x] = col
        for a, b in edges:
            line((V[a][1], V[a][2]), (V[b][1], V[b][2]), (0.4, 0.4, 0.45))
        evr = rig.evaluated_get(dg)
        for n in ("root", "body", "bed", "cyl", "rod"):
            b = evr.pose.bones[n]
            h, t = evr.matrix_world @ b.head, evr.matrix_world @ b.tail
            line((h.y, h.z), (t.y, t.z), (0.95, 0.6, 0.15) if n in ("cyl", "rod") else (0.3, 0.7, 1.0))
        line((-2, 0), (2, 0), (0.3, 0.3, 0.3))
        tiles.append(img)
    pb["root"].location = (0, 0, 0)
    pb["bed"].rotation_euler = (0, 0, 0)
    sheet = np.concatenate(tiles, axis=1)
    rgba = np.concatenate([sheet, np.ones(sheet.shape[:2] + (1,), np.float32)], axis=2)
    out = bpy.data.images.new("sk", sheet.shape[1], H)
    out.pixels = rgba[::-1].ravel()
    out.filepath_raw = path
    out.file_format = "PNG"
    out.save()


def main():
    out = os.path.join(CH, "COMPLETED_EXAMPLES")
    make("starter")
    L.save(os.path.join(CH, "STARTER_FILES", "ch06_07_truck_starter.blend"))
    for k in ("no_drivers", "wrong_radius", "wrong_axis", "unparented_wheels", "no_track", "no_limit"):
        make(k)
        L.save(os.path.join(out, "COUNTER_EXAMPLES", f"ch06_07_truck_{k}.blend"))
    geo, rig = make("solution")
    L.save(os.path.join(out, "ch06_07_truck_solution.blend"))
    sketch(geo, rig, os.path.join(out, "ch06_07_truck_reference.png"))


if __name__ == "__main__":
    L.run(main)
