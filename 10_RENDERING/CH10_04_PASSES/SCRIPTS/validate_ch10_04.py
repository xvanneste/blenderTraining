"""
validate_ch10_04.py — Correcteur « Passes, AOV, View Layers » (CH10.04).
Usage : … --python-exit-code 1 --python validate_ch10_04.py -- --exercise passes [--debug]
Objets : Hero (collection Hero, cube), Backdrop (collection Backdrop), KEY, FILL, CAM, matériau MA_Hero. Le correcteur contrôle des RÉGLAGES (calques, passes, groupes, AOV, sortie) et
RENDU RÉEL : il rend tous les calques en EXR multicouche temporaire (Cycles CPU, 64 × 36, 1 échantillon, sans débruitage ; le type de média est forcé en multicouche pour ce contrôle) et lit les NOMS DE CANAUX dans l'en-tête (multi-parties) :
  calques « FG » et « BG » ; FG : Depth.Z, Normal.X, Diffuse Color.R, Object Index.X, CryptoObject00.r, tint.R, Combined_key.R, Combined_fill.R ; BG : Depth.Z ;
  Hero.pass_index = 1 et Backdrop.pass_index = 2 ; KEY.lightgroup = key, FILL.lightgroup = fill ; nœud Shader AOV Output « tint » dans MA_Hero ;
  Backdrop exclu de FG, Hero exclu de BG ; réglage de sortie de l'élève : type de média multicouche et 16 bits.
Testé avec : Blender 5.3.0.
"""
import os
import struct
import sys
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bpy  # noqa: E402


def exr_channels(path):
    data = open(path, "rb").read()
    names, pos = [], 0
    while True:
        i = data.find(b"channels\x00chlist\x00", pos)
        if i < 0:
            break
        size = struct.unpack("<i", data[i + 16:i + 20])[0]
        blob, j = data[i + 20:i + 20 + size], 0
        while j < len(blob) and blob[j] != 0:
            k = blob.index(b"\x00", j)
            names.append(blob[j:k].decode())
            j = k + 1 + 16
        pos = i + 20 + size
    return names


def main():
    debug = L.flag("--debug")
    r = L.Report("CH10.04 — Passes, AOV, View Layers")
    O = bpy.data.objects
    if not r.check(all(O.get(n) for n in ("Hero", "Backdrop", "KEY", "FILL", "CAM")), "Hero, Backdrop, KEY, FILL et CAM présents", "Partez du fichier de départ.", 2):
        return r.finish()
    sc = bpy.context.scene
    names = [v.name for v in sc.view_layers]
    r.check("FG" in names and "BG" in names, f"Calques de vue : {names} (FG et BG attendus)", "Scene > View Layer : renommez le calque en FG et ajoutez BG (New).", 6)
    ims = sc.render.image_settings
    r.check(ims.media_type == "MULTI_LAYER_IMAGE" and ims.color_depth == "16", f"Sortie : type de média {ims.media_type}, profondeur {ims.color_depth} bits (OpenEXR multicouche, 16 bits)", "Output Properties > Output : multicouche, 16 bits.", 5)
    r.check(O["Hero"].pass_index == 1 and O["Backdrop"].pass_index == 2, f"Pass Index : Hero {O['Hero'].pass_index} (1), Backdrop {O['Backdrop'].pass_index} (2)", "Object Properties > Relations > Pass Index.", 5)
    r.check(O["KEY"].lightgroup == "key" and O["FILL"].lightgroup == "fill", f"Light Group des lampes : KEY « {O['KEY'].lightgroup} », FILL « {O['FILL'].lightgroup} »", "Object Properties > Shading > Light Group.", 5)
    mat = bpy.data.materials.get("MA_Hero")
    has_node = mat is not None and mat.node_tree is not None and any(n.bl_idname == "ShaderNodeOutputAOV" and n.aov_name == "tint" for n in mat.node_tree.nodes)
    r.check(has_node, "Nœud Shader AOV Output « tint » dans MA_Hero", "Ajoutez le nœud (Add > Output > AOV Output) et nommez l'AOV tint.", 5)
    if "FG" in names and "BG" in names:
        fg, bg = sc.view_layers["FG"], sc.view_layers["BG"]
        ex = fg.layer_collection.children["Backdrop"].exclude and not fg.layer_collection.children["Hero"].exclude and bg.layer_collection.children["Hero"].exclude and not bg.layer_collection.children["Backdrop"].exclude
        r.check(ex, "FG exclut Backdrop ; BG exclut Hero", "View Layer : cochez/décochez Exclude dans l'Outliner par calque.", 5)
    sc.render.engine = "CYCLES"
    sc.cycles.device = "CPU"
    sc.cycles.samples = 1
    sc.cycles.use_denoising = False
    sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage = 64, 36, 100
    p = os.path.join(tempfile.gettempdir(), "bcma_ch1004_val.exr")
    if os.path.exists(p):
        os.remove(p)
    keep = (ims.media_type, ims.file_format, ims.color_depth)
    ims.media_type = "MULTI_LAYER_IMAGE"
    sc.render.filepath = p
    bpy.ops.render.render(write_still=True)
    ims.media_type = keep[0]
    ch = exr_channels(p) if os.path.exists(p) else []
    if debug:
        print("[DEBUG]", len(ch), sorted({c.rsplit(".", 1)[0] for c in ch}))
    need = [("FG.Depth.Z", "Depth (Z)"), ("FG.Normal.X", "Normal"), ("FG.Diffuse Color.R", "Diffuse Color"), ("FG.Object Index.X", "Object Index"), ("FG.CryptoObject00.r", "Cryptomatte Object"),
            ("FG.tint.R", "AOV tint"), ("FG.Combined_key.R", "Light Group key"), ("FG.Combined_fill.R", "Light Group fill"), ("BG.Depth.Z", "BG : Depth (Z)")]
    for chan, label in need:
        r.check(chan in ch, f"Canal {chan} dans l'EXR ({label})", {"Normal": "View Layer Properties > Passes > Data > Normal.", "Depth (Z)": "Passes > Data > Z.", "Diffuse Color": "Passes > Light > Diffuse > Color.",
                "Object Index": "Passes > Data > Object Index.", "Cryptomatte Object": "Passes > Cryptomatte > Object.", "AOV tint": "Passes > Shader AOV : ajoutez tint (Color).",
                "Light Group key": "Passes > Light Groups : ajoutez key.", "Light Group fill": "Passes > Light Groups : ajoutez fill.", "BG : Depth (Z)": "Calque BG : Passes > Data > Z."}.get(label, ""), 4)
    return r.finish()


if __name__ == "__main__":
    L.run(main)
