"""
build_ch12_02_files.py — « Montage narratif » (CH12.02 : rythme, alternance des échelles de plan, résolution, fondu enchaîné).

Scène (24 i/s, 64 × 36, Workbench, vue Standard) : six « plans » (strips COLOR) : SH1_wide (rouge), SH2_medium (orange), SH3_close (jaune), SH4_medium (vert), SH5_close (cyan), SH6_wide (bleu). Le nom indique l'échelle de plan (wide, medium, close).
  Départ : bout à bout sur le canal 1 avec un rythme décousu : durées 10, 40, 10, 40, 10, 10 (SH1 1–10, SH2 11–50, SH3 51–60, SH4 61–100, SH5 101–110, SH6 111–120), aucune transition ; plage 1–120.
  Consigne : monter une séquence dont le rythme ACCÉLÈRE puis se résout, avec un fondu enchaîné final :
    1. ordre SH1 → SH6 (par le début) et aucune échelle identique deux plans de suite ;
    2. rythme : durées SH1 ≥ SH2 ≥ SH3 ≥ SH4 ≥ SH5 (le montage accélère) ; la résolution SH6 dure au moins 2 fois SH5 ;
    3. fondu enchaîné SH5 → SH6 : SH6 sur le canal 2, commençant avant la fin de SH5 (recouvrement de 8 à 16 images) ; un strip Crossfade (type CROSS) dont les entrées sont SH5 puis SH6 ;
    4. la plage de la scène se termine à la dernière image du montage ; total de 100 à 130 images.
    5. rendu : au milieu du fondu, la couleur est le mélange à 50 % du cyan de SH5 et du bleu de SH6 (écart ≤ 0,15).
  Solution : SH1 30 images (1–30), SH2 24 (31–54), SH3 18 (55–72), SH4 12 (73–84), SH5 12 (85–96) sur le canal 1 ; SH6 28 images sur le canal 2 de 85 à 112 ; Crossfade 85–96 (canal 3) ; plage 1–112.
  STARTER_FILES/ch12_02_editing_starter.blend ; COMPLETED_EXAMPLES/ch12_02_editing_solution.blend (+ _reference.png : durées en barres et trois images du fondu)
  COUNTER_EXAMPLES/ : jump_cut (SH3 et SH5, tous deux « close », se suivent), slow_rhythm (SH4 plus long que SH3), no_resolution (SH6 trop court), no_crossfade (SH6 enchaîné sec sur le canal 1), frame_end (plage non ajustée)
Usage : blender -b --factory-startup --python-exit-code 1 --python build_ch12_02_files.py
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
NOTE = """CH12.02 — MONTAGE NARRATIF (SH1_wide … SH6_wide)
Le rythme est décousu (10, 40, 10, 40, 10, 10 images). Montez une séquence qui ACCÉLÈRE puis se RÉSOUT :
1. Ordre SH1 → SH6 ; jamais deux plans de la même échelle (wide, medium, close) à la suite.
2. Durées : SH1 ≥ SH2 ≥ SH3 ≥ SH4 ≥ SH5 ; SH6 (la résolution) ≥ 2 × SH5.
3. Fondu enchaîné SH5 → SH6 : SH6 sur le canal 2, commençant 8 à 16 images avant la fin de SH5 ; sélectionnez SH5 puis SH6 : Add > Transition > Crossfade.
4. Plage de la scène : jusqu'à la dernière image du montage (100 à 130 images au total).
Vérification : SCRIPTS/validate_ch12_02.py -- --exercise editing
"""
LAST_OF = []
SHOTS = ["SH1_wide", "SH2_medium", "SH3_close", "SH4_medium", "SH5_close", "SH6_wide"]
COL = {"SH1_wide": (1, 0, 0), "SH2_medium": (1, 0.5, 0), "SH3_close": (1, 1, 0), "SH4_medium": (0, 1, 0), "SH5_close": (0, 1, 1), "SH6_wide": (0, 0, 1)}


def plans(kind):
    """{nom: (début, durée, canal)} et fondu éventuel (début, durée)."""
    cross = None
    LAST_OF.clear()
    if kind == "starter":
        d = [10, 40, 10, 40, 10, 10]
        p, t = {}, 1
        for n, k in zip(SHOTS, d):
            p[n] = (t, k, 1)
            t += k
        return p, None
    base = [("SH1_wide", 30), ("SH2_medium", 24), ("SH3_close", 18), ("SH4_medium", 12), ("SH5_close", 12)]
    order = [n for n, _ in base]
    dur = dict(base)
    if kind == "jump_cut":
        order = ["SH1_wide", "SH2_medium", "SH3_close", "SH5_close", "SH4_medium"]
    if kind == "slow_rhythm":
        dur["SH4_medium"] = 30
    p, t = {}, 1
    for n in order:
        p[n] = (t, dur[n], 1)
        t += dur[n]
    end5 = t  # première image après le dernier plan du canal 1
    LAST_OF.append(order[-1])
    if kind == "no_crossfade":
        p["SH6_wide"] = (end5, 28, 1)
        return p, None
    d6 = 22 if kind == "no_resolution" else 28
    p["SH6_wide"] = (end5 - 12, d6, 2)
    cross = (end5 - 12, 12)
    return p, cross


def build(kind):
    L.reset("SC_EDITING")
    sc = bpy.context.scene
    sc.render.fps = 24
    sc.render.engine = "BLENDER_WORKBENCH"
    sc.view_settings.view_transform = "Standard"
    sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage = 64, 36, 100
    sc.render.use_sequencer = True
    se = sc.sequence_editor_create()
    p, cross = plans(kind)
    S = {}
    for n, (st, du, ch) in p.items():
        s = se.strips.new_effect(name=n, type="COLOR", channel=ch, frame_start=st, length=du)
        s.color = COL[n]
        S[n] = s
    if cross:
        se.strips.new_effect(name="Crossfade", type="CROSS", channel=3, frame_start=cross[0], length=cross[1], input1=S[LAST_OF[0]], input2=S["SH6_wide"])
    last = max(s.frame_final_end for s in se.strips_all if s.type == "COLOR") - 1
    sc.frame_start = 1
    sc.frame_end = 120 if kind in ("starter", "frame_end") else last
    sc.frame_set(1)
    L.instructions(NOTE)


def render(frame):
    sc = bpy.context.scene
    sc.frame_set(frame)
    sc.render.image_settings.file_format = "PNG"
    sc.render.image_settings.color_mode = "RGB"
    pth = os.path.join(tempfile.gettempdir(), "bcma_ch1202.png")
    sc.render.filepath = pth
    bpy.ops.render.render(write_still=True)
    im = bpy.data.images.load(pth)
    px = np.array(im.pixels[:], np.float32).reshape(36, 64, 4)[..., :3][::-1].copy()
    bpy.data.images.remove(im)
    return px


def calibrate():
    for kind in ("starter", "solution", "jump_cut", "slow_rhythm", "no_resolution", "no_crossfade", "frame_end"):
        build(kind)
        se = bpy.context.scene.sequence_editor
        print("[edit]", kind, {s.name: (s.frame_final_start, s.frame_final_duration, s.channel) for s in se.strips_all}, "end", bpy.context.scene.frame_end)


def sketch(path):
    build("solution")
    tiles = [np.repeat(np.repeat(render(f), 4, axis=0), 4, axis=1) for f in (80, 90, 100)]
    bars = np.zeros((144, 256, 3), np.float32)
    se = bpy.context.scene.sequence_editor
    x = 4
    for n in SHOTS:
        s = se.strips_all[n] if hasattr(se.strips_all, "__getitem__") and False else next(t for t in se.strips_all if t.name == n)
        w = max(int(s.frame_final_duration * 2), 2)
        h = int(8 + s.frame_final_duration * 4)
        bars[144 - h:144, x:x + w - 1, :] = COL[n]
        x += w
    img = np.concatenate(tiles + [bars], axis=1)
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
    L.save(os.path.join(CH, "STARTER_FILES", "ch12_02_editing_starter.blend"))
    for k in ("jump_cut", "slow_rhythm", "no_resolution", "no_crossfade", "frame_end"):
        build(k)
        L.save(os.path.join(out, "COUNTER_EXAMPLES", f"ch12_02_editing_{k}.blend"))
    sketch(os.path.join(out, "ch12_02_editing_reference.png"))
    build("solution")
    L.save(os.path.join(out, "ch12_02_editing_solution.blend"))


if __name__ == "__main__":
    L.run(main)
