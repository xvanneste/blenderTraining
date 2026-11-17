"""
build_p9_reference.py — Construit la référence du projet P9 « Cinq plans, cinq émotions » : cinq scènes (SH_JOY … SH_FEAR) partageant un sujet (Hero), chacune avec son monde, ses lampes et sa caméra,
puis la planche de contact (renders/p9_contact_sheet.png, 5 × 400 px = 2 000 px de large) et la copie des mesures.
Assemble les chapitres : lumière et exposition (CH09.01–06), composition (CH09.07), focale (CH09.08), couleur (CH09.11), échelle de plan (CH09.10).
Usage : blender -b --factory-startup --python-exit-code 1 --python build_p9_reference.py [-- --calibrate]
Testé avec : Blender 5.3.0.
"""
import importlib.util
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bmesh  # noqa: E402
import bpy  # noqa: E402
import numpy as np  # noqa: E402

spec = importlib.util.spec_from_file_location("validate_p9", os.path.join(HERE, "validate_p9.py"))
V = importlib.util.module_from_spec(spec)
spec.loader.exec_module(V)

NOTE = """P9 — CINQ PLANS, CINQ ÉMOTIONS (scènes SH_JOY, SH_SADNESS, SH_ANGER, SH_CALM, SH_FEAR ; sujet partagé Hero)
Une scène par émotion : lumière (monde et lampes), couleur, cadrage (caméra, focale, Shift X). Hero ne bouge pas. Critères : README et SCRIPTS/validate_p9.py."""

# monde (couleur, force), lampes (énergie W, couleur, position), caméra (position, focale, Shift X)
SHOTS = {
    "JOY": dict(world=((1.0, 0.85, 0.6), 0.8), lights=[(800, (1.0, 0.8, 0.5), (-2, 2, 4))], cam=((0, 0, 1.6), 35, 0.167)),
    "SADNESS": dict(world=((0.3, 0.45, 1.0), 0.035), lights=[(18, (0.5, 0.6, 1.0), (2, 2, 3))], cam=((0, 0, 1.6), 35, -0.167)),
    "ANGER": dict(world=((1.0, 0.1, 0.05), 0.15), lights=[(3000, (1.0, 0.15, 0.1), (-2, 3, 3))], cam=((0, 0, 0.9), 50, 0.0)),
    "CALM": dict(world=((0.5, 0.7, 1.0), 0.3), lights=[], cam=((0, 0, 1.6), 35, 0.167)),
    "FEAR": dict(world=((0.1, 0.1, 0.2), 0.05), lights=[(200, (0.8, 1.0, 0.8), (3, 8, 0.3))], cam=((0, -6, 1.6), 35, 0.25)),
}


def make_scene(name, hero, floor, spec_, first=False):
    sc = bpy.context.scene if first else bpy.data.scenes.new("SH_" + name)
    sc.name = "SH_" + name
    sc.render.engine = "CYCLES"
    sc.cycles.device = "CPU"
    sc.cycles.samples = 32
    sc.cycles.use_denoising = False
    sc.view_settings.view_transform = "Standard"
    sc.view_settings.look = "None"
    sc.render.fps = 24
    wo = bpy.data.worlds.new("WO_" + name)
    col, st = spec_["world"]
    bg = wo.node_tree.nodes["Background"]
    bg.inputs["Color"].default_value = (*col, 1)
    bg.inputs["Strength"].default_value = st
    sc.world = wo
    for o in (hero, floor):
        sc.collection.objects.link(o)
    for i, (w, c, pos) in enumerate(spec_["lights"]):
        ld = bpy.data.lights.new(f"{name}_L{i}", "POINT")
        ld.energy, ld.color, ld.shadow_soft_size = w, c, 0.3
        lo = bpy.data.objects.new(f"{name}_L{i}", ld)
        sc.collection.objects.link(lo)
        lo.location = pos
    (cp, lens, sx) = spec_["cam"]
    cam = bpy.data.objects.new("CAM_" + name, bpy.data.cameras.new("CAM_" + name))
    sc.collection.objects.link(cam)
    cam.location = cp
    cam.rotation_euler = (math.radians(90), 0, 0)
    cam.data.lens, cam.data.shift_x, cam.data.sensor_width = lens, sx, 36
    sc.camera = cam
    sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage = 400, 225, 100
    return sc


def build(shots=SHOTS):
    L.reset("SH_JOY")
    bm = bmesh.new()
    bmesh.ops.create_cone(bm, cap_ends=True, segments=32, radius1=0.25, radius2=0.25, depth=1.8)
    me = bpy.data.meshes.new("ME_Hero")
    bm.to_mesh(me)
    bm.free()
    for p in me.polygons:
        p.use_smooth = True
    hero = bpy.data.objects.new("Hero", me)
    hero.location = (0, 6, 0.9)
    hero.color = (1, 0, 0, 1)
    mat = bpy.data.materials.new("MAT_Hero")
    mat.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (0.8, 0.8, 0.8, 1)
    mat.node_tree.nodes["Principled BSDF"].inputs["Roughness"].default_value = 1.0
    hero.data.materials.append(mat)
    bm = bmesh.new()
    bmesh.ops.create_grid(bm, x_segments=1, y_segments=1, size=60)
    me2 = bpy.data.meshes.new("ME_Floor")
    bm.to_mesh(me2)
    bm.free()
    floor = bpy.data.objects.new("Floor", me2)
    floor.color = (0.35, 0.35, 0.35, 1)
    fm = bpy.data.materials.new("MAT_Floor")
    fm.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (0.5, 0.5, 0.5, 1)
    fm.node_tree.nodes["Principled BSDF"].inputs["Roughness"].default_value = 1.0
    floor.data.materials.append(fm)
    for i, (name, sp) in enumerate(shots.items()):
        make_scene(name, hero, floor, sp, first=(i == 0))
    L.instructions(NOTE)


def contact_sheet(path):
    tiles = []
    for n in V.SHOTS:
        sc = bpy.data.scenes["SH_" + n]
        px = V._render_png(sc, os.path.join(os.path.dirname(path), f"_tmp_{n}.png"), 400, 225)
        tiles.append(px)
        os.remove(os.path.join(os.path.dirname(path), f"_tmp_{n}.png"))
    sheet = np.concatenate(tiles, axis=1)  # 225 × 2000
    rgba = np.concatenate([sheet, np.ones(sheet.shape[:2] + (1,), np.float32)], axis=2)
    out = bpy.data.images.new("sheet", sheet.shape[1], sheet.shape[0])
    out.pixels = rgba[::-1].ravel()
    out.filepath_raw = path
    out.file_format = "PNG"
    out.save()


def main():
    calibrate = L.flag("--calibrate")
    build()
    if calibrate:
        for n in V.SHOTS:
            m = V.measure_shot(n)
            print("[p9]", n, {k: round(v, 3) for k, v in m.items()}, "R/B", round(m["R"] / max(m["B"], 1e-6), 2), "Rshare", round(m["R"] / (m["R"] + m["G"] + m["B"]), 2))
        return
    ref = os.path.join(HERE, "REFERENCE")
    os.makedirs(os.path.join(ref, "renders"), exist_ok=True)
    contact_sheet(os.path.join(ref, "renders", "p9_contact_sheet.png"))
    L.save(os.path.join(ref, "p9_scene_reference.blend"))


if __name__ == "__main__":
    L.run(main)
