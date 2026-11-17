"""
build_ch11_09_files.py — « Intégration 3D/réel » (CH11.09 : shadow catcher, film transparent, direction de la lumière, composition sur la plaque).

Données : la PLAQUE « plate » (320 × 180, générée par numpy et empaquetée) : ciel bleu clair en haut, sol gris (0,55) à partir de la rangée 70 (horizon), et un vrai poteau sombre à droite (x ≈ 250) dont l'OMBRE s'étire VERS LA DROITE : le soleil de la prise de vue est à GAUCHE.
  Scène 3D (Cycles CPU, 320 × 180, 32 échantillons, sans débruitage) : Cube (1 m, rouge, posé en (0, 0, 0,5)), Floor (plan de 40 m à z = 0), SUN, CAM en (0, −8, 3) inclinée de 75° (rotation X), focale 35 mm. Le compositeur contient déjà le nœud Image de la plaque et Render Layers.
  Consigne : intégrer le cube dans la plaque :
    1. Floor = Shadow Catcher (Object Properties > Visibility > Mask > Shadow Catcher : object.is_shadow_catcher) : le sol ne reçoit que l'ombre ;
    2. Film > Transparent (render.film_transparent) : le fond du rendu devient transparent ;
    3. SUN : l'ombre du cube doit tomber VERS LA DROITE comme celle du poteau de la plaque (soleil à gauche) : mesuré, rotation Z de −50° avec X de 50° ;
    4. compositeur : Alpha Over : Background = plaque, Foreground = Render Layers Image ; sortie Group Output.
  Mesures (voir validate_ch11_09.py), sur l'image composée : cube visible (centre rouge, écart ≤ 0,15) ; ombre à DROITE du cube : luminance du sol à droite du cube plus sombre que la plaque d'au moins 0,08 ; côté GAUCHE inchangé (±0,03) ; sol lointain = plaque (±0,03 : le plan du sol n'est pas visible).
  Départ : sol opaque, fond non transparent, soleil à droite, pas d'Alpha Over (la plaque n'est pas utilisée). Solution : tout ce qui précède.
  STARTER_FILES/ch11_09_integration_starter.blend ; COMPLETED_EXAMPLES/ch11_09_integration_solution.blend (+ _reference.png : plaque, départ, solution)
  COUNTER_EXAMPLES/ : no_catcher, no_transparent, wrong_side (soleil à droite : ombre à gauche), no_composite (rendu seul)
Usage : blender -b --factory-startup --python-exit-code 1 --python build_ch11_09_files.py
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
NOTE = """CH11.09 — INTÉGRATION 3D/RÉEL (Cube, Floor, SUN, CAM ; plaque « plate »)
Posez le cube rouge dans la plaque. Sur la plaque, l'ombre du poteau tombe vers la DROITE (soleil à gauche).
1. Floor : Object Properties > Visibility > Mask > Shadow Catcher.
2. Render Properties > Film > Transparent.
3. SUN : faites tomber l'ombre du cube vers la droite (rotation X 50°, Z −50°).
4. Compositeur : Alpha Over : Background = Image (plaque), Foreground = Render Layers Image → Group Output.
Cible : cube visible ; ombre à droite plus sombre d'au moins 0,08 ; côté gauche et sol lointain = plaque (± 0,03).
Vérification : SCRIPTS/validate_ch11_09.py -- --exercise integration
"""
W, H = 320, 180
SUN_RIGHT = (math.radians(50), 0.0, math.radians(50))   # soleil à droite : ombre à gauche
SUN_LEFT = (math.radians(50), 0.0, math.radians(-50))   # soleil à gauche : ombre à droite


def make_plate():
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    img = np.zeros((H, W, 3), np.float32)
    sky = np.clip(1.0 - yy / 70.0, 0, 1)
    img[:] = (0.75, 0.82, 0.95)
    img[..., 0] -= 0.1 * (1 - sky)
    ground = yy >= 70
    img[ground] = (0.55, 0.55, 0.55)
    img[ground] *= (0.9 + 0.1 * np.clip((yy[ground] - 70) / 110.0, 0, 1))[:, None]
    # poteau réel (x 246–254, rangées 40 à 120) et son ombre vers la droite
    post = (xx >= 246) & (xx <= 254) & (yy >= 40) & (yy <= 120)
    img[post] = (0.12, 0.10, 0.08)
    shadow = (yy >= 118) & (yy <= 126) & (xx >= 250) & (xx <= 310)
    img[shadow] *= 0.55
    out = bpy.data.images.new("plate", W, H, alpha=False)
    out.colorspace_settings.name = "sRGB"
    out.pixels = np.concatenate([np.clip(img, 0, 1), np.ones((H, W, 1), np.float32)], axis=2)[::-1].ravel().tolist()
    out.pack()
    return out


def build(kind):
    L.reset("SC_INTEG")
    sc = bpy.context.scene
    plate = make_plate()
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    me = bpy.data.meshes.new("ME_Cube")
    bm.to_mesh(me)
    bm.free()
    cube = bpy.data.objects.new("Cube", me)
    cube.location = (0, 0, 0.5)
    mat = bpy.data.materials.new("MA_Cube")
    mat.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (0.8, 0.1, 0.1, 1)
    mat.node_tree.nodes["Principled BSDF"].inputs["Roughness"].default_value = 0.8
    cube.data.materials.append(mat)
    sc.collection.objects.link(cube)
    bm = bmesh.new()
    bmesh.ops.create_grid(bm, x_segments=1, y_segments=1, size=20)
    mf = bpy.data.meshes.new("ME_Floor")
    bm.to_mesh(mf)
    bm.free()
    fl = bpy.data.objects.new("Floor", mf)
    fm = bpy.data.materials.new("MA_Floor")
    fm.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (0.5, 0.5, 0.5, 1)
    fl.data.materials.append(fm)
    sc.collection.objects.link(fl)
    ld = bpy.data.lights.new("SUN", "SUN")
    ld.energy = 4
    ld.angle = math.radians(2)
    lo = bpy.data.objects.new("SUN", ld)
    sc.collection.objects.link(lo)
    cam = bpy.data.objects.new("CAM", bpy.data.cameras.new("CAM"))
    sc.collection.objects.link(cam)
    cam.location = (0, -8, 3)
    cam.rotation_euler = (math.radians(75), 0, 0)
    cam.data.lens = 35
    sc.camera = cam
    wo = bpy.data.worlds.new("WO_Sky")
    sc.world = wo
    wo.node_tree.nodes["Background"].inputs["Color"].default_value = (0.7, 0.8, 1.0, 1)
    wo.node_tree.nodes["Background"].inputs["Strength"].default_value = 0.8
    sc.render.engine = "CYCLES"
    sc.cycles.device = "CPU"
    sc.cycles.samples = 32
    sc.cycles.use_denoising = False
    sc.view_settings.view_transform = "Standard"
    sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage = W, H, 100
    solved = kind != "starter"
    fl.is_shadow_catcher = solved and kind != "no_catcher"
    sc.render.film_transparent = solved and kind != "no_transparent"
    lo.rotation_euler = SUN_RIGHT if kind in ("starter", "wrong_side") else SUN_LEFT
    ng = bpy.data.node_groups.new("Comp", "CompositorNodeTree")
    sc.compositing_node_group = ng
    ng.interface.new_socket("Image", in_out="OUTPUT", socket_type="NodeSocketColor")
    rl = ng.nodes.new("CompositorNodeRLayers")
    rl.location = (-600, 100)
    ni = ng.nodes.new("CompositorNodeImage")
    ni.image = plate
    ni.location = (-600, -150)
    out = ng.nodes.new("NodeGroupOutput")
    out.location = (500, 0)
    if solved and kind != "no_composite":
        ao = ng.nodes.new("CompositorNodeAlphaOver")
        ao.location = (0, 0)
        ng.links.new(ni.outputs["Image"], ao.inputs["Background"])
        ng.links.new(rl.outputs["Image"], ao.inputs["Foreground"])
        ng.links.new(ao.outputs["Image"], out.inputs[0])
    else:
        ng.links.new(rl.outputs["Image"], out.inputs[0])
    sc.render.use_compositing = True
    sc.frame_set(1)
    L.instructions(NOTE)
    return plate


def render():
    sc = bpy.context.scene
    sc.render.image_settings.file_format = "PNG"
    sc.render.image_settings.color_mode = "RGB"
    p = os.path.join(tempfile.gettempdir(), "bcma_ch1109.png")
    sc.render.filepath = p
    bpy.ops.render.render(write_still=True)
    im = bpy.data.images.load(p)
    px = np.array(im.pixels[:], np.float32).reshape(H, W, 4)[..., :3][::-1].copy()
    bpy.data.images.remove(im)
    return px


def plate_px():
    im = bpy.data.images["plate"]
    return np.array(im.pixels[:], np.float32).reshape(H, W, 4)[..., :3][::-1].copy()


def lum(a):
    return a[..., 0] * 0.2126 + a[..., 1] * 0.7152 + a[..., 2] * 0.0722


def measure(px=None):
    px = render() if px is None else px
    pl = plate_px()
    red = (px[..., 0] - np.maximum(px[..., 1], px[..., 2])) >= 0.3
    ys, xs = np.nonzero(red)
    out = {"cube_px": int(red.sum())}
    if len(xs) >= 30:
        x0, x1, y1 = int(xs.min()), int(xs.max()), int(ys.max())
        d = lambda a, b, c, e: float((lum(px[c:e, a:b]) - lum(pl[c:e, a:b])).mean())
        out["right"] = d(x1 + 3, min(x1 + 28, W), y1 - 8, y1 + 4)
        out["left"] = d(max(x0 - 28, 0), x0 - 3, y1 - 8, y1 + 4)
        out["far"] = d(20, 70, 140, 170)
        out["cube_col"] = float(np.abs(px[ys, xs].mean(axis=0) - np.array([1.0, 0.42, 0.42])).mean())
    return out


def calibrate():
    for kind in ("starter", "solution", "no_catcher", "no_transparent", "wrong_side", "no_composite"):
        build(kind)
        print("[int]", kind, {k: round(v, 3) for k, v in measure().items()})


def sketch(path):
    tiles = [None]
    build("solution")
    tiles[0] = plate_px()
    for kind in ("starter", "solution"):
        build(kind)
        tiles.append(render())
    img = np.concatenate([np.repeat(np.repeat(t, 2, axis=0), 2, axis=1) for t in tiles], axis=1)
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
    L.save(os.path.join(CH, "STARTER_FILES", "ch11_09_integration_starter.blend"))
    for k in ("no_catcher", "no_transparent", "wrong_side", "no_composite"):
        build(k)
        L.save(os.path.join(out, "COUNTER_EXAMPLES", f"ch11_09_integration_{k}.blend"))
    sketch(os.path.join(out, "ch11_09_integration_reference.png"))
    build("solution")
    L.save(os.path.join(out, "ch11_09_integration_solution.blend"))


if __name__ == "__main__":
    L.run(main)
