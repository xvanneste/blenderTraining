"""
build_ch10_01_files.py — « EEVEE en profondeur » (CH10.01 : ombres, ray tracing, échantillons).

Scène (EEVEE, 240 × 135) : Floor (sol clair brillant, rugosité 0,1), Wall (mur rouge vertical en x = −3), Ball (sphère blanche de 1 m de rayon en (0,5, 0, 1)), Chrome (sphère métallique miroir de 0,6 m en (2,2, −1, 0,6)),
  SUN (soleil de 3 W/m²), monde bleuté (force 0,5), CAM en (1, −8, 3).
  Consigne : régler EEVEE (Render Properties) : (1) Sampling > Shadows activé ; (2) Raytracing activé (la sphère chromée doit refléter le sol, le mur et la boule) ; (3) Sampling > Render > Samples de 16 à 128 (compromis qualité/temps).
  Départ : Shadows désactivé, Raytracing désactivé, Samples = 1. Solution : Shadows, Raytracing, Samples 64 (Fast GI Approximation laissé désactivé : non mesuré ici).
  Mesures (voir validate_ch10_01.py) : rapport ombre / lumière sur le sol (sans ombres 0,96 ; avec 0,70) ; écart-type de la luminance de la sphère chromée (sans ray tracing 0,008–0,03 ; avec 0,082).
  STARTER_FILES/ch10_01_eevee_starter.blend ; COMPLETED_EXAMPLES/ch10_01_eevee_solution.blend (+ _reference.png : départ et solution côte à côte)
  COUNTER_EXAMPLES/ : no_shadows, no_raytracing, samples_low (8), samples_high (512), cycles (moteur Cycles)
Usage : blender -b --factory-startup --python-exit-code 1 --python build_ch10_01_files.py
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
NOTE = """CH10.01 — EEVEE EN PROFONDEUR (Floor, Wall, Ball, Chrome, SUN, CAM)
Le rendu est en EEVEE mais trois réglages manquent. Render Properties :
1. Sampling > Shadows : activez (case dans l'en-tête du panneau) : la boule doit projeter une ombre.
2. Raytracing : activez (case dans l'en-tête) : la sphère chromée doit refléter le sol, le mur et la boule.
3. Sampling > Render > Samples : entre 16 et 128 (compromis qualité / temps).
Fast GI Approximation (sous-panneau de Raytracing) est un réglage de plus : pas mesuré dans cet exercice.
Vérification : SCRIPTS/validate_ch10_01.py -- --exercise eevee
"""


def mat(name, col, rough=1.0, metal=0.0):
    m = bpy.data.materials.new(name)
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*col, 1)
    b.inputs["Roughness"].default_value = rough
    b.inputs["Metallic"].default_value = metal
    return m


def obj_from(name, make, loc, material):
    bm = bmesh.new()
    make(bm)
    me = bpy.data.meshes.new("ME_" + name)
    bm.to_mesh(me)
    bm.free()
    for p in me.polygons:
        p.use_smooth = True
    o = bpy.data.objects.new(name, me)
    bpy.context.scene.collection.objects.link(o)
    o.location = loc
    o.data.materials.append(material)
    return o


def build(kind):
    L.reset("SC_EEVEE")
    sc = bpy.context.scene
    obj_from("Floor", lambda bm: bmesh.ops.create_grid(bm, x_segments=1, y_segments=1, size=6), (0, 0, 0), mat("MA_Floor", (0.8, 0.8, 0.8), 0.1))
    w = obj_from("Wall", lambda bm: bmesh.ops.create_grid(bm, x_segments=1, y_segments=1, size=3), (-3, 0, 3), mat("MA_Wall", (0.9, 0.05, 0.05)))
    w.rotation_euler = (0, math.radians(90), 0)
    obj_from("Ball", lambda bm: bmesh.ops.create_uvsphere(bm, u_segments=32, v_segments=16, radius=1.0), (0.5, 0, 1), mat("MA_Ball", (0.8, 0.8, 0.8)))
    obj_from("Chrome", lambda bm: bmesh.ops.create_uvsphere(bm, u_segments=32, v_segments=16, radius=0.6), (2.2, -1, 0.6), mat("MA_Chrome", (1, 1, 1), 0.0, 1.0))
    ld = bpy.data.lights.new("SUN", "SUN")
    ld.energy = 3
    lo = bpy.data.objects.new("SUN", ld)
    sc.collection.objects.link(lo)
    lo.rotation_euler = (0.9, 0.3, 0.6)
    wo = bpy.data.worlds.new("WO_Sky")
    sc.world = wo
    bg = wo.node_tree.nodes["Background"]
    bg.inputs["Color"].default_value = (0.4, 0.5, 0.7, 1)
    bg.inputs["Strength"].default_value = 0.5
    cam = bpy.data.objects.new("CAM", bpy.data.cameras.new("CAM"))
    sc.collection.objects.link(cam)
    cam.location = (1, -8, 3)
    cam.rotation_euler = (math.radians(70), 0, math.radians(4))
    sc.camera = cam
    sc.render.engine = "BLENDER_EEVEE"
    sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage = 240, 135, 100
    ev = sc.eevee
    shadows, rt, samples = {"starter": (False, False, 1), "solution": (True, True, 64), "no_shadows": (False, True, 64), "no_raytracing": (True, False, 64),
                            "samples_low": (True, True, 8), "samples_high": (True, True, 512), "cycles": (True, True, 64)}[kind]
    ev.use_shadows, ev.use_raytracing, ev.taa_render_samples = shadows, rt, samples
    if kind == "cycles":
        sc.render.engine = "CYCLES"
    sc.frame_set(1)
    L.instructions(NOTE)


def render():
    sc = bpy.context.scene
    sc.render.image_settings.file_format = "PNG"
    sc.render.image_settings.color_mode = "RGB"
    p = os.path.join(tempfile.gettempdir(), "bcma_ch1001.png")
    sc.render.filepath = p
    bpy.ops.render.render(write_still=True)
    im = bpy.data.images.load(p)
    px = np.array(im.pixels[:], np.float32).reshape(135, 240, 4)[..., :3][::-1].copy()
    bpy.data.images.remove(im)
    return px


def measure(px):
    Y = px[..., 0] * 0.2126 + px[..., 1] * 0.7152 + px[..., 2] * 0.0722
    shadow, lit = float(Y[48:58, 50:90].mean()), float(Y[100:120, 150:200].mean())
    return {"shadow_ratio": shadow / lit, "chrome_std": float(Y[62:84, 172:212].std())}


def calibrate():
    for kind in ("starter", "solution", "no_shadows", "no_raytracing", "samples_low", "samples_high"):
        build(kind)
        print("[eevee]", kind, {k: round(v, 3) for k, v in measure(render()).items()})


def sketch(path):
    tiles = []
    for kind in ("starter", "solution"):
        build(kind)
        tiles.append(render())
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
    L.save(os.path.join(CH, "STARTER_FILES", "ch10_01_eevee_starter.blend"))
    for k in ("no_shadows", "no_raytracing", "samples_low", "samples_high", "cycles"):
        build(k)
        L.save(os.path.join(out, "COUNTER_EXAMPLES", f"ch10_01_eevee_{k}.blend"))
    sketch(os.path.join(out, "ch10_01_eevee_reference.png"))
    build("solution")
    L.save(os.path.join(out, "ch10_01_eevee_solution.blend"))


if __name__ == "__main__":
    L.run(main)
