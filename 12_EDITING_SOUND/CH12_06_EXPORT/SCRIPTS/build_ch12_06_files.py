"""
build_ch12_06_files.py — « Export et livraison » (CH12.06 : conteneur, codec vidéo, codec audio, résolution, cadence, durée).

Données générées (ASSETS/ch12_06_audio/tone.wav : sinusoïde de 220 Hz, 2 s, 48 kHz mono) et scène (24 i/s, plage 1–48 = 2 s) : un strip COLOR « PICTURE » (canal 1, images 1–48, bleu) et un strip sonore « TONE » (canal 2).
  Départ : sortie en suite d'images PNG, résolution à 50 %, cadence 30 i/s, plage 1–24, sans codec : rien n'est livrable.
  Consigne : régler la sortie (Output Properties) pour livrer une vidéo WEB : (1) fichier vidéo FFmpeg : conteneur MPEG-4 (.mp4), codec vidéo H.264, codec audio AAC ; (2) 640 × 360 pixels (résolution 640 × 360 à 100 %) ;
    (3) 24 images par seconde ; (4) plage 1–48 : durée de 2 s à ± 0,1 s ; (5) poids du fichier ≤ 400 Ko.
  Le correcteur LANCE le rendu de l'animation avec VOS réglages (dans un dossier temporaire) puis ANALYSE le fichier produit avec un lecteur de boîtes MP4 (SCRIPTS/mp4probe.py : pas de ffprobe sur la machine) : conteneur (ftyp), piste vidéo (avc1 = H.264), piste audio (mp4a = AAC), largeur × hauteur, durée.
  Solution : média Vidéo, File Format FFmpeg Video, conteneur MPEG-4, codec H.264, audio AAC (192 kb/s), 640 × 360 à 100 %, 24 i/s, plage 1–48.
  STARTER_FILES/ch12_06_export_starter.blend ; COMPLETED_EXAMPLES/ch12_06_export_solution.blend (+ _reference.png : fiche des mesures du fichier exporté)
  COUNTER_EXAMPLES/ : mpeg4_codec (codec vidéo MPEG-4 : mp4v au lieu de avc1), no_audio (audio NONE), half_res (50 % : 320 × 180), fps30 (30 i/s : durée 1,6 s), short_range (plage 1–24 : 1 s)
Usage : blender -b --factory-startup --python-exit-code 1 --python build_ch12_06_files.py
Testé avec : Blender 5.3.0.
"""
import glob
import os
import shutil
import sys
import tempfile
import wave

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "SCRIPTS"))
sys.path.insert(0, HERE)
import bcma_lib as L  # noqa: E402
import bpy  # noqa: E402
import mp4probe  # noqa: E402
import numpy as np  # noqa: E402

CH = L.chapter_dir(__file__)
AUDIO = os.path.join(CH, "ASSETS", "ch12_06_audio")
NOTE = """CH12.06 — EXPORT ET LIVRAISON (strips PICTURE et TONE, 24 i/s, plage 1–48)
Livrez une vidéo web : Output Properties > Output : média Vidéo, File Format FFmpeg Video ; Encoding : Container MPEG-4, Video Codec H.264, Audio Codec AAC ;
résolution 640 × 360 à 100 % ; cadence 24 i/s ; plage 1–48 (2 s) ; fichier ≤ 400 Ko.
Le correcteur rend l'animation avec vos réglages et analyse le fichier .mp4 produit.
Vérification : SCRIPTS/validate_ch12_06.py -- --exercise export
"""


def make_audio():
    os.makedirs(AUDIO, exist_ok=True)
    t = np.arange(96000) / 48000.0
    with wave.open(os.path.join(AUDIO, "tone.wav"), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(48000)
        w.writeframes((0.3 * np.sin(2 * np.pi * 220 * t) * 32000).astype("<i2").tobytes())


def build(kind):
    L.reset("SC_EXPORT")
    sc = bpy.context.scene
    sc.render.engine = "BLENDER_WORKBENCH"
    sc.render.use_sequencer = True
    se = sc.sequence_editor_create()
    pic = se.strips.new_effect(name="PICTURE", type="COLOR", channel=1, frame_start=1, length=48)
    pic.color = (0.2, 0.5, 0.9)
    se.strips.new_sound(name="TONE", filepath=os.path.join(AUDIO, "tone.wav"), channel=2, frame_start=1)
    s = sc.render.image_settings
    ff = sc.render.ffmpeg
    if kind == "starter":
        s.media_type, s.file_format = "IMAGE", "PNG"
        sc.render.fps = 30
        sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage = 1280, 720, 50
        sc.frame_start, sc.frame_end = 1, 24
    else:
        s.media_type = "VIDEO"
        ff.format, ff.codec, ff.audio_codec = "MPEG4", "H264", "AAC"
        ff.audio_bitrate, ff.constant_rate_factor = 192, "MEDIUM"
        sc.render.fps = 30 if kind == "fps30" else 24
        pct = 50 if kind == "half_res" else 100
        sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage = 640, 360, pct
        sc.frame_start, sc.frame_end = 1, 24 if kind == "short_range" else 48
        if kind == "mpeg4_codec":
            ff.codec = "MPEG4"
        if kind == "no_audio":
            ff.audio_codec = "NONE"
    sc.render.filepath = "//export/web_"
    sc.frame_set(1)
    L.instructions(NOTE)


def fix_paths():
    for s in bpy.data.sounds:
        s.filepath = "//../ASSETS/ch12_06_audio/" + os.path.basename(s.filepath.replace("\\", "/"))


def export_probe():
    sc = bpy.context.scene
    tmp = tempfile.mkdtemp(prefix="bcma_ch1206_")
    keep = sc.render.filepath
    sc.render.filepath = os.path.join(tmp, "web_")
    bpy.ops.render.render(animation=True)
    sc.render.filepath = keep
    fs = glob.glob(os.path.join(tmp, "web_*.mp4"))
    res = mp4probe.analyse(fs[0]) if fs else None
    size = os.path.getsize(fs[0]) if fs else 0
    shutil.rmtree(tmp, ignore_errors=True)
    return res, size


def calibrate():
    for kind in ("solution", "mpeg4_codec", "no_audio", "half_res", "fps30", "short_range"):
        build(kind)
        res, size = export_probe()
        print("[exp]", kind, res, size)


def sketch(path):
    """Fiche : barres horizontales : largeur, hauteur, durée × 100, poids en Ko / 10 du fichier exporté de la solution."""
    build("solution")
    res, size = export_probe()
    W, H = 640, 200
    img = np.full((H, W, 3), 0.1, np.float32)
    vals = [(res["tracks"][0]["width"] / 2000.0, (0.3, 0.7, 1.0)), (res["tracks"][0]["height"] / 2000.0, (0.3, 1.0, 0.7)), (res["duration"] / 5.0, (1.0, 0.8, 0.3)), (size / 1e6, (1.0, 0.4, 0.4))]
    for i, (v, c) in enumerate(vals):
        y = 20 + i * 42
        img[y:y + 30, 20:20 + max(int(v * 600), 2), :] = c
    rgba = np.concatenate([img, np.ones(img.shape[:2] + (1,), np.float32)], axis=2)
    out = bpy.data.images.new("sk", W, H)
    out.pixels = rgba[::-1].ravel()
    out.filepath_raw = path
    out.file_format = "PNG"
    out.save()
    print("[exp-solution]", res, size)


def main():
    out = os.path.join(CH, "COMPLETED_EXAMPLES")
    make_audio()
    calibrate()
    build("starter")
    fix_paths()
    L.save(os.path.join(CH, "STARTER_FILES", "ch12_06_export_starter.blend"))
    for k in ("mpeg4_codec", "no_audio", "half_res", "fps30", "short_range"):
        build(k)
        fix_paths()
        L.save(os.path.join(out, "COUNTER_EXAMPLES", f"ch12_06_export_{k}.blend"))
    sketch(os.path.join(out, "ch12_06_export_reference.png"))
    build("solution")
    fix_paths()
    L.save(os.path.join(out, "ch12_06_export_solution.blend"))


if __name__ == "__main__":
    L.run(main)
