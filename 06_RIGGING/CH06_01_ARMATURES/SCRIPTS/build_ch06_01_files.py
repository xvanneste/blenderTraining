"""
build_ch06_01_files.py — « Armatures et bones » (CH06.01).

Une armature humanoïde simple RIG_Hero (données ARM_Hero) de 1,76 m, pose en A, à la taille du mannequin de CH03.10 :
  Axe : root · pelvis · spine.001 · spine.002 · spine.003 · neck · head
  Bras (× 2, suffixes .L / .R) : shoulder · upper_arm · forearm · hand      Jambes (× 2) : thigh · shin · foot · toe
  Hiérarchie : root > pelvis > spine.001 > spine.002 > spine.003 > neck > head ; spine.003 > shoulder.* > upper_arm.* > forearm.* > hand.* ; pelvis > thigh.* > shin.* > foot.* > toe.*
  Chaînes connectées (use_connect) : colonne, cou, tête, bras (forearm, hand), jambes (shin, foot, toe) ; épaules et cuisses NON connectées.
  Symétrie : les bones .R sont l'image miroir (X → −X) des bones .L ; roll nul ; root ne déforme pas (use_deform = False), tous les autres si.
  STARTER_FILES/ch06_01_armature_starter.blend : une armature SALE (noms « Bone.001 », pas de côté droit, bras non parenté, jambe décalée) + le mannequin en référence (REF_Body).
  COMPLETED_EXAMPLES/ch06_01_armature_solution.blend (+ _reference.png : croquis de face et de profil)
  COUNTER_EXAMPLES/ : missing_right, bad_names, asymmetric, unparented, disconnected, pose_dirty, deform_root
Usage : blender -b --factory-startup --python-exit-code 1 --python build_ch06_01_files.py
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
SRC = os.path.join(HERE, "..", "..", "..", "03_SCULPTING", "CH03_10_RIG_READY", "COMPLETED_EXAMPLES", "ch03_10_char_solution.blend")
NOTE = """CH06.01 — ARMATURES ET BONES (RIG_Hero, données ARM_Hero) : construire le squelette du mannequin REF_Body (1,76 m, pose en A, face à −Y)
Bones à créer (Edit Mode) : root, pelvis, spine.001/.002/.003, neck, head ; pour chaque côté (.L à +X, .R à −X) : shoulder, upper_arm, forearm, hand, thigh, shin, foot, toe.
Hiérarchie : root > pelvis > spine.001 > spine.002 > spine.003 > neck > head ; spine.003 > shoulder > upper_arm > forearm > hand ; pelvis > thigh > shin > foot > toe.
Connexions (Connected) : colonne, cou, tête, forearm, hand, shin, foot, toe ; PAS pour shoulder et thigh. Symétrie exacte (X → −X) ; roll 0 ; root ne déforme pas, les autres déforment.
Objet : échelle 1, rotation 0, position (0, 0, 0) ; pose de repos propre (aucune transformation en Pose Mode).
Vérification : SCRIPTS/validate_ch06_01.py -- --exercise armature
"""
# nom : (tête, queue, parent, connecté)
AXIS = {
    "root": ((0, 0, 0), (0, 0.2, 0), None, False),
    "pelvis": ((0, 0, 0.95), (0, 0, 1.05), "root", False),
    "spine.001": ((0, 0, 1.05), (0, 0, 1.18), "pelvis", True),
    "spine.002": ((0, 0, 1.18), (0, 0, 1.32), "spine.001", True),
    "spine.003": ((0, 0, 1.32), (0, 0, 1.45), "spine.002", True),
    "neck": ((0, 0, 1.45), (0, 0, 1.58), "spine.003", True),
    "head": ((0, 0, 1.58), (0, 0, 1.76), "neck", True),
}
D = (math.sin(math.radians(40)), 0.0, -math.cos(math.radians(40)))     # direction du bras (A, 40° de la verticale)
SH = (0.17, 0.0, 1.42)
UA = tuple(SH[i] + 0.30 * D[i] for i in range(3))
FA = tuple(UA[i] + 0.27 * D[i] for i in range(3))
HA = tuple(FA[i] + 0.10 * D[i] for i in range(3))
SIDE = {   # pour .L (x > 0)
    "shoulder": ((0.03, 0, 1.42), SH, "spine.003", False),
    "upper_arm": (SH, UA, "shoulder", True),
    "forearm": (UA, FA, "upper_arm", True),
    "hand": (FA, HA, "forearm", True),
    "thigh": ((0.09, 0, 0.95), (0.09, 0, 0.52), "pelvis", False),
    "shin": ((0.09, 0, 0.52), (0.09, 0, 0.09), "thigh", True),
    "foot": ((0.09, 0, 0.09), (0.09, -0.18, 0.0), "shin", True),
    "toe": ((0.09, -0.18, 0.0), (0.09, -0.26, 0.0), "foot", True),
}


def spec(kind):
    sp = dict(AXIS)
    for side, sx in ((".L", 1), (".R", -1)):
        for n, (h, t, par, conn) in SIDE.items():
            if kind == "missing_right" and side == ".R" and n in ("shoulder", "upper_arm", "forearm", "hand"):
                continue
            hh = (h[0] * sx, h[1], h[2])
            tt = (t[0] * sx, t[1], t[2])
            sp[n + side] = (hh, tt, par if par in AXIS else par + side, conn)
    return sp


def make_armature(kind):
    bpy.ops.object.select_all(action="DESELECT")
    arm = bpy.data.armatures.new("ARM_Hero")
    ob = bpy.data.objects.new("RIG_Hero", arm)
    bpy.context.scene.collection.objects.link(ob)
    bpy.context.view_layer.objects.active = ob
    ob.select_set(True)
    bpy.ops.object.mode_set(mode="EDIT")
    sp = spec(kind)
    eb = {}
    for n, (h, t, par, conn) in sp.items():
        name = n
        if kind == "bad_names":
            name = {"spine.002": "Bone.003", "forearm.L": "Bone", "shin.R": "Bone.001"}.get(n, n)
        b = arm.edit_bones.new(name)
        if kind == "asymmetric" and n == "shoulder.L":          # épaule non connectée : son décalage n'est pas « réparé » par la connexion
            h = (h[0] + 0.05, h[1], h[2] + 0.03)
        b.head, b.tail = Vector(h), Vector(t)
        b.roll = 0.0
        eb[n] = b
    for n, (h, t, par, conn) in sp.items():
        if par is None:
            continue
        if kind == "unparented" and n == "hand.L":
            continue
        b = eb[n]
        b.parent = eb[par]
        b.use_connect = conn and not (kind == "disconnected" and n == "spine.002")
    for n, b in eb.items():
        b.use_deform = (n != "root") if kind != "deform_root" else True
    bpy.ops.object.mode_set(mode="OBJECT")
    if kind == "pose_dirty":
        pb = ob.pose.bones["upper_arm.L"]
        pb.rotation_mode = "XYZ"
        pb.rotation_euler = (0.0, 0.0, 0.6)
        ob.pose.bones["head"].location = (0.0, 0.0, 0.05)
    return ob


def make_messy():
    """Armature SALE du fichier de départ."""
    arm = bpy.data.armatures.new("Armature")
    ob = bpy.data.objects.new("Armature", arm)
    bpy.context.scene.collection.objects.link(ob)
    bpy.context.view_layer.objects.active = ob
    ob.select_set(True)
    bpy.ops.object.mode_set(mode="EDIT")
    rows = [("Bone", (0, 0, 0.95), (0, 0, 1.2)), ("Bone.001", (0, 0, 1.2), (0, 0, 1.45)), ("Bone.002", (0, 0, 1.45), (0, 0, 1.76)),
            ("Bone.003", (0.17, 0, 1.42), (0.36, 0, 1.19)), ("Bone.004", (0.36, 0, 1.19), (0.54, 0, 0.98)),
            ("Bone.005", (0.1, 0, 0.95), (0.1, 0, 0.5)), ("Bone.006", (0.1, 0, 0.5), (0.12, 0, 0.0))]
    for n, h, t in rows:
        b = arm.edit_bones.new(n)
        b.head, b.tail = Vector(h), Vector(t)
    bpy.ops.object.mode_set(mode="OBJECT")
    ob.scale = (1.0, 1.0, 1.0)
    return ob


def reference_body():
    with bpy.data.libraries.load(os.path.abspath(SRC)) as (src, dst):
        dst.objects = ["CHR_Hero_Body"]
    ob = dst.objects[0]
    ob.name = "REF_Body"
    ob.data.name = "ME_REF_Body"
    ob.parent = None
    bpy.context.scene.collection.objects.link(ob)
    ob.display_type = "WIRE"
    ob.hide_select = True
    return ob


def sketch(ob, ref, path):
    """Croquis de face (x, z) et de profil (y, z) : sommets du mannequin en gris, bones en couleur."""
    W, H = 400, 600
    img = np.zeros((H, 2 * W, 4), np.float32)
    img[..., :3] = 0.10
    img[..., 3] = 1.0
    V = np.array([v.co[:] for v in ref.data.vertices])[::6]

    def to_px(x, z, off):
        return int(off + W / 2 + x * 190), int(H - 20 - z * 300)
    for off, ax in ((0, 0), (W, 1)):
        for v in V:
            px, py = to_px(v[ax], v[2], off)
            if 0 <= px < 2 * W and 0 <= py < H:
                img[py, px, :3] = 0.35
        for b in ob.data.bones:
            h, t = b.head_local, b.tail_local
            x0, y0 = to_px(h[ax], h[2], off)
            x1, y1 = to_px(t[ax], t[2], off)
            col = (0.95, 0.55, 0.15) if b.name.endswith(".L") else ((0.3, 0.7, 1.0) if b.name.endswith(".R") else (0.9, 0.9, 0.3))
            n = max(abs(x1 - x0), abs(y1 - y0)) + 1
            for k in range(n + 1):
                px, py = int(x0 + (x1 - x0) * k / n), int(y0 + (y1 - y0) * k / n)
                if 0 <= px < 2 * W and 0 <= py < H:
                    img[max(py - 1, 0):py + 2, max(px - 1, 0):px + 2, :3] = col
    out = bpy.data.images.new("sk", 2 * W, H)
    out.pixels = img[::-1].ravel()          # l'origine d'une image Blender est en bas
    out.filepath_raw = path
    out.file_format = "PNG"
    out.save()


def build(kind):
    L.reset("SC_ARM")
    L.studio(subject_height=1.76)
    ref = reference_body()
    ob = make_messy() if kind == "starter" else make_armature(kind)
    ob.show_in_front = True
    ob.data.display_type = "OCTAHEDRAL"
    L.instructions(NOTE)
    return ob, ref


def main():
    out = os.path.join(CH, "COMPLETED_EXAMPLES")
    build("starter")
    L.save(os.path.join(CH, "STARTER_FILES", "ch06_01_armature_starter.blend"))
    for k in ("missing_right", "bad_names", "asymmetric", "unparented", "disconnected", "pose_dirty", "deform_root"):
        build(k)
        L.save(os.path.join(out, "COUNTER_EXAMPLES", f"ch06_01_armature_{k}.blend"))
    ob, ref = build("solution")
    L.save(os.path.join(out, "ch06_01_armature_solution.blend"))
    sketch(ob, ref, os.path.join(out, "ch06_01_armature_reference.png"))


if __name__ == "__main__":
    L.run(main)
