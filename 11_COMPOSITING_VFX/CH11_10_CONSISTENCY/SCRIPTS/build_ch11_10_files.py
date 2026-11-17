"""
build_ch11_10_files.py — « Cohérence visuelle » (CH11.10 : raccorder un élément 3D à la plaque : exposition, dominante de couleur, grain ; contrôle qualité).

Données : la plaque « plate » (320 × 180) : ciel, sol (0,55 ; 0,50 ; 0,42) chaud avec du GRAIN (écart-type 0,015), un poteau ; Cube gris neutre (0,6) posé sur Floor (shadow catcher), film transparent, SUN (4 W/m², à gauche : ombre à droite),
  CAM (0, −8, 3) à 75° (35 mm) ; Cycles CPU, 320 × 180, sans débruitage. L'arbre de départ : Image (plaque) → Alpha Over (Background) ← Render Layers Image (Foreground) → Group Output : l'intégration CH11.09 est faite, mais le cube est
  TROP CLAIR (rapport 1,86 avec le sol), NEUTRE (sans la dominante chaude : écart de dominante −0,20) et PROPRE (128 échantillons : bruit 0,0016, la plaque est granuleuse).
  Consigne : corriger le cube SEUL pour qu'un contrôle qualité passe (mesuré sur la face du dessus du cube et un patch de sol de la plaque) :
    1. exposition : luminance de la face du dessus / luminance du sol voisin de la plaque de 0,85 à 1,15 (solution : Exposure −2 diaphragmes, rapport 1,01) ;
    2. dominante : (rouge − bleu) du dessus moins (rouge − bleu) du sol : entre −0,04 et +0,04 (solution : Gain (1,3 ; 1,0 ; 0,6) du nœud Color Balance Lift/Gamma/Gain, écart 0,007) ;
    3. grain : bruit mesuré de la face du dessus (deux rendus à graines différentes : écart-type de la différence / √2) de 0,008 à 0,02 (solution : 2 échantillons Cycles, 0,012 ; 128 échantillons : 0,0016 ; la plaque : 0,011) ;
    4. aucun nœud orphelin, compositing activé ; scène (cube, soleil, caméra) non modifiée sauf le nombre d'échantillons.
  Départ : aucun nœud de correction, 128 échantillons. Solution : Exposure −2, Color Balance Gain chaud, 2 échantillons.
  STARTER_FILES/ch11_10_consistency_starter.blend ; COMPLETED_EXAMPLES/ch11_10_consistency_solution.blend (+ _reference.png : plaque, départ, solution)
  COUNTER_EXAMPLES/ : exposure_only (exposition juste, cube neutre), warm_only (chaud mais trop clair), clean_cube (exposition et couleur justes, mais cube propre : 128 échantillons)
Usage : blender -b --factory-startup --python-exit-code 1 --python build_ch11_10_files.py
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
from bpy_extras.object_utils import world_to_camera_view  # noqa: E402

CH = L.chapter_dir(__file__)
NOTE = """CH11.10 — COHÉRENCE VISUELLE (Cube, Floor, SUN, CAM ; plaque « plate »)
L'intégration est faite mais le cube est trop clair, neutre et trop propre (la plaque a du grain). Corrigez le cube SEUL, entre Render Layers et Alpha Over.
1. Exposition (nœud Exposure) : luminance du dessus du cube / sol voisin de la plaque entre 0,85 et 1,15.
2. Couleur (Color Balance, Gain) : (rouge − bleu) du dessus du cube égal à celui du sol de la plaque à ± 0,04.
3. Grain : la plaque est granuleuse (0,011) : le cube doit l'être aussi : bruit mesuré de 0,008 à 0,02 (Cycles : peu d'échantillons, sans débruitage).
Pas de nœud orphelin ; compositing activé ; scène inchangée.
Vérification : SCRIPTS/validate_ch11_10.py -- --exercise consistency
"""
W, H = 320, 180
GROUND = (0.55, 0.50, 0.42)


def make_plate():
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    img = np.zeros((H, W, 3), np.float32)
    img[:] = (0.75, 0.80, 0.90)
    ground = yy >= 70
    img[ground] = GROUND
    post = (xx >= 246) & (xx <= 254) & (yy >= 40) & (yy <= 120)
    img[post] = (0.12, 0.10, 0.08)
    shadow = (yy >= 118) & (yy <= 126) & (xx >= 250) & (xx <= 310)
    img[shadow] *= 0.7
    img += np.random.RandomState(5).normal(0, 0.015, img.shape).astype(np.float32)  # grain de la plaque : écart-type 0,015
    out = bpy.data.images.new("plate", W, H, alpha=False)
    out.colorspace_settings.name = "sRGB"
    out.pixels = np.concatenate([np.clip(img, 0, 1), np.ones((H, W, 1), np.float32)], axis=2)[::-1].ravel().tolist()
    out.pack()
    return out


SETS = {  # (exposition EV, Gain RGB, échantillons Cycles) ; None = pas de nœud
    "starter": None,
    "solution": (-2.0, (1.3, 1.0, 0.6), 2),
    "exposure_only": (-2.0, None, 2),
    "warm_only": (0.0, (1.25, 1.0, 0.75), 2),
    "clean_cube": (-2.0, (1.3, 1.0, 0.6), 128),
}


def build(kind):
    L.reset("SC_CONSIST")
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
    mat.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (0.6, 0.6, 0.6, 1)
    mat.node_tree.nodes["Principled BSDF"].inputs["Roughness"].default_value = 0.8
    cube.data.materials.append(mat)
    sc.collection.objects.link(cube)
    bm = bmesh.new()
    bmesh.ops.create_grid(bm, x_segments=1, y_segments=1, size=20)
    mf = bpy.data.meshes.new("ME_Floor")
    bm.to_mesh(mf)
    bm.free()
    fl = bpy.data.objects.new("Floor", mf)
    fl.data.materials.append(bpy.data.materials.new("MA_Floor"))
    fl.is_shadow_catcher = True
    sc.collection.objects.link(fl)
    ld = bpy.data.lights.new("SUN", "SUN")
    ld.energy = 4
    ld.angle = math.radians(2)
    lo = bpy.data.objects.new("SUN", ld)
    sc.collection.objects.link(lo)
    lo.rotation_euler = (math.radians(50), 0, math.radians(-50))
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
    sc.render.film_transparent = True
    sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage = W, H, 100
    ng = bpy.data.node_groups.new("Comp", "CompositorNodeTree")
    sc.compositing_node_group = ng
    ng.interface.new_socket("Image", in_out="OUTPUT", socket_type="NodeSocketColor")
    rl = ng.nodes.new("CompositorNodeRLayers")
    rl.location = (-900, 100)
    ni = ng.nodes.new("CompositorNodeImage")
    ni.image = plate
    ni.location = (-900, -200)
    ao = ng.nodes.new("CompositorNodeAlphaOver")
    ao.location = (100, 0)
    out = ng.nodes.new("NodeGroupOutput")
    out.location = (500, 0)
    prev = rl.outputs["Image"]
    s = SETS[kind]
    sc.cycles.samples = 128 if s is None else s[2]
    if s is not None:
        ev, gain, _ = s
        if ev != 0.0:
            ex = ng.nodes.new("CompositorNodeExposure")
            ex.location = (-600, 100)
            ex.inputs["Exposure"].default_value = ev
            ng.links.new(prev, ex.inputs["Image"])
            prev = ex.outputs["Image"]
        if gain is not None:
            cb = ng.nodes.new("CompositorNodeColorBalance")
            cb.location = (-300, 100)
            cb.inputs["Type"].default_value = "Lift/Gamma/Gain"
            cb.inputs[8].default_value = (*gain, 1)
            ng.links.new(prev, cb.inputs["Image"])
            prev = cb.outputs["Image"]
    ng.links.new(ni.outputs["Image"], ao.inputs["Background"])
    ng.links.new(prev, ao.inputs["Foreground"])
    ng.links.new(ao.outputs["Image"], out.inputs[0])
    sc.render.use_compositing = True
    sc.frame_set(1)
    L.instructions(NOTE)
    return plate


def render():
    sc = bpy.context.scene
    sc.render.image_settings.file_format = "PNG"
    sc.render.image_settings.color_mode = "RGB"
    p = os.path.join(tempfile.gettempdir(), "bcma_ch1110.png")
    sc.render.filepath = p
    bpy.ops.render.render(write_still=True)
    im = bpy.data.images.load(p)
    px = np.array(im.pixels[:], np.float32).reshape(H, W, 4)[..., :3][::-1].copy()
    bpy.data.images.remove(im)
    return px


def lum(a):
    return a[..., 0] * 0.2126 + a[..., 1] * 0.7152 + a[..., 2] * 0.0722


def faces():
    """Rectangles image (rangées, colonnes) des centres de la face du dessus et de la face avant du cube, et d'un patch de sol à gauche."""
    sc = bpy.context.scene
    cam = sc.camera

    def pix(p):
        from mathutils import Vector
        v = world_to_camera_view(sc, cam, Vector(p))
        return int(v.x * W), int((1 - v.y) * H)
    tx, ty = pix((0, 0, 1.0))
    fx, fy = pix((0, -0.5, 0.5))
    return (ty - 3, ty + 4, tx - 8, tx + 9), (fy - 5, fy + 6, fx - 8, fx + 9), (140, 165, 40, 90)


def measure(px=None):
    sc = bpy.context.scene
    sc.cycles.seed = 0
    px = render() if px is None else px
    sc.cycles.seed = 1
    px2 = render()
    sc.cycles.seed = 0
    pl = np.array(bpy.data.images["plate"].pixels[:], np.float32).reshape(H, W, 4)[..., :3][::-1].copy()
    top, front, gr = faces()
    t = px[top[0]:top[1], top[2]:top[3]]
    f = px[front[0]:front[1], front[2]:front[3]]
    g = pl[gr[0]:gr[1], gr[2]:gr[3]]
    t2 = px2[top[0]:top[1], top[2]:top[3]]
    return {"ratio": float(lum(t).mean() / lum(g).mean()), "cast": float((t[..., 0] - t[..., 2]).mean() - (g[..., 0] - g[..., 2]).mean()), "noise": float(np.std(lum(t) - lum(t2)) / math.sqrt(2.0)), "plate_noise": float(np.std(lum(g)))}


def calibrate():
    for kind in SETS:
        build(kind)
        print("[con]", kind, {k: round(v, 3) for k, v in measure().items()})


def sketch(path):
    build("starter")
    tiles = [np.array(bpy.data.images["plate"].pixels[:], np.float32).reshape(H, W, 4)[..., :3][::-1].copy(), render()]
    build("solution")
    tiles.append(render())
    img = np.concatenate([np.repeat(np.repeat(t, 2, axis=0), 2, axis=1) for t in tiles], axis=1)
    rgba = np.concatenate([img, np.ones(img.shape[:2] + (1,), np.float32)], axis=2)
    out = bpy.data.images.new("sk", img.shape[1], img.shape[0])
    out.pixels = rgba[::-1].ravel()
    out.filepath_raw = path
    out.file_format = "PNG"
    out.save()


def trial():
    for smp in (128, 32, 16, 12, 8, 4, 2, 1):
        SETS["trial"] = (-2.0, (1.3, 1.0, 0.6), smp)
        build("trial")
        print("[trial] samples", smp, {k: round(v, 4) for k, v in measure().items()})


def main():
    if L.flag("--trial"):
        return trial()
    out = os.path.join(CH, "COMPLETED_EXAMPLES")
    calibrate()
    build("starter")
    L.save(os.path.join(CH, "STARTER_FILES", "ch11_10_consistency_starter.blend"))
    for k in ("exposure_only", "warm_only", "clean_cube"):
        build(k)
        L.save(os.path.join(out, "COUNTER_EXAMPLES", f"ch11_10_consistency_{k}.blend"))
    sketch(os.path.join(out, "ch11_10_consistency_reference.png"))
    build("solution")
    L.save(os.path.join(out, "ch11_10_consistency_solution.blend"))


if __name__ == "__main__":
    L.run(main)
