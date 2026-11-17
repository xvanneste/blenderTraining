"""
build_ch07_07_files.py — « Posing et silhouette » (CH07.07 : ligne d'action, contrapposto, silhouette lisible).

Un mannequin FK simple : CHR_Mannequin (capsules et ellipsoïdes rigides, un groupe de sommets par bone) et son armature RIG_Mannequin (vue de face : le mannequin regarde −Y, X vers sa gauche) :
  hips (z 0,95–1,05), spine (0,95 → 1,25), chest (1,25 → 1,45), neck (1,45 → 1,55), head (1,55 → 1,75) ; thigh.L/.R (hanche à x = ±0,10, z 0,95 → 0,52), shin.L/.R (0,52 → cheville à z 0,05) ;
  upper_arm.L/.R (épaule à x = ±0,20, z 1,40 → coude à ±0,50), fore.L/.R (coude → poignet à x = ±0,75). Starter : T-pose droite et symétrique (pose de repos).
  Solution (posée par script, pivots au point d'attache de chaque bone, rotations dans le repère MONDE) :
    hips +8° autour de Y (bascule des hanches), spine −4°, chest −14° (cumul : −10° : les épaules basculent à l'opposé des hanches : CONTRAPPOSTO), neck et head −4° ;
    jambe d'appui : droite, tendue (la hanche droite est la plus haute) ; jambe libre : gauche, genou fléchi de 28° (le pied part en arrière) ; les cuisses compensent la bascule des hanches (jambes verticales) ;
    bras : gauche abaissé de 35° (autour de Y), avant-bras fléchi de 25° ; droit levé de 40°, avant-bras fléchi de −30°.
  STARTER_FILES/ch07_07_posing_starter.blend (T-pose) ; COMPLETED_EXAMPLES/ch07_07_posing_solution.blend (+ _reference.png : silhouettes de face, de la T-pose et de la pose)
  COUNTER_EXAMPLES/ : no_tilt, twin_tilt, both_bent, unbalanced, no_curve, arms_at_sides
Usage : blender -b --factory-startup --python-exit-code 1 --python build_ch07_07_files.py
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
NOTE = """CH07.07 — POSING ET SILHOUETTE (CHR_Mannequin, RIG_Mannequin)
Le mannequin est en T-pose : droit, symétrique, bras tendus : une pose sans vie. Posez-le (Pose Mode, rotations des bones) pour obtenir une pose lisible de face :
1. CONTRAPPOSTO : les hanches basculent d'un côté, les épaules de l'autre (lignes des épaules et des hanches inclinées en sens opposés, chacune de 4° à 20°).
2. APPUI : une jambe porte le poids (tendue, cheville au sol, sous les hanches : écart horizontal ≤ 10 cm) ; l'autre est relâchée (genou plié d'au moins 15°, pied au-dessus du sol ou en arrière).
3. LIGNE D'ACTION : la colonne forme une courbe en C (angle entre spine → chest et chest → head de 8° à 40°).
4. SILHOUETTE : les bras se détachent du corps : la silhouette (rendu Workbench à plat, de face) a une solidité (aire / aire de l'enveloppe convexe) inférieure à 0,70.
Le correcteur mesure ces quatre points sur la pose enregistrée (positions des bones et rendu réel de la silhouette).
Vérification : SCRIPTS/validate_ch07_07.py -- --exercise posing
"""


def make_rig(name="RIG_Mannequin"):
    arm = bpy.data.armatures.new("ARM_Mannequin")
    rig = bpy.data.objects.new(name, arm)
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


def rotate_world(rig, name, axis, deg):
    """Tourne le bone `name` (avec ses enfants) autour de l'axe MONDE, pivot = sa tête dans la pose courante."""
    pb = rig.pose.bones[name]
    bpy.context.view_layer.update()
    h = Vector(pb.head)
    M = Matrix.Translation(h) @ Matrix.Rotation(math.radians(deg), 4, axis) @ Matrix.Translation(-h)
    pb.matrix = M @ pb.matrix
    bpy.context.view_layer.update()


def pose(rig, kind):
    if kind == "starter":
        return
    hips, spine, chest = {"no_tilt": (0, 0, 0), "twin_tilt": (8, 0, 0), "no_curve": (8, -18, 0)}.get(kind, (8, -4, -14))
    rotate_world(rig, "hips", "Y", hips)
    for n in ("thigh.L", "thigh.R"):                          # les jambes restent verticales malgré la bascule des hanches
        rotate_world(rig, n, "Y", -hips)
    rotate_world(rig, "spine", "Y", spine)
    rotate_world(rig, "chest", "Y", chest)
    if kind != "no_curve":
        rotate_world(rig, "neck", "Y", -4)
        rotate_world(rig, "head", "Y", -4)
    rotate_world(rig, "shin.L", "X", 28)                      # jambe LIBRE : genou fléchi, le pied part en arrière
    if kind == "both_bent":
        rotate_world(rig, "shin.R", "X", 28)
    if kind == "unbalanced":
        rotate_world(rig, "thigh.R", "Y", 25)                 # la jambe d'appui s'écarte : le poids n'est plus sous les hanches
    if kind == "arms_at_sides":
        rotate_world(rig, "upper_arm.L", "Y", 82)
        rotate_world(rig, "upper_arm.R", "Y", -82)
    else:
        rotate_world(rig, "upper_arm.L", "Y", 35)
        rotate_world(rig, "fore.L", "Y", 25)
        rotate_world(rig, "upper_arm.R", "Y", 40)
        rotate_world(rig, "fore.R", "Y", -30)


def build(kind):
    L.reset("SC_POSING")
    L.studio(subject_height=1.76)
    body = make_body()
    rig = make_rig()
    m = body.modifiers.new("Armature", "ARMATURE")
    m.object = rig
    body.parent = rig
    for n in rig.pose.bones.keys():
        rig.pose.bones[n].rotation_mode = "XYZ"
    pose(rig, kind)
    L.instructions(NOTE)
    return body, rig


def silhouette(body, rig, path=None, w=240, h=360):
    """Silhouette réelle : rendu Workbench à plat, de face (caméra orthographique)."""
    sc = bpy.context.scene
    cam_d = bpy.data.cameras.new("CAM_Sil")
    cam_d.type = "ORTHO"
    cam_d.ortho_scale = 2.4
    cam = bpy.data.objects.new("CAM_Sil", cam_d)
    sc.collection.objects.link(cam)
    cam.location = (0, -6, 1.0)
    cam.rotation_euler = (math.radians(90), 0, 0)
    old = (sc.camera, sc.render.engine, sc.render.resolution_x, sc.render.resolution_y, sc.render.film_transparent)
    sc.camera = cam
    sc.render.engine = "BLENDER_WORKBENCH"
    sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage = w, h, 100
    sc.render.film_transparent = False
    sh = sc.display.shading
    sh.light, sh.color_type, sh.single_color = "FLAT", "SINGLE", (1, 1, 1)
    sh.background_type = "VIEWPORT"
    sh.background_color = (0, 0, 0)
    vis = {o: o.hide_render for o in bpy.data.objects}
    for o in bpy.data.objects:
        o.hide_render = o not in (body,)
    sc.render.filepath = path or os.path.join(bpy.app.tempdir, "sil.png")
    sc.render.image_settings.file_format = "PNG"
    sc.render.image_settings.color_mode = "RGB"
    bpy.ops.render.render(write_still=True)
    img = bpy.data.images.load(sc.render.filepath)
    px = np.array(img.pixels[:], np.float32).reshape(img.size[1], img.size[0], 4)[..., 0]
    bpy.data.images.remove(img)
    for o, v in vis.items():
        o.hide_render = v
    sc.camera, sc.render.engine, sc.render.resolution_x, sc.render.resolution_y, sc.render.film_transparent = old
    bpy.data.objects.remove(cam)
    return px > 0.5


def solidity(mask):
    ys, xs = np.nonzero(mask)
    pts = sorted(set(zip(xs.tolist(), ys.tolist())))
    if len(pts) < 3:
        return 1.0

    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    lo, up = [], []
    for p in pts:
        while len(lo) >= 2 and cross(lo[-2], lo[-1], p) <= 0:
            lo.pop()
        lo.append(p)
    for p in reversed(pts):
        while len(up) >= 2 and cross(up[-2], up[-1], p) <= 0:
            up.pop()
        up.append(p)
    hull = lo[:-1] + up[:-1]
    area = 0.0
    for i in range(len(hull)):
        x0, y0 = hull[i]
        x1, y1 = hull[(i + 1) % len(hull)]
        area += x0 * y1 - x1 * y0
    return float(mask.sum()) / max(abs(area) / 2, 1.0)


def sketch(path):
    body, rig = build("starter")
    m0 = silhouette(body, rig)
    body, rig = build("solution")
    m1 = silhouette(body, rig)
    img = np.concatenate([m0, np.zeros((m0.shape[0], 20), bool), m1], axis=1).astype(np.float32)
    rgba = np.stack([img, img, img, np.ones_like(img)], axis=2)
    out = bpy.data.images.new("sk", img.shape[1], img.shape[0])
    out.pixels = rgba.ravel()                      # le rendu est déjà en lignes de bas en haut
    out.filepath_raw = path
    out.file_format = "PNG"
    out.save()
    print(f"[sil] solidité T-pose {solidity(m0):.3f}, pose {solidity(m1):.3f}")


def main():
    out = os.path.join(CH, "COMPLETED_EXAMPLES")
    build("starter")
    L.save(os.path.join(CH, "STARTER_FILES", "ch07_07_posing_starter.blend"))
    for k in ("no_tilt", "twin_tilt", "both_bent", "unbalanced", "no_curve", "arms_at_sides"):
        b, r = build(k)
        print(f"[sil] {k} : solidité {solidity(silhouette(b, r)):.3f}")
        L.save(os.path.join(out, "COUNTER_EXAMPLES", f"ch07_07_posing_{k}.blend"))
    build("solution")
    L.save(os.path.join(out, "ch07_07_posing_solution.blend"))
    sketch(os.path.join(out, "ch07_07_posing_reference.png"))


if __name__ == "__main__":
    L.run(main)
