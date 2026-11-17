"""
build_ch10_03_files.py — « Bruit et débruitage » (CH10.03 : OpenImageDenoise, passes, préfiltre ; débruiter sans perdre le détail).

Scène (Cycles CPU, 160 × 90) : Floor (plan de 6 m à damier fin : 60 cases par mètre... Scale 60, cases claires 0,9 / sombres 0,05), Ball (sphère de 0,8 m au même damier), Light (lampe de zone 1,5 m, 60 W), monde bleuté (force 0,3), CAM en (0, −4, 2,2).
  Consigne (Render Properties, Cycles) : le rendu est limité à 8 échantillons au plus (budget serré) ; débruitez : Sampling > Render > Denoise coché (Denoiser OpenImageDenoise, Passes Albedo+Normal, Prefilter Accurate) pour rapprocher l'image d'une référence de 256 échantillons.
  Mesures (voir validate_ch10_03.py) : EQM entre l'image rendue et la référence sur la zone du damier ≤ 0,065 (4 échantillons sans débruitage 0,073 ; avec 0,056) ; rapport de contraste du damier (écart-type rendu / référence) de 0,85 à 1,15.
  Départ : 4 échantillons, débruitage désactivé. Solution : 4 échantillons, débruitage activé (OpenImageDenoise, RGB_ALBEDO_NORMAL, ACCURATE).
  STARTER_FILES/ch10_03_denoising_starter.blend ; COMPLETED_EXAMPLES/ch10_03_denoising_solution.blend (+ _reference.png : départ, solution et référence côte à côte)
  COUNTER_EXAMPLES/ : no_denoise (départ), no_prefilter (préfiltre None : 0,071), one_sample (1 échantillon, débruité : 0,110), too_many_samples (64 échantillons : hors budget)
Usage : blender -b --factory-startup --python-exit-code 1 --python build_ch10_03_files.py
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
NOTE = """CH10.03 — BRUIT ET DÉBRUITAGE (Floor, Ball, Light, CAM)
Le rendu est limité à 8 échantillons au plus (budget serré) : il est bruité. Débruitez-le sans perdre le damier fin.
Render Properties (Cycles) > Sampling > Render > Denoise : cochez la case de l'en-tête ; Denoiser : OpenImageDenoise ; Passes : Albedo and Normal ; Prefilter : Accurate.
Cible : écart quadratique moyen (EQM) avec une référence de 256 échantillons ≤ 0,065 sur la zone du damier, contraste du damier conservé (0,85 à 1,15 de la référence).
OptiX (carte NVIDIA) n'est pas testé ici.
Vérification : SCRIPTS/validate_ch10_03.py -- --exercise denoising
"""


def build(kind):
    L.reset("SC_DENOISE")
    sc = bpy.context.scene
    m = bpy.data.materials.new("MA_Checker")
    nt = m.node_tree
    b = nt.nodes["Principled BSDF"]
    ck = nt.nodes.new("ShaderNodeTexChecker")
    ck.inputs["Scale"].default_value = 60
    ck.inputs["Color1"].default_value = (0.9, 0.9, 0.9, 1)
    ck.inputs["Color2"].default_value = (0.05, 0.05, 0.05, 1)
    tc = nt.nodes.new("ShaderNodeTexCoord")
    nt.links.new(tc.outputs["UV"], ck.inputs["Vector"])
    nt.links.new(ck.outputs["Color"], b.inputs["Base Color"])
    b.inputs["Roughness"].default_value = 1.0
    bpy.ops.mesh.primitive_plane_add(size=6)
    fl = bpy.context.object
    fl.name = "Floor"
    fl.data.materials.append(m)
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.8, location=(0.8, 0.6, 0.8))
    ball = bpy.context.object
    ball.name = "Ball"
    ball.data.materials.append(m)
    ld = bpy.data.lights.new("Light", "AREA")
    ld.energy, ld.size = 60, 1.5
    lo = bpy.data.objects.new("Light", ld)
    sc.collection.objects.link(lo)
    lo.location = (-1.5, -1, 3)
    lo.rotation_euler = (0.5, -0.4, 0)
    wo = bpy.data.worlds.new("WO_Sky")
    sc.world = wo
    wo.node_tree.nodes["Background"].inputs["Color"].default_value = (0.2, 0.3, 0.5, 1)
    wo.node_tree.nodes["Background"].inputs["Strength"].default_value = 0.3
    cam = bpy.data.objects.new("CAM", bpy.data.cameras.new("CAM"))
    sc.collection.objects.link(cam)
    cam.location = (0, -4, 2.2)
    cam.rotation_euler = (math.radians(62), 0, 0)
    sc.camera = cam
    cy = sc.cycles
    sc.render.engine = "CYCLES"
    cy.device = "CPU"
    cy.use_adaptive_sampling = False
    cy.seed = 0
    sc.view_settings.view_transform = "Standard"
    sc.view_settings.look = "None"
    samples, den, pre = {"starter": (4, False, "ACCURATE"), "solution": (4, True, "ACCURATE"), "no_denoise": (4, False, "ACCURATE"), "no_prefilter": (4, True, "NONE"),
                         "one_sample": (1, True, "ACCURATE"), "too_many_samples": (64, True, "ACCURATE")}[kind]
    cy.samples, cy.use_denoising, cy.denoising_prefilter = samples, den, pre
    cy.denoiser, cy.denoising_input_passes = "OPENIMAGEDENOISE", "RGB_ALBEDO_NORMAL"
    sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage = 160, 90, 100
    sc.frame_set(1)
    L.instructions(NOTE)


def render(samples=None, den=None):
    sc = bpy.context.scene
    cy = sc.cycles
    keep = (cy.samples, cy.use_denoising)
    if samples is not None:
        cy.samples, cy.use_denoising = samples, den
    sc.render.image_settings.file_format = "PNG"
    sc.render.image_settings.color_mode = "RGB"
    p = os.path.join(tempfile.gettempdir(), "bcma_ch1003.png")
    sc.render.filepath = p
    bpy.ops.render.render(write_still=True)
    im = bpy.data.images.load(p)
    px = np.array(im.pixels[:], np.float32).reshape(90, 160, 4)[..., :3][::-1].copy()
    bpy.data.images.remove(im)
    cy.samples, cy.use_denoising = keep
    return px


def lum(px):
    return px[..., 0] * 0.2126 + px[..., 1] * 0.7152 + px[..., 2] * 0.0722


PATCH = (slice(55, 85), slice(30, 130))


def measure():
    y = lum(render())
    ref = lum(render(256, False))
    return {"rmse": float(np.sqrt(((y[PATCH] - ref[PATCH]) ** 2).mean())), "contrast": float(y[PATCH].std() / ref[PATCH].std())}


def calibrate():
    for kind in ("starter", "solution", "no_prefilter", "one_sample", "too_many_samples"):
        build(kind)
        print("[den]", kind, {k: round(v, 4) for k, v in measure().items()})


def sketch(path):
    tiles = []
    for kind in ("starter", "solution"):
        build(kind)
        tiles.append(render())
    tiles.append(render(256, False))
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
    L.save(os.path.join(CH, "STARTER_FILES", "ch10_03_denoising_starter.blend"))
    for k in ("no_denoise", "no_prefilter", "one_sample", "too_many_samples"):
        build(k)
        L.save(os.path.join(out, "COUNTER_EXAMPLES", f"ch10_03_denoising_{k}.blend"))
    sketch(os.path.join(out, "ch10_03_denoising_reference.png"))
    build("solution")
    L.save(os.path.join(out, "ch10_03_denoising_solution.blend"))


if __name__ == "__main__":
    L.run(main)
