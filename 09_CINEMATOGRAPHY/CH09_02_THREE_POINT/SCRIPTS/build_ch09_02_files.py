"""
build_ch09_02_files.py — « Trois points et variantes » (CH09.02 : key, fill, rim sur une sphère grise, ratio key : fill).

Scène : Subject (UV sphère de 1 m de rayon, gris 50 % mat) à l'origine ; CAM à (0, −4,5, 0), focale 50, regarde le sujet ; monde noir ; trois lampes de zone (Area, carrées, 1,5 m) visant EMP_Target (Track To) :
  LIGHT_Key  à (−3, −3, 2,5)  : côté gauche de l'image, devant, au-dessus ;
  LIGHT_Fill à ( 3, −3, 0,5)  : côté droit, devant, bas ;
  LIGHT_Rim  à ( 0, 1,5, 4,5) : derrière le sujet, très haut (contre-jour : à (0, 3, 3) elle n'éclairait presque pas le bord visible).
  Solution : Key 250 W, Fill 35 W, Rim 300 W (valeurs mesurées par calibrate()).
  Le correcteur rend 3 images Cycles 96 × 96 (toutes les lampes ; sans Rim ; sans Fill) et lit des zones du sujet : flanc éclairé (gauche), flanc d'ombre (droit), bande du haut (contre-jour).
  STARTER_FILES/ch09_02_three_point_starter.blend : Key 100 W, Fill 100 W, Rim 0 W (éclairage plat sans contre-jour).
  COMPLETED_EXAMPLES/ch09_02_three_point_solution.blend (+ _reference.png : le sujet rendu avec Key seul, Key + Fill, Key + Fill + Rim)
  COUNTER_EXAMPLES/ : flat (Fill 150 W), no_fill (Fill 0 W), no_rim (Rim 0 W), key_on_right (Key à droite)
Usage : blender -b --factory-startup --python-exit-code 1 --python build_ch09_02_files.py
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
NOTE = """CH09.02 — TROIS POINTS (Subject, LIGHT_Key, LIGHT_Fill, LIGHT_Rim)
Éclairez la sphère en trois points : la Key (lumière principale, à gauche devant), la Fill (déboucheur côté opposé, plus faible) et la Rim (contre-jour qui détache le sujet du fond).
1. Power de chaque lampe : la Key domine ; la Fill déboucle l'ombre sans l'effacer (ratio Key : Fill de 2 : 1 à 5 : 1 sur le sujet) ; la Rim dessine le bord haut.
2. Ne déplacez pas les lampes : seules les puissances (Power) sont à régler (Key 250 W, Fill 35 W, Rim 300 W est une bonne réponse).
Contrôles (3 rendus de 96 × 96) : flanc éclairé / flanc d'ombre entre 2 et 5 ; la Fill éclaire le flanc d'ombre (au moins 20 % de sa luminance) ; la Rim éclaire la bande du haut (sa contribution au moins 40 % de la luminance de cette bande et au moins 0,02) ; la Key est la lampe la plus puissante.
Vérification : SCRIPTS/validate_ch09_02.py -- --exercise three_point
"""


def build(kind):
    L.reset("SC_THREEPOINT")
    sc = bpy.context.scene
    sc.render.engine = "CYCLES"
    sc.cycles.device = "CPU"
    sc.cycles.use_denoising = False
    sc.view_settings.view_transform = "Standard"
    sc.view_settings.look = "None"
    wo = bpy.data.worlds.new("WO_Black")
    wo.color = (0, 0, 0)
    wo.node_tree.nodes["Background"].inputs["Color"].default_value = (0, 0, 0, 1)
    sc.world = wo
    bm = bmesh.new()
    bmesh.ops.create_uvsphere(bm, u_segments=48, v_segments=24, radius=1.0)
    me = bpy.data.meshes.new("ME_Subject")
    bm.to_mesh(me)
    bm.free()
    for p in me.polygons:
        p.use_smooth = True
    sub = bpy.data.objects.new("Subject", me)
    sc.collection.objects.link(sub)
    mat = bpy.data.materials.new("MAT_Subject")
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (0.5, 0.5, 0.5, 1)
    bsdf.inputs["Roughness"].default_value = 1.0
    sub.data.materials.append(mat)
    tgt = bpy.data.objects.new("EMP_Target", None)
    sc.collection.objects.link(tgt)
    cam = bpy.data.objects.new("CAM", bpy.data.cameras.new("CAM"))
    sc.collection.objects.link(cam)
    cam.location = (0, -4.5, 0)
    cam.rotation_euler = (math.radians(90), 0, 0)
    cam.data.lens = 50
    sc.camera = cam
    kx = 3.0 if kind == "key_on_right" else -3.0
    pw = {"solution": (250, 35, 300), "starter": (100, 100, 0), "flat": (250, 150, 300), "no_fill": (250, 0, 300), "no_rim": (250, 35, 0), "key_on_right": (250, 35, 300)}[kind]
    for name, loc, w in (("LIGHT_Key", (kx, -3, 2.5), pw[0]), ("LIGHT_Fill", (-kx, -3, 0.5), pw[1]), ("LIGHT_Rim", (0, 1.5, 4.5), pw[2])):
        ld = bpy.data.lights.new(name, "AREA")
        ld.shape, ld.size, ld.energy = "SQUARE", 1.5, w
        lo = bpy.data.objects.new(name, ld)
        sc.collection.objects.link(lo)
        lo.location = loc
        lo.visible_camera = False
        c = lo.constraints.new("TRACK_TO")
        c.target, c.track_axis, c.up_axis = tgt, "TRACK_NEGATIVE_Z", "UP_Y"
    sc.frame_set(1)
    L.instructions(NOTE)
    return sub


def render(res=96, samples=48, hide=()):
    sc = bpy.context.scene
    sc.cycles.samples = samples
    sc.render.resolution_x = sc.render.resolution_y = res
    sc.render.resolution_percentage = 100
    for n in ("LIGHT_Key", "LIGHT_Fill", "LIGHT_Rim"):
        bpy.data.objects[n].hide_render = n in hide
    sc.render.image_settings.file_format = "OPEN_EXR"
    sc.render.image_settings.color_depth = "32"
    p = os.path.join(tempfile.gettempdir(), "bcma_ch0902.exr")
    sc.render.filepath = p
    bpy.ops.render.render(write_still=True)
    im = bpy.data.images.load(p)
    px = np.array(im.pixels[:], np.float32).reshape(res, res, 4)[..., :3].copy()
    bpy.data.images.remove(im)
    return px[..., 0] * 0.2126 + px[..., 1] * 0.7152 + px[..., 2] * 0.0722


def zones(Y):
    """Luminance moyenne du flanc gauche (éclairé), du flanc droit (ombre) et de la bande du haut (contre-jour) du sujet. Lignes de l'EXR : de BAS en HAUT."""
    c = Y.shape[0] // 2
    lit = Y[c - 8:c + 8, c - 25:c - 10].mean()
    shd = Y[c - 8:c + 8, c + 10:c + 25].mean()
    top = Y[c + 22:c + 27, c - 8:c + 8].mean()
    return float(lit), float(shd), float(top)


def calibrate():
    for kind in ("solution", "starter", "flat", "no_fill", "no_rim", "key_on_right"):
        build(kind)
        a = zones(render())
        nr = zones(render(hide=("LIGHT_Rim",)))
        nf = zones(render(hide=("LIGHT_Fill",)))
        print(f"[3pt] {kind:13s} lit {a[0]:.4f} shade {a[1]:.4f} ratio {a[0] / max(a[1], 1e-9):.2f} | top {a[2]:.4f} (sans rim {nr[2]:.4f}, part rim {(a[2] - nr[2]) / max(a[2], 1e-9):.2f}) | part fill sur l'ombre {(a[1] - nf[1]) / max(a[1], 1e-9):.2f}")


def sketch(path):
    W, H = 780, 270
    img = np.zeros((H, W, 3), np.float32)
    build("solution")
    panels = [render(hide=("LIGHT_Fill", "LIGHT_Rim")), render(hide=("LIGHT_Rim",)), render()]
    peak = max(float(p.max()) for p in panels)
    for i, Y in enumerate(panels):
        big = np.kron(Y, np.ones((2, 2), np.float32))  # 192 × 192
        v = np.clip(big / peak, 0, 1) ** (1 / 2.2)
        y0, x0 = 39, 20 + i * 255
        img[y0:y0 + 192, x0:x0 + 192, :] = v[::-1][..., None]
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
    L.save(os.path.join(CH, "STARTER_FILES", "ch09_02_three_point_starter.blend"))
    for k in ("flat", "no_fill", "no_rim", "key_on_right"):
        build(k)
        L.save(os.path.join(out, "COUNTER_EXAMPLES", f"ch09_02_three_point_{k}.blend"))
    sketch(os.path.join(out, "ch09_02_three_point_reference.png"))
    build("solution")
    L.save(os.path.join(out, "ch09_02_three_point_solution.blend"))


if __name__ == "__main__":
    L.run(main)
