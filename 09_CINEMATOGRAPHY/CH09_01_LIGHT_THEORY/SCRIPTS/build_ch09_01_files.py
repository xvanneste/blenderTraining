"""
build_ch09_01_files.py — « Théorie de la lumière » (CH09.01 : intensité, distance (inverse du carré), dureté de l'ombre, couleur).

Scène : Plate (plan de 6 × 6 m, gris 50 %, mat), Occluder (cube plat de 1 × 1 × 0,2 m à z = 1 m, qui projette une ombre), Camera (au-dessus, z = 6 m, regarde vers le bas, focale 50), monde noir (la seule lumière est LIGHT_Key), Cycles CPU, vue Standard.
  Référence : une lampe ponctuelle blanche de 10 W à 1 m du plan donne une luminance de 0,1004 (linéaire) au centre du plan (mesuré par le script ; voir REF_LUM).
  Consigne : déplacer LIGHT_Key à 3 m du plan en gardant la MÊME exposition au centre (luminance de la référence ± 20 %), adoucir l'ombre (Radius de 0,3 m ou plus ; 0,5 m recommandé), la réchauffer (rouge / bleu ≥ 1,25).
  Solution : LIGHT_Key point à z = 3 m, 100 W, Radius 0,5 m, couleur (1, 0,85, 0,65).
  Mesures : voir validate_ch09_01.py (deux rendus Cycles de 64 échantillons : plan seul, puis avec l'ombre de Occluder).
  STARTER_FILES/ch09_01_light_starter.blend : lampe blanche de 10 W à 1 m, Radius 0. COMPLETED_EXAMPLES/ch09_01_light_solution.blend (+ _reference.png : profil de l'ombre (hard, soft) et exposition)
  COUNTER_EXAMPLES/ : under_exposed (10 W à 3 m), over_exposed (400 W à 3 m), too_close (44 W à 2 m : bonne exposition, mauvaise distance), hard_shadow (Radius 0), cold_light (couleur bleue)
Usage : blender -b --factory-startup --python-exit-code 1 --python build_ch09_01_files.py
Testé avec : Blender 5.3.0.
"""
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
NOTE = """CH09.01 — THÉORIE DE LA LUMIÈRE (LIGHT_Key, Plate, Occluder)
Une lampe blanche de 10 W à 1 m du plan donne l'exposition de référence. Reculez la lampe à 3 m du plan SANS changer l'exposition, adoucissez l'ombre et réchauffez la lumière.
1. LIGHT_Key : Location Z = 3 (au-dessus du centre : X = Y = 0).
2. Power : l'éclairement varie comme l'INVERSE DU CARRÉ de la distance : 3 fois plus loin = 9 fois moins de lumière. Compensez (10 W × 9 = 90 W) et ajustez à l'œil pour la couleur chaude (100 W est un bon départ).
3. Radius : 0,5 m (une source plus grande = une ombre plus douce).
4. Color : chaud, par exemple rouge 1, vert 0,85, bleu 0,65.
Contrôles : lampe au-dessus du centre à 2,7–3,3 m ; luminance au centre du plan = celle de la référence ± 20 % ; pénombre de l'ombre d'au moins 5 pixels ; rouge / bleu ≥ 1,25.
Vérification : SCRIPTS/validate_ch09_01.py -- --exercise light
"""
REF_LUM = 0.1004  # luminance linéaire au centre : 10 W blanc à 1 m (mesurée par calibrate())


def box(name, size, loc):
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    for v in bm.verts:
        v.co = (v.co.x * size[0], v.co.y * size[1], v.co.z * size[2])
    me = bpy.data.meshes.new("ME_" + name)
    bm.to_mesh(me)
    bm.free()
    ob = bpy.data.objects.new(name, me)
    bpy.context.scene.collection.objects.link(ob)
    ob.location = loc
    return ob


def build(kind):
    L.reset("SC_LIGHT")
    sc = bpy.context.scene
    sc.render.engine = "CYCLES"
    sc.cycles.device = "CPU"
    sc.cycles.use_denoising = False
    sc.view_settings.view_transform = "Standard"
    sc.view_settings.look = "None"
    wo = bpy.data.worlds.new("WO_Black")
    wo.color = (0, 0, 0)
    wo.node_tree.nodes["Background"].inputs["Color"].default_value = (0, 0, 0, 1)  # sinon fond gris 0,05 qui éclaire le plan
    sc.world = wo
    bm = bmesh.new()
    bmesh.ops.create_grid(bm, x_segments=1, y_segments=1, size=3.0)
    me = bpy.data.meshes.new("ME_Plate")
    bm.to_mesh(me)
    bm.free()
    plate = bpy.data.objects.new("Plate", me)
    sc.collection.objects.link(plate)
    mat = bpy.data.materials.new("MAT_Plate")
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (0.5, 0.5, 0.5, 1)
    bsdf.inputs["Roughness"].default_value = 1.0
    plate.data.materials.append(mat)
    occ = box("Occluder", (1.0, 1.0, 0.2), (0, 0, 1.0))
    occ.visible_camera = False  # invisible à la caméra (elle est au-dessus) mais projette son ombre
    cam = bpy.data.objects.new("CAM", bpy.data.cameras.new("CAM"))
    sc.collection.objects.link(cam)
    cam.location = (0, 0, 6.0)
    cam.data.lens = 50
    sc.camera = cam
    d, power, radius, color = {"solution": (3.0, 100.0, 0.5, (1.0, 0.85, 0.65)), "under_exposed": (3.0, 10.0, 0.5, (1.0, 0.85, 0.65)), "over_exposed": (3.0, 400.0, 0.5, (1.0, 0.85, 0.65)),
                               "too_close": (2.0, 44.0, 0.5, (1.0, 0.85, 0.65)), "hard_shadow": (3.0, 100.0, 0.0, (1.0, 0.85, 0.65)), "cold_light": (3.0, 100.0, 0.5, (0.65, 0.85, 1.0)),
                               "starter": (1.0, 10.0, 0.0, (1.0, 1.0, 1.0))}[kind]
    ld = bpy.data.lights.new("LIGHT_Key", "POINT")
    ld.energy, ld.shadow_soft_size, ld.color = power, radius, color
    lo = bpy.data.objects.new("LIGHT_Key", ld)
    sc.collection.objects.link(lo)
    lo.location = (0, 0, d)
    lo.visible_camera = False
    sc.frame_set(1)
    L.instructions(NOTE)
    return lo


def render(res, samples, occluder):
    sc = bpy.context.scene
    sc.cycles.samples = samples
    sc.render.resolution_x = sc.render.resolution_y = res
    sc.render.resolution_percentage = 100
    bpy.data.objects["Occluder"].hide_render = not occluder
    sc.render.image_settings.file_format = "OPEN_EXR"
    sc.render.image_settings.color_depth = "32"
    p = os.path.join(tempfile.gettempdir(), "bcma_ch0901.exr")
    sc.render.filepath = p
    bpy.ops.render.render(write_still=True)
    im = bpy.data.images.load(p)
    px = np.array(im.pixels[:], np.float32).reshape(res, res, 4)[..., :3].copy()
    bpy.data.images.remove(im)
    return px


def lum(c):
    return float(0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2])


def measure():
    a = render(64, 64, False)
    c = a[28:36, 28:36].mean(axis=(0, 1))
    b = render(128, 64, True)
    row = b[60:68, :, :].mean(axis=0)
    y = row[:, 0] * 0.2126 + row[:, 1] * 0.7152 + row[:, 2] * 0.0722
    return c, y


def penumbra(y):
    """Largeur (pixels) de la transition 10 % → 90 % du bord gauche de l'ombre, sur un profil de luminance."""
    ys = np.convolve(y, np.ones(3) / 3, mode="same")
    hi, lo = float(np.median(ys[:12])), float(ys[48:80].min())
    if hi - lo < 1e-4:
        return 0
    t10, t90 = lo + 0.1 * (hi - lo), lo + 0.9 * (hi - lo)
    mid = int(np.argmin(ys[40:88])) + 40
    left = ys[:mid]
    i10 = int(np.where(left > t90)[0].max()) if (left > t90).any() else 0
    i90 = int(np.where(left < t10)[0].min()) if (left < t10).any() else mid
    return max(i90 - i10, 0)


def sketch(path):
    W, H = 780, 300
    img = np.full((H, W, 3), 0.08, np.float32)
    img[270, 20:W - 20] = (0.3, 0.3, 0.3)
    prof = {}
    for kind, col in (("solution", (0.95, 0.6, 0.25)), ("hard_shadow", (0.3, 0.7, 1.0))):
        build(kind)
        c, y = measure()
        prof[kind] = (y, c)
        top = max(float(np.max(y)), 1e-6)
        for x in range(128):
            yy = int(270 - 230 * y[x] / top)
            xx = int(30 + x * 5.6)
            img[max(yy - 2, 0):yy + 3, xx:xx + 5] = col
    rgba = np.concatenate([img, np.ones(img.shape[:2] + (1,), np.float32)], axis=2)
    out = bpy.data.images.new("sk", W, H)
    out.pixels = rgba[::-1].ravel()
    out.filepath_raw = path
    out.file_format = "PNG"
    out.save()
    print("[light] solution : couleur centre", np.round(prof["solution"][1], 4), "luminance", round(lum(prof["solution"][1]), 4), "pénombre", penumbra(prof["solution"][0]), "px ; ombre dure : pénombre", penumbra(prof["hard_shadow"][0]), "px")


def calibrate():
    build("starter")
    a = render(64, 64, False)
    c = a[28:36, 28:36].mean(axis=(0, 1))
    print("[light] référence (10 W blanc à 1 m) : luminance", round(lum(c), 5), "RGB", np.round(c, 5))
    for kind in ("solution", "under_exposed", "over_exposed", "too_close", "hard_shadow", "cold_light"):
        build(kind)
        cc, y = measure()
        print("[light]", kind, "lum", round(lum(cc), 5), "R/B", round(float(cc[0] / max(cc[2], 1e-9)), 2), "pénombre", penumbra(y))


def main():
    out = os.path.join(CH, "COMPLETED_EXAMPLES")
    calibrate()
    build("starter")
    L.save(os.path.join(CH, "STARTER_FILES", "ch09_01_light_starter.blend"))
    for k in ("under_exposed", "over_exposed", "too_close", "hard_shadow", "cold_light"):
        build(k)
        L.save(os.path.join(out, "COUNTER_EXAMPLES", f"ch09_01_light_{k}.blend"))
    build("solution")
    L.save(os.path.join(out, "ch09_01_light_solution.blend"))
    sketch(os.path.join(out, "ch09_01_light_reference.png"))
    build("solution")
    L.save(os.path.join(out, "ch09_01_light_solution.blend"))


if __name__ == "__main__":
    L.run(main)
