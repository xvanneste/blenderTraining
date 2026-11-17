"""
build_ch11_01_files.py — « Compositor » (CH11.01 : arbre de nœuds de compositing, Render Layers, Exposure, Blur, sortie).

Scène (Cycles CPU, 128 × 72, 2 échantillons : volontairement sombre et bruitée) : Ball (sphère de 1 m en (0, 7, 0)), Floor (plan gris 0,6 à z = −1), SUN (soleil de 0,6 W/m²), monde gris sombre, CAM à l'origine (visée +Y).
  Blender 5.3 : le compositeur est un GROUPE DE NŒUDS (scene.compositing_node_group, arbre « CompositorNodeTree ») ; la sortie est un nœud Group Output avec une prise « Image » ; les réglages d'un nœud sont des PRISES
  (Exposure : « Exposure » ; Blur : « Size » (2 valeurs en pixels) et « Type »).
  Consigne : construire l'arbre Render Layers → Exposure → Blur → Group Output : (1) Exposure pour amener la luminance moyenne de l'image finale dans [0,35 ; 0,65] ; (2) Blur pour ramener le bruit (écart-type de la différence de deux rendus à graines différentes / √2) à ≤ 0,012 ;
    (3) la sphère reste lisible : (luminance du centre − luminance du coin) / luminance moyenne ≥ 0,65 ; (4) aucun nœud orphelin (chaque nœud mène à la sortie) ; Scene > use_compositing activé.
  Départ : Render Layers → Group Output directement (image sombre et bruitée). Solution : Exposure +1,5, Blur (3, 3) pixels.
  STARTER_FILES/ch11_01_compositor_starter.blend ; COMPLETED_EXAMPLES/ch11_01_compositor_solution.blend (+ _reference.png : départ et solution)
  COUNTER_EXAMPLES/ : no_exposure, no_blur, over_blur (Blur 60 px), orphan_node (nœud Glare non connecté), compositing_off
Usage : blender -b --factory-startup --python-exit-code 1 --python build_ch11_01_files.py
Testé avec : Blender 5.3.0.
"""
import math
import os
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bpy  # noqa: E402
import numpy as np  # noqa: E402

CH = L.chapter_dir(__file__)
NOTE = """CH11.01 — COMPOSITOR (Ball, SUN, CAM ; arbre de compositing)
Le rendu est sombre et bruité. Dans l'éditeur Compositor (espace de travail Compositing), construisez : Render Layers → Exposure → Blur → Group Output.
1. Exposure : réglez la prise « Exposure » (en diaphragmes) pour que la luminance moyenne de l'image finale soit entre 0,35 et 0,65.
2. Blur : réglez la prise « Size » (pixels, X et Y) pour que le bruit mesuré soit ≤ 0,012 ; trop fort, la sphère disparaît ((centre − coin) / moyenne ≥ 0,65).
3. Pas de nœud orphelin ; Render Properties : le compositing doit être actif (use_compositing).
Vérification : SCRIPTS/validate_ch11_01.py -- --exercise compositor
"""


def build(kind):
    L.reset("SC_COMP")
    sc = bpy.context.scene
    bpy.ops.mesh.primitive_uv_sphere_add(radius=1.0, location=(0, 7, 0), segments=48, ring_count=24)
    ball = bpy.context.object
    ball.name = "Ball"
    m = bpy.data.materials.new("MA_Ball")
    m.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (0.8, 0.8, 0.8, 1)
    m.node_tree.nodes["Principled BSDF"].inputs["Roughness"].default_value = 1.0
    ball.data.materials.append(m)
    bpy.ops.mesh.primitive_plane_add(size=60, location=(0, 4, -1.0))
    fl = bpy.context.object
    fl.name = "Floor"
    fm = bpy.data.materials.new("MA_Floor")
    fm.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (0.6, 0.6, 0.6, 1)
    fm.node_tree.nodes["Principled BSDF"].inputs["Roughness"].default_value = 1.0
    fl.data.materials.append(fm)
    ld = bpy.data.lights.new("SUN", "SUN")
    ld.energy = 0.6
    lo = bpy.data.objects.new("SUN", ld)
    sc.collection.objects.link(lo)
    lo.rotation_euler = (math.radians(55), 0, math.radians(30))
    wo = bpy.data.worlds.new("WO_Dark")
    sc.world = wo
    wo.node_tree.nodes["Background"].inputs["Color"].default_value = (0.2, 0.2, 0.2, 1)
    wo.node_tree.nodes["Background"].inputs["Strength"].default_value = 0.15
    cam = bpy.data.objects.new("CAM", bpy.data.cameras.new("CAM"))
    sc.collection.objects.link(cam)
    cam.rotation_euler = (math.radians(90), 0, 0)
    cam.data.lens = 50
    sc.camera = cam
    sc.render.engine = "CYCLES"
    sc.cycles.device = "CPU"
    sc.cycles.samples = 2
    sc.cycles.use_denoising = False
    sc.view_settings.view_transform = "Standard"
    sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage = 128, 72, 100
    ng = bpy.data.node_groups.new("Comp", "CompositorNodeTree")
    sc.compositing_node_group = ng
    ng.interface.new_socket("Image", in_out="OUTPUT", socket_type="NodeSocketColor")
    rl = ng.nodes.new("CompositorNodeRLayers")
    rl.location = (-600, 0)
    out = ng.nodes.new("NodeGroupOutput")
    out.location = (400, 0)
    prev = rl.outputs["Image"]
    if kind != "starter":
        if kind != "no_exposure":
            ex = ng.nodes.new("CompositorNodeExposure")
            ex.location = (-300, 0)
            ex.inputs["Exposure"].default_value = 1.5
            ng.links.new(prev, ex.inputs["Image"])
            prev = ex.outputs["Image"]
        if kind != "no_blur":
            bl = ng.nodes.new("CompositorNodeBlur")
            bl.location = (0, 0)
            bl.inputs["Size"].default_value = (60, 60) if kind == "over_blur" else (3, 3)
            ng.links.new(prev, bl.inputs["Image"])
            prev = bl.outputs["Image"]
    ng.links.new(prev, out.inputs[0])
    if kind == "orphan_node":
        orph = ng.nodes.new("CompositorNodeGlare")
        orph.location = (0, -300)
    sc.render.use_compositing = kind != "compositing_off"
    sc.frame_set(1)
    L.instructions(NOTE)


def render(seed):
    sc = bpy.context.scene
    sc.cycles.seed = seed
    sc.render.image_settings.file_format = "PNG"
    sc.render.image_settings.color_mode = "RGB"
    p = os.path.join(tempfile.gettempdir(), "bcma_ch1101.png")
    sc.render.filepath = p
    bpy.ops.render.render(write_still=True)
    im = bpy.data.images.load(p)
    px = np.array(im.pixels[:], np.float32).reshape(72, 128, 4)[..., :3][::-1].copy()
    bpy.data.images.remove(im)
    return px[..., 0] * 0.2126 + px[..., 1] * 0.7152 + px[..., 2] * 0.0722


def measure():
    a, b = render(0), render(1)
    flat = (slice(52, 70), slice(5, 40))
    return {"mean": float(a.mean()), "noise": float(np.std(a[flat] - b[flat]) / math.sqrt(2.0)), "contrast": float(a[32:40, 60:68].mean() - a[2:10, 2:10].mean())}


def calibrate():
    for kind in ("starter", "solution", "no_exposure", "no_blur", "over_blur", "compositing_off"):
        build(kind)
        print("[comp]", kind, {k: round(v, 4) for k, v in measure().items()})


def sketch(path):
    tiles = []
    for kind in ("starter", "solution"):
        build(kind)
        t = render(0)
        tiles.append(np.repeat(np.repeat(np.stack([t] * 3, axis=2), 3, axis=0), 3, axis=1))
    img = np.concatenate(tiles, axis=1)
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
    L.save(os.path.join(CH, "STARTER_FILES", "ch11_01_compositor_starter.blend"))
    for k in ("no_exposure", "no_blur", "over_blur", "orphan_node", "compositing_off"):
        build(k)
        L.save(os.path.join(out, "COUNTER_EXAMPLES", f"ch11_01_compositor_{k}.blend"))
    sketch(os.path.join(out, "ch11_01_compositor_reference.png"))
    build("solution")
    L.save(os.path.join(out, "ch11_01_compositor_solution.blend"))


if __name__ == "__main__":
    L.run(main)
