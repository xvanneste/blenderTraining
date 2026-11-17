"""
validate_ch10_06.py — Correcteur « EXR et couleur » (CH10.06).
Usage : … --python-exit-code 1 --python validate_ch10_06.py -- --exercise exr [--debug]
Objets : Panel (plan émissif, couleur (1 ; 0,5 ; 0,25), force 1000,7 : pixel central (1000,7 ; 500,35 ; 250,175)), CAM. Le correcteur lit les réglages de sortie de l'élève (type de média, profondeur, codec) puis écrit DEUX fichiers avec ces réglages :
  un EXR multicouche : canal ViewLayer.Combined.R en FLOAT (32 bits), canal ViewLayer.Depth.Z présent (passe Z) ;
  un EXR monocouche (mêmes profondeur et codec), relu par Blender : valeur centrale du canal rouge égale à 1000,7 à 0,05 près (32 bits ZIP/PIZ : 1000,700 ; 16 bits : 1000,5 ; DWAA : 1001,5).
  Réglage de l'élève : type de média multicouche.
La scène (Panel : force 1000,7) ne doit pas être modifiée.
Testé avec : Blender 5.3.0.
"""
import os
import struct
import sys
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bpy  # noqa: E402
import numpy as np  # noqa: E402


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


def main():
    debug = L.flag("--debug")
    r = L.Report("CH10.06 — EXR et couleur")
    if not r.check(bpy.data.objects.get("Panel") is not None and bpy.data.objects.get("CAM") is not None, "Panel et CAM présents", "Partez du fichier de départ.", 2):
        return r.finish()
    sc = bpy.context.scene
    emis = bpy.data.objects["Panel"].data.materials[0].node_tree.nodes["Emission"].inputs["Strength"].default_value
    r.check(abs(emis - 1000.7) < 1e-3, f"Scène inchangée : émission {emis:.1f}", "Réglez la sortie, pas la scène.", 3)
    s = sc.render.image_settings
    media, depth, codec = s.media_type, s.color_depth, s.exr_codec
    r.check(media == "MULTI_LAYER_IMAGE", f"Type de média : {media} (multicouche)", "Output Properties > Output : multicouche (OpenEXR MultiLayer).", 5)
    sc.render.engine = "CYCLES"
    sc.cycles.device = "CPU"
    sc.cycles.samples = 1
    sc.cycles.use_denoising = False
    sc.render.resolution_x = sc.render.resolution_y = 16
    # fichier multicouche aux réglages de l'élève (changer de type de média remet profondeur et codec par défaut : on les réapplique)
    s.media_type = "MULTI_LAYER_IMAGE"
    s.color_depth, s.exr_codec = depth, codec
    p1 = os.path.join(tempfile.gettempdir(), "bcma_ch1006_val_ml.exr")
    sc.render.filepath = p1
    bpy.ops.render.render(write_still=True)
    types = parse(p1)
    s.media_type = "IMAGE"
    s.file_format = "OPEN_EXR"
    s.color_depth, s.exr_codec = depth, codec
    p2 = os.path.join(tempfile.gettempdir(), "bcma_ch1006_val_sl.exr")
    sc.render.filepath = p2
    bpy.ops.render.render(write_still=True)
    im = bpy.data.images.load(p2)
    px = np.array(im.pixels[:], np.float32).reshape(-1, 4)
    val = float(px[len(px) // 2][0])
    bpy.data.images.remove(im)
    ct = types.get("ViewLayer.Combined.R", -1)
    r.check(ct == 2, f"Couleur de l'EXR multicouche : {'32 bits flottants' if ct == 2 else '16 bits' if ct == 1 else 'canal absent'} ; profondeur réglée : {depth}", "Output > Color Depth : Float (Full), 32 bits.", 8)
    r.check("ViewLayer.Depth.Z" in types, "Canal Depth.Z présent dans l'EXR multicouche", "View Layer Properties > Passes > Data > Z.", 6)
    r.check(abs(val - 1000.7) <= 0.05, f"Valeur HDR relue : {val:.3f} (1000,7 ± 0,05) ; codec {codec}, profondeur {depth}", "32 bits et un codec sans perte (ZIP, PIZ, RLE, ZIPS) : 16 bits et DWAA déforment les valeurs.", 8)
    if debug:
        print("[DEBUG] media", media, "depth", depth, "codec", codec, "types", {k: v for k, v in types.items() if k.endswith((".R", ".Z"))}, "val", val)
    return r.finish()


if __name__ == "__main__":
    L.run(main)
