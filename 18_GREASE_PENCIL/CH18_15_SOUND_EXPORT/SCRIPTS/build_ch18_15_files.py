"""
build_ch18_15_files.py — « Son, rythme, transitions, export, révision » (CH18.15, phase 18 module D).

  ASSETS/ch18_15_panels/SQ020_SH0010.png … SH0120.png
      Une image par plan, rendue depuis l'animatique CH18.14 (1280 × 720).
  ASSETS/ch18_15_audio/*.wav  (générés par ce script, 48 kHz, licence BCMA)
      music_bed.wav (nappe de 19 s), sfx_whoosh.wav (chute), sfx_catch.wav (rattrapage),
      temp_dialogue_oh.wav (« réplique temporaire » : un signal vocal synthétique, à remplacer
      par votre propre voix enregistrée).
  STARTER_FILES/ch18_15_edit_starter.blend
      Scène SC_Edit (24 i/s, 1280 × 720, 456 images) : Video Sequencer avec les 12 images de plans
      (canal 2, aux durées de la liste), marqueurs, aucun son, aucune transition, sortie PNG,
      texte REVIEW_NOTES vide.
  COMPLETED_EXAMPLES/ch18_15_edit_solution.blend (+ _contact.png, ch18_15_animatic_v001.mp4)
      Musique avec fondus d'entrée et de sortie, 2 bruitages et la réplique synchronisés sur les
      plans, fondu enchaîné SH0110 → SH0120, fondu au noir final, incrustation, sortie MPEG-4
      H.264 + AAC, 4 notes de révision ; vidéo exportée réellement (640 × 360).
Dépend de : COMPLETED_EXAMPLES de CH18.14 (animatique source).
Usage : blender -b --factory-startup --python build_ch18_15_files.py --python-exit-code 1
Testé avec : Blender 5.3.0.
"""
import math
import os
import sys
import wave

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bpy  # noqa: E402
import numpy as np  # noqa: E402

CH = L.chapter_dir(__file__)
SRC = os.path.join(os.path.dirname(CH), "CH18_14_ANIMATIC", "COMPLETED_EXAMPLES", "ch18_14_animatic_solution.blend")
PANELS = os.path.join(CH, "ASSETS", "ch18_15_panels")
AUDIO = os.path.join(CH, "ASSETS", "ch18_15_audio")
FPS, SR = 24, 48000
SHOTS = [("SQ020_SH0010", 3), ("SQ020_SH0020", 1.5), ("SQ020_SH0030", 1), ("SQ020_SH0040", 0.8),
         ("SQ020_SH0050", 0.5), ("SQ020_SH0060", 1), ("SQ020_SH0070", 0.7), ("SQ020_SH0080", 1),
         ("SQ020_SH0090", 2), ("SQ020_SH0100", 2), ("SQ020_SH0110", 1.5), ("SQ020_SH0120", 4)]
NOTES = ["SQ020_SH0020 · 0090 · le geste de B qui heurte la table est trop rapide : +6 images",
         "SQ020_SH0050 · 0155 · chute illisible en 12 images : essayer 16 images",
         "SQ020_SH0080 · 0205 · bruitage du rattrapage en avance d'une image : caler sur 0206",
         "SQ020_SH0120 · 0440 · fondu au noir trop court : commencer à 0420"]
NOTE = """CH18.15 — LE MONTAGE SON ET L'EXPORT (espace de travail Video Editing, éditeur Sequencer)
Les 12 plans sont posés sur le canal 2. Sons : ASSETS/ch18_15_audio (Add > Sound…).
1. Musique music_bed.wav dès l'image 1 ; Add > Fade > Fade In and Out (strip sélectionné).
2. Bruitages synchronisés (± 2 images) : sfx_whoosh au début de SQ020_SH0050 (image 152),
   sfx_catch au début de SQ020_SH0080 (image 205) ; réplique temp_dialogue_oh au début de
   SQ020_SH0040 (image 133, ± 3).
3. Fondu enchaîné SH0110 → SH0120 : SH0120 sur le canal 3, commencé 12 images plus tôt (fin
   inchangée à 456) ; sélectionnez SH0110 puis SH0120 : Add > Transition > Crossfade.
4. Fondu au noir final : SH0120 sélectionné, Add > Fade > Fade Out.
5. Durée totale inchangée : 456 images.
6. Output Properties > Output : Media Type Video (File Format FFmpeg Video) ; Encoding : Container MPEG-4, Video Codec H.264,
   Audio Codec AAC ; Metadata : Strip Name + Frame + Burn Into Image ; Output //export/…
7. Revue : dans le texte REVIEW_NOTES, au moins 3 notes « SQ020_SH0050 · 0155 · remarque »
   (image comprise dans le plan cité).
Vérification : SCRIPTS/validate_ch18_15.py -- --exercise edit [--render pour exporter et contrôler]
"""


def frames():
    out, f = [], 1
    for code, d in SHOTS:
        n = round(d * FPS)
        out.append((code, f, n))
        f += n
    return out, f - 1


# --- sons générés ---------------------------------------------------------------------------

def write_wav(name, x):
    os.makedirs(AUDIO, exist_ok=True)
    x = np.clip(x, -1, 1)
    st = np.repeat((x * 32000).astype("<i2")[:, None], 2, axis=1)   # stéréo
    p = os.path.join(AUDIO, name)
    with wave.open(p, "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(st.tobytes())
    return p


def env(n, a, r):
    e = np.ones(n)
    a, r = int(a * SR), int(r * SR)
    e[:a] = np.linspace(0, 1, a)
    e[n - r:] = np.linspace(1, 0, r)
    return e


def make_audio():
    rng = np.random.default_rng(1815)
    t = np.arange(int(19 * SR)) / SR
    chord = sum(np.sin(2 * np.pi * f * t) for f in (220.0, 277.18, 329.63, 440.0)) / 4
    trem = 0.75 + 0.25 * np.sin(2 * np.pi * 0.25 * t)
    write_wav("music_bed.wav", 0.35 * chord * trem)
    n = int(0.5 * SR)
    tt = np.arange(n) / SR
    noise = rng.standard_normal(n)
    sweep = np.sin(2 * np.pi * (300 + 2400 * tt) * tt)
    write_wav("sfx_whoosh.wav", 0.4 * (0.6 * noise + 0.4 * sweep) * np.sin(np.pi * tt / 0.5))
    n = int(0.35 * SR)
    tt = np.arange(n) / SR
    write_wav("sfx_catch.wav", 0.9 * np.sin(2 * np.pi * 110 * tt) * np.exp(-tt * 18) + 0.2 * rng.standard_normal(n) * np.exp(-tt * 60))
    n = int(0.6 * SR)
    tt = np.arange(n) / SR
    f0 = 260 - 60 * tt / 0.6                                  # intonation descendante (« oh… »)
    ph = 2 * np.pi * np.cumsum(f0) / SR
    voice = sum(np.sin(k * ph) / k for k in range(1, 9))
    formant = 1 + 0.5 * np.sin(2 * np.pi * 5 * tt)
    write_wav("temp_dialogue_oh.wav", 0.3 * voice * formant * env(n, 0.05, 0.2))


# --- images des plans -----------------------------------------------------------------------

def render_panels():
    bpy.ops.wm.open_mainfile(filepath=SRC)
    sc = bpy.context.scene
    sc.render.use_stamp = False
    sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage = 1280, 720, 100
    sc.render.image_settings.file_format = "PNG"
    sc.render.image_settings.color_mode = "RGB"
    sc.render.image_settings.compression = 100
    os.makedirs(PANELS, exist_ok=True)
    fr, _end = frames()
    for code, f, n in fr:
        sc.frame_set(f + n // 2 if code != "SQ020_SH0120" else f + n - 1)
        sc.render.filepath = os.path.join(PANELS, code + ".png")
        bpy.ops.render.render(write_still=True)


# --- montage --------------------------------------------------------------------------------

def stamp(sc):
    r = sc.render
    for k in dir(r):
        if k.startswith("use_stamp_") and k != "use_stamp_labels":
            setattr(r, k, False)
    r.use_stamp = True
    r.use_stamp_sequencer_strip = r.use_stamp_frame = True
    r.stamp_font_size = 18


def key(strip, prop, pts):
    for f, v in pts:
        setattr(strip, prop, v)
        strip.keyframe_insert(prop, frame=f)


def edit(sol):
    sc = L.reset("SC_Edit")
    sc.render.fps, sc.render.fps_base = FPS, 1.0
    sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage = 1280, 720, 100
    fr, end = frames()
    sc.frame_start, sc.frame_end = 1, end
    sc.view_settings.view_transform = "Standard"      # sinon (AgX) le papier blanc devient gris
    se = sc.sequence_editor_create()
    strips = {}
    for code, f, n in fr:
        s = se.strips.new_image(code, os.path.join(PANELS, code + ".png"), 2, f, fit_method="FIT")
        s.frame_final_duration = n
        strips[code] = s
        sc.timeline_markers.new(code, frame=f)
    sc.render.image_settings.file_format = "PNG"
    sc.render.filepath = "//renders/edit_"
    t = L.instructions("# code · image · remarque\n", "REVIEW_NOTES")
    if sol:
        start = {c: f for c, f, _n in fr}
        mus = se.strips.new_sound("music_bed", os.path.join(AUDIO, "music_bed.wav"), 5, 1)
        key(mus, "volume", [(1, 0.0), (24, 0.6), (end - 24, 0.6), (end, 0.0)])
        se.strips.new_sound("sfx_whoosh", os.path.join(AUDIO, "sfx_whoosh.wav"), 6, start["SQ020_SH0050"])
        se.strips.new_sound("sfx_catch", os.path.join(AUDIO, "sfx_catch.wav"), 6, start["SQ020_SH0080"])
        se.strips.new_sound("temp_dialogue_oh", os.path.join(AUDIO, "temp_dialogue_oh.wav"), 7, start["SQ020_SH0040"])
        last = strips["SQ020_SH0120"]
        last.channel = 3
        last.frame_start = start["SQ020_SH0120"] - 12
        last.frame_final_duration = end - (start["SQ020_SH0120"] - 12) + 1
        x = se.strips.new_effect("XF_SH0110_SH0120", "CROSS", 4, start["SQ020_SH0120"] - 12,
                                 input1=strips["SQ020_SH0110"], input2=last)
        print(f"[BCMA] fondu enchaîné {x.frame_final_start}–{x.frame_final_end}")
        key(last, "blend_alpha", [(end - 24, 1.0), (end, 0.0)])
        stamp(sc)
        im = sc.render.image_settings
        im.media_type = "VIDEO"
        im.file_format = "FFMPEG"
        ff = sc.render.ffmpeg
        ff.format, ff.codec, ff.audio_codec, ff.audio_channels = "MPEG4", "H264", "AAC", "STEREO"
        ff.constant_rate_factor = "MEDIUM"
        sc.render.filepath = "//export/ch18_15_animatic_v001_"
        t.write("\n".join(NOTES) + "\n")
    L.instructions(NOTE)
    return sc


def export_video(sc, out_dir):
    """Exporte réellement la vidéo (640 × 360) et renvoie le chemin du fichier produit.
    Blender ajoute la plage d'images au nom (…v0010001-0456.mp4) : on renomme ensuite."""
    final = os.path.join(out_dir, "ch18_15_animatic_v001.mp4")
    for f in os.listdir(out_dir):
        if f.startswith("ch18_15_animatic_v001") and f.endswith(".mp4"):
            os.remove(os.path.join(out_dir, f))
    sc.render.resolution_percentage = 50
    keep = sc.render.filepath
    sc.render.filepath = os.path.join(out_dir, "ch18_15_animatic_v001")
    sc.render.use_file_extension = True
    bpy.ops.render.render(animation=True)
    sc.render.filepath = keep
    sc.render.resolution_percentage = 100
    produced = [f for f in os.listdir(out_dir) if f.startswith("ch18_15_animatic_v001") and f.endswith(".mp4")]
    os.replace(os.path.join(out_dir, produced[0]), final)
    return final


def contact(sc, frames_, out):
    sc.render.image_settings.media_type = "IMAGE"
    sc.render.image_settings.file_format = "PNG"
    sc.render.resolution_percentage = 30
    W, H = sc.render.resolution_x * 30 // 100, sc.render.resolution_y * 30 // 100
    sheet = np.zeros((H, W * len(frames_), 4), dtype=np.float32)
    for i, f in enumerate(frames_):
        sc.frame_set(f)
        p = os.path.join(bpy.app.tempdir, f"edit_{f}.png")
        sc.render.filepath = p
        bpy.ops.render.render(write_still=True)
        im = bpy.data.images.load(p)
        sheet[:, i * W:(i + 1) * W] = np.array(im.pixels[:], dtype=np.float32).reshape(H, W, 4)
        bpy.data.images.remove(im)
    img = bpy.data.images.new("contact", W * len(frames_), H)
    img.pixels = sheet.ravel()
    img.filepath_raw = out
    img.file_format = "PNG"
    img.save()


def main():
    out = os.path.join(CH, "COMPLETED_EXAMPLES")
    make_audio()
    render_panels()
    edit(False)
    L.save(os.path.join(CH, "STARTER_FILES", "ch18_15_edit_starter.blend"))
    sc = edit(True)
    L.save(os.path.join(out, "ch18_15_edit_solution.blend"))
    video = export_video(sc, out)
    print(f"[BCMA] vidéo {video} : {os.path.getsize(video)} octets")
    contact(sc, [140, 354, 446], os.path.join(out, "ch18_15_edit_contact.png"))


if __name__ == "__main__":
    L.run(main)
