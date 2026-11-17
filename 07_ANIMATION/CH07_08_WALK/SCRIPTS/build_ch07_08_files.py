"""
build_ch07_08_files.py — « Cycles de marche » (CH07.08 : contact, descente, passage, montée ; marche sur place en 24 images).

Le mannequin FK de CH07.07 (CHR_Mannequin, RIG_Mannequin ; 13 bones) marche SUR PLACE : le sol défile sous ses pieds. Cycle de 24 images (clés 1 à 25, l'image 25 reprend l'image 1), 24 i/s, plage 1–25.
  Solution (calculée par script, IK analytique à deux segments dans le plan Y–Z ; le genou plie vers l'avant, −Y) :
    longueur de pas S = 0,60 m ; jambe = cuisse 0,43 m + jambe 0,47 m ; cheville à 0,05 m du sol.
    pied gauche (phase t = (f − 1)/24) : appui de 0 à 0,5 (la cheville recule de y = −0,30 à +0,30 à vitesse constante, au sol) ; ballant de 0,5 à 1 (retour de +0,30 à −0,30, levée de 0,12 m en sinus) ; pied droit : décalé d'un DEMI-cycle (12 images).
    hanches : z = 0,05 + √(0,90² − y_appui²) (le point le plus bas aux contacts : 0,899 m ; le plus haut au passage : 0,95 m) ; bras : abaissés de 82° autour de Y puis balancement ±20° autour de X, à l'OPPOSÉ de la jambe du même côté.
  Poses clés lisibles : CONTACT (image 1), DESCENTE (4), PASSAGE (7), MONTÉE (10) puis les mêmes de l'autre côté (13, 16, 19, 22).
  STARTER_FILES/ch07_08_walk_starter.blend : mannequin en T-pose, bras abaissés, sans animation. COMPLETED_EXAMPLES/ch07_08_walk_solution.blend (+ _reference.png : huit images du cycle, de profil)
  COUNTER_EXAMPLES/ : no_loop, uneven_stance, no_bob, same_side_arm, shuffle, short_stride
Usage : blender -b --factory-startup --python-exit-code 1 --python build_ch07_08_files.py
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
BONES = {
    "hips": ((0, 0, 0.95), (0, 0, 1.05), None), "spine": ((0, 0, 0.95), (0, 0, 1.25), "hips"), "chest": ((0, 0, 1.25), (0, 0, 1.45), "spine"), "neck": ((0, 0, 1.45), (0, 0, 1.55), "chest"), "head": ((0, 0, 1.55), (0, 0, 1.75), "neck"),
    "thigh.L": ((0.10, 0, 0.95), (0.10, 0, 0.52), "hips"), "shin.L": ((0.10, 0, 0.52), (0.10, 0, 0.05), "thigh.L"),
    "thigh.R": ((-0.10, 0, 0.95), (-0.10, 0, 0.52), "hips"), "shin.R": ((-0.10, 0, 0.52), (-0.10, 0, 0.05), "thigh.R"),
    "upper_arm.L": ((0.20, 0, 1.40), (0.50, 0, 1.40), "chest"), "fore.L": ((0.50, 0, 1.40), (0.75, 0, 1.40), "upper_arm.L"),
    "upper_arm.R": ((-0.20, 0, 1.40), (-0.50, 0, 1.40), "chest"), "fore.R": ((-0.50, 0, 1.40), (-0.75, 0, 1.40), "upper_arm.R"),
}
RAD = {"hips": 0.15, "spine": 0.14, "chest": 0.16, "neck": 0.05, "head": 0.10, "thigh": 0.075, "shin": 0.055, "upper_arm": 0.05, "fore": 0.04}
L1, L2, ANK = 0.43, 0.47, 0.05
NOTE = """CH07.08 — CYCLES DE MARCHE (CHR_Mannequin, RIG_Mannequin)
Le mannequin doit marcher SUR PLACE (le sol défile) : un cycle de 24 images, clés de l'image 1 à l'image 25 (l'image 25 = l'image 1), 24 images par seconde, plage 1–25.
Les quatre poses d'un pas : CONTACT (le talon touche, jambes écartées de 0,6 m), DESCENTE (le corps s'abaisse sur la jambe d'appui), PASSAGE (la jambe libre passe sous le corps ; hanches au plus haut), MONTÉE (la jambe d'appui pousse). Images 1, 4, 7, 10 puis 13, 16, 19, 22 de l'autre côté.
Règles : pied d'appui AU SOL et qui recule à vitesse constante (0,05 m/image : pas de glissement) ; pied libre levé d'au moins 6 cm ; hanches qui montent et descendent de 3 à 8 cm (plus bas aux contacts) ; bras opposés aux jambes ; l'image 25 reprend exactement l'image 1.
Le correcteur mesure les chevilles, les hanches et les poignets sur les 25 images.
Vérification : SCRIPTS/validate_ch07_08.py -- --exercise walk
"""


def make_rig():
    arm = bpy.data.armatures.new("ARM_Mannequin")
    rig = bpy.data.objects.new("RIG_Mannequin", arm)
    bpy.context.scene.collection.objects.link(rig)
    bpy.context.view_layer.objects.active = rig
    rig.select_set(True)
    bpy.ops.object.mode_set(mode="EDIT")
    for n, (h, t, p) in BONES.items():
        b = arm.edit_bones.new(n)
        b.head, b.tail = Vector(h), Vector(t)
    for n, (h, t, p) in BONES.items():
        if p:
            arm.edit_bones[n].parent = arm.edit_bones[p]
    bpy.ops.object.mode_set(mode="OBJECT")
    rig.show_in_front = True
    return rig


def capsule(bm, a, b, r):
    d = b - a
    ret = bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=14, radius1=r, radius2=r, depth=d.length)
    rot = Vector((0, 0, 1)).rotation_difference(d.normalized()).to_matrix().to_4x4()
    for v in ret["verts"]:
        v.co = rot @ v.co + (a + b) / 2
    return ret["verts"]


def make_body():
    bm = bmesh.new()
    parts = {}
    for n, (h, t, p) in BONES.items():
        base = n.split(".")[0]
        if n == "head":
            ret = bmesh.ops.create_uvsphere(bm, u_segments=20, v_segments=12, radius=RAD["head"])
            for v in ret["verts"]:
                v.co = v.co * Vector((1, 1, 1.15)) + Vector((0, 0, 1.65))
            parts[n] = list(ret["verts"])
        elif n == "chest":
            parts[n] = capsule(bm, Vector((0, 0, 1.30)), Vector((0, 0, 1.42)), RAD["chest"])
        elif n == "hips":
            parts[n] = capsule(bm, Vector((0, 0, 0.96)), Vector((0, 0, 1.04)), RAD["hips"])
        else:
            parts[n] = capsule(bm, Vector(h), Vector(t), RAD[base])
    idx = {n: [v.index for v in vs] for n, vs in parts.items()}
    me = bpy.data.meshes.new("ME_Mannequin")
    bm.to_mesh(me)
    bm.free()
    ob = bpy.data.objects.new("CHR_Mannequin", me)
    bpy.context.scene.collection.objects.link(ob)
    for p in me.polygons:
        p.use_smooth = True
    for n, ids in idx.items():
        g = ob.vertex_groups.new(name=n)
        g.add(ids, 1.0, "REPLACE")
    return ob


def set_dir(pb, head, direction):
    """Oriente le bone (rotation la plus courte depuis sa direction de repos) avec sa tête en `head` (espace armature)."""
    rest = pb.bone.matrix_local.to_3x3()
    rest_dir = (rest @ Vector((0, 1, 0))).normalized()
    R = rest_dir.rotation_difference(Vector(direction).normalized()).to_matrix()
    pb.matrix = Matrix.Translation(head) @ (R @ rest).to_4x4()


def leg_ik(hip, ankle):
    """Genou d'une chaîne à deux segments dans le plan Y–Z (x fixe), genou vers l'avant (−Y)."""
    d = Vector((0, ankle.y - hip.y, ankle.z - hip.z))
    D = min(d.length, L1 + L2 - 1e-6)
    u = d.normalized()
    a = math.acos(max(-1, min(1, (L1 * L1 + D * D - L2 * L2) / (2 * L1 * D))))
    best = None
    for s in (1, -1):
        c, sn = math.cos(s * a), math.sin(s * a)
        v = Vector((0, u.y * c - u.z * sn, u.y * sn + u.z * c))
        k = Vector((hip.x, hip.y, hip.z)) + v * L1
        if best is None or k.y < best.y:
            best = k
    return best


def walk_params(kind):
    S = 0.20 if kind == "short_stride" else 0.60
    H = 0.0 if kind == "shuffle" else 0.12
    period = 26.0 if kind == "no_loop" else 24.0
    return S, H, period


def foot_path(phi, S, H, kind):
    if phi < 0.5:                                                   # appui : la cheville recule
        u = phi / 0.5
        if kind == "uneven_stance":
            u = u * u
        return -S / 2 + S * u, 0.0
    u = (phi - 0.5) / 0.5                                          # ballant
    return S / 2 - S * u, H * math.sin(math.pi * u)


def pose_frame(rig, f, kind):
    S, H, period = walk_params(kind)
    t = ((f - 1) / period)
    pb = rig.pose.bones
    stance_y = {}
    ank = {}
    for side, ph in (("L", t % 1.0), ("R", (t + 0.5) % 1.0)):
        y, z = foot_path(ph, S, H, kind)
        ank[side] = Vector((0.10 if side == "L" else -0.10, y, ANK + z))
        stance_y[side] = y if ph < 0.5 else None
    ys = [v for v in stance_y.values() if v is not None]
    ref = ys[0] if ys else 0.0
    zh = 0.90 if kind == "no_bob" else ANK + math.sqrt(0.90 ** 2 - ref ** 2)
    pb["hips"].matrix = Matrix.Translation((0, 0, zh - 0.95)) @ pb["hips"].bone.matrix_local
    bpy.context.view_layer.update()
    for side in ("L", "R"):
        hip = Vector((ank[side].x, 0, zh))
        knee = leg_ik(hip, ank[side])
        set_dir(pb["thigh." + side], hip, knee - hip)
        bpy.context.view_layer.update()
        set_dir(pb["shin." + side], knee, ank[side] - knee)
        bpy.context.view_layer.update()
    # bras : abaissés de 82° autour de Y, balancement ±20° autour de X à l'opposé (ou du même côté) de la jambe
    sw = 20.0 * math.cos(2 * math.pi * t)
    for side, sign in (("L", 1), ("R", -1)):
        pa, pf = pb["upper_arm." + side], pb["fore." + side]
        amp = sw if side == "L" else -sw
        if kind == "same_side_arm":
            amp = -amp
        sh = pa.bone.head_local
        shoulder = Vector(sh)
        shoulder.z += 0.0
        arm_dir = Vector((0.0, 0.0, -1.0))
        ang = math.radians(amp)
        arm_dir = Vector((0.0, math.sin(ang), -math.cos(ang)))
        set_dir(pa, shoulder, arm_dir)
        bpy.context.view_layer.update()
        elbow = Vector(pa.tail)
        set_dir(pf, elbow, arm_dir)
        bpy.context.view_layer.update()


def build(kind):
    L.reset("SC_WALK")
    sc = bpy.context.scene
    sc.render.fps = 24
    sc.frame_start, sc.frame_end = 1, 25
    body = make_body()
    rig = make_rig()
    m = body.modifiers.new("Armature", "ARMATURE")
    m.object = rig
    body.parent = rig
    for n in rig.pose.bones.keys():
        rig.pose.bones[n].rotation_mode = "XYZ"
    if kind == "starter":
        for side in ("L", "R"):                                   # bras abaissés (82°) dans le starter
            sgn = 1 if side == "L" else -1
            pa = rig.pose.bones["upper_arm." + side]
            set_dir(pa, Vector(pa.bone.head_local), Vector((0, 0, -1)))
            bpy.context.view_layer.update()
            pf = rig.pose.bones["fore." + side]
            set_dir(pf, Vector(pa.tail), Vector((0, 0, -1)))
            bpy.context.view_layer.update()
    else:
        for f in range(1, 26):
            pose_frame(rig, f, kind)
            for n in rig.pose.bones.keys():
                pb = rig.pose.bones[n]
                pb.keyframe_insert("rotation_euler", frame=f)
                if n == "hips":
                    pb.keyframe_insert("location", frame=f)
        sc.frame_set(1)
    L.instructions(NOTE)
    return body, rig


def sketch(path):
    body, rig = build("solution")
    sc = bpy.context.scene
    frames = (1, 4, 7, 10, 13, 16, 19, 22)
    W, H = 100, 260
    img = np.full((H, W * len(frames), 3), 0.08, np.float32)

    def line(a, b, col, th=2):
        x0, y0, x1, y1 = a[0], a[1], b[0], b[1]
        n = int(max(abs(x1 - x0), abs(y1 - y0))) + 1
        for k in range(n + 1):
            x, y = int(x0 + (x1 - x0) * k / n), int(y0 + (y1 - y0) * k / n)
            if th <= x < img.shape[1] - th and th <= y < H - th:
                img[y - th + 1:y + th, x - th + 1:x + th] = col
    for i, f in enumerate(frames):
        sc.frame_set(f)
        bpy.context.view_layer.update()

        def px(p):
            return (W * i + W / 2 - p.y * 120, H - 15 - p.z * 125)
        line((W * i + 5, H - 15 + 6), (W * (i + 1) - 5, H - 15 + 6), (0.3, 0.3, 0.3), 1)
        for n in ("spine", "chest", "neck", "head", "hips"):
            b = rig.pose.bones[n]
            line(px(b.head), px(b.tail), (0.75, 0.75, 0.75))
        for side, col in (("L", (0.9, 0.55, 0.2)), ("R", (0.3, 0.7, 1.0))):
            for n in ("thigh.", "shin.", "upper_arm.", "fore."):
                b = rig.pose.bones[n + side]
                line(px(b.head), px(b.tail), col)
    rgba = np.concatenate([img, np.ones(img.shape[:2] + (1,), np.float32)], axis=2)
    out = bpy.data.images.new("sk", img.shape[1], H)
    out.pixels = rgba[::-1].ravel()
    out.filepath_raw = path
    out.file_format = "PNG"
    out.save()


def table():
    body, rig = build("solution")
    sc = bpy.context.scene
    for f in (1, 4, 7, 10):
        sc.frame_set(f)
        bpy.context.view_layer.update()
        pb = rig.pose.bones
        a = pb["shin.L"].tail
        print(f"[walk] image {f} : cheville G y={a.y:+.3f} z={a.z:.3f} ; D y={pb['shin.R'].tail.y:+.3f} z={pb['shin.R'].tail.z:.3f} ; hanches z={pb['hips'].head.z:.3f}")


def main():
    out = os.path.join(CH, "COMPLETED_EXAMPLES")
    build("starter")
    L.save(os.path.join(CH, "STARTER_FILES", "ch07_08_walk_starter.blend"))
    for k in ("no_loop", "uneven_stance", "no_bob", "same_side_arm", "shuffle", "short_stride"):
        build(k)
        L.save(os.path.join(out, "COUNTER_EXAMPLES", f"ch07_08_walk_{k}.blend"))
    table()
    build("solution")
    L.save(os.path.join(out, "ch07_08_walk_solution.blend"))
    sketch(os.path.join(out, "ch07_08_walk_reference.png"))


if __name__ == "__main__":
    L.run(main)
