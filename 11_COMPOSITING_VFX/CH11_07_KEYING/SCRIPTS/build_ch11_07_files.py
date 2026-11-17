"""
build_ch11_07_files.py — « Keying » (CH11.07 : incrustation sur fond vert : matte, nettoyage, contamination (spill), nouveau fond).

Scène (aucun objet 3D) : l'image « greenscreen » (160 × 90, 8 bits, générée par numpy et EMPAQUETÉE dans le .blend) : fond vert (0,10 ; 0,80 ; 0,15) avec un léger grain, un sujet elliptique (centre (80, 45), demi-axes 30 × 28 pixels) de couleur (0,75 ; 0,35 ; 0,30)
  dont le bord (4 pixels) est mélangé au vert (contour doux) et CONTAMINÉ par du vert (spill : le vert déborde sur le sujet à moins de 6 pixels du bord).
  Consigne (compositeur) : Image (greenscreen) → Keying (Key Color = le vert du fond) → [Color Spill, optionnel] → Alpha Over (Background = nœud RGB bleu (0,10 ; 0,20 ; 0,80), Foreground = le sujet détouré) → Group Output :
    1. fond remplacé : écart moyen des couleurs des quatre coins au bleu ≤ 0,08 ; 2. sujet conservé : écart de la couleur du centre du sujet à (0,75 ; 0,35 ; 0,30) ≤ 0,1 ;
    3. contamination retirée : sur l'anneau du sujet (d entre 0,86 et 0,95 : de 1,5 à 4 pixels à l'intérieur du bord), vert − (rouge + bleu)/2 ≤ 0,06 (départ : image brute, + 0,13) ; 4. aucun nœud orphelin, compositing activé.
  Départ : Image → Group Output (le fond vert). Solution : Image → Keying (Key Color vert) → Color Spill (canal G) → Alpha Over (fond bleu) → Group Output.
  STARTER_FILES/ch11_07_keying_starter.blend ; COMPLETED_EXAMPLES/ch11_07_keying_solution.blend (+ _reference.png : départ, solution)
  COUNTER_EXAMPLES/ : no_key (Alpha Over sans Keying), wrong_key_color (Key Color bleu), no_spill (Chroma Matte sans Color Spill : contamination restante), no_background (Keying seul : fond noir au lieu de bleu)
Usage : blender -b --factory-startup --python-exit-code 1 --python build_ch11_07_files.py
Testé avec : Blender 5.3.0.
"""
import os
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bpy  # noqa: E402
import numpy as np  # noqa: E402

CH = L.chapter_dir(__file__)
NOTE = """CH11.07 — KEYING (image greenscreen, nœuds Keying, Color Spill, Alpha Over)
Un sujet sur fond vert, avec du vert qui déborde sur ses bords (spill). Remplacez le fond par un bleu (0,10 ; 0,20 ; 0,80).
Arbre : Image → Keying (Key Color = (0,10 ; 0,80 ; 0,15)) → Color Spill (canal G, optionnel) → Alpha Over (Background = nœud RGB bleu, Foreground = le sujet) → Group Output.
Cible : quatre coins ≈ bleu (écart ≤ 0,08) ; centre du sujet ≈ (0,75 ; 0,35 ; 0,30) (écart ≤ 0,1) ; anneau du sujet sans vert : vert − (rouge + bleu)/2 ≤ 0,06 ; pas de nœud orphelin ; compositing activé.
Vérification : SCRIPTS/validate_ch11_07.py -- --exercise keying
"""
GREEN = (0.10, 0.80, 0.15)
SUBJ = (0.75, 0.35, 0.30)
BLUE = (0.10, 0.20, 0.80)  # couleur du nœud RGB (linéaire)
SBLUE = tuple(float(c) if False else (c * 12.92 if c <= 0.0031308 else 1.055 * c ** (1 / 2.4) - 0.055) for c in BLUE)  # sa valeur AFFICHÉE (Standard)


def make_image(path_name="greenscreen"):
    W, H = 160, 90
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    rng = np.random.RandomState(7)
    img = np.zeros((H, W, 3), np.float32)
    img[:] = GREEN
    img += rng.normal(0, 0.012, img.shape).astype(np.float32)
    d = np.sqrt(((xx - 80) / 30.0) ** 2 + ((yy - 45) / 28.0) ** 2)  # 1 au bord
    edge_px = 1.0 / 30.0 * 4  # ≈ 4 pixels en unités normalisées
    alpha = np.clip((1.0 - d) / edge_px + 0.5, 0, 1)  # bord doux
    subj = np.array(SUBJ, np.float32)[None, None, :] * np.ones((H, W, 1), np.float32)
    s = np.clip(1.0 - (1.0 - d) / (6.0 / 30.0), 0, 1) * (d < 1.0)  # 1 au bord, 0 à 6 pixels à l'intérieur
    spill_col = np.array((0.45, 0.75, 0.25), np.float32)  # le vert du fond déborde sur le sujet
    subj = subj * (1 - s[..., None]) + spill_col[None, None, :] * s[..., None]
    out = img * (1 - alpha[..., None]) + subj * alpha[..., None]
    out = np.clip(out, 0, 1)
    im = bpy.data.images.new(path_name, W, H, alpha=False)
    im.colorspace_settings.name = "sRGB"
    rgba = np.concatenate([out, np.ones((H, W, 1), np.float32)], axis=2)
    im.pixels = rgba[::-1].ravel().tolist()
    im.pack()
    return im


def build(kind):
    L.reset("SC_KEYING")
    sc = bpy.context.scene
    cam = bpy.data.objects.new("CAM", bpy.data.cameras.new("CAM"))
    sc.collection.objects.link(cam)
    sc.camera = cam
    sc.render.engine = "BLENDER_WORKBENCH"
    sc.view_settings.view_transform = "Standard"
    sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage = 160, 90, 100
    im = make_image()
    ng = bpy.data.node_groups.new("Comp", "CompositorNodeTree")
    sc.compositing_node_group = ng
    ng.interface.new_socket("Image", in_out="OUTPUT", socket_type="NodeSocketColor")
    ni = ng.nodes.new("CompositorNodeImage")
    ni.image = im
    ni.location = (-800, 0)
    out = ng.nodes.new("NodeGroupOutput")
    out.location = (600, 0)
    prev = ni.outputs["Image"]
    if kind != "starter":
        if kind == "no_spill":
            cm = ng.nodes.new("CompositorNodeChromaMatte")  # un matte SANS correction de contamination
            cm.location = (-500, 0)
            cm.inputs["Key Color"].default_value = (*GREEN, 1)
            ng.links.new(prev, cm.inputs["Image"])
            prev = cm.outputs["Image"]
        elif kind != "no_key":
            k = ng.nodes.new("CompositorNodeKeying")
            k.location = (-500, 0)
            k.inputs["Key Color"].default_value = (*BLUE, 1) if kind == "wrong_key_color" else (*GREEN, 1)
            ng.links.new(prev, k.inputs["Image"])
            prev = k.outputs["Image"]
        if kind not in ("no_spill", "no_key"):
            cs = ng.nodes.new("CompositorNodeColorSpill")
            cs.location = (-250, 0)
            ng.links.new(prev, cs.inputs["Image"])
            prev = cs.outputs["Image"]
        if kind != "no_background":
            bg = ng.nodes.new("CompositorNodeRGB")
            bg.location = (-250, -250)
            bg.outputs[0].default_value = (*BLUE, 1)
            ao = ng.nodes.new("CompositorNodeAlphaOver")
            ao.location = (100, 0)
            ng.links.new(bg.outputs[0], ao.inputs["Background"])
            ng.links.new(prev, ao.inputs["Foreground"])
            prev = ao.outputs["Image"]
    ng.links.new(prev, out.inputs[0])
    sc.render.use_compositing = True
    sc.frame_set(1)
    L.instructions(NOTE)


def render():
    sc = bpy.context.scene
    sc.render.image_settings.file_format = "PNG"
    sc.render.image_settings.color_mode = "RGB"
    p = os.path.join(tempfile.gettempdir(), "bcma_ch1107.png")
    sc.render.filepath = p
    bpy.ops.render.render(write_still=True)
    im = bpy.data.images.load(p)
    px = np.array(im.pixels[:], np.float32).reshape(90, 160, 4)[..., :3][::-1].copy()
    bpy.data.images.remove(im)
    return px


def measure(px=None):
    px = render() if px is None else px
    corners = np.concatenate([px[2:10, 2:10].reshape(-1, 3), px[2:10, 150:158].reshape(-1, 3), px[80:88, 2:10].reshape(-1, 3), px[80:88, 150:158].reshape(-1, 3)])
    bg_err = float(np.abs(corners.mean(axis=0) - np.array(SBLUE)).mean())
    subj_err = float(np.abs(px[40:50, 75:85].reshape(-1, 3).mean(axis=0) - np.array(SUBJ)).mean())
    yy, xx = np.mgrid[0:90, 0:160].astype(np.float32)
    d = np.sqrt(((xx - 80) / 30.0) ** 2 + ((yy - 45) / 28.0) ** 2)
    ring = (d > 0.86) & (d < 0.95)
    rp = px[ring]
    spill = float((rp[:, 1] - (rp[:, 0] + rp[:, 2]) / 2).mean())
    return {"bg_err": bg_err, "subj_err": subj_err, "spill": spill}


def calibrate():
    for kind in ("starter", "solution", "no_key", "wrong_key_color", "no_spill", "no_background"):
        build(kind)
        print("[key]", kind, {k: round(v, 4) for k, v in measure().items()})


def sketch(path):
    tiles = []
    for kind in ("starter", "solution"):
        build(kind)
        tiles.append(np.repeat(np.repeat(render(), 3, axis=0), 3, axis=1))
    img = np.concatenate(tiles, axis=1)
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
    L.save(os.path.join(CH, "STARTER_FILES", "ch11_07_keying_starter.blend"))
    for k in ("no_key", "wrong_key_color", "no_spill", "no_background"):
        build(k)
        L.save(os.path.join(out, "COUNTER_EXAMPLES", f"ch11_07_keying_{k}.blend"))
    sketch(os.path.join(out, "ch11_07_keying_reference.png"))
    build("solution")
    L.save(os.path.join(out, "ch11_07_keying_solution.blend"))


if __name__ == "__main__":
    L.run(main)
