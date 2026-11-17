"""
build_ch09_04_files.py — « Dramatique et stylisé » (CH09.04 : une même sphère, deux intentions : low-key dramatique et high-key doux).

Fichier à DEUX SCÈNES (Scene Properties, menu des scènes en haut de la fenêtre) : LOWKEY et HIGHKEY. Le sujet (Subject), la caméra (CAM) et la visée (EMP_Target) sont partagés ;
chaque scène a ses trois lampes de zone : LOW_Key, LOW_Fill, LOW_Rim et HIGH_Key, HIGH_Fill, HIGH_Rim (mêmes positions qu'en CH09.02 : Key (−3, −3, 2,5), Fill (3, −3, 0,5), Rim (0, 1,5, 4,5)).
  Solution :
    LOWKEY  : Key 70 W (orange (1 ; 0,65 ; 0,35)), Fill 0,5 W (blanc), Rim 250 W (bleu-vert (0,35 ; 0,75 ; 1)) → image sombre, fort contraste, couleurs complémentaires.
    HIGHKEY : Key 250 W (blanc), Fill 150 W (blanc), Rim 100 W (blanc) → image claire, ombres ouvertes, contraste doux.
  Le correcteur rend chaque scène (Cycles 96 × 96, 48 échantillons, EXR linéaire) trois fois (toutes les lampes, sans Rim, sans Fill) et lit les zones du sujet (flanc éclairé, flanc d'ombre, bande du haut).
  STARTER_FILES/ch09_04_dramatic_starter.blend : les deux scènes avec Key 100 W, Fill 100 W, Rim 0 W, toutes blanches.
  COMPLETED_EXAMPLES/ch09_04_dramatic_solution.blend (+ _reference.png : les deux ambiances côte à côte)
  COUNTER_EXAMPLES/ : low_not_dark, low_low_ratio, mono_color, high_too_contrasty, high_dark
Usage : blender -b --factory-startup --python-exit-code 1 --python build_ch09_04_files.py
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
import bmesh  # noqa: E402
import bpy  # noqa: E402
import numpy as np  # noqa: E402

CH = L.chapter_dir(__file__)
NOTE = """CH09.04 — DRAMATIQUE ET STYLISÉ (scènes LOWKEY et HIGHKEY)
Deux intentions pour la même sphère : LOWKEY (sombre, dramatique, contrasté, couleurs complémentaires) et HIGHKEY (clair, doux, ombres ouvertes). Changez de scène avec le sélecteur de scène en haut de la fenêtre.
LOWKEY  : Key 70 W orange, Fill 0,5 W, Rim 250 W bleu-vert. Mesures : flanc éclairé / flanc d'ombre ≥ 7 ; luminance moyenne des deux flancs ≤ 0,15 ; la Rim apporte au moins 25 % de la bande du haut ; teintes de la Key et de la Rim distantes d'au moins 120° (couleurs complémentaires).
HIGHKEY : Key 250 W, Fill 150 W, Rim 100 W (blanches). Mesures : flanc éclairé / flanc d'ombre de 0,7 à 1,6 ; luminance moyenne des deux flancs ≥ 0,45.
Réglez seulement Power et Color des lampes. Vérification : SCRIPTS/validate_ch09_04.py -- --exercise dramatic
"""
POS = {"Key": (-3, -3, 2.5), "Fill": (3, -3, 0.5), "Rim": (0, 1.5, 4.5)}
WHITE = (1.0, 1.0, 1.0)
ORANGE, TEAL = (1.0, 0.65, 0.35), (0.35, 0.75, 1.0)
SETS = {  # (key W, fill W, rim W, key colour, rim colour) pour LOW puis HIGH
    "solution": ((70, 0.5, 250, ORANGE, TEAL), (250, 150, 100, WHITE, WHITE)),
    "starter": ((100, 100, 0, WHITE, WHITE), (100, 100, 0, WHITE, WHITE)),
    "low_not_dark": ((250, 1.5, 250, ORANGE, TEAL), (250, 150, 100, WHITE, WHITE)),
    "low_low_ratio": ((70, 25, 250, ORANGE, TEAL), (250, 150, 100, WHITE, WHITE)),
    "mono_color": ((70, 0.5, 250, WHITE, WHITE), (250, 150, 100, WHITE, WHITE)),
    "high_too_contrasty": ((70, 0.5, 250, ORANGE, TEAL), (250, 8, 100, WHITE, WHITE)),
    "high_dark": ((70, 0.5, 250, ORANGE, TEAL), (60, 40, 30, WHITE, WHITE)),
}


def make_scene(name, subject, cam, tgt, spec, prefix):
    sc = bpy.data.scenes.new(name) if name != "LOWKEY" else bpy.context.scene
    sc.name = name
    sc.render.engine = "CYCLES"
    sc.cycles.device = "CPU"
    sc.cycles.use_denoising = False
    sc.view_settings.view_transform = "Standard"
    sc.view_settings.look = "None"
    wo = bpy.data.worlds.new("WO_" + name)
    wo.node_tree.nodes["Background"].inputs["Color"].default_value = (0, 0, 0, 1)
    sc.world = wo
    for o in (subject, cam, tgt):
        if o.name not in sc.collection.objects:
            sc.collection.objects.link(o)
    sc.camera = cam
    kw, fw, rw, kc, rc = spec
    for role, w, col in (("Key", kw, kc), ("Fill", fw, WHITE), ("Rim", rw, rc)):
        ld = bpy.data.lights.new(f"{prefix}_{role}", "AREA")
        ld.shape, ld.size, ld.energy, ld.color = "SQUARE", 1.5, w, col
        lo = bpy.data.objects.new(f"{prefix}_{role}", ld)
        sc.collection.objects.link(lo)
        lo.location = POS[role]
        lo.visible_camera = False
        c = lo.constraints.new("TRACK_TO")
        c.target, c.track_axis, c.up_axis = tgt, "TRACK_NEGATIVE_Z", "UP_Y"
    return sc


def build(kind):
    L.reset("LOWKEY")
    bm = bmesh.new()
    bmesh.ops.create_uvsphere(bm, u_segments=48, v_segments=24, radius=1.0)
    me = bpy.data.meshes.new("ME_Subject")
    bm.to_mesh(me)
    bm.free()
    for p in me.polygons:
        p.use_smooth = True
    sub = bpy.data.objects.new("Subject", me)
    mat = bpy.data.materials.new("MAT_Subject")
    mat.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (0.5, 0.5, 0.5, 1)
    mat.node_tree.nodes["Principled BSDF"].inputs["Roughness"].default_value = 1.0
    sub.data.materials.append(mat)
    tgt = bpy.data.objects.new("EMP_Target", None)
    cam = bpy.data.objects.new("CAM", bpy.data.cameras.new("CAM"))
    cam.location = (0, -4.5, 0)
    cam.rotation_euler = (math.radians(90), 0, 0)
    cam.data.lens = 50
    low, high = SETS[kind]
    make_scene("LOWKEY", sub, cam, tgt, low, "LOW")
    make_scene("HIGHKEY", sub, cam, tgt, high, "HIGH")
    bpy.context.window.scene = bpy.data.scenes["LOWKEY"] if bpy.context.window else None
    L.instructions(NOTE)


def render(scene, prefix, hide=(), res=96, samples=48):
    sc = bpy.data.scenes[scene]
    sc.cycles.samples = samples
    sc.render.resolution_x = sc.render.resolution_y = res
    sc.render.resolution_percentage = 100
    for role in ("Key", "Fill", "Rim"):
        bpy.data.objects[f"{prefix}_{role}"].hide_render = role in hide
    sc.render.image_settings.file_format = "OPEN_EXR"
    sc.render.image_settings.color_depth = "32"
    p = os.path.join(tempfile.gettempdir(), "bcma_ch0904.exr")
    sc.render.filepath = p
    bpy.ops.render.render(write_still=True, scene=scene)
    im = bpy.data.images.load(p)
    px = np.array(im.pixels[:], np.float32).reshape(res, res, 4)[..., :3].copy()
    bpy.data.images.remove(im)
    return px[..., 0] * 0.2126 + px[..., 1] * 0.7152 + px[..., 2] * 0.0722


def zones(Y):
    c = Y.shape[0] // 2
    return float(Y[c - 8:c + 8, c - 25:c - 10].mean()), float(Y[c - 8:c + 8, c + 10:c + 25].mean()), float(Y[c + 22:c + 27, c - 8:c + 8].mean())


def hue(c):
    return colorsys.rgb_to_hsv(*c)[0] * 360.0


def measure(scene, prefix):
    a = zones(render(scene, prefix))
    nr = zones(render(scene, prefix, hide=("Rim",)))
    return a, (a[2] - nr[2]) / max(a[2], 1e-9)


def calibrate():
    for kind in SETS:
        build(kind)
        (la, lr), (ha, hr) = measure("LOWKEY", "LOW"), measure("HIGHKEY", "HIGH")
        print(f"[dram] {kind:19s} LOW lit {la[0]:.3f} shade {la[1]:.3f} ratio {la[0] / max(la[1], 1e-9):.1f} mean {(la[0] + la[1]) / 2:.3f} rim {lr:.2f} | HIGH ratio {ha[0] / max(ha[1], 1e-9):.2f} mean {(ha[0] + ha[1]) / 2:.3f}")
    print("[dram] teintes : orange", round(hue(ORANGE)), "bleu-vert", round(hue(TEAL)))


def sketch(path):
    build("solution")
    W, H = 780, 270
    img = np.zeros((H, W, 3), np.float32)
    for i, (scene, prefix) in enumerate((("LOWKEY", "LOW"), ("HIGHKEY", "HIGH"))):
        sc = bpy.data.scenes[scene]
        Y = render(scene, prefix)
        # image couleur : relire le rendu complet
        p = os.path.join(tempfile.gettempdir(), "bcma_ch0904.exr")
        im = bpy.data.images.load(p)
        px = np.array(im.pixels[:], np.float32).reshape(96, 96, 4)[..., :3].copy()
        bpy.data.images.remove(im)
        v = np.clip(px, 0, 1) ** (1 / 2.2)
        big = np.kron(v, np.ones((2, 2, 1), np.float32))[::-1]
        img[39:231, 60 + i * 340:252 + i * 340, :] = big
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
    L.save(os.path.join(CH, "STARTER_FILES", "ch09_04_dramatic_starter.blend"))
    for k in ("low_not_dark", "low_low_ratio", "mono_color", "high_too_contrasty", "high_dark"):
        build(k)
        L.save(os.path.join(out, "COUNTER_EXAMPLES", f"ch09_04_dramatic_{k}.blend"))
    sketch(os.path.join(out, "ch09_04_dramatic_reference.png"))
    build("solution")
    L.save(os.path.join(out, "ch09_04_dramatic_solution.blend"))


if __name__ == "__main__":
    L.run(main)
