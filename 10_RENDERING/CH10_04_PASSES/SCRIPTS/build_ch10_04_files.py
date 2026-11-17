"""
build_ch10_04_files.py — « Passes, AOV, View Layers » (CH10.04 : rendu multi-passes, light groups, AOV, couches de vue, EXR multicouche).

Scène (Cycles CPU, 64 × 36, 1 échantillon : on ne regarde pas l'image, on inspecte le FICHIER EXR) : collections « Hero » (cube Hero, 1 m, matériau MA_Hero) et « Backdrop » (plan Backdrop de 6 m), deux lampes KEY et FILL (points), CAM.
  Consigne (View Layer Properties, Object Properties, Output Properties) :
    1. Passes : Data > Z (Depth) et Normal, Object Index ; Light > Diffuse > Color ; Cryptomatte > Object.
    2. Object Properties : Hero reçoit Relations > Pass Index 1, Backdrop 2.
    3. Light Groups : deux groupes « key » et « fill » dans le calque, KEY.lightgroup = key, FILL.lightgroup = fill (Object Properties > Shading > Light Group).
    4. Shader AOV : un AOV de type Color nommé « tint » dans le calque ET un nœud Shader AOV Output (aov_name « tint ») dans MA_Hero.
    5. Deux calques de vue : « FG » (premier plan : la collection Backdrop est exclue) avec tous ces passes, et « BG » (fond : Hero est exclu) avec au moins la passe Z (Depth).
    6. Sortie : fichier OpenEXR multicouche en 16 bits (Output Properties > Output : image_settings.media_type = 'MULTI_LAYER_IMAGE', color_depth 16).
  Le correcteur rend tous les calques dans un EXR multicouche temporaire et lit les NOMS DE CANAUX dans l'en-tête (parseur d'en-tête EXR de bcma : multi-parties) : FG.Depth.Z, FG.Normal.X, FG.Diffuse Color.R, FG.Object Index.X, FG.CryptoObject00.r, FG.tint.R, FG.Combined_key.R, FG.Combined_fill.R, BG.Depth.Z.
  Départ : un seul calque « ViewLayer » avec seulement Combined, aucun passes, aucun groupe, aucun AOV, sortie PNG. Solution : tout ce qui précède.
  STARTER_FILES/ch10_04_passes_starter.blend ; COMPLETED_EXAMPLES/ch10_04_passes_solution.blend (+ _reference.png : liste des canaux du départ et de la solution)
  COUNTER_EXAMPLES/ : no_normal, no_lightgroups, no_aov, wrong_index, no_bg_layer, png_output
Usage : blender -b --factory-startup --python-exit-code 1 --python build_ch10_04_files.py
Testé avec : Blender 5.3.0.
"""
import math
import os
import struct
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bmesh  # noqa: E402
import bpy  # noqa: E402
import numpy as np  # noqa: E402

CH = L.chapter_dir(__file__)
NOTE = """CH10.04 — PASSES, AOV, VIEW LAYERS (Hero, Backdrop, KEY, FILL, CAM)
Objectif : un EXR multicouche prêt pour le compositing. Le départ n'écrit que Combined.
1. View Layer Properties > Passes : Data > Z et Normal, Object Index ; Light > Diffuse > Color ; Cryptomatte > Object.
2. Object Properties > Relations > Pass Index : Hero 1, Backdrop 2.
3. View Layer Properties > Light Groups : « key » et « fill » ; Object Properties > Shading > Light Group : KEY = key, FILL = fill.
4. View Layer Properties > Shader AOV : un AOV Color « tint » ; dans le matériau MA_Hero, un nœud Shader AOV Output nommé « tint ».
5. Deux calques de vue : « FG » (Backdrop exclu, tous les passes) et « BG » (Hero exclu, au moins la passe Z).
6. Sortie : OpenEXR multicouche, 16 bits.
Vérification : SCRIPTS/validate_ch10_04.py -- --exercise passes
"""


def exr_channels(path):
    """Noms de canaux d'un EXR multi-parties (parcourt tous les en-têtes 'channels')."""
    data = open(path, "rb").read()
    names, pos = [], 0
    while True:
        i = data.find(b"channels\x00chlist\x00", pos)
        if i < 0:
            break
        size = struct.unpack("<i", data[i + 16:i + 20])[0]
        blob, j = data[i + 20:i + 20 + size], 0
        while j < len(blob) and blob[j] != 0:
            k = blob.index(b"\x00", j)
            names.append(blob[j:k].decode())
            j = k + 1 + 16
        pos = i + 20 + size
    return names


def build(kind):
    L.reset("SC_PASSES")
    sc = bpy.context.scene
    hero_col = bpy.data.collections.new("Hero")
    back_col = bpy.data.collections.new("Backdrop")
    sc.collection.children.link(hero_col)
    sc.collection.children.link(back_col)
    mat = bpy.data.materials.new("MA_Hero")
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    me = bpy.data.meshes.new("ME_Hero")
    bm.to_mesh(me)
    bm.free()
    hero = bpy.data.objects.new("Hero", me)
    hero.location = (0, 0, 0.5)
    hero.data.materials.append(mat)
    hero_col.objects.link(hero)
    bm = bmesh.new()
    bmesh.ops.create_grid(bm, x_segments=1, y_segments=1, size=3)
    me2 = bpy.data.meshes.new("ME_Backdrop")
    bm.to_mesh(me2)
    bm.free()
    back = bpy.data.objects.new("Backdrop", me2)
    back_col.objects.link(back)
    lights = {}
    for name, loc in (("KEY", (2, -2, 3)), ("FILL", (-2, -2, 1.5))):
        ld = bpy.data.lights.new(name, "POINT")
        ld.energy = 300
        lo = bpy.data.objects.new(name, ld)
        sc.collection.objects.link(lo)
        lo.location = loc
        lights[name] = lo
    cam = bpy.data.objects.new("CAM", bpy.data.cameras.new("CAM"))
    sc.collection.objects.link(cam)
    cam.location = (0, -5, 2)
    cam.rotation_euler = (math.radians(70), 0, 0)
    sc.camera = cam
    sc.render.engine = "CYCLES"
    sc.cycles.device = "CPU"
    sc.cycles.samples = 1
    sc.cycles.use_denoising = False
    sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage = 64, 36, 100
    vl = sc.view_layers[0]
    if kind == "starter":
        sc.render.image_settings.file_format = "PNG"
        L.instructions(NOTE)
        return
    vl.name = "FG"
    vl.use_pass_z = True
    vl.use_pass_normal = kind != "no_normal"
    vl.use_pass_object_index = True
    vl.use_pass_diffuse_color = True
    vl.use_pass_cryptomatte_object = True
    hero.pass_index = 0 if kind == "wrong_index" else 1
    back.pass_index = 2
    if kind != "no_lightgroups":
        vl.lightgroups.add(name="key")
        vl.lightgroups.add(name="fill")
        lights["KEY"].lightgroup, lights["FILL"].lightgroup = "key", "fill"
    if kind != "no_aov":
        a = vl.aovs.add()
        a.name, a.type = "tint", "COLOR"
        nt = mat.node_tree
        node = nt.nodes.new("ShaderNodeOutputAOV")
        node.aov_name = "tint"
        node.name = "AOV_tint"
    vl.layer_collection.children["Backdrop"].exclude = True
    if kind != "no_bg_layer":
        bg = sc.view_layers.new("BG")
        bg.use_pass_z = True
        bg.layer_collection.children["Hero"].exclude = True
    if kind == "png_output":
        sc.render.image_settings.file_format = "PNG"
    else:
        sc.render.image_settings.media_type = "MULTI_LAYER_IMAGE"
        sc.render.image_settings.color_depth = "16"
    sc.frame_set(1)
    L.instructions(NOTE)


def render_channels():
    sc = bpy.context.scene
    p = os.path.join(tempfile.gettempdir(), "bcma_ch1004.exr")
    if os.path.exists(p):
        os.remove(p)
    sc.render.filepath = p
    ims = sc.render.image_settings
    keep = (ims.media_type, ims.file_format)
    ims.media_type = "MULTI_LAYER_IMAGE"  # le contrôle des canaux force l'EXR multicouche
    bpy.ops.render.render(write_still=True)
    ims.media_type = keep[0]
    if keep[0] == "IMAGE":
        ims.file_format = keep[1]
    return exr_channels(p) if os.path.exists(p) else []


def calibrate():
    for kind in ("starter", "solution", "no_normal", "no_lightgroups", "no_aov", "wrong_index", "no_bg_layer"):
        build(kind)
        ch = render_channels()
        print("[pass]", kind, len(ch), sorted({c.rsplit(".", 1)[0] for c in ch}))


def sketch(path):
    """Les deux calques de la solution rendus séparément (FG : Hero seul ; BG : Backdrop seul), en 256 × 144, côte à côte."""
    build("solution")
    sc = bpy.context.scene
    sc.render.resolution_x, sc.render.resolution_y = 256, 144
    sc.cycles.samples = 16
    ims = sc.render.image_settings
    ims.media_type = "IMAGE"
    ims.file_format = "PNG"
    tiles = []
    for layer in ("FG", "BG"):
        p = os.path.join(tempfile.gettempdir(), f"bcma_ch1004_{layer}.png")
        sc.render.filepath = p
        bpy.ops.render.render(write_still=True, layer=layer)
        im = bpy.data.images.load(p)
        px = np.array(im.pixels[:], np.float32).reshape(144, 256, 4)[..., :3][::-1].copy()
        bpy.data.images.remove(im)
        tiles.append(px)
    img = np.concatenate([tiles[0], np.full((144, 8, 3), 0.5, np.float32), tiles[1]], axis=1)
    rgba = np.concatenate([img, np.ones(img.shape[:2] + (1,), np.float32)], axis=2)
    out = bpy.data.images.new("sk", img.shape[1], img.shape[0])
    out.pixels = rgba[::-1].ravel()
    out.filepath_raw = path
    out.file_format = "PNG"
    out.save()


def main():
    out = os.path.join(CH, "COMPLETED_EXAMPLES")
    calibrate()
    build("starter")
    L.save(os.path.join(CH, "STARTER_FILES", "ch10_04_passes_starter.blend"))
    for k in ("no_normal", "no_lightgroups", "no_aov", "wrong_index", "no_bg_layer", "png_output"):
        build(k)
        L.save(os.path.join(out, "COUNTER_EXAMPLES", f"ch10_04_passes_{k}.blend"))
    sketch(os.path.join(out, "ch10_04_passes_reference.png"))
    build("solution")
    L.save(os.path.join(out, "ch10_04_passes_solution.blend"))


if __name__ == "__main__":
    L.run(main)
