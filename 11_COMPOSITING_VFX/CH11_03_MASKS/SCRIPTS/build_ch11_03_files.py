"""
build_ch11_03_files.py — « Masques et Cryptomatte » (CH11.03 : isoler un objet par son index (ID Mask) ou par Cryptomatte, et le traiter seul).

Scène (Cycles CPU, 192 × 72, 16 échantillons, sans débruitage) : trois sphères de 1 m alignées : Sphere_A rouge en (−2,5, 7, 0) (Pass Index 1), Sphere_B verte en (0, 7, 0) (Pass Index 2), Sphere_C bleue en (2,5, 7, 0) (Pass Index 3) ;
  SUN, monde gris, CAM à l'origine (visée +Y). Le calque de vue a les passes Object Index et Cryptomatte Object : Render Layers offre la prise « Object Index ».
  Consigne : n'en garder en couleur QUE la sphère verte (Sphere_B), tout le reste de l'image devient gris (désaturé) : Render Layers Image → Hue/Saturation (Saturation 0) comme fond ; masque de Sphere_B (nœud ID Mask : « ID value » ← Object Index, Index 2, Anti-Alias) ;
    Mix (RGBA, mode Mix) avec Factor = masque, A = image désaturée, B = image d'origine ; sortie Group Output. Mesures (voir validate_ch11_03.py) : saturation HSV moyenne sur chaque sphère : B ≥ 0,4 ; A et C ≤ 0,1 ; fond ≤ 0,1.
  Variante acceptée (non fournie) : Cryptomatte V2 (source Render, matte_id « Sphere_B ») à la place de l'ID Mask : vérifiée (voir SOLUTIONS).
  Départ : Render Layers Image → Group Output (trois sphères en couleur). Solution : fond désaturé + ID Mask index 2 + Mix.
  STARTER_FILES/ch11_03_masks_starter.blend ; COMPLETED_EXAMPLES/ch11_03_masks_solution.blend (+ _reference.png : départ, solution, masque)
  COUNTER_EXAMPLES/ : wrong_index (masque de l'index 1 : la sphère rouge reste en couleur), all_gray (pas de masque : tout désaturé), inverted (masque inversé : B grise, A et C en couleur), no_mask_node (aucun nœud de masque : tout en couleur)
Usage : blender -b --factory-startup --python-exit-code 1 --python build_ch11_03_files.py
Testé avec : Blender 5.3.0.
"""
import colorsys
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
NOTE = """CH11.03 — MASQUES ET CRYPTOMATTE (Sphere_A rouge, Sphere_B verte, Sphere_C bleue)
Ne gardez en couleur que la sphère verte ; tout le reste devient gris. Les spheres ont les Pass Index 1, 2, 3 ; le calque de vue a les passes Object Index et Cryptomatte Object (Render Layers : prise Object Index).
Arbre : Render Layers (Image) → Hue/Saturation (Saturation 0) = fond ; nœud ID Mask (ID value ← Object Index, Index 2) = masque ; nœud Mix (Factor = masque, A = fond désaturé, B = image d'origine) → Group Output.
Cible : saturation moyenne sur Sphere_B ≥ 0,4 ; sur Sphere_A, Sphere_C et le fond ≤ 0,1.
Vous pouvez remplacer l'ID Mask par un nœud Cryptomatte (matte_id « Sphere_B »).
Vérification : SCRIPTS/validate_ch11_03.py -- --exercise masks
"""
COL = {"A": (0.9, 0.1, 0.1), "B": (0.1, 0.8, 0.1), "C": (0.1, 0.2, 0.9)}


def build(kind):
    L.reset("SC_MASKS")
    sc = bpy.context.scene
    for i, (k, x) in enumerate((("A", -2.5), ("B", 0.0), ("C", 2.5)), start=1):
        bpy.ops.mesh.primitive_uv_sphere_add(radius=1.0, location=(x, 7, 0), segments=32, ring_count=16)
        o = bpy.context.object
        o.name = f"Sphere_{k}"
        o.pass_index = i
        m = bpy.data.materials.new(f"MA_{k}")
        m.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (*COL[k], 1)
        m.node_tree.nodes["Principled BSDF"].inputs["Roughness"].default_value = 1.0
        o.data.materials.append(m)
        for p in o.data.polygons:
            p.use_smooth = True
    ld = bpy.data.lights.new("SUN", "SUN")
    ld.energy = 3
    lo = bpy.data.objects.new("SUN", ld)
    sc.collection.objects.link(lo)
    lo.rotation_euler = (math.radians(55), 0, math.radians(20))
    wo = bpy.data.worlds.new("WO_Grey")
    sc.world = wo
    wo.node_tree.nodes["Background"].inputs["Color"].default_value = (0.5, 0.5, 0.5, 1)
    wo.node_tree.nodes["Background"].inputs["Strength"].default_value = 0.6
    cam = bpy.data.objects.new("CAM", bpy.data.cameras.new("CAM"))
    sc.collection.objects.link(cam)
    cam.rotation_euler = (math.radians(90), 0, 0)
    cam.data.lens = 40
    sc.camera = cam
    vl = sc.view_layers[0]
    vl.use_pass_object_index = True
    vl.use_pass_cryptomatte_object = True
    sc.render.engine = "CYCLES"
    sc.cycles.device = "CPU"
    sc.cycles.samples = 16
    sc.cycles.use_denoising = False
    sc.view_settings.view_transform = "Standard"
    sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage = 192, 72, 100
    ng = bpy.data.node_groups.new("Comp", "CompositorNodeTree")
    sc.compositing_node_group = ng
    ng.interface.new_socket("Image", in_out="OUTPUT", socket_type="NodeSocketColor")
    rl = ng.nodes.new("CompositorNodeRLayers")
    rl.location = (-800, 0)
    out = ng.nodes.new("NodeGroupOutput")
    out.location = (600, 0)
    if kind in ("starter", "no_mask_node"):
        ng.links.new(rl.outputs["Image"], out.inputs[0])
    else:
        hs = ng.nodes.new("CompositorNodeHueSat")
        hs.location = (-500, 150)
        hs.inputs["Saturation"].default_value = 0.0
        ng.links.new(rl.outputs["Image"], hs.inputs["Image"])
        mix = ng.nodes.new("ShaderNodeMix")
        mix.location = (100, 0)
        mix.data_type = "RGBA"
        mix.blend_type = "MIX"
        if kind == "all_gray":
            mix.inputs["Factor"].default_value = 0.0
        else:
            idm = ng.nodes.new("CompositorNodeIDMask")
            idm.location = (-500, -150)
            idm.inputs["Index"].default_value = 1 if kind == "wrong_index" else 2
            ng.links.new(rl.outputs["Object Index"], idm.inputs["ID value"])
            if kind == "inverted":
                inv = ng.nodes.new("CompositorNodeInvert")
                inv.location = (-250, -150)
                ng.links.new(idm.outputs["Alpha"], inv.inputs["Color"])
                ng.links.new(inv.outputs[0], mix.inputs["Factor"])
            else:
                ng.links.new(idm.outputs["Alpha"], mix.inputs["Factor"])
        ng.links.new(hs.outputs["Image"], mix.inputs["A"])
        ng.links.new(rl.outputs["Image"], mix.inputs["B"])
        ng.links.new(mix.outputs["Result"], out.inputs[0])
    sc.render.use_compositing = True
    sc.frame_set(1)
    L.instructions(NOTE)


def render():
    sc = bpy.context.scene
    sc.render.image_settings.file_format = "PNG"
    sc.render.image_settings.color_mode = "RGB"
    p = os.path.join(tempfile.gettempdir(), "bcma_ch1103.png")
    sc.render.filepath = p
    bpy.ops.render.render(write_still=True)
    im = bpy.data.images.load(p)
    px = np.array(im.pixels[:], np.float32).reshape(72, 192, 4)[..., :3][::-1].copy()
    bpy.data.images.remove(im)
    return px


def sat(patch):
    m = patch.reshape(-1, 3).mean(axis=0)
    return colorsys.rgb_to_hsv(*[float(t) for t in m])[1]


def measure(px=None):
    px = render() if px is None else px
    # centres des sphères : colonnes 48, 96, 144 ; rayon ≈ 17 px
    return {"A": sat(px[30:42, 42:54]), "B": sat(px[30:42, 90:102]), "C": sat(px[30:42, 138:150]), "bg": sat(px[2:10, 2:190])}


def calibrate():
    for kind in ("starter", "solution", "wrong_index", "all_gray", "inverted", "no_mask_node"):
        build(kind)
        print("[mask]", kind, {k: round(v, 3) for k, v in measure().items()})


def sketch(path):
    tiles = []
    for kind in ("starter", "solution"):
        build(kind)
        tiles.append(np.repeat(np.repeat(render(), 2, axis=0), 2, axis=1))
    img = np.concatenate(tiles, axis=0)
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
    L.save(os.path.join(CH, "STARTER_FILES", "ch11_03_masks_starter.blend"))
    for k in ("wrong_index", "all_gray", "inverted", "no_mask_node"):
        build(k)
        L.save(os.path.join(out, "COUNTER_EXAMPLES", f"ch11_03_masks_{k}.blend"))
    sketch(os.path.join(out, "ch11_03_masks_reference.png"))
    build("solution")
    L.save(os.path.join(out, "ch11_03_masks_solution.blend"))


if __name__ == "__main__":
    L.run(main)
