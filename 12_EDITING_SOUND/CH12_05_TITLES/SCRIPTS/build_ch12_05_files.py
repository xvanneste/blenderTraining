"""
build_ch12_05_files.py — « Titres et sous-titres » (CH12.05 : strips de texte, carton-titre, sous-titres synchronisés, export SRT).

Scène (24 i/s, 320 × 180, Workbench, vue Standard, plage 1–120) : fond noir (strip COLOR « BG », canal 1, images 1–120), un texte « SUBTITLES.srt » (le fichier de sous-titres de référence, au format SRT) et des strips de texte (type TEXT).
  Contenu de référence (SRT) : 1 : 00:00:02,000 → 00:00:03,500 « Bonjour. » ; 2 : 00:00:03,750 → 00:00:05,000 « Il fait nuit. » (à 24 i/s : images 49 à 84 pour le premier, 91 à 120 pour le second ; l'image 1 = temps 0).
  Départ : un carton « TITRE » minuscule en haut à gauche ; deux strips de sous-titres FAUX (« Bonjour » sans point sur 40–70, « Il fait nuit » sans point sur 100–110) placés en haut de l'image.
  Consigne : (1) carton-titre : le strip « TITLE » dit « LE LONG VOYAGE », commence à l'image 1, dure 36 images (± 2), au CENTRE de l'image (anchor Center, location (0,5 ; 0,5)), taille de police ≥ 40 ;
    (2) sous-titres : deux strips (n'importe quels noms sauf TITLE) dont l'EXPORT SRT (Sequencer > Export Subtitles) donne exactement les textes de référence aux temps de référence à ± 2 images ;
    (3) position et lisibilité des sous-titres : dans le tiers INFÉRIEUR de l'image (location y ≤ 0,2), blancs, taille de police entre 20 et 40 ; rendu : au milieu du premier sous-titre, les pixels clairs ont leur centre dans le tiers inférieur et ≥ 150 pixels ;
    (4) rendu du titre à l'image 18 : centre des pixels clairs dans la zone centrale (35–65 % de la hauteur, 30–70 % de la largeur), ≥ 300 pixels clairs.
  Solution : TITLE « LE LONG VOYAGE » 1–36, taille 56 ; SUB1 « Bonjour. » 49–84 ; SUB2 « Il fait nuit. » 91–120 ; location (0,5 ; 0,1), taille 30.
  STARTER_FILES/ch12_05_titles_starter.blend ; COMPLETED_EXAMPLES/ch12_05_titles_solution.blend (+ _reference.png : titre, sous-titre 1, sous-titre 2 ; + ch12_05_titles_solution.srt : l'export du correcteur)
  COUNTER_EXAMPLES/ : typo (« Bonjour » sans point), late_sub (sous-titre 1 en retard de 12 images), top_sub (sous-titres en haut), tiny_title (titre taille 12), title_off_center (titre en bas à gauche)
Usage : blender -b --factory-startup --python-exit-code 1 --python build_ch12_05_files.py
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
SRT_REF = """1
00:00:02,000 --> 00:00:03,500
Bonjour.

2
00:00:03,750 --> 00:00:05,000
Il fait nuit.
"""
NOTE = """CH12.05 — TITRES ET SOUS-TITRES (strips de texte ; SUBTITLES.srt = référence)
1. Carton-titre : strip TITLE, texte « LE LONG VOYAGE », images 1–36 (± 2), centré (Anchor Center, location 0,5 / 0,5), taille ≥ 40.
2. Sous-titres : « Bonjour. » (2,000 s → 3,500 s) et « Il fait nuit. » (3,750 s → 5,000 s) : strips de texte aux images 49–84 et 91–120 ; Sequencer > Export Subtitles doit redonner ces textes et ces temps (± 2 images).
3. Sous-titres dans le tiers inférieur (location y ≤ 0,2), blancs, taille 20 à 40.
Vérification : SCRIPTS/validate_ch12_05.py -- --exercise titles
"""


def txt(se, name, text, start, end, size, loc, ch):
    s = se.strips.new_effect(name=name, type="TEXT", channel=ch, frame_start=start, length=end - start + 1)
    s.text = text
    s.font_size = size
    s.location = loc
    s.color = (1, 1, 1, 1)
    s.anchor_x, s.anchor_y = "CENTER", "CENTER"
    return s


def build(kind):
    L.reset("SC_TITLES")
    sc = bpy.context.scene
    sc.render.fps = 24
    sc.render.engine = "BLENDER_WORKBENCH"
    sc.view_settings.view_transform = "Standard"
    sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage = 320, 180, 100
    sc.render.use_sequencer = True
    sc.frame_start, sc.frame_end = 1, 120
    se = sc.sequence_editor_create()
    bg = se.strips.new_effect(name="BG", type="COLOR", channel=1, frame_start=1, length=120)
    bg.color = (0, 0, 0)
    t = bpy.data.texts.new("SUBTITLES.srt")
    t.write(SRT_REF)
    low, y = (0.5, 0.1), None
    if kind == "starter":
        txt(se, "TITLE", "TITRE", 1, 36, 14, (0.12, 0.9), 2)
        txt(se, "SUB1", "Bonjour", 40, 70, 30, (0.5, 0.9), 3)
        txt(se, "SUB2", "Il fait nuit", 100, 110, 30, (0.5, 0.9), 3)
    else:
        size = 12 if kind == "tiny_title" else 56
        loc = (0.12, 0.1) if kind == "title_off_center" else (0.5, 0.5)
        txt(se, "TITLE", "LE LONG VOYAGE", 1, 36, size, loc, 2)
        sub_loc = (0.5, 0.9) if kind == "top_sub" else (0.5, 0.1)
        s1 = (61, 96) if kind == "late_sub" else (49, 84)
        txt(se, "SUB1", "Bonjour" if kind == "typo" else "Bonjour.", s1[0], s1[1], 30, sub_loc, 3)
        txt(se, "SUB2", "Il fait nuit.", 91, 120, 30, sub_loc, 3)
    sc.frame_set(1)
    L.instructions(NOTE)


def export_srt():
    sc = bpy.context.scene
    se = sc.sequence_editor
    for s in se.strips_all:
        s.select = s.type == "TEXT"
    texts = [s for s in se.strips_all if s.type == "TEXT"]
    se.active_strip = texts[0]
    win = bpy.context.window_manager.windows[0]
    area = win.screen.areas[0]
    keep = area.type
    area.type = "SEQUENCE_EDITOR"
    sp = area.spaces.active
    reg = [r for r in area.regions if r.type == "WINDOW"][0]
    out = os.path.join(tempfile.gettempdir(), "bcma_ch1205.srt")
    if os.path.exists(out):
        os.remove(out)
    try:
        with bpy.context.temp_override(window=win, area=area, region=reg, space_data=sp, scene=sc, sequencer_scene=sc):
            bpy.ops.sequencer.export_subtitles(filepath=out)
    finally:
        area.type = keep
    return open(out, encoding="utf-8").read()


def render(frame):
    sc = bpy.context.scene
    sc.frame_set(frame)
    sc.render.image_settings.file_format = "PNG"
    sc.render.image_settings.color_mode = "RGB"
    p = os.path.join(tempfile.gettempdir(), "bcma_ch1205.png")
    sc.render.filepath = p
    bpy.ops.render.render(write_still=True)
    im = bpy.data.images.load(p)
    px = np.array(im.pixels[:], np.float32).reshape(180, 320, 4)[..., :3][::-1].copy()
    bpy.data.images.remove(im)
    return px


def stats(px):
    ys, xs = np.nonzero(px.max(axis=2) > 0.5)
    if len(xs) == 0:
        return {"n": 0}
    return {"n": int(len(xs)), "cx": float(xs.mean() / 320), "cy": float(ys.mean() / 180)}


def calibrate():
    for kind in ("starter", "solution", "typo", "late_sub", "top_sub", "tiny_title", "title_off_center"):
        build(kind)
        print("[ttl]", kind, "title", stats(render(18)), "sub", stats(render(66)))
        print("      srt", " | ".join(export_srt().replace("\n", " ").split("  ")))


def sketch(path):
    build("solution")
    tiles = [np.repeat(np.repeat(render(f), 2, axis=0), 2, axis=1) for f in (18, 66, 105)]
    img = np.concatenate(tiles, axis=1)
    rgba = np.concatenate([img, np.ones(img.shape[:2] + (1,), np.float32)], axis=2)
    out = bpy.data.images.new("sk", img.shape[1], img.shape[0])
    out.pixels = rgba[::-1].ravel()
    out.filepath_raw = path
    out.file_format = "PNG"
    out.save()
    open(os.path.join(os.path.dirname(path), "ch12_05_titles_solution.srt"), "w", encoding="utf-8").write(export_srt())


def main():
    out = os.path.join(CH, "COMPLETED_EXAMPLES")
    calibrate()
    build("starter")
    L.save(os.path.join(CH, "STARTER_FILES", "ch12_05_titles_starter.blend"))
    for k in ("typo", "late_sub", "top_sub", "tiny_title", "title_off_center"):
        build(k)
        L.save(os.path.join(out, "COUNTER_EXAMPLES", f"ch12_05_titles_{k}.blend"))
    sketch(os.path.join(out, "ch12_05_titles_reference.png"))
    build("solution")
    L.save(os.path.join(out, "ch12_05_titles_solution.blend"))


if __name__ == "__main__":
    L.run(main)
