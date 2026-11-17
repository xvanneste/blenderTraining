"""
build_ch09_03_files.py — « Naturel et HDRI » (CH09.03 : éclairer une scène par une image d'environnement à grande plage dynamique).

HDRI fournie : STARTER_FILES/ch09_03_sunset_hdri.exr — image équirectangulaire 256 × 128, flottante, GÉNÉRÉE par ce script (pas une photo) : ciel dégradé (horizon orangé, zénith bleu), sol sombre,
  soleil = disque de 2,5° de rayon, de couleur (1 ; 0,8 ; 0,6), de luminance 1 500 (la valeur d'un pixel de soleil est des milliers de fois celle du ciel : c'est ce qui fait une ombre nette).
Scène : Ground (dalle de 10 × 10 m, gris 50 %, mat), Pole (poteau de 0,2 × 0,2 × 1 m), caméra orthographique au zénith (z = 8 m, échelle 8 m) ; monde : Texture Coordinate (Generated) → Mapping → Environment Texture → Background → World Output.
  Mesures du script (rendu 128 × 128, 64 échantillons) : sans rotation le soleil est du côté +X : l'ombre du poteau part vers −X (angle 180°, longueur 2,56 m pour un soleil à 20° : attendu 2,75 m) ;
  rotation Z du Mapping de 180° → l'ombre part vers +X (angle 0°) ; Strength 1 → luminance médiane du sol 0,493 ; ombre bleutée (rouge / bleu 0,57 : seule la lumière du ciel l'éclaire).
  Consigne : tourner l'environnement pour que le soleil vienne de la GAUCHE (−X : l'ombre part vers +X, à ± 20°), et régler Strength pour une luminance médiane du sol de 0,35 à 0,7.
  Solution : rotation Z 180°, Strength 1. STARTER_FILES/ch09_03_natural_hdri_starter.blend : rotation 0°, Strength 0,3.
  COMPLETED_EXAMPLES/ch09_03_natural_hdri_solution.blend (+ _reference.png : vue du dessus : solution, rotation 90°)
  COUNTER_EXAMPLES/ : wrong_rotation (90°), too_dark (Strength 0,3), too_bright (Strength 3), no_hdri (fond gris uni), ldr_image (même image écrêtée en PNG 8 bits : le soleil n'est plus que 1)
Usage : blender -b --factory-startup --python-exit-code 1 --python build_ch09_03_files.py
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
NOTE = """CH09.03 — NATUREL ET HDRI (monde, Ground, Pole)
Le monde est éclairé par une image d'environnement HDRI (soleil à 20° au-dessus de l'horizon, ciel bleu, horizon orangé). Un poteau projette son ombre sur la dalle ; la caméra regarde du dessus.
1. Properties > World > (nœuds du monde, éditeur Shader Editor en mode World) : sélectionnez le nœud Mapping et réglez Rotation Z pour que le soleil vienne de la GAUCHE de l'image (l'ombre part vers la droite, +X). Indice : sans rotation l'ombre part vers la gauche.
2. Background > Strength : réglez la luminosité pour que le sol soit bien exposé (luminance médiane de 0,35 à 0,7 ; la valeur 1 donne 0,49).
Contrôles (un rendu Cycles de 128 × 128) : Environment Texture reliée au Background avec une image flottante (HDRI) ; ombre du poteau d'au moins 30 pixels, orientée vers +X à ± 20° ; luminance médiane du sol de 0,35 à 0,7 ; ombre bleutée (bleu / rouge ≥ 1,3).
Vérification : SCRIPTS/validate_ch09_03.py -- --exercise hdri
"""


def hdri_array():
    W, H = 256, 128
    u = (np.arange(W) + 0.5) / W
    v = (np.arange(H) + 0.5) / H
    PH, TH = np.meshgrid((u - 0.5) * 2 * math.pi, (v - 0.5) * math.pi)
    dx, dy, dz = -np.cos(PH) * np.cos(TH), np.sin(PH) * np.cos(TH), np.sin(TH)
    el = math.radians(20)
    s = np.array([-math.cos(el), 0.0, math.sin(el)])
    t = np.clip(dz, 0, 1)
    sky = (1 - t)[..., None] * np.array([1.0, 0.7, 0.5]) * 0.6 + t[..., None] * np.array([0.25, 0.45, 1.0]) * 0.8
    img = np.where(dz[..., None] >= 0, sky, np.array([0.08, 0.08, 0.08])).astype(np.float32)
    sun = (dx * s[0] + dy * s[1] + dz * s[2]) > math.cos(math.radians(2.5))
    img[sun] = np.array([1.0, 0.8, 0.6]) * 1500
    return img


def save_hdri(path):
    img = hdri_array()
    H, W = img.shape[:2]
    im = bpy.data.images.new("hdri_gen", W, H, float_buffer=True)
    im.pixels = np.concatenate([img, np.ones((H, W, 1), np.float32)], axis=2).ravel()
    im.filepath_raw = path
    im.file_format = "OPEN_EXR"
    im.save()
    bpy.data.images.remove(im)


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
    mat = bpy.data.materials.new("MAT_" + name)
    mat.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (0.5, 0.5, 0.5, 1)
    mat.node_tree.nodes["Principled BSDF"].inputs["Roughness"].default_value = 1.0
    ob.data.materials.append(mat)
    return ob


def build(kind):
    L.reset("SC_HDRI")
    sc = bpy.context.scene
    sc.render.engine = "CYCLES"
    sc.cycles.device = "CPU"
    sc.cycles.use_denoising = False
    sc.view_settings.view_transform = "Standard"
    sc.view_settings.look = "None"
    box("Ground", (10, 10, 0.1), (0, 0, -0.05))
    box("Pole", (0.2, 0.2, 1.0), (0, 0, 0.5))
    cam = bpy.data.objects.new("CAM", bpy.data.cameras.new("CAM"))
    sc.collection.objects.link(cam)
    cam.data.type = "ORTHO"
    cam.data.ortho_scale = 8.0
    cam.location = (0, 0, 8)
    sc.camera = cam
    rot, st = {"starter": (0, 0.3), "solution": (180, 1.0), "wrong_rotation": (90, 1.0), "too_dark": (180, 0.3), "too_bright": (180, 3.0), "no_hdri": (0, 1.0), "ldr_image": (180, 1.0)}[kind]
    wo = bpy.data.worlds.new("WO_HDRI")
    sc.world = wo
    nt = wo.node_tree
    for n in list(nt.nodes):
        nt.nodes.remove(n)
    out = nt.nodes.new("ShaderNodeOutputWorld")
    bg = nt.nodes.new("ShaderNodeBackground")
    bg.inputs["Strength"].default_value = st
    nt.links.new(bg.outputs["Background"], out.inputs["Surface"])
    if kind == "no_hdri":
        bg.inputs["Color"].default_value = (0.5, 0.5, 0.5, 1)
    else:
        et = nt.nodes.new("ShaderNodeTexEnvironment")
        mp = nt.nodes.new("ShaderNodeMapping")
        tc = nt.nodes.new("ShaderNodeTexCoord")
        mp.inputs["Rotation"].default_value[2] = math.radians(rot)
        if kind == "ldr_image":
            img = hdri_array()
            H, W = img.shape[:2]
            im = bpy.data.images.new("hdri_ldr", W, H, float_buffer=False)
            im.pixels = np.concatenate([np.clip(img, 0, 1) ** (1 / 2.2), np.ones((H, W, 1), np.float32)], axis=2).ravel()
            im.pack()
            et.image = im
        else:
            im = bpy.data.images.load(os.path.join(CH, "STARTER_FILES", "ch09_03_sunset_hdri.exr"))
            im.pack()
            et.image = im
        nt.links.new(tc.outputs["Generated"], mp.inputs["Vector"])
        nt.links.new(mp.outputs["Vector"], et.inputs["Vector"])
        nt.links.new(et.outputs["Color"], bg.inputs["Color"])
    sc.frame_set(1)
    L.instructions(NOTE)


def render(res=128, samples=64):
    sc = bpy.context.scene
    sc.cycles.samples = samples
    sc.render.resolution_x = sc.render.resolution_y = res
    sc.render.resolution_percentage = 100
    sc.render.image_settings.file_format = "OPEN_EXR"
    sc.render.image_settings.color_depth = "32"
    p = os.path.join(tempfile.gettempdir(), "bcma_ch0903.exr")
    sc.render.filepath = p
    bpy.ops.render.render(write_still=True)
    im = bpy.data.images.load(p)
    px = np.array(im.pixels[:], np.float32).reshape(res, res, 4)[..., :3].copy()
    bpy.data.images.remove(im)
    return px


def analyse(px):
    R = px.shape[0]
    Y = px[..., 0] * 0.2126 + px[..., 1] * 0.7152 + px[..., 2] * 0.0722
    med = float(np.median(Y))
    mask = Y < 0.5 * med
    mask[R // 2 - 3:R // 2 + 4, R // 2 - 3:R // 2 + 4] = False
    ys, xs = np.nonzero(mask)
    mpp = 8.0 / R
    n = len(xs)
    ang = math.degrees(math.atan2((ys.mean() - R / 2 + 0.5), (xs.mean() - R / 2 + 0.5))) if n else 999.0
    shd = px[mask].mean(axis=0) if n else np.zeros(3)
    return med, n, ang, float(shd[2] / max(shd[0], 1e-9)) if n else 0.0


def calibrate():
    for kind in ("solution", "starter", "wrong_rotation", "too_dark", "too_bright", "no_hdri", "ldr_image"):
        build(kind)
        med, n, ang, bR = analyse(render())
        print(f"[hdri] {kind:14s} médiane {med:.3f} ombre {n} px angle {ang:.1f}° bleu/rouge {bR:.2f}")


def sketch(path):
    W, H = 780, 270
    img = np.zeros((H, W, 3), np.float32)
    for i, kind in enumerate(("solution", "wrong_rotation")):
        build(kind)
        px = render()
        v = np.clip(px, 0, 1) ** (1 / 2.2)
        big = np.kron(v, np.ones((2, 2, 1), np.float32))[::-1]  # 256 × 256
        img[7:263, 20 + i * 300:276 + i * 300, :] = big
    rgba = np.concatenate([img, np.ones(img.shape[:2] + (1,), np.float32)], axis=2)
    out = bpy.data.images.new("sk", W, H)
    out.pixels = rgba[::-1].ravel()
    out.filepath_raw = path
    out.file_format = "PNG"
    out.save()


def main():
    out = os.path.join(CH, "COMPLETED_EXAMPLES")
    os.makedirs(os.path.join(CH, "STARTER_FILES"), exist_ok=True)
    save_hdri(os.path.join(CH, "STARTER_FILES", "ch09_03_sunset_hdri.exr"))
    calibrate()
    build("starter")
    L.save(os.path.join(CH, "STARTER_FILES", "ch09_03_natural_hdri_starter.blend"))
    for k in ("wrong_rotation", "too_dark", "too_bright", "no_hdri", "ldr_image"):
        build(k)
        L.save(os.path.join(out, "COUNTER_EXAMPLES", f"ch09_03_natural_hdri_{k}.blend"))
    sketch(os.path.join(out, "ch09_03_natural_hdri_reference.png"))
    build("solution")
    L.save(os.path.join(out, "ch09_03_natural_hdri_solution.blend"))


if __name__ == "__main__":
    L.run(main)
