"""
build_ch06_10_files.py — « Contrôleurs et ergonomie » (CH06.10 : formes personnalisées, collections de bones, couleurs, verrous, déformation séparée).

Le rig RIG_Ctl (vue de face, bras en T) sépare trois familles de bones :
  Déformation (DEF-spine, DEF-arm.L, DEF-arm.R : use_deform) — suivent les contrôleurs par Copy Transforms (World → World) ;
  Contrôleurs (root, ctl_spine, ctl_arm.L, ctl_arm.R : jamais de déformation) — ce que touche l'animateur ;
  Mécanisme (MCH-pivot : parent de ctl_spine, ne se touche jamais).
  Solution : (1) trois collections de bones « Controls », « Deform », « Mechanism » ; Deform et Mechanism MASQUÉES ; (2) une forme personnalisée (objet WGT_*) sur chaque contrôleur, objets rangés dans une collection WIDGETS masquée ;
             (3) couleurs : root = THEME09, centre (ctl_spine) = THEME03, gauche = THEME04, droite = THEME01 (palettes de Blender) ; (4) verrous : ctl_arm.* ne bougent qu'en rotation (location et scale verrouillés), ctl_spine : scale verrouillé.
  STARTER_FILES/ch06_10_controls_starter.blend : rig fonctionnel, mais bones sans collection, sans forme, sans couleur, sans verrou.
  COMPLETED_EXAMPLES/ch06_10_controls_solution.blend (+ _reference.png : formes personnalisées colorées en projection oblique, bones DEF en gris)
  COUNTER_EXAMPLES/ : no_collections, not_hidden, no_shapes, no_colors, no_locks, broken_link, deform_flags
Usage : blender -b --factory-startup --python-exit-code 1 --python build_ch06_10_files.py
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
BONES = {
    # nom : (tête, queue, parent, famille)
    "MCH-pivot": ((0, 0, 0.90), (0, 0, 0.95), None, "mch"),
    "root": ((0, 0, 0.0), (0, 0, 0.25), None, "ctl"),
    "ctl_spine": ((0, 0, 0.90), (0, 0, 1.40), "MCH-pivot", "ctl"),
    "ctl_arm.L": ((0.2, 0, 1.35), (0.6, 0, 1.35), "ctl_spine", "ctl"),
    "ctl_arm.R": ((-0.2, 0, 1.35), (-0.6, 0, 1.35), "ctl_spine", "ctl"),
    "DEF-spine": ((0, 0, 0.90), (0, 0, 1.40), None, "def"),
    "DEF-arm.L": ((0.2, 0, 1.35), (0.6, 0, 1.35), "DEF-spine", "def"),
    "DEF-arm.R": ((-0.2, 0, 1.35), (-0.6, 0, 1.35), "DEF-spine", "def"),
}
FOLLOW = {"DEF-spine": "ctl_spine", "DEF-arm.L": "ctl_arm.L", "DEF-arm.R": "ctl_arm.R"}
COLORS = {"root": "THEME09", "ctl_spine": "THEME03", "ctl_arm.L": "THEME04", "ctl_arm.R": "THEME01"}
SHAPES = {"root": "WGT_circle", "ctl_spine": "WGT_box", "ctl_arm.L": "WGT_circle", "ctl_arm.R": "WGT_circle"}
NOTE = """CH06.10 — CONTRÔLEURS ET ERGONOMIE (RIG_Ctl)
Le rig fonctionne mais il est illisible : toutes les familles de bones sont mélangées, sans formes ni couleurs.
1. Bone collections (Armature properties > Bone Collections) : « Controls » (root, ctl_*), « Deform » (DEF-*), « Mechanism » (MCH-*) ; masquez Deform et Mechanism.
2. Formes personnalisées : créez les objets WGT_circle et WGT_box (maillages en fil de fer, rangés dans une collection WIDGETS masquée) ; Bone properties > Viewport Display > Custom Shape sur chaque contrôleur.
3. Couleurs : Bone properties > Bone Color : root THEME09, ctl_spine THEME03, gauche (.L) THEME04, droite (.R) THEME01.
4. Verrous : ctl_arm.L/.R : verrouiller Location et Scale (rotation seule) ; ctl_spine : verrouiller Scale.
5. Les bones de contrôle ne doivent pas déformer (use_deform décoché) ; les DEF-* oui.
Le correcteur vérifie la structure ET que le rig fonctionne encore : tourner ctl_arm.L de 30° fait tourner DEF-arm.L de 30°, sans toucher au bras droit.
Vérification : SCRIPTS/validate_ch06_10.py -- --exercise controls
"""


def wire(name, pts, edges):
    me = bpy.data.meshes.new(name)
    me.from_pydata([Vector(p) for p in pts], edges, [])
    ob = bpy.data.objects.new(name, me)
    return ob


def make_widgets():
    wc = bpy.data.collections.new("WIDGETS")
    bpy.context.scene.collection.children.link(wc)
    n = 24
    circle = wire("WGT_circle", [(0.5 * math.cos(2 * math.pi * k / n), 0.0, 0.5 * math.sin(2 * math.pi * k / n)) for k in range(n)], [(k, (k + 1) % n) for k in range(n)])
    c = [(-0.5, 0.0, -0.5), (0.5, 0.0, -0.5), (0.5, 0.0, 0.5), (-0.5, 0.0, 0.5)]
    box = wire("WGT_box", [(x, y, z) for y in (-0.5, 0.5) for (x, _, z) in c], [(0, 1), (1, 2), (2, 3), (3, 0), (4, 5), (5, 6), (6, 7), (7, 4), (0, 4), (1, 5), (2, 6), (3, 7)])
    for o in (circle, box):
        wc.objects.link(o)
    wc.hide_viewport = True
    wc.hide_render = True
    return {"WGT_circle": circle, "WGT_box": box}


def build(kind):
    for o in list(bpy.data.objects):
        bpy.data.objects.remove(o, do_unlink=True)
    for c in list(bpy.data.collections):
        bpy.data.collections.remove(c)
    for a in list(bpy.data.armatures):
        bpy.data.armatures.remove(a)
    L.reset("SC_CTL")
    arm = bpy.data.armatures.new("ARM_Ctl")
    rig = bpy.data.objects.new("RIG_Ctl", arm)
    bpy.context.scene.collection.objects.link(rig)
    bpy.context.view_layer.objects.active = rig
    rig.select_set(True)
    bpy.ops.object.mode_set(mode="EDIT")
    E = arm.edit_bones
    for n, (h, t, p, fam) in BONES.items():
        b = E.new(n)
        b.head, b.tail = Vector(h), Vector(t)
        b.use_deform = fam == "def" or (kind == "deform_flags" and fam == "ctl")
    for n, (h, t, p, fam) in BONES.items():
        if p:
            E[n].parent = E[p]
    bpy.ops.object.mode_set(mode="POSE")
    for dn, cn in FOLLOW.items():
        if kind != "broken_link":
            c = rig.pose.bones[dn].constraints.new("COPY_TRANSFORMS")
            c.target, c.subtarget = rig, cn
            c.target_space = c.owner_space = "WORLD"
    for n in ("ctl_spine", "ctl_arm.L", "ctl_arm.R", "root"):
        rig.pose.bones[n].rotation_mode = "XYZ"
    bpy.ops.object.mode_set(mode="OBJECT")
    if kind != "starter":
        if kind not in ("no_collections",):
            fam_of = {n: v[3] for n, v in BONES.items()}
            cols = {f: arm.collections.new(nm) for f, nm in (("ctl", "Controls"), ("def", "Deform"), ("mch", "Mechanism"))}
            for n, fam in fam_of.items():
                cols[fam].assign(arm.bones[n])
            if kind != "not_hidden":
                cols["def"].is_visible = False
                cols["mch"].is_visible = False
        if kind != "no_shapes":
            wg = make_widgets()
            for n, s in SHAPES.items():
                rig.pose.bones[n].custom_shape = wg[s]
        if kind != "no_colors":
            for n, pal in COLORS.items():
                rig.pose.bones[n].color.palette = pal
        if kind != "no_locks":
            for n in ("ctl_arm.L", "ctl_arm.R"):
                rig.pose.bones[n].lock_location = (True, True, True)
                rig.pose.bones[n].lock_scale = (True, True, True)
            rig.pose.bones["ctl_spine"].lock_scale = (True, True, True)
    rig.show_in_front = True
    L.instructions(NOTE)
    return rig


PAL = {"THEME01": (0.9, 0.25, 0.25), "THEME03": (0.95, 0.85, 0.2), "THEME04": (0.25, 0.7, 0.95), "THEME09": (0.85, 0.5, 0.95)}


def sketch(rig, path):
    W, H = 420, 380
    img = np.full((H, W, 3), 0.08, np.float32)

    def px(p):
        return int(W / 2 + (p[0] + 0.55 * p[1]) * 250), int(H - 30 - (p[2] + 0.35 * p[1]) * 200)     # projection oblique : les anneaux autour des bones restent lisibles

    def line(a, b, col, th=1):
        x0, y0 = px(a); x1, y1 = px(b)
        n = max(abs(x1 - x0), abs(y1 - y0)) + 1
        for k in range(n + 1):
            x, y = int(x0 + (x1 - x0) * k / n), int(y0 + (y1 - y0) * k / n)
            if th <= x < W - th and th <= y < H - th:
                img[y - th + 1:y + th, x - th + 1:x + th] = col
    for n in ("DEF-spine", "DEF-arm.L", "DEF-arm.R"):
        b = rig.data.bones[n]
        line(b.head_local, b.tail_local, (0.45, 0.45, 0.45), 3)
    for n, s in SHAPES.items():
        pb = rig.pose.bones[n]
        wgt = pb.custom_shape
        length = pb.bone.length
        M = rig.matrix_world @ pb.matrix
        col = PAL[COLORS[n]]
        vs = [M @ (Vector(v.co) * length) for v in wgt.data.vertices]
        for e in wgt.data.edges:
            line(vs[e.vertices[0]], vs[e.vertices[1]], col, 2)
        line(pb.head, pb.tail, col, 1)
    rgba = np.concatenate([img, np.ones(img.shape[:2] + (1,), np.float32)], axis=2)
    out = bpy.data.images.new("sk", W, H)
    out.pixels = rgba[::-1].ravel()
    out.filepath_raw = path
    out.file_format = "PNG"
    out.save()


def main():
    out = os.path.join(CH, "COMPLETED_EXAMPLES")
    build("starter")
    L.save(os.path.join(CH, "STARTER_FILES", "ch06_10_controls_starter.blend"))
    for k in ("no_collections", "not_hidden", "no_shapes", "no_colors", "no_locks", "broken_link", "deform_flags"):
        build(k)
        L.save(os.path.join(out, "COUNTER_EXAMPLES", f"ch06_10_controls_{k}.blend"))
    rig = build("solution")
    L.save(os.path.join(out, "ch06_10_controls_solution.blend"))
    sketch(rig, os.path.join(out, "ch06_10_controls_reference.png"))


if __name__ == "__main__":
    L.run(main)
