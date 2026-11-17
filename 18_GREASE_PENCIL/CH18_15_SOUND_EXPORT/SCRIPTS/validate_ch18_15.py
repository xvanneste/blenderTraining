"""
validate_ch18_15.py — Correcteur « Son, rythme, transitions, export, révision » (CH18.15).
Usage : … --python-exit-code 1 --python validate_ch18_15.py -- --exercise edit [--render]
Vérifie dans le Video Sequencer : plans intacts (durée 456), musique avec fondus d'entrée et de
sortie, bruitages et réplique calés sur les marqueurs des plans, fondu enchaîné SH0110 → SH0120,
fondu au noir final, réglages d'export (MPEG-4, H.264, AAC), incrustation, notes de révision.
--render : exporte réellement la vidéo (25 %) dans un dossier temporaire et contrôle le fichier
(nombre d'images, piste son présente et non muette).
Testé avec : Blender 5.3.0.
"""
import os
import re
import sys
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bpy  # noqa: E402

END = 456
SYNC = [("sfx_whoosh", "SQ020_SH0050", 2), ("sfx_catch", "SQ020_SH0080", 2), ("temp_dialogue_oh", "SQ020_SH0040", 3)]
NOTE_RE = re.compile(r"(SQ\d{3}_SH\d{4})\s*[·;|-]\s*(\d{1,5})\s*[·;|-]\s*(\S.{4,})")
PATH_RE = re.compile(r'strips(?:_all)?\["(.+?)"\]\.(\w+)')


def anim_curves(sc):
    """{(nom du strip, propriété): [(image, valeur), …]} — actions par couches (Blender ≥ 4.4)."""
    out = {}
    ad = sc.animation_data
    if not ad or not ad.action:
        return out
    curves = []
    for lay in getattr(ad.action, "layers", []):
        for st in lay.strips:
            for bag in getattr(st, "channelbags", []):
                curves.extend(bag.fcurves)
    for fc in curves:
        m = PATH_RE.search(fc.data_path)
        if m:
            out[(m.group(1), m.group(2))] = sorted((k.co.x, k.co.y) for k in fc.keyframe_points)
    return out


def sound_strips(se, stem):
    return [s for s in se.strips_all if s.type == "SOUND" and s.sound and stem in os.path.basename(s.sound.filepath)]


def main():
    sc = bpy.context.scene
    r = L.Report("CH18.15 — Montage son, transitions, export, révision")
    se = sc.sequence_editor
    if not r.check(se is not None, "Video Sequencer présent", "Repartez du starter.", 1):
        return r.finish()
    markers = {m.name: m.frame for m in sc.timeline_markers}
    codes = sorted(c for c in markers if re.fullmatch(r"SQ\d{3}_SH\d{4}", c))
    images = [s for s in se.strips_all if s.type == "IMAGE"]
    r.check(len(codes) == 12 and len(images) >= 12, f"12 plans et 12 marqueurs ({len(images)} images, {len(codes)} marqueurs)",
            "Ne supprimez ni les plans ni les marqueurs.", 1)
    r.check(sc.frame_end == END and sc.render.fps == 24, f"Durée inchangée : fin {sc.frame_end} (456), {sc.render.fps} i/s",
            "Le son et les transitions ne changent pas la durée de l'animatique.", 2)
    curves = anim_curves(sc)
    # musique et fondus
    mus = sound_strips(se, "music_bed")
    ok_fade = False
    if mus:
        k = curves.get((mus[0].name, "volume"), [])
        if len(k) >= 3:
            vals = [v for _f, v in k]
            ok_fade = vals[0] < max(vals) - 0.1 and vals[-1] < max(vals) - 0.1
    r.check(bool(mus) and mus[0].frame_final_start <= 3, "Musique posée dès le début", "Add > Sound… music_bed.wav à l'image 1.", 2)
    r.check(ok_fade, "Musique : fondu d'entrée et de sortie (volume animé)", "Strip sélectionné : Add > Fade > Fade In and Out.", 2)
    # synchronisation
    bad = []
    for stem, code, tol in SYNC:
        ss = sound_strips(se, stem)
        if not ss or code not in markers:
            bad.append(f"{stem} absent")
            continue
        off = ss[0].frame_final_start - markers[code]
        if abs(off) > tol:
            bad.append(f"{stem} décalé de {off:+d} image(s) / {code}")
    r.check(not bad, f"Bruitages et réplique synchronisés ({3 - len(bad)}/3)", " ; ".join(bad), 3)
    # transition
    trans = [s for s in se.strips_all if s.type in ("CROSS", "GAMMA_CROSS", "WIPE")]
    pair = any({getattr(t.input_1, "name", ""), getattr(t.input_2, "name", "")} >= {"SQ020_SH0110", "SQ020_SH0120"}
               or ({getattr(t.input_1, "name", "")[:12], getattr(t.input_2, "name", "")[:12]} == {"SQ020_SH0110", "SQ020_SH0120"})
               for t in trans)
    r.check(pair, f"Fondu enchaîné SH0110 → SH0120 ({len(trans)} transition(s))",
            "Chevauchez les deux plans (canaux 2 et 3), sélectionnez-les : Add > Transition > Crossfade.", 2)
    if trans:
        r.check(all(t.frame_final_duration >= 6 for t in trans), "Transition d'au moins 6 images (¼ s)", "Augmentez le chevauchement.", 1)
    # fondu au noir
    black = False
    for (name, prop), k in curves.items():
        if prop == "blend_alpha" and len(k) >= 2 and k[-1][1] <= 0.05 and k[-1][0] >= END - 2 and max(v for _f, v in k) >= 0.9:
            black = True
    r.check(black, "Fondu au noir final (opacité → 0 à la fin)", "Dernier plan sélectionné : Add > Fade > Fade Out.", 2)
    # export
    im, ff = sc.render.image_settings, sc.render.ffmpeg
    r.check(im.file_format == "FFMPEG" and ff.format == "MPEG4" and ff.codec == "H264",
            f"Export vidéo MPEG-4 / H.264 ({im.file_format}, {ff.format}, {ff.codec})",
            "Output Properties > Output : FFmpeg Video ; Encoding : MPEG-4, H.264.", 2)
    r.check(ff.audio_codec == "AAC", f"Piste son exportée en AAC ({ff.audio_codec})", "Encoding > Audio > Audio Codec : AAC.", 2)
    rd = sc.render
    r.check(rd.use_stamp and rd.use_stamp_frame and (rd.use_stamp_sequencer_strip or rd.use_stamp_marker),
            "Incrustation (Strip Name ou Marker + Frame)", "Output Properties > Metadata + Burn Into Image.", 1)
    # notes de révision
    notes, wrong = [], []
    t = bpy.data.texts.get("REVIEW_NOTES")
    starts = sorted(markers[c] for c in codes)
    for line in (t.as_string().splitlines() if t else []):
        m = NOTE_RE.search(line)
        if not m or m.group(1) not in markers:
            continue
        f, s0 = int(m.group(2)), markers[m.group(1)]
        nxt = min([x for x in starts if x > s0], default=END + 1)
        (notes if s0 <= f < nxt else wrong).append(line)
    r.check(len(notes) >= 3, f"{len(notes)} note(s) de révision valides (≥ 3)",
            "Format « SQ020_SH0050 · 0155 · remarque », image comprise dans le plan." + (f" Hors plan : {wrong[:2]}" if wrong else ""), 2)
    if L.flag("--render"):
        export_check(r, sc)
    return r.finish()


def export_check(r, sc):
    import aud
    import numpy as np
    d = tempfile.mkdtemp(prefix="bcma1815_")
    sc.render.filepath = os.path.join(d, "check")
    sc.render.resolution_percentage = 25
    bpy.ops.render.render(animation=True)
    vids = [f for f in os.listdir(d) if f.endswith(".mp4")]
    if not r.check(bool(vids), "Vidéo exportée (.mp4)", "Vérifiez les réglages d'export.", 2):
        return
    p = os.path.join(d, vids[0])
    clip = bpy.data.movieclips.load(p)
    r.check(clip.frame_duration == sc.frame_end - sc.frame_start + 1, f"Vidéo de {clip.frame_duration} images", "", 1)
    try:
        data = aud.Sound(p).data()
        rms = float(np.sqrt(np.mean(np.square(data)))) if data.size else 0.0
        secs = data.shape[0] / 48000 if data.size else 0
    except Exception as e:  # piste absente
        rms, secs = 0.0, 0
        print("aud:", e)
    r.check(rms > 0.005 and secs > 15, f"Piste son présente et audible (RMS {rms:.3f}, {secs:.1f} s)",
            "Audio Codec ≠ No Audio, sons non muets.", 2)


if __name__ == "__main__":
    L.run(main)
