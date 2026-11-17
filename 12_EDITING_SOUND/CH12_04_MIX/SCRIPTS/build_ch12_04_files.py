"""
build_ch12_04_files.py — « Mixage » (CH12.04 : niveaux, ducking de la musique sous la voix, panoramique, niveau global).

Données générées (48 kHz, mono, ASSETS/ch12_04_audio/) : music_pad.wav (nappe de trois sinusoïdes 220/277/330 Hz, 4,2 s, RMS 0,20), sfx_hit.wav (coup, RMS fort), voice_line.wav (réplique synthétique 0,8 s).
Scène (24 i/s, plage 1–96) : trois strips sonores : MUSIC (canal 1, image 1), VOICE (canal 2, image 61), HIT (canal 3, image 49) ; mixage de départ : tous au volume 1 et au centre : la musique écrase la voix.
  Consigne : mixer :
    1. niveau de la musique : RMS du strip MUSIC seul sur les images 20–40 de 0,03 à 0,09 (volume ≈ 0,3) ;
    2. ducking : RMS de la MUSIC seule sur les images 61–72 (pendant la réplique) ≤ 0,5 fois celui des images 20–40 (volume animé : 0,3 avant, ≈ 0,1 pendant, retour après : clés sur la propriété Volume) ;
    3. intelligibilité : RMS de VOICE seule (61–72) ≥ 2 fois celui de MUSIC seule (61–72) ;
    4. panoramique : HIT seul : le canal gauche ≥ 3 fois le droit (pan ≤ −0,6) ;
    5. niveau global : RMS du mixage complet (images 1–96) de 0,03 à 0,12 ; crête ≤ 0,9.
  Le correcteur mixe chaque strip SEUL (les autres temporairement muets, puis restaurés) et le mixage complet.
  Départ : tous volumes 1, pan 0. Solution : MUSIC volume 0,3 avec clés (0,3 → 0,1 de 58 à 61, 0,1 jusqu'à 72, retour à 0,3 en 76), HIT pan −1 et volume 0,8, VOICE volume 1.
  STARTER_FILES/ch12_04_mix_starter.blend ; COMPLETED_EXAMPLES/ch12_04_mix_solution.blend (+ _reference.png : enveloppes du départ et de la solution)
  COUNTER_EXAMPLES/ : no_duck (musique constante), loud_music (musique à 1 avec ducking relatif : trop forte), no_pan (HIT au centre), hot_mix (tout fort : crête > 0,9), quiet_mix (tout faible : RMS < 0,03)
Usage : blender -b --factory-startup --python-exit-code 1 --python build_ch12_04_files.py
Testé avec : Blender 5.3.0.
"""
import os
import sys
import tempfile
import wave

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bpy  # noqa: E402
import numpy as np  # noqa: E402

CH = L.chapter_dir(__file__)
AUDIO = os.path.join(CH, "ASSETS", "ch12_04_audio")
SR, FPS = 48000, 24
NOTE = """CH12.04 — MIXAGE (strips MUSIC, VOICE, HIT)
Tous les sons sont à fond et au centre : la musique écrase la voix. Mixez :
1. MUSIC : volume ≈ 0,3 (RMS de 0,03 à 0,09 sur les images 20–40).
2. Ducking : pendant la réplique (images 61–72) la musique baisse à ≤ 0,5 fois son niveau : animez la propriété Volume du strip MUSIC (clés : 0,3 → 0,1 → 0,3).
3. VOICE au moins deux fois plus fort que MUSIC pendant la réplique.
4. HIT à gauche : Pan ≤ −0,6.
5. Mixage complet : RMS de 0,03 à 0,12, crête ≤ 0,9.
Vérification : SCRIPTS/validate_ch12_04.py -- --exercise mix
"""


def write_wav(name, x):
    os.makedirs(AUDIO, exist_ok=True)
    p = os.path.join(AUDIO, name)
    with wave.open(p, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((np.clip(x, -1, 1) * 32000).astype("<i2").tobytes())
    return p


def make_audio():
    t = np.arange(int(4.2 * SR)) / SR
    pad = sum(np.sin(2 * np.pi * f * t) for f in (220, 277, 330)) * (0.7 + 0.3 * np.sin(2 * np.pi * 0.4 * t))
    pad = pad / np.sqrt((pad ** 2).mean()) * 0.20
    write_wav("music_pad.wav", pad)
    t = np.arange(int(0.5 * SR)) / SR
    write_wav("sfx_hit.wav", 0.8 * np.sin(2 * np.pi * 120 * t) * np.exp(-t * 10))
    t = np.arange(int(0.8 * SR)) / SR
    env = np.sin(np.pi * t / 0.8) ** 0.5
    write_wav("voice_line.wav", 0.3 * env * (np.sin(2 * np.pi * (220 + 30 * np.sin(2 * np.pi * 5 * t)) * t) + 0.5 * np.sin(2 * np.pi * 440 * t)))


def keys(s, pts):
    s.volume = pts[0][1]
    for f, v in pts:
        s.volume = v
        s.keyframe_insert("volume", frame=f)


def build(kind):
    L.reset("SC_MIX")
    sc = bpy.context.scene
    sc.render.fps = FPS
    sc.render.engine = "BLENDER_WORKBENCH"
    sc.frame_start, sc.frame_end = 1, 96
    sc.timeline_markers.new("LINE", frame=61)
    se = sc.sequence_editor_create()
    S = {}
    for ch, (name, f, st) in enumerate((("MUSIC", "music_pad.wav", 1), ("VOICE", "voice_line.wav", 61), ("HIT", "sfx_hit.wav", 49)), start=1):
        S[name] = se.strips.new_sound(name=name, filepath=os.path.join(AUDIO, f), channel=ch, frame_start=st)
    if kind != "starter":
        mv = {"solution": 0.3, "no_duck": 0.3, "loud_music": 1.0, "no_pan": 0.3, "hot_mix": 0.3, "quiet_mix": 0.03}[kind]
        if kind in ("no_duck", "hot_mix", "quiet_mix"):
            S["MUSIC"].volume = mv
        else:
            low = 0.1 if kind != "loud_music" else 0.34
            keys(S["MUSIC"], [(1, mv), (58, mv), (61, low), (72, low), (76, mv)])
        S["HIT"].pan = 0.0 if kind == "no_pan" else -1.0
        S["HIT"].volume = 0.8
        if kind == "hot_mix":
            S["VOICE"].volume = 4.0
            S["HIT"].volume = 4.0
        if kind == "quiet_mix":
            S["VOICE"].volume = 0.05
            S["HIT"].volume = 0.05
    sc.frame_set(1)
    L.instructions(NOTE)
    return S


def fix_paths(rel):
    for s in bpy.data.sounds:
        s.filepath = rel + os.path.basename(s.filepath.replace("\\", "/"))


def mix(solo=None):
    se = bpy.context.scene.sequence_editor
    keep = {s.name: s.mute for s in se.strips_all}
    if solo:
        for s in se.strips_all:
            s.mute = s.name != solo
    p = os.path.join(tempfile.gettempdir(), "bcma_ch1204_mix.wav")
    if os.path.exists(p):
        os.remove(p)
    bpy.ops.sound.mixdown(filepath=p, check_existing=False, container="WAV", codec="PCM", format="S16", accuracy=1024, bitrate=192, split_channels=False)
    for s in se.strips_all:
        s.mute = keep[s.name]
    with wave.open(p, "rb") as w:
        n, ch, sr = w.getnframes(), w.getnchannels(), w.getframerate()
        x = np.frombuffer(w.readframes(n), dtype="<i2").astype(np.float32).reshape(-1, ch) / 32768.0
    return x, sr


def rms(x, sr, f0, f1, chan=None):
    a, b = int((f0 - 1) / FPS * sr), int(f1 / FPS * sr)
    seg = x[a:b] if chan is None else x[a:b, chan:chan + 1]
    return float(np.sqrt((seg ** 2).mean())) if seg.size else 0.0


def analyse():
    mu, sr = mix("MUSIC")
    vo, _ = mix("VOICE")
    hi, _ = mix("HIT")
    full, _ = mix()
    return {"mus_ref": rms(mu, sr, 20, 40), "mus_vo": rms(mu, sr, 61, 72), "voice": rms(vo, sr, 61, 72), "hitL": rms(hi, sr, 49, 62, 0), "hitR": rms(hi, sr, 49, 62, 1),
            "total": rms(full, sr, 1, 96), "peak": float(np.abs(full).max())}


def calibrate():
    for kind in ("starter", "solution", "no_duck", "loud_music", "no_pan", "hot_mix", "quiet_mix"):
        build(kind)
        print("[mix]", kind, {k: round(v, 4) for k, v in analyse().items()})


def sketch(path):
    W, H = 760, 300
    img = np.full((H, W, 3), 0.1, np.float32)
    for row, kind in enumerate(("starter", "solution")):
        build(kind)
        for ci, (nm, col) in enumerate((("MUSIC", (0.3, 0.6, 1.0)), ("VOICE", (1.0, 0.8, 0.2)), ("HIT", (1.0, 0.3, 0.3)))):
            x, sr = mix(nm)
            x = np.abs(x).mean(axis=1)
            n = W - 20
            env = np.array([x[int(i * len(x) / n):int((i + 1) * len(x) / n)].max() if len(x) else 0 for i in range(n)])
            base = 70 + row * 150
            for i, v in enumerate(env):
                h = int(min(v, 1.0) * 55)
                if h > 0:
                    img[base - h:base + 1, 10 + i, :] = np.maximum(img[base - h:base + 1, 10 + i, :], col)
    rgba = np.concatenate([img, np.ones(img.shape[:2] + (1,), np.float32)], axis=2)
    out = bpy.data.images.new("sk", W, H)
    out.pixels = rgba[::-1].ravel()
    out.filepath_raw = path
    out.file_format = "PNG"
    out.save()


def main():
    out = os.path.join(CH, "COMPLETED_EXAMPLES")
    make_audio()
    calibrate()
    build("starter")
    fix_paths("//../ASSETS/ch12_04_audio/")
    L.save(os.path.join(CH, "STARTER_FILES", "ch12_04_mix_starter.blend"))
    for k in ("no_duck", "loud_music", "no_pan", "hot_mix", "quiet_mix"):
        build(k)
        fix_paths("//../../ASSETS/ch12_04_audio/")
        L.save(os.path.join(out, "COUNTER_EXAMPLES", f"ch12_04_mix_{k}.blend"))
    sketch(os.path.join(out, "ch12_04_mix_reference.png"))
    build("solution")
    fix_paths("//../ASSETS/ch12_04_audio/")
    L.save(os.path.join(out, "ch12_04_mix_solution.blend"))


if __name__ == "__main__":
    L.run(main)
