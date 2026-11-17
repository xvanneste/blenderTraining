"""
build_ch12_01_files.py — « Video Sequencer » (CH12.01 : strips, canaux, durées, montage bout à bout sans trou).

Scène (24 i/s, 64 × 36, Workbench, vue Standard) : quatre strips COLOR sur le canal 1 : A_red (rouge), B_green (vert), C_blue (bleu), D_yellow (jaune), aux durées et aux positions fausses.
  Départ : A_red 1–24 (24 images) ; B_green 30–70 (41 images, un trou de 5 images avant) ; C_blue 75–99 (25 images) ; D_yellow 110–139 (30 images) ; plage de la scène 1–139.
  Consigne : monter bout à bout SANS TROU NI RECOUVREMENT, sur le canal 1, dans l'ordre rouge, vert, bleu, jaune, avec les durées A 24, B 30, C 18, D 24 images (total 96) : A 1–24, B 25–54, C 55–72, D 73–96 ; plage de la scène 1–96.
  Mesures (voir validate_ch12_01.py) : données (frame_final_start, durée, canal) et RENDU du séquenceur à l'image 12 (rouge), 40 (vert), 63 (bleu) et 85 (jaune) : la couleur dominante du pixel central.
  STARTER_FILES/ch12_01_vse_starter.blend ; COMPLETED_EXAMPLES/ch12_01_vse_solution.blend (+ _reference.png : quatre images du montage)
  COUNTER_EXAMPLES/ : gap (trou de 5 images avant B), wrong_durations (B reste à 41 images), wrong_order (vert avant rouge), wrong_channel (C_blue sur le canal 2), frame_end (plage de la scène non réduite)
Usage : blender -b --factory-startup --python-exit-code 1 --python build_ch12_01_files.py
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
NOTE = """CH12.01 — VIDEO SEQUENCER (strips A_red, B_green, C_blue, D_yellow)
Quatre strips de couleur sont mal placés. Montez-les bout à bout, sans trou ni recouvrement, sur le canal 1, dans l'ordre rouge, vert, bleu, jaune :
A_red 24 images (1–24), B_green 30 images (25–54), C_blue 18 images (55–72), D_yellow 24 images (73–96). Plage de la scène : 1–96.
Outils : poignées de strip (durée), déplacer (G), propriétés du strip (Strip > Time : Channel, Start, Final Duration).
Vérification : SCRIPTS/validate_ch12_01.py -- --exercise vse
"""
COL = {"A_red": (1, 0, 0), "B_green": (0, 1, 0), "C_blue": (0, 0, 1), "D_yellow": (1, 1, 0)}
START = {"A_red": (1, 24, 1), "B_green": (30, 41, 1), "C_blue": (75, 25, 1), "D_yellow": (110, 30, 1)}  # début, durée, canal
GOOD = {"A_red": (1, 24, 1), "B_green": (25, 30, 1), "C_blue": (55, 18, 1), "D_yellow": (73, 24, 1)}


def build(kind):
    L.reset("SC_VSE")
    sc = bpy.context.scene
    sc.render.fps = 24
    sc.render.engine = "BLENDER_WORKBENCH"
    sc.view_settings.view_transform = "Standard"
    sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage = 64, 36, 100
    sc.render.use_sequencer = True
    se = sc.sequence_editor_create()
    plan = dict(GOOD if kind != "starter" else START)
    if kind == "gap":
        plan = {"A_red": (1, 24, 1), "B_green": (30, 30, 1), "C_blue": (60, 18, 1), "D_yellow": (78, 24, 1)}
    elif kind == "wrong_durations":
        plan = {"A_red": (1, 24, 1), "B_green": (25, 41, 1), "C_blue": (66, 18, 1), "D_yellow": (84, 24, 1)}
    elif kind == "wrong_order":
        plan = {"B_green": (1, 30, 1), "A_red": (31, 24, 1), "C_blue": (55, 18, 1), "D_yellow": (73, 24, 1)}
    elif kind == "wrong_channel":
        plan = dict(GOOD)
        plan["C_blue"] = (55, 18, 2)
    for name, (st, du, ch) in plan.items():
        s = se.strips.new_effect(name=name, type="COLOR", channel=ch, frame_start=st, length=du)
        s.color = COL[name]
    sc.frame_start = 1
    sc.frame_end = 139 if kind in ("starter", "frame_end") else 96
    sc.frame_set(1)
    L.instructions(NOTE)


def render(frame):
    sc = bpy.context.scene
    sc.frame_set(frame)
    sc.render.image_settings.file_format = "PNG"
    sc.render.image_settings.color_mode = "RGB"
    p = os.path.join(tempfile.gettempdir(), "bcma_ch1201.png")
    sc.render.filepath = p
    bpy.ops.render.render(write_still=True)
    im = bpy.data.images.load(p)
    px = np.array(im.pixels[:], np.float32).reshape(36, 64, 4)[..., :3][::-1].copy()
    bpy.data.images.remove(im)
    return px


def calibrate():
    for kind in ("starter", "solution", "gap", "wrong_durations", "wrong_order", "wrong_channel", "frame_end"):
        build(kind)
        se = bpy.context.scene.sequence_editor
        print("[vse]", kind, {s.name: (s.frame_final_start, s.frame_final_duration, s.channel) for s in se.strips_all}, "end", bpy.context.scene.frame_end,
              [tuple(render(f)[18, 32].round(1)) for f in (12, 40, 63, 85)])


def sketch(path):
    build("solution")
    tiles = [np.repeat(np.repeat(render(f), 4, axis=0), 4, axis=1) for f in (12, 40, 63, 85)]
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
    L.save(os.path.join(CH, "STARTER_FILES", "ch12_01_vse_starter.blend"))
    for k in ("gap", "wrong_durations", "wrong_order", "wrong_channel", "frame_end"):
        build(k)
        L.save(os.path.join(out, "COUNTER_EXAMPLES", f"ch12_01_vse_{k}.blend"))
    sketch(os.path.join(out, "ch12_01_vse_reference.png"))
    build("solution")
    L.save(os.path.join(out, "ch12_01_vse_solution.blend"))


if __name__ == "__main__":
    L.run(main)
