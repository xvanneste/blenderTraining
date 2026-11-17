"""
build_ch10_02_files.py — « Cycles en profondeur » (CH10.02 : rebonds de lumière, échantillonnage adaptatif, seuil de bruit).

Scène (Cycles CPU, 128 × 72, sans débruitage) : une pièce ouverte sur le devant (murs, sol, plafond blancs 0,8 ; boîte de 4 × 4 × 3 m, face avant manquante), une lampe de zone de 1 × 1 m orientée VERS LE BAS à 0,3 m sous le plafond
  (Light, 20 W) : le plafond n'est éclairé que par la lumière indirecte ; CAM en (0, −5, 1,5) regardant vers +Y ; monde noir.
  Consigne (Render Properties, Cycles) : (1) Light Paths > Max Bounces > Diffuse ≥ 2 : le plafond doit recevoir de la lumière indirecte ; (2) Sampling > Render : cochez la case du seuil de bruit (Noise Threshold, échantillonnage adaptatif),
  Noise Threshold ≤ 0,05 et Max Samples de 32 à 256 ; (3) le bruit mesuré (deux rendus avec deux graines) sur le mur du fond doit rester ≤ le seuil du correcteur (voir validate_ch10_02.py).
  Départ : Diffuse 0, échantillonnage adaptatif désactivé, 4 échantillons. Solution : Diffuse 4, adaptatif activé, seuil 0,02, 64 échantillons maximum (le seuil limite le nombre réel).
  STARTER_FILES/ch10_02_cycles_starter.blend ; COMPLETED_EXAMPLES/ch10_02_cycles_solution.blend (+ _reference.png : départ et solution côte à côte)
  COUNTER_EXAMPLES/ : no_indirect (Diffuse 0), few_samples (4 échantillons, adaptatif sans effet), no_adaptive (adaptatif désactivé), loose_threshold (seuil 0,5), too_many_samples (4 096 échantillons)
Usage : blender -b --factory-startup --python-exit-code 1 --python build_ch10_02_files.py
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
NOTE = """CH10.02 — CYCLES EN PROFONDEUR (Room, Light, CAM)
Une pièce blanche éclairée par une lampe orientée vers le bas : le plafond n'est éclairé que par la lumière qui rebondit. Le rendu de départ est noir au plafond et très bruité.
Render Properties (Render Engine : Cycles) :
1. Light Paths > Max Bounces > Diffuse : au moins 2.
2. Sampling > Render : cochez la case de l'en-tête (Noise Threshold = échantillonnage adaptatif), Noise Threshold ≤ 0,05, Max Samples entre 32 et 256.
3. Le bruit mesuré par le correcteur (deux rendus, deux graines) doit rester sous sa limite.
Light Tree (Sampling > Lights) reste activé : non mesuré ici.
Vérification : SCRIPTS/validate_ch10_02.py -- --exercise cycles
"""


def build(kind):
    L.reset("SC_CYCLES")
    sc = bpy.context.scene
    m = bpy.data.materials.new("MA_White")
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (0.8, 0.8, 0.8, 1)
    b.inputs["Roughness"].default_value = 1.0
    bm = bmesh.new()
    res = bmesh.ops.create_cube(bm, size=1.0)
    bmesh.ops.scale(bm, vec=(4, 4, 3), verts=bm.verts)
    bmesh.ops.translate(bm, vec=(0, 0, 1.5), verts=bm.verts)
    front = [f for f in bm.faces if f.normal.y < -0.9]  # face avant (y = -2)
    bmesh.ops.delete(bm, geom=front, context="FACES")
    bmesh.ops.reverse_faces(bm, faces=bm.faces)  # normales vers l'intérieur
    me = bpy.data.meshes.new("ME_Room")
    bm.to_mesh(me)
    bm.free()
    room = bpy.data.objects.new("Room", me)
    sc.collection.objects.link(room)
    room.data.materials.append(m)
    ld = bpy.data.lights.new("Light", "AREA")
    ld.shape, ld.size, ld.energy = "SQUARE", 1.0, 20
    lo = bpy.data.objects.new("Light", ld)
    sc.collection.objects.link(lo)
    lo.location = (0, 0, 2.7)  # rotation 0 : la lampe de zone éclaire vers -Z
    lo.visible_camera = False
    wo = bpy.data.worlds.new("WO_Black")
    sc.world = wo
    wo.node_tree.nodes["Background"].inputs["Color"].default_value = (0, 0, 0, 1)
    cam = bpy.data.objects.new("CAM", bpy.data.cameras.new("CAM"))
    sc.collection.objects.link(cam)
    cam.location = (0, -5, 1.5)
    cam.rotation_euler = (math.radians(90), 0, 0)
    cam.data.lens = 20
    sc.camera = cam
    cy = sc.cycles
    sc.render.engine = "CYCLES"
    cy.device = "CPU"
    cy.use_denoising = False
    sc.view_settings.view_transform = "Standard"
    sc.view_settings.look = "None"
    diffuse, adaptive, thr, samples = {"starter": (0, False, 0.01, 4), "solution": (4, True, 0.02, 64), "no_indirect": (0, True, 0.02, 64), "few_samples": (4, True, 0.02, 4),
                                       "no_adaptive": (4, False, 0.02, 64), "loose_threshold": (4, True, 0.5, 64), "too_many_samples": (4, True, 0.02, 4096)}[kind]
    cy.diffuse_bounces, cy.use_adaptive_sampling, cy.adaptive_threshold, cy.samples = diffuse, adaptive, thr, samples
    sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage = 128, 72, 100
    sc.frame_set(1)
    L.instructions(NOTE)


def render(seed=0):
    sc = bpy.context.scene
    sc.cycles.seed = seed
    sc.render.image_settings.file_format = "PNG"
    sc.render.image_settings.color_mode = "RGB"
    p = os.path.join(tempfile.gettempdir(), "bcma_ch1002.png")
    sc.render.filepath = p
    bpy.ops.render.render(write_still=True)
    im = bpy.data.images.load(p)
    px = np.array(im.pixels[:], np.float32).reshape(72, 128, 4)[..., :3][::-1].copy()
    bpy.data.images.remove(im)
    return px[..., 0] * 0.2126 + px[..., 1] * 0.7152 + px[..., 2] * 0.0722


def measure():
    a, b = render(0), render(1)
    ceil = float(a[2:10, 40:90].mean())
    wall = (slice(30, 50), slice(50, 80))
    noise = float(np.std(a[wall] - b[wall]) / math.sqrt(2.0))
    return {"ceiling": ceil, "noise": noise, "wall": float(a[wall].mean())}


def calibrate():
    import time
    for kind in ("starter", "solution", "no_indirect", "few_samples", "no_adaptive", "loose_threshold", "too_many_samples"):
        build(kind)
        t = time.time()
        m = measure()
        print("[cyc]", kind, {k: round(v, 4) for k, v in m.items()}, "t", round(time.time() - t, 1))


def sketch(path):
    tiles = []
    for kind in ("starter", "solution"):
        build(kind)
        tiles.append(np.repeat(np.repeat(render(0), 2, axis=0), 2, axis=1))
    img = np.concatenate(tiles, axis=1)
    img = np.stack([img] * 3, axis=2) if img.ndim == 2 else img
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
    L.save(os.path.join(CH, "STARTER_FILES", "ch10_02_cycles_starter.blend"))
    for k in ("no_indirect", "few_samples", "no_adaptive", "loose_threshold", "too_many_samples"):
        build(k)
        L.save(os.path.join(out, "COUNTER_EXAMPLES", f"ch10_02_cycles_{k}.blend"))
    sketch(os.path.join(out, "ch10_02_cycles_reference.png"))
    build("solution")
    L.save(os.path.join(out, "ch10_02_cycles_solution.blend"))


if __name__ == "__main__":
    L.run(main)
