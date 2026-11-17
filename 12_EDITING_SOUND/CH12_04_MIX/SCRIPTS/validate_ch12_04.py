"""
validate_ch12_04.py — Correcteur « Mixage » (CH12.04).
Usage : … --python-exit-code 1 --python validate_ch12_04.py -- --exercise mix [--debug]
Objets : strips sonores MUSIC (canal 1, image 1), VOICE (canal 2, image 61), HIT (canal 3, image 49) ; 24 i/s, plage 1–96. Le correcteur MIXE (bpy.ops.sound.mixdown, WAV PCM stéréo) chaque strip SEUL (les autres temporairement muets) puis le mixage complet, et mesure le RMS par fenêtres d'images :
  niveau de la musique : MUSIC seule, images 20–40, RMS de 0,03 à 0,09 (solution 0,040) ;
  ducking : MUSIC seule, images 61–72 / images 20–40 ≤ 0,5 (solution 0,40 ; sans ducking 1,19) ;
  intelligibilité : VOICE seule (61–72) ≥ 2 fois MUSIC seule (61–72) (solution 8,7) ;
  panoramique : HIT seul : RMS gauche ≥ 3 fois RMS droit (solution : droit nul ; au centre : égal) ;
  niveau global : RMS du mixage complet sur les images 1–96 de 0,03 à 0,12 (solution 0,077) et crête ≤ 0,9 (solution 0,60).
Les fichiers sonores et les positions des strips (MUSIC 1, VOICE 61, HIT 49) ne doivent pas être modifiés.
Testé avec : Blender 5.3.0.
"""
import os
import sys
import tempfile
import wave

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bpy  # noqa: E402
import numpy as np  # noqa: E402

FPS = 24


def mix(solo=None):
    se = bpy.context.scene.sequence_editor
    keep = {s.name: s.mute for s in se.strips_all}
    for s in se.strips_all:
        s.mute = False if solo is None else s.name != solo
    p = os.path.join(tempfile.gettempdir(), "bcma_ch1204_val.wav")
    if os.path.exists(p):
        os.remove(p)
    try:
        bpy.ops.sound.mixdown(filepath=p, check_existing=False, container="WAV", codec="PCM", format="S16", accuracy=1024, bitrate=192, split_channels=False)
    finally:
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


def main():
    debug = L.flag("--debug")
    r = L.Report("CH12.04 — Mixage")
    sc = bpy.context.scene
    se = sc.sequence_editor
    S = {s.name: s for s in se.strips_all if s.type == "SOUND"} if se else {}
    if not r.check(sorted(S) == ["HIT", "MUSIC", "VOICE"], f"Les trois strips sonores sont présents : {sorted(S)}", "Ne supprimez ni n'ajoutez de strip.", 3):
        return r.finish()
    r.check(S["MUSIC"].frame_final_start == 1 and S["VOICE"].frame_final_start == 61 and S["HIT"].frame_final_start == 49, "Positions inchangées : MUSIC 1, VOICE 61, HIT 49", "Mixez sans déplacer les strips.", 3)
    mu, sr = mix("MUSIC")
    vo, _ = mix("VOICE")
    hi, _ = mix("HIT")
    full, _ = mix()
    ref, duck, voice = rms(mu, sr, 20, 40), rms(mu, sr, 61, 72), rms(vo, sr, 61, 72)
    hl, hr = rms(hi, sr, 49, 62, 0), rms(hi, sr, 49, 62, 1)
    total, peak = rms(full, sr, 1, 96), float(np.abs(full).max())
    r.check(0.03 <= ref <= 0.09, f"Niveau de la musique : RMS {ref:.3f} (0,03–0,09) ; volume {S['MUSIC'].volume:.2f}", "MUSIC : volume ≈ 0,3.", 8)
    r.check(ref > 1e-4 and duck / ref <= 0.5, f"Ducking : musique pendant la réplique / avant = {duck / max(ref, 1e-6):.2f} (≤ 0,5)", "Animez le Volume du strip MUSIC : clés 0,3 → 0,1 sur 58–61, retour à 0,3 vers 76.", 10)
    r.check(duck > 1e-5 and voice >= 2 * duck, f"Intelligibilité : voix {voice:.3f}, musique {duck:.3f} pendant la réplique (rapport {voice / max(duck, 1e-6):.1f}, ≥ 2)", "La voix doit dominer la musique.", 8)
    r.check(hl >= 3 * hr and hl > 1e-4, f"Panoramique : HIT gauche {hl:.3f}, droite {hr:.3f} (gauche ≥ 3 × droite ; pan {S['HIT'].pan:+.1f})", "HIT : Pan −1 (gauche).", 8)
    r.check(0.03 <= total <= 0.12, f"Niveau global : RMS {total:.3f} (0,03–0,12)", "Ni trop faible ni trop fort : ajustez les volumes.", 8)
    r.check(peak <= 0.9, f"Crête : {peak:.2f} (≤ 0,9)", "Baissez les volumes : le mixage ne doit pas approcher 1,0.", 8)
    if debug:
        print("[DEBUG]", {"ref": ref, "duck": duck, "voice": voice, "hl": hl, "hr": hr, "total": total, "peak": peak})
    return r.finish()


if __name__ == "__main__":
    L.run(main)
