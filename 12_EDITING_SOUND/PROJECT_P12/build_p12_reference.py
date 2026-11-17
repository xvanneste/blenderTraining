"""
build_p12_reference.py — Construit la référence du projet P12 : séquence finalisée de 112 images (4,67 s à 24 i/s) :
  six plans de couleur (SH1_wide … SH6_wide, durées 30, 24, 18, 12, 12 puis 28 images, Crossfade SH5 → SH6), carton-titre « LE LONG VOYAGE » (images 1–30, centré), deux sous-titres (« Bonjour. » 31–54, « Il fait nuit. » 85–104),
  son : ambiance AMB, bruitage HIT sur IMPACT (image 55), réplique VOICE sur LINE (image 85), musique MUSIC (volume 0,3 avec ducking 0,1 de 82 à 106), exports renders/p12_web.mp4 (640 × 360) et renders/p12_master.mp4 (1280 × 720), H.264 + AAC.
Assemble CH12.01 à CH12.06. Les sons sont générés (ASSETS/p12_audio/*.wav, licence BCMA).
Usage : blender -b --factory-startup --python-exit-code 1 --python build_p12_reference.py
Testé avec : Blender 5.3.0.
"""
import math
import os
import sys
import wave

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bpy  # noqa: E402
import numpy as np  # noqa: E402

AUDIO = os.path.join(HERE, "ASSETS", "p12_audio")
SR = 48000
NOTE = """P12 — UNE SÉQUENCE FINALISÉE (six plans, titre, sous-titres, son, mixage, exports web et master)
Reprenez le montage, le titre, les sous-titres, le son et le mixage, puis exportez renders/p12_web.mp4 (640 × 360) et renders/p12_master.mp4 (1280 × 720) en H.264 + AAC. Critères : README et SCRIPTS/validate_p12.py."""
COL = {"SH1_wide": (1, 0, 0), "SH2_medium": (1, 0.5, 0), "SH3_close": (1, 1, 0), "SH4_medium": (0, 1, 0), "SH5_close": (0, 1, 1), "SH6_wide": (0, 0, 1)}


def write_wav(name, x):
    os.makedirs(AUDIO, exist_ok=True)
    with wave.open(os.path.join(AUDIO, name), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((np.clip(x, -1, 1) * 32000).astype("<i2").tobytes())
    return os.path.join(AUDIO, name)


def make_audio():
    rng = np.random.RandomState(4)
    n = int(5.0 * SR)
    t = np.arange(n) / SR
    amb = np.convolve(rng.normal(0, 1, n), np.ones(40) / 40.0, mode="same")
    write_wav("amb_room.wav", amb / amb.std() * 0.02)
    pad = sum(np.sin(2 * np.pi * f * t) for f in (220, 277, 330)) * (0.7 + 0.3 * np.sin(2 * np.pi * 0.4 * t))
    write_wav("music_pad.wav", pad / np.sqrt((pad ** 2).mean()) * 0.20)
    t = np.arange(int(0.5 * SR)) / SR
    write_wav("sfx_hit.wav", 0.8 * np.sin(2 * np.pi * 120 * t) * np.exp(-t * 10))
    t = np.arange(int(0.8 * SR)) / SR
    env = np.sin(np.pi * t / 0.8) ** 0.5
    write_wav("voice_line.wav", 0.3 * env * (np.sin(2 * np.pi * (220 + 30 * np.sin(2 * np.pi * 5 * t)) * t) + 0.5 * np.sin(2 * np.pi * 440 * t)))


def txt(se, name, text, start, end, size, loc, ch):
    s = se.strips.new_effect(name=name, type="TEXT", channel=ch, frame_start=start, length=end - start + 1)
    s.text, s.font_size, s.location, s.color = text, size, loc, (1, 1, 1, 1)
    return s


def build():
    L.reset("SC_P12")
    sc = bpy.context.scene
    sc.render.fps = 24
    sc.render.engine = "BLENDER_WORKBENCH"
    sc.view_settings.view_transform = "Standard"
    sc.render.use_sequencer = True
    sc.timeline_markers.new("IMPACT", frame=55)
    sc.timeline_markers.new("LINE", frame=85)
    se = sc.sequence_editor_create()
    S = {}
    t = 1
    for n, d in (("SH1_wide", 30), ("SH2_medium", 24), ("SH3_close", 18), ("SH4_medium", 12), ("SH5_close", 12)):
        S[n] = se.strips.new_effect(name=n, type="COLOR", channel=1, frame_start=t, length=d)
        S[n].color = COL[n]
        t += d
    S["SH6_wide"] = se.strips.new_effect(name="SH6_wide", type="COLOR", channel=2, frame_start=t - 12, length=28)
    S["SH6_wide"].color = COL["SH6_wide"]
    se.strips.new_effect(name="Crossfade", type="CROSS", channel=3, frame_start=t - 12, length=12, input1=S["SH5_close"], input2=S["SH6_wide"])
    last = max(s.frame_final_end for s in S.values()) - 1
    txt(se, "TITLE", "LE LONG VOYAGE", 1, 30, 56, (0.5, 0.5), 4)
    txt(se, "SUB1", "Bonjour.", 31, 54, 30, (0.5, 0.1), 5)
    txt(se, "SUB2", "Il fait nuit.", 85, 104, 30, (0.5, 0.1), 5)
    snd = {}
    for ch, (name, f, st) in enumerate((("AMB", "amb_room.wav", 1), ("MUSIC", "music_pad.wav", 1), ("HIT", "sfx_hit.wav", 55), ("VOICE", "voice_line.wav", 85)), start=6):
        snd[name] = se.strips.new_sound(name=name, filepath=os.path.join(AUDIO, f), channel=ch, frame_start=st)
    mu = snd["MUSIC"]
    for f, v in ((1, 0.3), (82, 0.3), (85, 0.1), (104, 0.1), (108, 0.3)):
        mu.volume = v
        mu.keyframe_insert("volume", frame=f)
    snd["HIT"].volume = 0.8
    sc.frame_start, sc.frame_end = 1, last
    sc.frame_set(1)
    L.instructions(NOTE)
    return last


def export(path, w, h):
    sc = bpy.context.scene
    s = sc.render.image_settings
    s.media_type = "VIDEO"
    ff = sc.render.ffmpeg
    ff.format, ff.codec, ff.audio_codec, ff.audio_bitrate, ff.constant_rate_factor = "MPEG4", "H264", "AAC", 192, "MEDIUM"
    sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage = w, h, 100
    sc.render.filepath = path
    bpy.ops.render.render(animation=True)


def fix_paths():
    for s in bpy.data.sounds:
        s.filepath = "//../ASSETS/p12_audio/" + os.path.basename(s.filepath.replace("\\", "/"))


def main():
    ref = os.path.join(HERE, "REFERENCE")
    rd = os.path.join(ref, "renders")
    os.makedirs(rd, exist_ok=True)
    for f in os.listdir(rd):
        if f.endswith(".mp4"):
            os.remove(os.path.join(rd, f))
    make_audio()
    last = build()
    export(os.path.join(rd, "web_"), 640, 360)
    export(os.path.join(rd, "master_"), 1280, 720)
    for f in os.listdir(rd):
        if f.startswith("web_") and f.endswith(".mp4"):
            os.replace(os.path.join(rd, f), os.path.join(rd, "p12_web.mp4"))
        if f.startswith("master_") and f.endswith(".mp4"):
            os.replace(os.path.join(rd, f), os.path.join(rd, "p12_master.mp4"))
    sc = bpy.context.scene
    sc.render.resolution_x, sc.render.resolution_y = 640, 360
    sc.render.filepath = "//renders/p12_"
    fix_paths()
    L.save(os.path.join(ref, "p12_scene_reference.blend"))
    print("[p12] last", last, [(f, os.path.getsize(os.path.join(rd, f))) for f in os.listdir(rd)])


if __name__ == "__main__":
    L.run(main)
