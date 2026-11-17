"""
build_ch12_03_files.py — « Son » (CH12.03 : habiller une séquence : ambiance, bruitage synchronisé, réplique).

Données générées par ce script (48 kHz, mono, licence BCMA, dossier ASSETS/ch12_03_audio/) : amb_room.wav (ambiance : bruit grave de 4,2 s, RMS 0,02), sfx_hit.wav (coup : sinusoïde de 120 Hz à attaque immédiate et décroissance, 0,5 s),
  voice_line.wav (réplique synthétique : tons modulés autour de 220 Hz, 0,8 s : à remplacer par votre voix).
Scène (24 i/s, plage 1–96 = 4 s, Workbench) : trois marqueurs de timeline : IMPACT (image 49, la chute d'un objet), LINE (image 61, l'ouverture de la bouche d'un personnage) ; trois strips sonores nommés AMB, HIT, VOICE.
  Départ : AMB 11–59 (trop court : commence tard et finit tôt, en dehors de 1–96), HIT sur l'image 30 (trop tôt de 19 images), VOICE sur l'image 20 (trop tôt de 41 images), canaux 1, 2, 3.
  Consigne : synchroniser : (1) AMB commence à l'image 1 ou avant et couvre jusqu'à l'image 96 au moins (durée suffisante : dupliquer ou prolonger la boucle) ; (2) HIT commence à IMPACT (49) à ± 2 images ; (3) VOICE commence à LINE (61) à ± 3 images ;
    (4) rien n'est muet ; (5) le mixage (mixdown WAV) : énergie (RMS) des images 49–55 au moins 5 fois celle des images 40–47 (le coup se détache de l'ambiance), énergie des images 61–72 au moins 3 fois celle des images 56–59... (voir validate_ch12_03.py) ; crête ≤ 0,98 (pas d'écrêtage).
  Solution : AMB 1–97 (prolongé par une copie), HIT à 49, VOICE à 61.
  STARTER_FILES/ch12_03_sound_starter.blend ; COMPLETED_EXAMPLES/ch12_03_sound_solution.blend (+ _reference.png : enveloppe du mixage du départ et de la solution)
  COUNTER_EXAMPLES/ : late_hit (HIT à 53), early_voice (VOICE à 50), short_ambience (AMB 1–60), clipping (HIT volume 6 : écrêtage), muted_hit (HIT muet)
Usage : blender -b --factory-startup --python-exit-code 1 --python build_ch12_03_files.py
Testé avec : Blender 5.3.0.
"""
import math
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
AUDIO = os.path.join(CH, "ASSETS", "ch12_03_audio")
SR, FPS = 48000, 24
NOTE = """CH12.03 — SON (strips AMB, HIT, VOICE ; marqueurs IMPACT à 49 et LINE à 61)
Synchronisez le son sur l'image : (1) AMB (ambiance) couvre toute la séquence (image 1 à 96 au moins) ; (2) HIT commence sur le marqueur IMPACT (49 ± 2 images) ; (3) VOICE sur LINE (61 ± 3) ; (4) aucun strip muet ;
(5) le mixage : le coup (images 49–55) doit dominer l'ambiance (≥ 5 fois l'énergie des images 40–47) ; la réplique (61–72) doit dominer l'ambiance ; pas d'écrêtage (crête ≤ 0,98).
Outils : déplacer un strip (G), duplicateur (Shift+D), propriétés du strip (Sound : Volume, Mute).
Vérification : SCRIPTS/validate_ch12_03.py -- --exercise sound
"""


def write_wav(name, x):
    os.makedirs(AUDIO, exist_ok=True)
    x = np.clip(x, -1, 1)
    p = os.path.join(AUDIO, name)
    with wave.open(p, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((x * 32000).astype("<i2").tobytes())
    return p


def make_audio():
    rng = np.random.RandomState(4)
    t = np.arange(int(4.2 * SR)) / SR
    amb = rng.normal(0, 1, t.shape)
    k = np.ones(40) / 40.0
    amb = np.convolve(amb, k, mode="same")
    amb = amb / amb.std() * 0.02
    write_wav("amb_room.wav", amb)
    t = np.arange(int(0.5 * SR)) / SR
    write_wav("sfx_hit.wav", 0.8 * np.sin(2 * np.pi * 120 * t) * np.exp(-t * 10))
    t = np.arange(int(0.8 * SR)) / SR
    env = np.sin(np.pi * t / 0.8) ** 0.5
    write_wav("voice_line.wav", 0.3 * env * (np.sin(2 * np.pi * (220 + 30 * np.sin(2 * np.pi * 5 * t)) * t) + 0.5 * np.sin(2 * np.pi * 440 * t)))


def build(kind, rel):
    L.reset("SC_SOUND")
    sc = bpy.context.scene
    sc.render.fps = FPS
    sc.render.engine = "BLENDER_WORKBENCH"
    sc.frame_start, sc.frame_end = 1, 96
    sc.timeline_markers.new("IMPACT", frame=49)
    sc.timeline_markers.new("LINE", frame=61)
    se = sc.sequence_editor_create()
    plan = {"solution": dict(AMB=1, HIT=49, VOICE=61), "starter": dict(AMB=11, HIT=30, VOICE=20), "late_hit": dict(AMB=1, HIT=53, VOICE=61), "early_voice": dict(AMB=1, HIT=49, VOICE=50),
            "short_ambience": dict(AMB=1, HIT=49, VOICE=61), "clipping": dict(AMB=1, HIT=49, VOICE=61), "muted_hit": dict(AMB=1, HIT=49, VOICE=61)}[kind]
    files = {"AMB": "amb_room.wav", "HIT": "sfx_hit.wav", "VOICE": "voice_line.wav"}
    strips = {}
    for ch, name in enumerate(("AMB", "HIT", "VOICE"), start=1):
        s = se.strips.new_sound(name=name, filepath=os.path.join(AUDIO, files[name]), channel=ch, frame_start=plan[name])
        strips[name] = s
    if kind in ("solution", "late_hit", "early_voice", "clipping", "muted_hit"):
        # ambiance prolongée : une copie de 12 images bout à bout pour couvrir 1–97 (le fichier dure 4,2 s = 100 images à 24 i/s : couvre déjà 1–100)
        pass
    if kind == "short_ambience":
        strips["AMB"].frame_final_duration = 60
    if kind == "starter":
        strips["AMB"].frame_final_duration = 49
    if kind == "clipping":
        strips["HIT"].volume = 6.0
    if kind == "muted_hit":
        strips["HIT"].mute = True
    sc.frame_set(1)
    L.instructions(NOTE)
    return strips


def fix_paths(rel):
    for s in bpy.data.sounds:
        s.filepath = rel + os.path.basename(s.filepath.replace("\\", "/"))


def mix():
    p = os.path.join(tempfile.gettempdir(), "bcma_ch1203_mix.wav")
    if os.path.exists(p):
        os.remove(p)
    bpy.ops.sound.mixdown(filepath=p, check_existing=False, container="WAV", codec="PCM", format="S16", accuracy=1024, bitrate=192, split_channels=False)
    with wave.open(p, "rb") as w:
        n, ch, sr = w.getnframes(), w.getnchannels(), w.getframerate()
        x = np.frombuffer(w.readframes(n), dtype="<i2").astype(np.float32) / 32768.0
    x = x.reshape(-1, ch).mean(axis=1)
    return x, sr


def win(x, sr, f0, f1):
    a, b = int((f0 - 1) / FPS * sr), int(f1 / FPS * sr)
    seg = x[a:b]
    return float(np.sqrt((seg ** 2).mean())) if len(seg) else 0.0


def analyse(x, sr):
    return {"amb": win(x, sr, 40, 47), "hit": win(x, sr, 49, 55), "line": win(x, sr, 61, 72), "gap": win(x, sr, 56, 59), "tail": win(x, sr, 85, 96), "peak": float(np.abs(x).max())}


def calibrate():
    for kind in ("starter", "solution", "late_hit", "early_voice", "short_ambience", "clipping", "muted_hit"):
        build(kind, None)
        x, sr = mix()
        print("[snd]", kind, {k: round(v, 4) for k, v in analyse(x, sr).items()})


def sketch(path):
    W, H = 760, 300
    img = np.full((H, W, 3), 0.1, np.float32)
    for row, kind in enumerate(("starter", "solution")):
        build(kind, None)
        x, sr = mix()
        n = W - 20
        env = np.array([np.abs(x[int(i * len(x) / n):int((i + 1) * len(x) / n)]).max() if len(x) else 0 for i in range(n)])
        base = 130 + row * 150
        for i, v in enumerate(env):
            h = int(min(v, 1.0) * 60)
            img[max(base - h, 0):base + h + 1, 10 + i, :] = (0.3, 0.8, 0.4) if row else (0.8, 0.4, 0.3)
        for f, c in ((49, (1, 1, 0)), (61, (1, 0.5, 1))):
            xx = 10 + int((f - 1) / 96 * n)
            img[base - 70:base + 70, xx, :] = c
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
    build("starter", None)
    fix_paths("//../ASSETS/ch12_03_audio/")
    L.save(os.path.join(CH, "STARTER_FILES", "ch12_03_sound_starter.blend"))
    for k in ("late_hit", "early_voice", "short_ambience", "clipping", "muted_hit"):
        build(k, None)
        fix_paths("//../../ASSETS/ch12_03_audio/")
        L.save(os.path.join(out, "COUNTER_EXAMPLES", f"ch12_03_sound_{k}.blend"))
    sketch(os.path.join(out, "ch12_03_sound_reference.png"))
    build("solution", None)
    fix_paths("//../ASSETS/ch12_03_audio/")
    L.save(os.path.join(out, "ch12_03_sound_solution.blend"))


if __name__ == "__main__":
    L.run(main)
