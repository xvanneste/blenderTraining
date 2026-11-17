"""
build_ch09_05_files.py — « Volumétrie » (CH09.05 : brouillard et faisceau de lumière : un spot dans un volume de brouillard).

Scène : Fog (cube de 8 × 8 × 6 m, z de 0 à 6, matériau de VOLUME : Principled Volume ; pas de surface), Floor (dalle de 8 × 8 m à z = 0, gris 50 %), LIGHT_Spot (spot à (0, 0, 5,5) qui vise vers le bas),
  CAM (à (0, −12, 3), focale 35, regarde vers +Y), monde noir. Cycles CPU.
  Consigne : régler la densité du brouillard (Principled Volume > Density) pour que le faisceau du spot soit lisible sans noyer l'image.
  Solution : Density 0,08 (Anisotropy 0,3) ; spot 3 000 W, angle 40°, Blend 0,3. Mesures (voir le correcteur) : le centre de l'image (le faisceau) est au moins 4 fois plus lumineux que les bords (le brouillard hors faisceau), et la luminance du centre est de 0,03 à 0,6.
  STARTER_FILES/ch09_05_volumetrics_starter.blend : Density 0 (pas de brouillard). COMPLETED_EXAMPLES/ch09_05_volumetrics_solution.blend (+ _reference.png : rendus sans brouillard, Density 0,08 et Density 1,5)
  COUNTER_EXAMPLES/ : too_thin (0,004), too_dense (1,5), wide_spot (angle 150°), no_floor_light (spot éteint : 0 W)
Usage : blender -b --factory-startup --python-exit-code 1 --python build_ch09_05_files.py
Testé avec : Blender 5.3.0.
"""
import math
import os
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bmesh  # noqa: E402
import bpy  # noqa: E402
import numpy as np  # noqa: E402

CH = L.chapter_dir(__file__)
NOTE = """CH09.05 — VOLUMÉTRIE (Fog, LIGHT_Spot)
Un spot éclaire un sol dans un cube de brouillard. Réglez la densité pour que le faisceau soit lisible sans noyer l'image.
1. Fog > Material : le nœud Principled Volume est relié à la sortie Volume du Material Output : réglez Density (0,08 est un bon départ) et Anisotropy (0,3).
2. Ne changez pas le spot (3 000 W, 40°).
Contrôles (un rendu Cycles de 96 × 96) : brouillard présent (Principled Volume relié à Volume) ; centre de l'image (le faisceau) au moins 4 fois plus lumineux que les bords ; luminance du centre de 0,03 à 0,6.
Vérification : SCRIPTS/validate_ch09_05.py -- --exercise volumetrics
"""


def box(name, size, loc):
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    for v in bm.verts:
        v.co = (v.co.x * size[0], v.co.y * size[1], v.co.z * size[2])
    me = bpy.data.meshes.new("ME_" + name)
    bm.to_mesh(me)
    bm.free()
    ob = bpy.data.objects.new(name, me)
    bpy.context.scene.collection.objects.link(ob)
    ob.location = loc
    return ob


def build(kind):
    L.reset("SC_VOLUME")
    sc = bpy.context.scene
    sc.render.engine = "CYCLES"
    sc.cycles.device = "CPU"
    sc.cycles.use_denoising = False
    sc.view_settings.view_transform = "Standard"
    sc.view_settings.look = "None"
    wo = bpy.data.worlds.new("WO_Black")
    wo.node_tree.nodes["Background"].inputs["Color"].default_value = (0, 0, 0, 1)
    sc.world = wo
    fl = box("Floor", (8, 8, 0.1), (0, 0, -0.05))
    m = bpy.data.materials.new("MAT_Floor")
    m.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (0.5, 0.5, 0.5, 1)
    m.node_tree.nodes["Principled BSDF"].inputs["Roughness"].default_value = 1.0
    fl.data.materials.append(m)
    fog = box("Fog", (8, 8, 6), (0, 0, 3))
    fm = bpy.data.materials.new("MAT_Fog")
    nt = fm.node_tree
    for n in list(nt.nodes):
        nt.nodes.remove(n)
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    vol = nt.nodes.new("ShaderNodeVolumePrincipled")
    dens = {"starter": 0.0, "solution": 0.08, "too_thin": 0.004, "too_dense": 1.5, "wide_spot": 0.08, "no_light": 0.08}[kind]
    vol.inputs["Density"].default_value = dens
    vol.inputs["Anisotropy"].default_value = 0.3
    nt.links.new(vol.outputs["Volume"], out.inputs["Volume"])
    fog.data.materials.append(fm)
    fog.display_type = "WIRE"
    ld = bpy.data.lights.new("LIGHT_Spot", "SPOT")
    ld.energy = 0.0 if kind == "no_light" else 3000.0
    ld.spot_size = math.radians(150 if kind == "wide_spot" else 40)
    ld.spot_blend = 0.3
    ld.shadow_soft_size = 0.05
    lo = bpy.data.objects.new("LIGHT_Spot", ld)
    sc.collection.objects.link(lo)
    lo.location = (0, 0, 5.5)
    lo.visible_camera = False
    cam = bpy.data.objects.new("CAM", bpy.data.cameras.new("CAM"))
    sc.collection.objects.link(cam)
    cam.location = (0, -12, 3)
    cam.rotation_euler = (math.radians(90), 0, 0)
    cam.data.lens = 35
    sc.camera = cam
    sc.frame_set(1)
    L.instructions(NOTE)


def render(res=96, samples=64):
    sc = bpy.context.scene
    sc.cycles.samples = samples
    sc.render.resolution_x = sc.render.resolution_y = res
    sc.render.resolution_percentage = 100
    sc.render.image_settings.file_format = "OPEN_EXR"
    sc.render.image_settings.color_depth = "32"
    p = os.path.join(tempfile.gettempdir(), "bcma_ch0905.exr")
    sc.render.filepath = p
    bpy.ops.render.render(write_still=True)
    im = bpy.data.images.load(p)
    px = np.array(im.pixels[:], np.float32).reshape(res, res, 4)[..., :3].copy()
    bpy.data.images.remove(im)
    return px


def stats(px):
    Y = px[..., 0] * 0.2126 + px[..., 1] * 0.7152 + px[..., 2] * 0.0722
    R = Y.shape[0]
    rows = slice(R // 3, 2 * R // 3)
    centre = float(Y[rows, R // 2 - 4:R // 2 + 5].mean())
    edge = float(np.concatenate([Y[rows, 4:14], Y[rows, R - 14:R - 4]], axis=1).mean())
    return centre, edge, centre / max(edge, 1e-6)


def calibrate():
    for kind in ("starter", "solution", "too_thin", "too_dense", "wide_spot", "no_light"):
        build(kind)
        c, e, r = stats(render())
        print(f"[vol] {kind:10s} centre {c:.4f} bords {e:.5f} rapport {r:.1f}")


def sketch(path):
    W, H = 780, 270
    img = np.zeros((H, W, 3), np.float32)
    for i, kind in enumerate(("starter", "solution", "too_dense")):
        build(kind)
        px = render()
        v = np.clip(px * 4, 0, 1) ** (1 / 2.2)
        big = np.kron(v, np.ones((2, 2, 1), np.float32))[::-1]
        img[39:231, 20 + i * 255:212 + i * 255, :] = big
    rgba = np.concatenate([img, np.ones(img.shape[:2] + (1,), np.float32)], axis=2)
    out = bpy.data.images.new("sk", W, H)
    out.pixels = rgba[::-1].ravel()
    out.filepath_raw = path
    out.file_format = "PNG"
    out.save()


def main():
    out = os.path.join(CH, "COMPLETED_EXAMPLES")
    calibrate()
    build("starter")
    L.save(os.path.join(CH, "STARTER_FILES", "ch09_05_volumetrics_starter.blend"))
    for k in ("too_thin", "too_dense", "wide_spot", "no_light"):
        build(k)
        L.save(os.path.join(out, "COUNTER_EXAMPLES", f"ch09_05_volumetrics_{k}.blend"))
    sketch(os.path.join(out, "ch09_05_volumetrics_reference.png"))
    build("solution")
    L.save(os.path.join(out, "ch09_05_volumetrics_solution.blend"))


if __name__ == "__main__":
    L.run(main)
