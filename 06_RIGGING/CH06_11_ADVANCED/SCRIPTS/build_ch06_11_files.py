"""
build_ch06_11_files.py — « Rigging avancé et réutilisation » (CH06.11 : bendy bones, bibliothèque de rig, link et override).

VOLET A — BENDY BONES. Un tube GEO_Tube (1 m le long de Z, rayon 5 cm, 41 anneaux de 12 sommets) lié par le groupe « spine » (poids 1) à RIG_Tube (un bone « spine » de 1 m).
  Solution : Bendy Bones : bbone_segments = 8 (le bone se découpe en 8 segments qui déforment le tube) ; modificateur Armature actif ; spine déformant.
  Le correcteur courbe le bone (Curve In X = Curve Out X = 0,3) et mesure la courbe du tube.
  STARTER_FILES/ch06_11_bendy_starter.blend (1 segment : le bone est rigide) ; COMPLETED_EXAMPLES/ch06_11_bendy_solution.blend (+ _reference.png : tube droit puis courbé, 1 segment contre 8)
  COUNTER_EXAMPLES/ : bendy_segments_1 (identique au starter), bendy_few_segments (2), bendy_no_modifier, bendy_no_deform

VOLET B — BIBLIOTHÈQUE ET OVERRIDE. STARTER_FILES/ch06_11_rig_library.blend : la BIBLIOTHÈQUE (collection COL_Rig : RIG_Lib, un bone « arm » de 0,6 m le long de X à z = 1, et GEO_Lib, un tube pesé sur arm).
  Le PLAN (shot) lie COL_Rig depuis la bibliothèque (chemin RELATIF) et crée un library override ÉDITABLE (override_hierarchy_create(..., do_fully_editable=True)) ; le rig est placé dans le plan (location (2, 0, 0)),
  et sa pose est posée par un keyframe (arm tourné de 30° autour de Z à l'image 1) : en 5.3, seules les poses portées par une Action persistent dans l'override.
  STARTER_FILES/ch06_11_shot_starter.blend (plan vide) ; COMPLETED_EXAMPLES/ch06_11_shot_solution.blend ; COUNTER_EXAMPLES/ : shot_linked_only, shot_appended, shot_absolute_path, shot_not_posed
Usage : blender -b --factory-startup --python-exit-code 1 --python build_ch06_11_files.py
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
LIB = os.path.join(CH, "STARTER_FILES", "ch06_11_rig_library.blend")
N_RING, N_SEG = 41, 12
NOTE_A = """CH06.11 — VOLET A : BENDY BONES (GEO_Tube, RIG_Tube)
Le bone « spine » est rigide : le tube ne peut que pivoter. Armature properties (ou Bone properties) > Bendy Bones : Segments = 8. Le bone peut alors se courber (Curve In X / Curve Out X dans Bone properties > Bendy Bones).
Le correcteur règle Curve In X = Curve Out X = 0,3 et mesure l'arche du tube : milieu décalé d'au moins 15 cm, extrémités fixes, courbe lisse (aucun virage de plus de 8° entre deux anneaux consécutifs).
Vérification : SCRIPTS/validate_ch06_11.py -- --exercise bendy
"""
NOTE_B = """CH06.11 — VOLET B : BIBLIOTHÈQUE ET OVERRIDE (plan)
1. File > Link : choisissez ch06_11_rig_library.blend (même dossier que ce plan), Collection > COL_Rig. Le chemin doit rester RELATIF (Relative Path coché).
2. Ajoutez la collection liée à la scène, puis créez un Library Override ÉDITABLE (Object > Library Override > Make > Selected & Content ; en Python : override_hierarchy_create(scene, view_layer, do_fully_editable=True)).
3. Placez le rig dans le plan (location à plus d'1 m de l'origine) ; en Pose Mode, tournez le bone arm de 30° autour de Z et insérez un keyframe (rotation) à l'image 1.
Le correcteur vérifie : une seule bibliothèque à chemin relatif et valide ; RIG_Lib et GEO_Lib sont des OVERRIDES éditables (ni un lien nu, ni une copie locale) ; la pose est portée par une Action et déforme le tube à l'image 1 ; le rig est placé.
Vérification : SCRIPTS/validate_ch06_11.py -- --exercise override
"""


# ---------------------------------------------------------------- volet A
def make_tube(name="GEO_Tube", length=1.0, axis="Z", radius=0.05, n_ring=N_RING):
    bm = bmesh.new()
    rings = []
    for i in range(n_ring):
        t = length * i / (n_ring - 1)
        ring = []
        for k in range(N_SEG):
            a = 2 * math.pi * k / N_SEG
            p = (radius * math.cos(a), radius * math.sin(a), t) if axis == "Z" else (t, radius * math.cos(a), 1.0 + radius * math.sin(a))
            ring.append(bm.verts.new(p))
        rings.append(ring)
    for i in range(n_ring - 1):
        for k in range(N_SEG):
            bm.faces.new((rings[i][k], rings[i][(k + 1) % N_SEG], rings[i + 1][(k + 1) % N_SEG], rings[i + 1][k]))
    me = bpy.data.meshes.new("ME_" + name)
    bm.to_mesh(me)
    bm.free()
    ob = bpy.data.objects.new(name, me)
    for p in me.polygons:
        p.use_smooth = True
    return ob


def make_bone(name_rig, bone, head, tail):
    arm = bpy.data.armatures.new("ARM_" + name_rig)
    rig = bpy.data.objects.new(name_rig, arm)
    bpy.context.scene.collection.objects.link(rig)
    bpy.context.view_layer.objects.active = rig
    for o in bpy.data.objects:
        o.select_set(False)
    rig.select_set(True)
    bpy.ops.object.mode_set(mode="EDIT")
    b = arm.edit_bones.new(bone)
    b.head, b.tail = Vector(head), Vector(tail)
    bpy.ops.object.mode_set(mode="OBJECT")
    rig.show_in_front = True
    return rig


def bind(geo, rig, group):
    g = geo.vertex_groups.new(name=group)
    g.add(list(range(len(geo.data.vertices))), 1.0, "REPLACE")
    m = geo.modifiers.new("Armature", "ARMATURE")
    m.object = rig
    geo.parent = rig
    return m


def build_bendy(kind):
    L.reset("SC_BENDY")
    geo = make_tube()
    bpy.context.scene.collection.objects.link(geo)
    rig = make_bone("RIG_Tube", "spine", (0, 0, 0), (0, 0, 1))
    m = bind(geo, rig, "spine")
    rig.data.bones["spine"].bbone_segments = {"starter": 1, "segments_1": 1, "few_segments": 2}.get(kind, 8)
    if kind == "no_modifier":
        geo.modifiers.remove(m)
    if kind == "no_deform":
        rig.data.bones["spine"].use_deform = False
    L.instructions(NOTE_A)
    return geo, rig


def tube_coords(geo):
    bpy.context.view_layer.update()
    ev = geo.evaluated_get(bpy.context.evaluated_depsgraph_get())
    me = ev.to_mesh()
    co = np.array([v.co[:] for v in me.vertices])
    ev.to_mesh_clear()
    return co


def sketch_bendy(path):
    W, H = 320, 340
    img = np.full((H, 4 * W, 3), 0.08, np.float32)
    for panel, (seg, curve) in enumerate(((1, 0.0), (8, 0.0), (1, 0.3), (8, 0.3))):
        geo, rig = build_bendy("solution")
        rig.data.bones["spine"].bbone_segments = seg
        pb = rig.pose.bones["spine"]
        pb.bbone_curveinx = pb.bbone_curveoutx = curve
        co = tube_coords(geo)
        for e in geo.data.edges:
            a, b = co[e.vertices[0]], co[e.vertices[1]]
            x0, y0 = panel * W + 90 + a[0] * 250, H - 20 - a[2] * 280
            x1, y1 = panel * W + 90 + b[0] * 250, H - 20 - b[2] * 280
            n = int(max(abs(x1 - x0), abs(y1 - y0))) + 1
            for k in range(n + 1):
                x, y = int(x0 + (x1 - x0) * k / n), int(y0 + (y1 - y0) * k / n)
                if 0 <= x < 4 * W and 0 <= y < H:
                    img[y, x] = (0.9, 0.55, 0.2) if seg == 1 else (0.3, 0.8, 0.5)
    rgba = np.concatenate([img, np.ones(img.shape[:2] + (1,), np.float32)], axis=2)
    out = bpy.data.images.new("sk", 4 * W, H)
    out.pixels = rgba[::-1].ravel()
    out.filepath_raw = path
    out.file_format = "PNG"
    out.save()


# ---------------------------------------------------------------- volet B
def build_library():
    L.reset("SC_LIB")
    col = bpy.data.collections.new("COL_Rig")
    bpy.context.scene.collection.children.link(col)
    geo = make_tube("GEO_Lib", length=0.6, axis="X", n_ring=13)
    col.objects.link(geo)
    rig = make_bone("RIG_Lib", "arm", (0, 0, 1), (0.6, 0, 1))
    bpy.context.scene.collection.objects.unlink(rig)
    col.objects.link(rig)
    bind(geo, rig, "arm")
    rig.pose.bones["arm"].rotation_mode = "XYZ"
    L.instructions("CH06.11 — BIBLIOTHÈQUE de rig : collection COL_Rig (RIG_Lib, GEO_Lib). À LIER (File > Link), pas à ouvrir : voir le volet B du chapitre.")
    L.save(LIB)


def build_shot(kind):
    L.reset("SC_SHOT")
    L.instructions(NOTE_B)
    if kind == "starter":
        return
    absolute = kind == "absolute_path"
    with bpy.data.libraries.load(LIB, link=(kind != "appended"), relative=not absolute) as (df, dt):
        dt.collections = ["COL_Rig"]
    coll = dt.collections[0]
    bpy.context.scene.collection.children.link(coll)
    if kind in ("linked_only", "appended"):
        return
    ov = coll.override_hierarchy_create(bpy.context.scene, bpy.context.view_layer, do_fully_editable=True)
    rig = bpy.data.objects["RIG_Lib"]
    rig.location = (2.0, 0.0, 0.0)
    if kind != "not_posed":
        pb = rig.pose.bones["arm"]
        pb.rotation_mode = "XYZ"
        pb.rotation_euler = (0, 0, math.radians(30))
        pb.keyframe_insert("rotation_euler", index=2, frame=1)
    bpy.context.scene.frame_set(1)


def save_shot(path, absolute=False):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    bpy.context.preferences.filepaths.save_version = 0
    bpy.ops.wm.save_as_mainfile(filepath=path, compress=True, relative_remap=not absolute)
    print(f"[BCMA] saved {path}")


def main():
    out = os.path.join(CH, "COMPLETED_EXAMPLES")
    cx = os.path.join(out, "COUNTER_EXAMPLES")
    build_bendy("starter")
    L.save(os.path.join(CH, "STARTER_FILES", "ch06_11_bendy_starter.blend"))
    for k in ("segments_1", "few_segments", "no_modifier", "no_deform"):
        build_bendy(k)
        L.save(os.path.join(cx, f"ch06_11_bendy_{k}.blend"))
    build_bendy("solution")
    L.save(os.path.join(out, "ch06_11_bendy_solution.blend"))
    sketch_bendy(os.path.join(out, "ch06_11_bendy_reference.png"))
    build_library()
    build_shot("starter")
    L.save(os.path.join(CH, "STARTER_FILES", "ch06_11_shot_starter.blend"))
    for k in ("linked_only", "appended", "absolute_path", "not_posed"):
        build_shot(k)
        save_shot(os.path.join(cx, f"ch06_11_shot_{k}.blend"), absolute=(k == "absolute_path"))
    build_shot("solution")
    save_shot(os.path.join(out, "ch06_11_shot_solution.blend"))


if __name__ == "__main__":
    L.run(main)
