"""
build_ch06_09_files.py — « Rig facial » (CH06.09 : mâchoire par bone, sourire et clignement par shape keys, contrôleurs à glissière).

Une tête simple GEO_Face (sphère de rayon 0,12 m, 32 segments × 16 anneaux, visage vers −Y, centrée à l'origine) et son armature RIG_Face :
  head (0,0,−0,10 → 0,15), jaw (charnière (0 ; 0,06 ; −0,02) → (0 ; −0,04 ; −0,02), enfant de head), ctl_smile et ctl_blink (glissières à (±0,25 ; 0 ; 0,05), bones verticaux, mobiles en X de 0 à 0,05 m).
  Peau : groupes « head » et « jaw » ; poids de jaw = smoothstep((0,04 − z)/0,14) (0 au-dessus de z = 0,04, 1 sous z = −0,10).
  Shape keys relatifs à Basis : « smile » (coins de la bouche à (±0,045 ; −0,1056 ; −0,04), montée de 12 mm, rayon d'influence 35 mm, poids normalisés : le sommet le plus proche du centre pèse 1) et « blink » (paupières à (±0,04 ; −0,1086 ; 0,03), descente de 12 mm, rayon 25 mm).
  Drivers : smile.value = loc_x(ctl_smile) / 0,05 ; blink.value = loc_x(ctl_blink) / 0,05 (Transform Channel, Location X, Local Space).
  Contraintes : Limit Location sur chaque glissière (X de 0 à 0,05 m ; Y et Z bloqués), repère Local.
  Jaw : rotation X ; le sens est CALIBRÉ par le script (le menton descend).
  STARTER_FILES/ch06_09_facial_starter.blend : tête, armature et groupes de peau SANS shape keys, driver ni limite.
  COMPLETED_EXAMPLES/ch06_09_facial_solution.blend (+ _reference.png : profil repos/mâchoire ouverte, face repos/sourire + clignement)
  COUNTER_EXAMPLES/ : no_drivers, crosstalk, no_limit, weak_driver, no_jaw_weights, jaw_rigid
Usage : blender -b --factory-startup --python-exit-code 1 --python build_ch06_09_files.py
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
R = 0.12
SLIDE = 0.05
CORNER = ((0.045, -0.1056, -0.04), (-0.045, -0.1056, -0.04))
EYE = ((0.04, -0.1086, 0.03), (-0.04, -0.1086, 0.03))
NOTE = """CH06.09 — RIG FACIAL (GEO_Face, RIG_Face)
1. Mâchoire : bone jaw (enfant de head) avec les groupes de sommets « head » et « jaw » : déjà faits. Tournez jaw (Pose Mode, rotation X) : le menton descend, le haut de la tête ne bouge pas.
2. Shape keys : sur GEO_Face, Basis puis « smile » (coins de la bouche vers le haut, 12 mm) et « blink » (paupières vers le bas, 12 mm), chacun limité à sa zone par un groupe de sommets (smile_zone, blink_zone).
3. Glissières : bones ctl_smile et ctl_blink ; Limit Location (X de 0 à 0,05 m, Y et Z à 0, Local Space) ; drivers : valeur du shape key = Location X de la glissière / 0,05.
Le correcteur ouvre la mâchoire (15°), déplace chaque glissière (0,025 puis 0,05 puis 0,20 m) et mesure les sommets : chaque commande n'agit que sur SA zone.
Vérification : SCRIPTS/validate_ch06_09.py -- --exercise facial
"""


def smooth(w):
    w = max(0.0, min(1.0, w))
    return w * w * (3 - 2 * w)


def make_head():
    bm = bmesh.new()
    bmesh.ops.create_uvsphere(bm, u_segments=32, v_segments=16, radius=R)
    me = bpy.data.meshes.new("ME_Face")
    bm.to_mesh(me)
    bm.free()
    # create_uvsphere : pôles sur Z ; le visage regarde −Y (la sphère est symétrique, le visage est défini par les zones)
    ob = bpy.data.objects.new("GEO_Face", me)
    bpy.context.scene.collection.objects.link(ob)
    for p in me.polygons:
        p.use_smooth = True
    return ob


def make_rig():
    arm = bpy.data.armatures.new("ARM_Face")
    ob = bpy.data.objects.new("RIG_Face", arm)
    bpy.context.scene.collection.objects.link(ob)
    bpy.context.view_layer.objects.active = ob
    for o in bpy.data.objects:
        o.select_set(False)
    ob.select_set(True)
    bpy.ops.object.mode_set(mode="EDIT")
    E = arm.edit_bones
    h = E.new("head"); h.head, h.tail = Vector((0, 0, -0.10)), Vector((0, 0, 0.15))
    j = E.new("jaw"); j.head, j.tail = Vector((0, 0.06, -0.02)), Vector((0, -0.04, -0.02)); j.parent = h
    for n, x in (("ctl_smile", 0.25), ("ctl_blink", -0.25)):
        c = E.new(n); c.head, c.tail = Vector((x, 0, 0.05)), Vector((x, 0, 0.10))
    bpy.ops.object.mode_set(mode="POSE")
    for n in ("jaw", "ctl_smile", "ctl_blink"):
        ob.pose.bones[n].rotation_mode = "XYZ"
    bpy.ops.object.mode_set(mode="OBJECT")
    ob.show_in_front = True
    return ob


def skin(face, rig, rigid=False, no_jaw=False):
    gh, gj = face.vertex_groups.new(name="head"), face.vertex_groups.new(name="jaw")
    for v in face.data.vertices:
        z = v.co.z
        if no_jaw:
            wj = 0.0
        elif rigid:
            wj = 1.0 if z < -0.03 else 0.0
        else:
            wj = smooth((0.04 - z) / 0.14)
        gh.add([v.index], 1.0 - wj, "REPLACE")
        if wj > 0:
            gj.add([v.index], wj, "REPLACE")
    m = face.modifiers.new("Armature", "ARMATURE")
    m.object = rig
    face.parent = rig


def zone_weights(face, name, centers, radius):
    g = face.vertex_groups.new(name=name)
    raw = {v.index: max(0.0, 1.0 - min((v.co - Vector(c)).length for c in centers) / radius) for v in face.data.vertices}
    top = max(raw.values())                                  # normalisé : le sommet le plus proche d'un centre pèse 1 (il se déplace de la valeur exacte)
    wts = {i: w / top for i, w in raw.items()}
    for i, w in wts.items():
        if w > 0:
            g.add([i], w, "REPLACE")
    return wts


def add_keys(face, kind):
    face.shape_key_add(name="Basis", from_mix=False)
    zones = {"smile": (CORNER, 0.035, 0.012), "blink": (EYE, 0.025, -0.012)}
    out = {}
    for name, (centers, rad, dz) in zones.items():
        wts = zone_weights(face, f"{name}_zone", centers, rad)
        sk = face.shape_key_add(name=name, from_mix=False)
        sk.slider_min, sk.slider_max = 0.0, 1.0
        for i, v in enumerate(face.data.vertices):
            w = wts[i]
            sk.data[i].co = v.co + Vector((0, 0, dz * w))
        sk.vertex_group = f"{name}_zone"
        out[name] = sk
    if kind == "crosstalk":                                  # le sourire fait aussi bouger les paupières (le key « smile » contient l'abaissement des yeux)
        raw = {v.index: max(0.0, 1.0 - min((v.co - Vector(c)).length for c in EYE) / 0.025) for v in face.data.vertices}
        wts = {i: w / max(raw.values()) for i, w in raw.items()}
        for i, v in enumerate(face.data.vertices):
            out["smile"].data[i].co = out["smile"].data[i].co + Vector((0, 0, -0.012 * wts[i]))
        out["smile"].vertex_group = ""
    return out


def add_driver(face, rig, key, ctl, div):
    fc = face.data.shape_keys.driver_add(f'key_blocks["{key}"].value')
    d = fc.driver
    d.type = "SCRIPTED"
    d.expression = f"x / {div}"
    v = d.variables.new()
    v.name = "x"
    v.type = "TRANSFORMS"
    v.targets[0].id = rig
    v.targets[0].bone_target = ctl
    v.targets[0].transform_type = "LOC_X"
    v.targets[0].transform_space = "LOCAL_SPACE"


JAW_SIGN = 1.0


def build(kind):
    L.reset("SC_FACE")
    face = make_head()
    rig = make_rig()
    if kind != "none":
        skin(face, rig, rigid=(kind == "jaw_rigid"), no_jaw=(kind == "no_jaw_weights"))
    if kind not in ("starter", "none"):
        add_keys(face, kind)
        div = 0.1 if kind == "weak_driver" else SLIDE
        if kind != "no_drivers":
            add_driver(face, rig, "smile", "ctl_smile", div)
            add_driver(face, rig, "blink", "ctl_blink", div)
        if kind != "no_limit":
            bpy.context.view_layer.objects.active = rig
            bpy.ops.object.mode_set(mode="POSE")
            for n in ("ctl_smile", "ctl_blink"):
                c = rig.pose.bones[n].constraints.new("LIMIT_LOCATION")
                c.use_min_x = c.use_max_x = c.use_min_y = c.use_max_y = c.use_min_z = c.use_max_z = True
                c.min_x, c.max_x = 0.0, SLIDE
                c.min_y = c.max_y = c.min_z = c.max_z = 0.0
                c.owner_space = "LOCAL"
            bpy.ops.object.mode_set(mode="OBJECT")
    L.instructions(NOTE)
    return face, rig


def coords(ob):
    bpy.context.view_layer.update()
    ev = ob.evaluated_get(bpy.context.evaluated_depsgraph_get())
    me = ev.to_mesh()
    co = np.array([v.co[:] for v in me.vertices])
    ev.to_mesh_clear()
    return co


def calibrate_jaw():
    global JAW_SIGN
    face, rig = build("starter")
    rest = np.array([v.co[:] for v in face.data.vertices])
    chin = int(np.argmin(rest[:, 2] + rest[:, 1] + 0.001 * np.abs(rest[:, 0])))            # menton : devant et en bas
    for s in (1.0, -1.0):
        rig.pose.bones["jaw"].rotation_euler = (math.radians(15) * s, 0, 0)
        co = coords(face)
        print(f"[calib] jaw sens {s:+.0f} : menton dz {co[chin][2] - rest[chin][2]:+.3f}")
        if co[chin][2] - rest[chin][2] < -0.02:
            JAW_SIGN = s
            break
    rig.pose.bones["jaw"].rotation_euler = (0, 0, 0)
    for k in ("solution", "jaw_rigid"):
        face, rig = build(k)
        rest = np.array([v.co[:] for v in face.data.vertices])
        rig.pose.bones["jaw"].rotation_euler = (math.radians(15) * JAW_SIGN, 0, 0)
        co = coords(face)
        st = 0.0
        for e in face.data.edges:
            a, b = e.vertices
            st = max(st, np.linalg.norm(co[a] - co[b]) / np.linalg.norm(rest[a] - rest[b]))
        print(f"[calib] {k} : étirement d'arête max {st:.2f}")
    return JAW_SIGN


def sketch(face, rig, path):
    W = 320
    img = np.full((W, 4 * W, 3), 0.08, np.float32)
    pb = rig.pose.bones

    def draw(panel, co, axes, col):
        for e in face.data.edges:
            a, b = co[e.vertices[0]], co[e.vertices[1]]
            x0, y0 = panel * W + W / 2 + a[axes[0]] * axes[2], W / 2 - a[2] * axes[2] if axes[1] == 2 else 0
            x0, y0 = panel * W + W / 2 + a[axes[0]] * 900 * axes[3], W / 2 - a[2] * 900
            x1, y1 = panel * W + W / 2 + b[axes[0]] * 900 * axes[3], W / 2 - b[2] * 900
            n = int(max(abs(x1 - x0), abs(y1 - y0))) + 1
            for k in range(n + 1):
                x, y = int(x0 + (x1 - x0) * k / n), int(y0 + (y1 - y0) * k / n)
                if 0 <= x < 4 * W and 0 <= y < W:
                    img[y, x] = col
    # axes = (axe horizontal, axe vertical, _, signe) : profil = y (avant à gauche : signe +1 pour −y affiché), face = x
    rest = coords(face)
    draw(0, rest, (1, 2, 0, 1), (0.9, 0.55, 0.2))                         # profil repos : avant (−Y) à gauche
    pb["jaw"].rotation_euler = (math.radians(15) * JAW_SIGN, 0, 0)
    draw(1, coords(face), (1, 2, 0, 1), (0.3, 0.8, 0.5))
    pb["jaw"].rotation_euler = (0, 0, 0)
    draw(2, rest, (0, 2, 0, 1), (0.9, 0.55, 0.2))                         # face repos
    pb["ctl_smile"].location = Vector((SLIDE, 0, 0))
    pb["ctl_blink"].location = Vector((SLIDE, 0, 0))
    draw(3, coords(face), (0, 2, 0, 1), (0.3, 0.8, 0.5))
    pb["ctl_smile"].location = (0, 0, 0)
    pb["ctl_blink"].location = (0, 0, 0)
    rgba = np.concatenate([img, np.ones(img.shape[:2] + (1,), np.float32)], axis=2)
    out = bpy.data.images.new("sk", 4 * W, W)
    out.pixels = rgba[::-1].ravel()
    out.filepath_raw = path
    out.file_format = "PNG"
    out.save()


def main():
    out = os.path.join(CH, "COMPLETED_EXAMPLES")
    calibrate_jaw()
    print("[calib] JAW_SIGN", JAW_SIGN)
    build("starter")
    L.save(os.path.join(CH, "STARTER_FILES", "ch06_09_facial_starter.blend"))
    for k in ("no_drivers", "crosstalk", "no_limit", "weak_driver", "no_jaw_weights", "jaw_rigid"):
        build(k)
        L.save(os.path.join(out, "COUNTER_EXAMPLES", f"ch06_09_facial_{k}.blend"))
    face, rig = build("solution")
    L.save(os.path.join(out, "ch06_09_facial_solution.blend"))
    sketch(face, rig, os.path.join(out, "ch06_09_facial_reference.png"))


if __name__ == "__main__":
    L.run(main)
