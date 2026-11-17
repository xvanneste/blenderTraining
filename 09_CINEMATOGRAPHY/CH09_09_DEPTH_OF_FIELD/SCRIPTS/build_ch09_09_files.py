"""
build_ch09_09_files.py — « Profondeur de champ » (CH09.09 : ouverture, distance de mise au point, flou d'arrière-plan).

Scène (rendu Cycles CPU, émission blanche sur fond noir) : deux barres émissives de 1,8 m (rayon 0,03 m) : Near à (-0,25, 5, 0,9) et Far à (0,6, 30, 0,9) ;
  CAM à (0, 0, 0,9) regardant vers +Y, focale 200 mm, capteur 36 mm, rendu 320 × 180.
  Consigne : activer la profondeur de champ (Camera > Depth of Field), mettre au point sur la barre proche (Focus Distance 5 m) avec une grande ouverture (F-Stop 1,0 ou moins) :
  la barre proche doit rester NETTE (pic ≥ 0,9), la barre lointaine doit être FLOUE (pic ≤ 0,6). Le pic = moyenne, sur les lignes centrales, du maximum d'une barre moins le fond, rapporté à une barre nette.
  Au départ : DOF désactivée (tout est net : pic 1,0 et 1,0). Solution : DOF activée, Focus Distance 5, F-Stop 1,0.
  STARTER_FILES/ch09_09_dof_starter.blend ; COMPLETED_EXAMPLES/ch09_09_dof_solution.blend (+ _reference.png)
  COUNTER_EXAMPLES/ : dof_off (départ), focus_far (mise au point sur 30 m : proche flou), small_aperture (f/16 : tout net), focus_between (12 m : tout flou), no_dof_bad_fstop (DOF désactivée avec f/1,0 : aucun effet)
Usage : blender -b --factory-startup --python-exit-code 1 --python build_ch09_09_files.py
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
NOTE = """CH09.09 — PROFONDEUR DE CHAMP (Near, Far, CAM)
Deux barres lumineuses : Near à 5 m, Far à 30 m. Tout est net : la profondeur de champ est désactivée.
Consigne : isolez la barre proche en ne modifiant que la caméra (CAM).
1. Camera > Depth of Field : activez-la.
2. Focus Distance : 5 m (distance de la barre proche).
3. F-Stop : 1,0 (grande ouverture = faible profondeur de champ).
Cible : barre proche nette, barre lointaine floue (mesuré par le correcteur).
Vérification : SCRIPTS/validate_ch09_09.py -- --exercise dof
"""


def bar(sc, name, x, y):
    bm = bmesh.new()
    bmesh.ops.create_cone(bm, cap_ends=True, segments=16, radius1=0.03, radius2=0.03, depth=1.8)
    me = bpy.data.meshes.new("ME_" + name)
    bm.to_mesh(me)
    bm.free()
    o = bpy.data.objects.new(name, me)
    sc.collection.objects.link(o)
    o.location = (x, y, 0.9)
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
    L.reset("SC_DOF")
    sc = bpy.context.scene
    sc.render.engine = "CYCLES"
    sc.cycles.device = "CPU"
    sc.cycles.samples = 32
    sc.cycles.use_denoising = False
    sc.view_settings.view_transform = "Standard"
    sc.view_settings.look = "None"
    wo = bpy.data.worlds.new("WO_Black")
    sc.world = wo
    for n in wo.node_tree.nodes:
        if n.type == "BACKGROUND":
            n.inputs["Color"].default_value = (0, 0, 0, 1)
    bar(sc, "Near", -0.25, 5.0)
    bar(sc, "Far", 0.6, 30.0)
    cam = bpy.data.objects.new("CAM", bpy.data.cameras.new("CAM"))
    sc.collection.objects.link(cam)
    cam.location = (0, 0, 0.9)
    cam.rotation_euler = (math.radians(90), 0, 0)
    cam.data.lens = 200
    cam.data.sensor_width = 36
    sc.camera = cam
    use, focus, fs = {"starter": (False, 10.0, 5.6), "dof_off": (False, 10.0, 5.6), "solution": (True, 5.0, 1.0), "focus_far": (True, 30.0, 1.0), "small_aperture": (True, 5.0, 16.0),
                      "focus_between": (True, 12.0, 1.0), "no_dof_bad_fstop": (False, 5.0, 1.0)}[kind]
    d = cam.data.dof
    d.use_dof, d.focus_distance, d.aperture_fstop = use, focus, fs
    sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage = 320, 180, 100
    sc.frame_set(1)
    L.instructions(NOTE)


def render():
    sc = bpy.context.scene
    sc.render.image_settings.file_format = "PNG"
    sc.render.image_settings.color_mode = "RGB"
    p = os.path.join(tempfile.gettempdir(), "bcma_ch0909.png")
    sc.render.filepath = p
    bpy.ops.render.render(write_still=True)
    im = bpy.data.images.load(p)
    px = np.array(im.pixels[:], np.float32).reshape(180, 320, 4)[..., :3][::-1].copy()
    bpy.data.images.remove(im)
    return px


def peaks(px):
    Y = px[..., 0] * 0.2126 + px[..., 1] * 0.7152 + px[..., 2] * 0.0722
    band = Y[80:100].mean(axis=0)  # lignes centrales
    bg = float(np.median(band))
    left, right = band[:160], band[160:]
    return {"near": float(left.max() - bg), "far": float(right.max() - bg), "bg": bg}


def calibrate():
    for kind in ("starter", "solution", "focus_far", "small_aperture", "focus_between", "no_dof_bad_fstop"):
        build(kind)
        a = peaks(render())
        print(f"[dof] {kind:17s}", {k: round(v, 3) for k, v in a.items()})


def sketch(path):
    W, H = 700, 230
    img = np.zeros((H, W, 3), np.float32)
    for i, kind in enumerate(("starter", "solution")):
        build(kind)
        px = np.clip(render(), 0, 1)
        tile = px[::-1][0:180, :, :]
        tile = tile[::-1] if False else px
        y0, x0 = 25, 20 + i * 340
        img[y0:y0 + 180, x0:x0 + 320, :] = px[::-1][::-1] if False else px
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
    L.save(os.path.join(CH, "STARTER_FILES", "ch09_09_dof_starter.blend"))
    for k in ("dof_off", "focus_far", "small_aperture", "focus_between", "no_dof_bad_fstop"):
        build(k)
        L.save(os.path.join(out, "COUNTER_EXAMPLES", f"ch09_09_dof_{k}.blend"))
    sketch(os.path.join(out, "ch09_09_dof_reference.png"))
    build("solution")
    L.save(os.path.join(out, "ch09_09_dof_solution.blend"))


if __name__ == "__main__":
    L.run(main)
