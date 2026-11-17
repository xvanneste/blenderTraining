"""
validate_ch18_22.py — Correcteur des 7 projets obligatoires de la phase 18 (CH18.22).
Usage : … --python-exit-code 1 --python validate_ch18_22.py -- --exercise p1|p2|…|p7 [--render]
  p1 planche de 12 cases          → critères du correcteur CH18.13 (exécuté tel quel)
  p2 dialogue storyboardé         → planche ≥ 8 cases normées, champ/contrechamp (≥ 2 plans serrés)
  p3 scène d'action de 30 s       → animatique GP : 25–35 s, ≥ 12 plans (marqueurs), un dessin par plan,
                                     durée moyenne ≤ 2,5 s
  p4 animatique complète de 1 min → montage VSE : 55–75 s, ≥ 15 plans, ≥ 3 sons, export MPEG-4/H.264/AAC,
                                     ≥ 3 notes de révision
  p5 animation GP de 15–30 s      → 15–30 s, ≥ 6 dessins/s en moyenne, ≥ 3 dessins différents
  p6 scène hybride 2D/3D          → critères du correcteur CH18.19 (exécuté tel quel)
  p7 court de 3–5 min             → montage VSE : 180–300 s, ≥ 40 plans, son, export, ≥ 3 notes de révision
Les critères artistiques se jugent avec les grilles d'EXERCISES.md.
Testé avec : Blender 5.3.0.
"""
import importlib.util
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "SCRIPTS"))
import bcma_board as B  # noqa: E402
import bcma_lib as L  # noqa: E402
import bpy  # noqa: E402

PH = os.path.dirname(os.path.dirname(HERE))
CODE = re.compile(r"SQ\d{3}_SH\d{4}")
NOTE_RE = re.compile(r"\S+\s*[·;|]\s*\d{1,5}\s*[·;|]\s*\S.{4,}")


def delegate(chapter, script):
    path = os.path.join(PH, chapter, "SCRIPTS", script)
    spec = importlib.util.spec_from_file_location(script[:-3], path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.main()


def seconds(sc):
    return (sc.frame_end - sc.frame_start + 1) / (sc.render.fps / sc.render.fps_base)


def review_notes(r):
    t = bpy.data.texts.get("REVIEW_NOTES")
    n = sum(1 for x in (t.as_string().splitlines() if t else []) if not x.strip().startswith("#") and NOTE_RE.search(x))
    r.check(n >= 3, f"{n} note(s) de révision « plan · image · remarque » (≥ 3)", "Texte REVIEW_NOTES (CH18.15).", 2)


def export_settings(r, sc):
    im, ff = sc.render.image_settings, sc.render.ffmpeg
    r.check(im.file_format == "FFMPEG" and ff.format == "MPEG4" and ff.codec == "H264" and ff.audio_codec == "AAC",
            f"Export MPEG-4 / H.264 / AAC ({im.file_format}, {ff.format}, {ff.codec}, {ff.audio_codec})",
            "Output Properties (CH18.15).", 2)


def vse_project(r, sc, lo, hi, min_shots, min_sounds):
    se = sc.sequence_editor
    if not r.check(se is not None, "Montage dans le Video Sequencer", "Espace Video Editing.", 1):
        return
    s = seconds(sc)
    r.check(lo <= s <= hi, f"Durée {s:.1f} s ({lo}–{hi} s)", "Frame Range End / Frame Rate.", 2)
    vis = [x for x in se.strips_all if x.type in ("IMAGE", "MOVIE", "SCENE")]
    snd = [x for x in se.strips_all if x.type == "SOUND"]
    r.check(len(vis) >= min_shots, f"{len(vis)} plans visuels (≥ {min_shots})", "Un strip par plan.", 2)
    r.check(len(snd) >= min_sounds, f"{len(snd)} son(s) (≥ {min_sounds})", "Dialogues temporaires, bruitages, musique.", 2)
    export_settings(r, sc)
    review_notes(r)


def p2(r, sc):
    info = B.read(sc)
    n = len(info["rects"])
    if not r.check(n >= 8, f"Planche de {n} cases (≥ 8)", "Gabarit bcma_board / CH18.12.", 2):
        return
    pp = info["per_panel"]
    r.check(min(pp) >= 3, f"Dessin dans chaque case (min {min(pp)} traits)", "", 2)
    comp = [x for x in info["notes"] if x["value"] and x["move"] and x["duration"] is not None and x["panel"] is not None]
    r.check(len({x["panel"] for x in comp}) == n, f"Une note normée sous chaque case ({len({x['panel'] for x in comp})}/{n})",
            "SQ050_SH0010 · PE · fixe · 3 s", 2)
    codes = [x["code"] for x in info["notes"]]
    r.check(len(codes) == len(set(codes)), "Codes uniques", "", 1)
    close = sum(1 for x in comp if x["value"] in ("PRP", "GP", "TGP", "PRT"))
    r.check(close >= 2, f"Champ / contrechamp : {close} plans serrés (≥ 2)", "Alternez les plans serrés sur chaque personnage (CH18.11).", 2)
    r.check(info["header"], "En-tête de page", "", 1)


def p3(r, sc):
    s = seconds(sc)
    r.check(25 <= s <= 35, f"Durée {s:.1f} s (25–35 s)", "", 2)
    mks = sorted([m for m in sc.timeline_markers if CODE.search(m.name)], key=lambda m: m.frame)
    if not r.check(len(mks) >= 12, f"{len(mks)} plans marqués (≥ 12)", "Un marqueur nommé par plan (CH18.14).", 2):
        return
    keys = {}
    for ob in sc.objects:
        if ob.type == "GREASEPENCIL":
            for lay in ob.data.layers:
                for fr in lay.frames:
                    keys[fr.frame_number] = max(keys.get(fr.frame_number, 0), len(fr.drawing.strokes))
    miss = [m.name for m in mks if keys.get(m.frame, 0) < 3]
    r.check(not miss, f"Un dessin au début de chaque plan ({len(mks) - len(miss)}/{len(mks)})", f"Manquants : {miss[:4]}", 3)
    mean = s / len(mks)
    r.check(mean <= 2.5, f"Rythme d'action : {mean:.2f} s par plan en moyenne (≤ 2,5)", "", 2)


def p5(r, sc):
    s = seconds(sc)
    r.check(15 <= s <= 30, f"Durée {s:.1f} s (15–30 s)", "", 2)
    n, sigs, layers = 0, set(), 0
    for ob in sc.objects:
        if ob.type != "GREASEPENCIL":
            continue
        for lay in ob.data.layers:
            frs = [fr for fr in lay.frames if sc.frame_start <= fr.frame_number <= sc.frame_end and len(fr.drawing.strokes)]
            if len(frs) >= 2:
                layers += 1
            n += len(frs)
            for fr in frs:
                sigs.add((len(fr.drawing.strokes), round(sum(p.position.x + p.position.z for st in fr.drawing.strokes for p in st.points), 1)))
    r.check(layers >= 1, f"{layers} calque(s) animé(s)", "", 1)
    r.check(n >= 6 * s, f"{n} dessins pour {s:.1f} s ({n / max(s, 1e-6):.1f} par seconde, ≥ 6)", "Animez au moins « en quatre » en moyenne.", 3)
    r.check(len(sigs) >= 3, f"{len(sigs)} dessins différents (≥ 3)", "", 1)
    if L.flag("--render"):
        lum = L.quick_render(15, 4)
        r.check(lum > 0.05, f"Rendu de contrôle non noir ({lum:.3f})", "", 1)


def main():
    ex = L.opt("--exercise", "p1")
    if ex == "p1":
        return delegate("CH18_13_COMPLEX_BOARDS", "validate_ch18_13.py")
    if ex == "p6":
        return delegate("CH18_19_DRAW_ON_3D", "validate_ch18_19.py")
    sc = bpy.context.scene
    titles = {"p2": "dialogue storyboardé", "p3": "scène d'action de 30 s", "p4": "animatique complète de 1 min",
              "p5": "animation Grease Pencil de 15–30 s", "p7": "storyboard + animatique d'un court de 3–5 min"}
    r = L.Report(f"CH18.22 — Projet {ex[1:]} : {titles[ex]}")
    if ex == "p2":
        p2(r, sc)
    elif ex == "p3":
        p3(r, sc)
    elif ex == "p4":
        vse_project(r, sc, 55, 75, 15, 3)
    elif ex == "p5":
        p5(r, sc)
    elif ex == "p7":
        vse_project(r, sc, 180, 300, 40, 1)
    return r.finish()


if __name__ == "__main__":
    L.run(main)
