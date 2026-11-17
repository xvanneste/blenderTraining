"""
build_ch11_02_files.py — « Compositing multipasse » (CH11.02 : recomposer un rendu par light groups, relighting en post).

Scène (Cycles CPU, 128 × 72, 32 échantillons, sans débruitage, monde noir) : Ball (sphère de 1 m en (0, 5, 0), matériau diffus gris 0,8), deux lampes ponctuelles de 60 W : KEY en (−3, 2, 1,5) (light group « key », couleur chaude) et
  FILL en (3, 2, 1,5) (light group « fill », couleur froide), CAM à l'origine (visée +Y, focale 50). Le calque de vue a deux light groups « key » et « fill » : le nœud Render Layers offre les prises « Combined_key » et « Combined_fill ».
  Les deux lampes sont identiques en puissance et symétriques : le rendu brut est équilibré (flanc gauche / flanc droit en luminance LINÉAIRE ≈ 1,0).
  Consigne : RELIGHTER EN POST sans toucher aux lampes : dans le compositeur, recomposer l'image à partir des deux light groups (Combined_key et Combined_fill passés chacun dans un nœud Exposure, puis additionnés par un nœud Mix en mode Add) :
    le flanc éclairé par KEY (gauche) doit être 3 à 5,5 fois plus lumineux que le flanc de FILL (droite) ; le côté de FILL ne s'éteint pas (flanc droit ≥ 0,01) ; les DEUX prises de light groups sont utilisées ; aucun nœud orphelin ; compositing activé.
  Départ : Render Layers (Image) → Group Output (rapport ≈ 1,0). Solution : Combined_key → Exposure +1 → Mix (Add) ← Exposure −1 ← Combined_fill → Group Output (rapport ≈ 4).
  STARTER_FILES/ch11_02_multipass_starter.blend ; COMPLETED_EXAMPLES/ch11_02_multipass_solution.blend (+ _reference.png : départ et solution)
  COUNTER_EXAMPLES/ : no_relight (exposures à 0), too_strong (+3 / −3), reversed (−1 / +1), missing_fill (KEY seul), image_only (Render Layers Image + Exposure : light groups ignorés)
Usage : blender -b --factory-startup --python-exit-code 1 --python build_ch11_02_files.py
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
NOTE = """CH11.02 — COMPOSITING MULTIPASSE (Ball, KEY, FILL, CAM ; light groups key et fill)
Les deux lampes sont identiques : le rendu est équilibré. Relightez en post, sans toucher aux lampes :
Render Layers : prises Combined_key et Combined_fill → un nœud Exposure chacune → un nœud Mix (mode Add) → Group Output.
Cible : le flanc gauche (KEY) 3 à 5,5 fois plus lumineux que le flanc droit (FILL) ; le flanc droit ne s'éteint pas (≥ 0,01) ; les deux prises sont utilisées ; pas de nœud orphelin ; compositing activé.
Vérification : SCRIPTS/validate_ch11_02.py -- --exercise multipass
"""


def build(kind):
    L.reset("SC_MULTIPASS")
    sc = bpy.context.scene
    bpy.ops.mesh.primitive_uv_sphere_add(radius=1.0, location=(0, 5, 0), segments=48, ring_count=24)
    ball = bpy.context.object
    ball.name = "Ball"
    m = bpy.data.materials.new("MA_Ball")
    m.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (0.8, 0.8, 0.8, 1)
    m.node_tree.nodes["Principled BSDF"].inputs["Roughness"].default_value = 1.0
    ball.data.materials.append(m)
    for name, loc, col in (("KEY", (-3, 2, 1.5), (1.0, 0.8, 0.6)), ("FILL", (3, 2, 1.5), (0.6, 0.7, 1.0))):
        ld = bpy.data.lights.new(name, "POINT")
        ld.energy, ld.color = 60, col
        lo = bpy.data.objects.new(name, ld)
        sc.collection.objects.link(lo)
        lo.location = loc
        lo.lightgroup = name.lower()
    wo = bpy.data.worlds.new("WO_Black")
    sc.world = wo
    wo.node_tree.nodes["Background"].inputs["Color"].default_value = (0, 0, 0, 1)
    cam = bpy.data.objects.new("CAM", bpy.data.cameras.new("CAM"))
    sc.collection.objects.link(cam)
    cam.rotation_euler = (math.radians(90), 0, 0)
    cam.data.lens = 50
    sc.camera = cam
    vl = sc.view_layers[0]
    vl.lightgroups.add(name="key")
    vl.lightgroups.add(name="fill")
    sc.render.engine = "CYCLES"
    sc.cycles.device = "CPU"
    sc.cycles.samples = 32
    sc.cycles.use_denoising = False
    sc.view_settings.view_transform = "Standard"
    sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage = 128, 72, 100
    ng = bpy.data.node_groups.new("Comp", "CompositorNodeTree")
    sc.compositing_node_group = ng
    ng.interface.new_socket("Image", in_out="OUTPUT", socket_type="NodeSocketColor")
    rl = ng.nodes.new("CompositorNodeRLayers")
    rl.location = (-700, 0)
    out = ng.nodes.new("NodeGroupOutput")
    out.location = (500, 0)
    if kind == "starter":
        ng.links.new(rl.outputs["Image"], out.inputs[0])
    elif kind == "image_only":
        ex = ng.nodes.new("CompositorNodeExposure")
        ex.inputs["Exposure"].default_value = 0.5
        ng.links.new(rl.outputs["Image"], ex.inputs["Image"])
        ng.links.new(ex.outputs["Image"], out.inputs[0])
    else:
        ek, ef = {"solution": (1.0, -1.0), "no_relight": (0.0, 0.0), "too_strong": (3.0, -3.0), "reversed": (-1.0, 1.0), "missing_fill": (1.0, None)}[kind]
        exk = ng.nodes.new("CompositorNodeExposure")
        exk.location = (-400, 150)
        exk.inputs["Exposure"].default_value = ek
        ng.links.new(rl.outputs["Combined_key"], exk.inputs["Image"])
        if ef is None:
            ng.links.new(exk.outputs["Image"], out.inputs[0])
        else:
            exf = ng.nodes.new("CompositorNodeExposure")
            exf.location = (-400, -150)
            exf.inputs["Exposure"].default_value = ef
            ng.links.new(rl.outputs["Combined_fill"], exf.inputs["Image"])
            mix = ng.nodes.new("ShaderNodeMix")
            mix.location = (0, 0)
            mix.data_type = "RGBA"
            mix.blend_type = "ADD"
            mix.inputs["Factor"].default_value = 1.0
            ng.links.new(exk.outputs["Image"], mix.inputs["A"])
            ng.links.new(exf.outputs["Image"], mix.inputs["B"])
            ng.links.new(mix.outputs["Result"], out.inputs[0])
    sc.render.use_compositing = True
    sc.frame_set(1)
    L.instructions(NOTE)


def render():
    sc = bpy.context.scene
    sc.render.image_settings.file_format = "PNG"
    sc.render.image_settings.color_mode = "RGB"
    p = os.path.join(tempfile.gettempdir(), "bcma_ch1102.png")
    sc.render.filepath = p
    bpy.ops.render.render(write_still=True)
    im = bpy.data.images.load(p)
    px = np.array(im.pixels[:], np.float32).reshape(72, 128, 4)[..., :3][::-1].copy()
    bpy.data.images.remove(im)
    return px[..., 0] * 0.2126 + px[..., 1] * 0.7152 + px[..., 2] * 0.0722, px


def measure():
    y, _ = render()
    lin = np.where(y <= 0.04045, y / 12.92, ((y + 0.055) / 1.055) ** 2.4)  # image affichée (sRGB) -> luminance linéaire
    left, right = float(lin[32:40, 36:46].mean()), float(lin[32:40, 82:92].mean())
    return {"left": left, "right": right, "ratio": left / max(right, 1e-6)}


def calibrate():
    for kind in ("starter", "solution", "no_relight", "too_strong", "reversed", "missing_fill", "image_only"):
        build(kind)
        print("[mp]", kind, {k: round(v, 4) for k, v in measure().items()})


def sketch(path):
    tiles = []
    for kind in ("starter", "solution"):
        build(kind)
        _, px = render()
        tiles.append(np.repeat(np.repeat(px, 3, axis=0), 3, axis=1))
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
    L.save(os.path.join(CH, "STARTER_FILES", "ch11_02_multipass_starter.blend"))
    for k in ("no_relight", "too_strong", "reversed", "missing_fill", "image_only"):
        build(k)
        L.save(os.path.join(out, "COUNTER_EXAMPLES", f"ch11_02_multipass_{k}.blend"))
    sketch(os.path.join(out, "ch11_02_multipass_reference.png"))
    build("solution")
    L.save(os.path.join(out, "ch11_02_multipass_solution.blend"))


if __name__ == "__main__":
    L.run(main)
