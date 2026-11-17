"""
build_ch10_06_files.py — « EXR et couleur » (CH10.06 : OpenEXR multicouche, profondeur de bits, compression sans perte, valeurs HDR).

Scène (Cycles CPU, 16 × 16, 1 échantillon) : Panel (plan émissif orange de 10 m en face de la caméra : couleur (1 ; 0,5 ; 0,25), force 1000,7) : le pixel central vaut exactement (1000,7 ; 500,35 ; 250,175) en lumière linéaire ; CAM à l'origine regardant vers +Y ; monde noir.
  Une valeur HDR de 1000 est typique d'un soleil ou d'une lampe dans le cadre : elle révèle la précision du format.
  Consigne (Output Properties) : produire un EXR « master » pour le compositing : (1) multicouche (media_type MULTI_LAYER_IMAGE) ; (2) 32 bits flottants ; (3) codec SANS perte visible ; (4) passe Z (Depth) activée dans le calque.
  Mesures (voir validate_ch10_06.py) : le correcteur écrit un EXR multicouche (canaux : couleur en FLOAT, Depth.Z présent) et relit un EXR monocouche aux MÊMES réglages (profondeur et codec) : la valeur centrale doit être égale à 1000,7 à 0,05 près
    (mesuré : 32 bits ZIP 1000,700 ; PIZ 1000,700 ; PXR24 1000,703 ; 16 bits 1000,5 ; DWAA 1001,5).
  Départ : monocouche (media_type IMAGE, OPEN_EXR), 16 bits, codec DWAA (avec perte), pas de passe Z. Solution : multicouche, 32 bits, ZIP, passe Z.
  STARTER_FILES/ch10_06_exr_starter.blend ; COMPLETED_EXAMPLES/ch10_06_exr_solution.blend (+ _reference.png : tableau des erreurs mesurées par réglage)
  COUNTER_EXAMPLES/ : half_float (16 bits), lossy_codec (DWAA), single_layer (EXR monocouche), no_z_pass (passe Z désactivée)
Usage : blender -b --factory-startup --python-exit-code 1 --python build_ch10_06_files.py
Testé avec : Blender 5.3.0.
"""
import math
import os
import struct
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bpy  # noqa: E402
import numpy as np  # noqa: E402

CH = L.chapter_dir(__file__)
NOTE = """CH10.06 — EXR ET COULEUR (Panel, CAM)
Un plan émissif de valeur 1000,7 (HDR) : le pixel central est (1000,7 ; 500,35 ; 250,175). Produisez un EXR « master » pour le compositing.
Output Properties > Output : Media Type = multicouche (OpenEXR MultiLayer) ; profondeur de couleur : 32 (Float) ; codec : sans perte (ZIP, PIZ, RLE, ZIPS…) — pas DWAA/DWAB/HTJ2K.
View Layer Properties > Passes > Data : Z (Depth).
Vérification : SCRIPTS/validate_ch10_06.py -- --exercise exr
Le correcteur contrôle la valeur relue dans un EXR monocouche aux mêmes réglages (1000,7 à 0,05 près) et le contenu de l'EXR multicouche (canaux en 32 bits, Depth.Z).
L'espace colorimétrique de l'EXR (Linear Rec.709) n'est pas évalué ici.
"""


def parse(path):
    d = open(path, "rb").read()
    types, pos = {}, 0
    while True:
        i = d.find(b"channels\x00chlist\x00", pos)
        if i < 0:
            break
        size = struct.unpack("<i", d[i + 16:i + 20])[0]
        blob, j = d[i + 20:i + 20 + size], 0
        while j < len(blob) and blob[j] != 0:
            k = blob.index(b"\x00", j)
            types[blob[j:k].decode()] = struct.unpack("<i", blob[k + 1:k + 5])[0]
            j = k + 1 + 16
        pos = i + 20 + size
    return types


def build(kind):
    L.reset("SC_EXR")
    sc = bpy.context.scene
    bpy.ops.mesh.primitive_plane_add(size=10, location=(0, 5, 0), rotation=(math.radians(90), 0, 0))
    pl = bpy.context.object
    pl.name = "Panel"
    m = bpy.data.materials.new("MA_Panel")
    nt = m.node_tree
    for n in list(nt.nodes):
        nt.nodes.remove(n)
    e = nt.nodes.new("ShaderNodeEmission")
    e.inputs["Color"].default_value = (1, 0.5, 0.25, 1)
    e.inputs["Strength"].default_value = 1000.7
    o = nt.nodes.new("ShaderNodeOutputMaterial")
    nt.links.new(e.outputs[0], o.inputs[0])
    pl.data.materials.append(m)
    cam = bpy.data.objects.new("CAM", bpy.data.cameras.new("CAM"))
    sc.collection.objects.link(cam)
    cam.rotation_euler = (math.radians(90), 0, 0)
    sc.camera = cam
    wo = bpy.data.worlds.new("WO_Black")
    sc.world = wo
    wo.node_tree.nodes["Background"].inputs["Color"].default_value = (0, 0, 0, 1)
    sc.render.engine = "CYCLES"
    sc.cycles.device = "CPU"
    sc.cycles.samples = 1
    sc.cycles.use_denoising = False
    sc.view_settings.view_transform = "Standard"
    sc.render.resolution_x = sc.render.resolution_y = 16
    s = sc.render.image_settings
    depth, codec, multilayer, zpass = {"starter": ("16", "DWAA", False, False), "solution": ("32", "ZIP", True, True), "half_float": ("16", "ZIP", True, True), "lossy_codec": ("32", "DWAA", True, True),
                                       "single_layer": ("32", "ZIP", False, True), "no_z_pass": ("32", "ZIP", True, False)}[kind]
    if multilayer:
        s.media_type = "MULTI_LAYER_IMAGE"
    else:
        s.media_type = "IMAGE"
        s.file_format = "OPEN_EXR"
    s.color_depth, s.exr_codec = depth, codec
    sc.view_layers[0].use_pass_z = zpass
    sc.frame_set(1)
    L.instructions(NOTE)


def center(path):
    im = bpy.data.images.load(path)
    px = np.array(im.pixels[:], np.float32).reshape(-1, 4)
    v = px[len(px) // 2]
    bpy.data.images.remove(im)
    return float(v[0]), float(v[1]), float(v[2])


def measure():
    sc = bpy.context.scene
    s = sc.render.image_settings
    keep = (s.media_type, s.file_format, s.color_depth, s.exr_codec)
    p1 = os.path.join(tempfile.gettempdir(), "bcma_ch1006_ml.exr")
    s.media_type = "MULTI_LAYER_IMAGE"
    s.color_depth, s.exr_codec = keep[2], keep[3]  # changer de type de média remet la profondeur et le codec par défaut
    sc.render.filepath = p1
    bpy.ops.render.render(write_still=True)
    types = parse(p1)
    s.media_type = "IMAGE"
    s.file_format = "OPEN_EXR"
    s.color_depth, s.exr_codec = keep[2], keep[3]
    p2 = os.path.join(tempfile.gettempdir(), "bcma_ch1006_sl.exr")
    sc.render.filepath = p2
    bpy.ops.render.render(write_still=True)
    v = center(p2)
    s.media_type = keep[0]
    if keep[0] == "IMAGE":
        s.file_format = keep[1]
    s.color_depth, s.exr_codec = keep[2], keep[3]
    return {"color_type": types.get("ViewLayer.Combined.R", -1), "has_depth": "ViewLayer.Depth.Z" in types, "value": v[0], "err": abs(v[0] - 1000.7)}


def calibrate():
    for kind in ("starter", "solution", "half_float", "lossy_codec", "single_layer", "no_z_pass"):
        build(kind)
        print("[exr]", kind, {k: (round(v, 4) if not isinstance(v, (bool, int)) else v) for k, v in measure().items()}, "media", bpy.context.scene.render.image_settings.media_type)


def sketch(path):
    rows = []
    for depth, codec in (("32", "ZIP"), ("32", "PIZ"), ("32", "PXR24"), ("16", "ZIP"), ("32", "DWAA")):
        build("solution")
        s = bpy.context.scene.render.image_settings
        s.color_depth, s.exr_codec = depth, codec
        rows.append((depth, codec, measure()["err"]))
        print("[exr-table]", depth, codec, round(rows[-1][2], 4))
    W, H = 600, 260
    img = np.full((H, W, 3), 0.1, np.float32)
    mx = max(r[2] for r in rows) or 1.0
    for i, (d, c, e) in enumerate(rows):
        y = 20 + i * 45
        n = int(500 * (e / mx))
        img[y:y + 30, 20:20 + max(n, 2), :] = (0.8, 0.3, 0.3) if e > 0.05 else (0.3, 0.8, 0.4)
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
    L.save(os.path.join(CH, "STARTER_FILES", "ch10_06_exr_starter.blend"))
    for k in ("half_float", "lossy_codec", "single_layer", "no_z_pass"):
        build(k)
        L.save(os.path.join(out, "COUNTER_EXAMPLES", f"ch10_06_exr_{k}.blend"))
    sketch(os.path.join(out, "ch10_06_exr_reference.png"))
    build("solution")
    L.save(os.path.join(out, "ch10_06_exr_solution.blend"))


if __name__ == "__main__":
    L.run(main)
