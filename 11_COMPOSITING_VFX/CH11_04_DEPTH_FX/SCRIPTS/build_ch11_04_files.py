"""
build_ch11_04_files.py — « Depth, defocus, motion blur » (CH11.04 : profondeur de champ et flou de mouvement en post, avec les passes Depth et Vector).

Scène (Cycles CPU, 320 × 180, 4 échantillons, sans débruitage, monde noir ; AUCUN flou dans le rendu : use_motion_blur désactivé, DOF de la caméra désactivée) : trois barres émissives fines (rayon 2 cm, 1,8 m de haut) :
  Near (−0,5, 5, 0,9) fixe ; Mover (5 m de la caméra) animée en x de −0,5 (image 1) à +0,5 (image 21) ; Far (2,0, 30, 0,9) fixe. CAM à (0, 0, 0,9), focale 135 mm. Le calque de vue a les passes Z (Depth) et Vector : Render Layers offre « Depth » et « Vector ».
  Consigne (image 10, à régler dans le compositeur et sur la caméra) :
    1. Profondeur de champ en post : nœud Defocus (Image ← Image, Z ← Depth ; use_zbuffer, f_stop 1) et distance de mise au point de la caméra (Camera > Depth of Field > Focus Distance) à 5 m : Near NETTE (pic ≥ 0,9), Far FLOUE (pic ≤ 0,5).
    2. Flou de mouvement en post : nœud Vector Blur (Speed ← Vector, Depth ← Depth, Shutter ≥ 0,7) : la barre Mover s'étale sur au moins 18 pixels de large (sans flou : 12 ; Shutter 1,0 : 22 mesuré).
  Départ : Render Layers (Image) → Group Output (tout net, Mover 12 px). Solution : Defocus (f-stop 1, mise au point 5 m) → Vector Blur (Shutter 1,0) → Group Output.
  STARTER_FILES/ch11_04_depth_fx_starter.blend ; COMPLETED_EXAMPLES/ch11_04_depth_fx_solution.blend (+ _reference.png : départ et solution)
  COUNTER_EXAMPLES/ : no_defocus, wrong_focus (mise au point 30 m), no_vector_blur, weak_shutter (Shutter 0,1)
Usage : blender -b --factory-startup --python-exit-code 1 --python build_ch11_04_files.py
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
NOTE = """CH11.04 — DEPTH, DEFOCUS, MOTION BLUR (Near, Mover, Far, CAM ; image 10)
Rendu net, sans flou. Ajoutez la profondeur de champ et le flou de mouvement en post :
1. Nœud Defocus : Image ← Render Layers Image, Z ← Depth ; Use Z-Buffer, F-stop 1 ; caméra : Depth of Field > Focus Distance = 5 m. Cible : Near nette (pic ≥ 0,9), Far floue (pic ≤ 0,5).
2. Nœud Vector Blur : Speed ← Vector, Depth ← Depth, Shutter ≥ 0,7. Cible : la barre Mover s'étale sur au moins 18 pixels (12 sans flou).
Arbre : Render Layers → Defocus → Vector Blur → Group Output ; pas de nœud orphelin ; compositing activé.
Vérification : SCRIPTS/validate_ch11_04.py -- --exercise depth_fx
"""


def bar(sc, name, x, y):
    bpy.ops.mesh.primitive_cylinder_add(radius=0.02, depth=1.8, location=(x, y, 0.9), vertices=16)
    o = bpy.context.object
    o.name = name
    m = bpy.data.materials.new("MA_" + name)
    nt = m.node_tree
    for n in list(nt.nodes):
        nt.nodes.remove(n)
    e = nt.nodes.new("ShaderNodeEmission")
    oo = nt.nodes.new("ShaderNodeOutputMaterial")
    nt.links.new(e.outputs[0], oo.inputs[0])
    o.data.materials.append(m)
    return o


def build(kind):
    L.reset("SC_DEPTHFX")
    sc = bpy.context.scene
    bar(sc, "Near", -0.5, 5)
    mv = bar(sc, "Mover", -0.5, 5)
    mv.location.x = -0.5
    mv.keyframe_insert("location", index=0, frame=1)
    mv.location.x = 0.5
    mv.keyframe_insert("location", index=0, frame=21)
    bar(sc, "Far", 2.0, 30)
    cam = bpy.data.objects.new("CAM", bpy.data.cameras.new("CAM"))
    sc.collection.objects.link(cam)
    cam.location = (0, 0, 0.9)
    cam.rotation_euler = (math.radians(90), 0, 0)
    cam.data.lens = 135
    cam.data.dof.use_dof = False
    cam.data.dof.focus_distance = 30.0 if kind == "wrong_focus" else (10.0 if kind == "starter" else 5.0)
    sc.camera = cam
    wo = bpy.data.worlds.new("WO_Black")
    sc.world = wo
    wo.node_tree.nodes["Background"].inputs["Color"].default_value = (0, 0, 0, 1)
    sc.render.engine = "CYCLES"
    sc.cycles.device = "CPU"
    sc.cycles.samples = 4
    sc.cycles.use_denoising = False
    sc.render.use_motion_blur = False
    sc.view_settings.view_transform = "Standard"
    sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage = 320, 180, 100
    vl = sc.view_layers[0]
    vl.use_pass_z = True
    vl.use_pass_vector = True
    ng = bpy.data.node_groups.new("Comp", "CompositorNodeTree")
    sc.compositing_node_group = ng
    ng.interface.new_socket("Image", in_out="OUTPUT", socket_type="NodeSocketColor")
    rl = ng.nodes.new("CompositorNodeRLayers")
    rl.location = (-800, 0)
    out = ng.nodes.new("NodeGroupOutput")
    out.location = (600, 0)
    prev = rl.outputs["Image"]
    if kind != "starter":
        if kind != "no_defocus":
            d = ng.nodes.new("CompositorNodeDefocus")
            d.location = (-400, 0)
            d.scene = sc
            d.use_zbuffer = True
            d.f_stop = 1.0
            d.blur_max = 64
            ng.links.new(prev, d.inputs["Image"])
            ng.links.new(rl.outputs["Depth"], d.inputs["Z"])
            prev = d.outputs["Image"]
        if kind != "no_vector_blur":
            v = ng.nodes.new("CompositorNodeVecBlur")
            v.location = (0, 0)
            v.inputs["Samples"].default_value = 32
            v.inputs["Shutter"].default_value = 0.1 if kind == "weak_shutter" else 1.0
            ng.links.new(prev, v.inputs["Image"])
            ng.links.new(rl.outputs["Vector"], v.inputs["Speed"])
            ng.links.new(rl.outputs["Depth"], v.inputs["Depth"])
            prev = v.outputs["Image"]
    ng.links.new(prev, out.inputs[0])
    sc.render.use_compositing = True
    sc.frame_set(10)
    L.instructions(NOTE)


def render():
    sc = bpy.context.scene
    sc.frame_set(10)
    sc.render.image_settings.file_format = "PNG"
    sc.render.image_settings.color_mode = "RGB"
    p = os.path.join(tempfile.gettempdir(), "bcma_ch1104.png")
    sc.render.filepath = p
    bpy.ops.render.render(write_still=True)
    im = bpy.data.images.load(p)
    px = np.array(im.pixels[:], np.float32).reshape(180, 320, 4)[..., :3][::-1].copy()
    bpy.data.images.remove(im)
    return px


def measure(px=None):
    px = render() if px is None else px
    y = px[..., 0] * 0.2126 + px[..., 1] * 0.7152 + px[..., 2] * 0.0722
    band = y[80:100].mean(axis=0)
    bg = float(np.median(band))
    return {"near": float(band[:100].max() - bg), "far": float(band[200:].max() - bg), "mover_w": int((band[110:200] - bg > 0.05).sum())}


def calibrate():
    for kind in ("starter", "solution", "no_defocus", "wrong_focus", "no_vector_blur", "weak_shutter"):
        build(kind)
        print("[dfx]", kind, {k: round(v, 3) for k, v in measure().items()})


def sketch(path):
    tiles = []
    for kind in ("starter", "solution"):
        build(kind)
        tiles.append(render())
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
    L.save(os.path.join(CH, "STARTER_FILES", "ch11_04_depth_fx_starter.blend"))
    for k in ("no_defocus", "wrong_focus", "no_vector_blur", "weak_shutter"):
        build(k)
        L.save(os.path.join(out, "COUNTER_EXAMPLES", f"ch11_04_depth_fx_{k}.blend"))
    sketch(os.path.join(out, "ch11_04_depth_fx_reference.png"))
    build("solution")
    L.save(os.path.join(out, "ch11_04_depth_fx_solution.blend"))


if __name__ == "__main__":
    L.run(main)
