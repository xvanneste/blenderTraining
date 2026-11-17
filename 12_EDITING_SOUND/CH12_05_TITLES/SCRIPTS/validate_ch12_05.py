"""
validate_ch12_05.py — Correcteur « Titres et sous-titres » (CH12.05).
Usage : … --python-exit-code 1 --python validate_ch12_05.py -- --exercise titles [--debug]
Données : fond noir (strip COLOR BG), strips de texte (type TEXT), 24 i/s, 320 × 180, plage 1–120. Le correcteur lit les strips, EXPORTE les sous-titres en SRT avec l'opérateur du Sequencer (bpy.ops.sequencer.export_subtitles : constaté, il exporte TOUS les strips de texte, y compris le titre : le correcteur ignore l'entrée du titre), compare à la référence et rend (Workbench, Standard) :
  titre : strip « TITLE » de texte « LE LONG VOYAGE », début à l'image 1 (± 2), durée 36 images (± 2), taille de police ≥ 40 ; rendu à l'image 18 : au moins 1 500 pixels clairs (> 0,5), de centre dans 30–70 % de la largeur et 35–65 % de la hauteur ;
  sous-titres (SRT exporté) : exactement deux entrées : « Bonjour. » de 2,000 s à 3,500 s et « Il fait nuit. » de 3,750 s à 5,000 s, à ± 2 images (0,0833 s) ;
  lisibilité : location y ≤ 0,2, couleur blanche (≥ 0,9), taille de police de 20 à 40 pour les sous-titres ; rendu au milieu du premier sous-titre : au moins 150 pixels clairs, de centre dans le tiers inférieur de l'image (≥ 66 % de la hauteur).
Testé avec : Blender 5.3.0.
"""
import os
import re
import sys
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bpy  # noqa: E402
import numpy as np  # noqa: E402

REF = [("Bonjour.", 2.0, 3.5), ("Il fait nuit.", 3.75, 5.0)]
FPS = 24.0


def parse_srt(s):
    out = []
    for blk in re.split(r"\n\s*\n", s.strip()):
        lines = [l for l in blk.strip().splitlines() if l.strip()]
        if len(lines) < 3:
            continue
        m = re.match(r"(\d+):(\d+):(\d+),(\d+) --> (\d+):(\d+):(\d+),(\d+)", lines[1])
        if not m:
            continue
        g = [int(v) for v in m.groups()]
        out.append((" ".join(lines[2:]), g[0] * 3600 + g[1] * 60 + g[2] + g[3] / 1000.0, g[4] * 3600 + g[5] * 60 + g[6] + g[7] / 1000.0))
    return out


def export_srt(sc, subs):
    se = sc.sequence_editor
    for s in se.strips_all:
        s.select = s in subs
    se.active_strip = subs[0]
    win = bpy.context.window_manager.windows[0]
    area = win.screen.areas[0]
    keep = area.type
    area.type = "SEQUENCE_EDITOR"
    sp = area.spaces.active
    reg = [r for r in area.regions if r.type == "WINDOW"][0]
    out = os.path.join(tempfile.gettempdir(), "bcma_ch1205_val.srt")
    if os.path.exists(out):
        os.remove(out)
    try:
        with bpy.context.temp_override(window=win, area=area, region=reg, space_data=sp, scene=sc, sequencer_scene=sc):
            bpy.ops.sequencer.export_subtitles(filepath=out)
    finally:
        area.type = keep
    return open(out, encoding="utf-8").read()


def render(sc, frame):
    sc.frame_set(frame)
    p = os.path.join(tempfile.gettempdir(), "bcma_ch1205_val.png")
    sc.render.filepath = p
    bpy.ops.render.render(write_still=True)
    im = bpy.data.images.load(p)
    px = np.array(im.pixels[:], np.float32).reshape(180, 320, 4)[..., :3][::-1].copy()
    bpy.data.images.remove(im)
    ys, xs = np.nonzero(px.max(axis=2) > 0.5)
    return (len(xs), float(xs.mean() / 320), float(ys.mean() / 180)) if len(xs) else (0, -1.0, -1.0)


def main():
    debug = L.flag("--debug")
    r = L.Report("CH12.05 — Titres et sous-titres")
    sc = bpy.context.scene
    se = sc.sequence_editor
    texts = [s for s in se.strips_all if s.type == "TEXT"] if se else []
    title = next((s for s in texts if s.name == "TITLE"), None)
    subs = [s for s in texts if s.name != "TITLE"]
    if not r.check(title is not None and len(subs) >= 1, f"Un carton TITLE et {len(subs)} strip(s) de sous-titre", "Gardez le strip TITLE et créez les strips de sous-titres (Add > Text).", 3):
        return r.finish()
    sc.render.engine = "BLENDER_WORKBENCH"
    sc.view_settings.view_transform = "Standard"
    sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage = 320, 180, 100
    sc.render.use_sequencer = True
    sc.render.image_settings.file_format = "PNG"
    sc.render.image_settings.color_mode = "RGB"
    r.check(title.text == "LE LONG VOYAGE" and abs(title.frame_final_start - 1) <= 2 and abs(title.frame_final_duration - 36) <= 2 and title.font_size >= 40,
            f"Titre : « {title.text} », début {title.frame_final_start}, durée {title.frame_final_duration}, taille {title.font_size:.0f}", "Texte « LE LONG VOYAGE », images 1–36, taille ≥ 40.", 8)
    n, cx, cy = render(sc, 18)
    r.check(n >= 1500 and 0.3 <= cx <= 0.7 and 0.35 <= cy <= 0.65, f"Titre rendu : {n} pixels clairs, centre ({cx:.2f}, {cy:.2f}) (≥ 1 500 ; 0,3–0,7 × 0,35–0,65)", "Titre au centre (location 0,5 / 0,5) et assez grand.", 8)
    srt = export_srt(sc, subs)
    ent = [e for e in parse_srt(srt) if e[0] != title.text]  # l'export contient aussi le carton-titre (tous les strips de texte) : on l'ignore
    ok = len(ent) == len(REF) and all(e[0] == w[0] and abs(e[1] - w[1]) <= 2 / FPS and abs(e[2] - w[2]) <= 2 / FPS for e, w in zip(sorted(ent, key=lambda e: e[1]), REF))
    detail = " ; ".join(f"« {e[0]} » {e[1]:.3f}→{e[2]:.3f}" for e in sorted(ent, key=lambda e: e[1]))
    r.check(ok, f"SRT exporté : {detail}" + ("" if ok else " (attendu : « Bonjour. » 2,000→3,500 ; « Il fait nuit. » 3,750→5,000)"), "Textes exacts (avec le point) et temps à ± 2 images : images 49–84 et 91–120.", 12)
    low = all(s.location[1] <= 0.2 and min(s.color[:3]) >= 0.9 and 20 <= s.font_size <= 40 for s in subs)
    r.check(low, "Sous-titres : en bas (y ≤ 0,2), blancs, taille 20–40" if low else "Sous-titres : " + ", ".join(f"{s.name} y {s.location[1]:.2f} taille {s.font_size:.0f}" for s in subs), "location y ≤ 0,2 ; couleur blanche ; taille 20–40.", 6)
    first = min(subs, key=lambda s: s.frame_final_start)
    mid = (first.frame_final_start + first.frame_final_end) // 2
    n2, cx2, cy2 = render(sc, mid)
    r.check(n2 >= 150 and cy2 >= 0.66, f"Sous-titre rendu (image {mid}) : {n2} pixels clairs, centre vertical {cy2:.2f} (≥ 150 ; ≥ 0,66)", "Placez les sous-titres dans le tiers inférieur de l'image.", 8)
    if debug:
        print("[DEBUG]", srt.replace("\n", " | "))
    return r.finish()


if __name__ == "__main__":
    L.run(main)
