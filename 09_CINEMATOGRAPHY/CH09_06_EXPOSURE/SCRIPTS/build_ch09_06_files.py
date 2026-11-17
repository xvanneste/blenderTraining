"""
build_ch09_06_files.py — « Exposition et contraste » (CH09.06 : vue (View Transform), exposition, Look ; lire une image par ses pourcentages de pixels brûlés et son contraste).

Scène : Floor (4 × 4 m, gris 50 %), trois sphères de 0,6 m de rayon posées au sol : Bright (émissive : Emission Strength 6), Mid (gris 50 %), Dark (albédo 0,02) ; soleil de 3 W/m² incliné de 50° ; monde gris très sombre (0,02) ; caméra à (0, −6, 2,5), focale 35. Cycles CPU.
  Le correcteur rend l'image AFFICHÉE (PNG 8 bits, après la gestion des couleurs de la scène : View Transform, Look, Exposure) et la lit.
  Mesures de référence (96 × 96) : Standard exposition 0 : moyenne 0,409, 4,5 % des pixels brûlés (≥ 0,99), écart p95 − p5 = 0,79 ; AgX exposition 0 : moyenne 0,374, 0 % brûlés, écart 0,62 ; AgX + 0,5 : 0,420, 0 %, 0,64 ;
  AgX « AgX - Punchy » : moyenne 0,279 (trop sombre) ; AgX « AgX - High Contrast » : 2,7 % brûlés ; Filmic « High Contrast » : 0,393, 0,1 %, 0,74 ; Khronos PBR Neutral : 0,332, 0 %, 0,87.
  Consigne : choisir la vue, l'exposition et le look pour : au plus 1 % de pixels brûlés ; luminance moyenne de 0,3 à 0,55 ; écart p95 − p5 d'au moins 0,55 (contraste).
  Solution : View Transform AgX, Look None, Exposure +0,5. STARTER : Standard, Look None, Exposure 0.
  STARTER_FILES/ch09_06_exposure_starter.blend ; COMPLETED_EXAMPLES/ch09_06_exposure_solution.blend (+ _reference.png : rendu Standard à gauche, solution à droite, avec leurs histogrammes)
  COUNTER_EXAMPLES/ : standard_clipped (Standard), too_dark (AgX −2,5), too_bright (AgX +3), punchy_dark (AgX - Punchy)
Usage : blender -b --factory-startup --python-exit-code 1 --python build_ch09_06_files.py
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
NOTE = """CH09.06 — EXPOSITION ET CONTRASTE (scène : Floor, Bright, Mid, Dark, soleil)
Une sphère émissive très lumineuse brûle dans la vue par défaut (Standard). Choisissez la vue (View Transform), l'exposition (Exposure) et éventuellement le Look pour obtenir une image bien exposée.
Properties > Render > Color Management : View Transform, Look, Exposure.
Contrôles (un rendu Cycles de 96 × 96, image affichée) : au plus 1 % de pixels brûlés (valeur ≥ 0,99) ; luminance moyenne de 0,3 à 0,55 ; écart p95 − p5 d'au moins 0,55 (contraste conservé).
Indice : AgX (ou Khronos PBR Neutral, Filmic) comprime les hautes lumières ; l'exposition règle la moyenne.
Vérification : SCRIPTS/validate_ch09_06.py -- --exercise exposure
"""


def build(kind):
    L.reset("SC_EXPOSURE")
    sc = bpy.context.scene
    sc.render.engine = "CYCLES"
    sc.cycles.device = "CPU"
    sc.cycles.use_denoising = False
    vt, look, ex = {"starter": ("Standard", "None", 0.0), "solution": ("AgX", "None", 0.5), "standard_clipped": ("Standard", "None", 0.0), "too_dark": ("AgX", "None", -2.5),
                    "too_bright": ("AgX", "None", 3.0), "punchy_dark": ("AgX", "AgX - Punchy", 0.0)}[kind]
    sc.view_settings.view_transform, sc.view_settings.look, sc.view_settings.exposure = vt, look, ex
    wo = bpy.data.worlds.new("WO_Dark")
    wo.node_tree.nodes["Background"].inputs["Color"].default_value = (0.02, 0.02, 0.02, 1)
    sc.world = wo

    def mat(color, emit=0.0):
        m = bpy.data.materials.new("MAT")
        b = m.node_tree.nodes["Principled BSDF"]
        b.inputs["Base Color"].default_value = color
        b.inputs["Roughness"].default_value = 1.0
        if emit:
            b.inputs["Emission Color"].default_value = (1, 0.9, 0.7, 1)
            b.inputs["Emission Strength"].default_value = emit
        return m

    bm = bmesh.new()
    bmesh.ops.create_grid(bm, x_segments=1, y_segments=1, size=4)
    me = bpy.data.meshes.new("ME_Floor")
    bm.to_mesh(me)
    bm.free()
    fl = bpy.data.objects.new("Floor", me)
    sc.collection.objects.link(fl)
    fl.data.materials.append(mat((0.5, 0.5, 0.5, 1)))
    for name, col, emit, x in (("Bright", (0.8, 0.8, 0.8, 1), 6.0, 1.5), ("Dark", (0.02, 0.02, 0.02, 1), 0.0, -1.5), ("Mid", (0.5, 0.5, 0.5, 1), 0.0, 0.0)):
        bm = bmesh.new()
        bmesh.ops.create_uvsphere(bm, u_segments=32, v_segments=16, radius=0.6)
        me = bpy.data.meshes.new("ME_" + name)
        bm.to_mesh(me)
        bm.free()
        for p in me.polygons:
            p.use_smooth = True
        o = bpy.data.objects.new(name, me)
        sc.collection.objects.link(o)
        o.location = (x, 0, 0.6)
        o.data.materials.append(mat(col, emit))
    sun = bpy.data.lights.new("SUN", "SUN")
    sun.energy = 3.0
    so = bpy.data.objects.new("SUN", sun)
    sc.collection.objects.link(so)
    so.rotation_euler = (math.radians(50), 0, math.radians(30))
    cam = bpy.data.objects.new("CAM", bpy.data.cameras.new("CAM"))
    sc.collection.objects.link(cam)
    cam.location = (0, -6, 2.5)
    cam.rotation_euler = (math.radians(75), 0, 0)
    cam.data.lens = 35
    sc.camera = cam
    sc.frame_set(1)
    L.instructions(NOTE)


def render(res=96, samples=48):
    sc = bpy.context.scene
    sc.cycles.samples = samples
    sc.render.resolution_x = sc.render.resolution_y = res
    sc.render.resolution_percentage = 100
    sc.render.image_settings.file_format = "PNG"
    sc.render.image_settings.color_mode = "RGB"
    p = os.path.join(tempfile.gettempdir(), "bcma_ch0906.png")
    sc.render.filepath = p
    bpy.ops.render.render(write_still=True)
    im = bpy.data.images.load(p)
    px = np.array(im.pixels[:], np.float32).reshape(res, res, 4)[..., :3].copy()
    bpy.data.images.remove(im)
    return px


def stats(px):
    Y = px[..., 0] * 0.2126 + px[..., 1] * 0.7152 + px[..., 2] * 0.0722
    return float(Y.mean()), 100.0 * float((Y >= 0.99).mean()), float(np.percentile(Y, 95) - np.percentile(Y, 5))


def calibrate():
    for kind in ("starter", "solution", "standard_clipped", "too_dark", "too_bright", "punchy_dark"):
        build(kind)
        m, c, s = stats(render())
        print(f"[exp] {kind:17s} moyenne {m:.3f} brûlés {c:.1f}% écart {s:.2f}")


def sketch(path):
    W, H = 780, 270
    img = np.zeros((H, W, 3), np.float32)
    for i, kind in enumerate(("starter", "solution")):
        build(kind)
        px = render()
        big = np.kron(px, np.ones((2, 2, 1), np.float32))[::-1]
        img[30:222, 20 + i * 390:212 + i * 390, :] = big
        Y = px[..., 0] * 0.2126 + px[..., 1] * 0.7152 + px[..., 2] * 0.0722
        h, _ = np.histogram(Y, bins=32, range=(0, 1))
        h = h / max(h.max(), 1)
        for b in range(32):
            hh = int(40 * h[b])
            x0 = 220 + i * 390
            img[262 - hh:262, x0 + b * 5:x0 + b * 5 + 4, :] = (0.95, 0.6, 0.25) if i == 0 else (0.3, 0.7, 1.0)
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
    L.save(os.path.join(CH, "STARTER_FILES", "ch09_06_exposure_starter.blend"))
    for k in ("standard_clipped", "too_dark", "too_bright", "punchy_dark"):
        build(k)
        L.save(os.path.join(out, "COUNTER_EXAMPLES", f"ch09_06_exposure_{k}.blend"))
    sketch(os.path.join(out, "ch09_06_exposure_reference.png"))
    build("solution")
    L.save(os.path.join(out, "ch09_06_exposure_solution.blend"))


if __name__ == "__main__":
    L.run(main)
