"""
validate_ch12_03.py — Correcteur « Son » (CH12.03).
Usage : … --python-exit-code 1 --python validate_ch12_03.py -- --exercise sound [--debug]
Objets : strips sonores AMB, HIT, VOICE ; marqueurs IMPACT (image 49) et LINE (image 61) ; 24 i/s, plage 1–96. Le correcteur lit les strips et MIXE réellement (bpy.ops.sound.mixdown en WAV), puis mesure l'énergie (RMS) sur des fenêtres d'images :
  données : HIT commence à ± 2 images de IMPACT ; VOICE à ± 3 images de LINE ; AMB commence à l'image 1 ou avant et finit à l'image 97 ou après ; aucun strip muet ;
  mixage : énergie des images 49–55 ≥ 5 fois celle des images 40–47 (le coup se détache de l'ambiance : solution 12 ×) ; énergie des images 56–59 ≤ 0,04 (silence relatif entre le coup et la réplique : solution 0,017) ;
  énergie des images 61–72 ≥ 5 fois celle des images 40–47 (réplique : 10 ×) ; énergie des images 85–96 ≥ 0,5 fois celle des images 40–47 (l'ambiance dure jusqu'au bout) ; crête du mixage ≤ 0,98.
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


def win(x, sr, f0, f1):
    a, b = int((f0 - 1) / FPS * sr), int(f1 / FPS * sr)
    seg = x[a:b]
    return float(np.sqrt((seg ** 2).mean())) if len(seg) else 0.0


def main():
    debug = L.flag("--debug")
    r = L.Report("CH12.03 — Son")
    sc = bpy.context.scene
    se = sc.sequence_editor
    S = {s.name: s for s in se.strips_all if s.type == "SOUND"} if se else {}
    if not r.check(sorted(S) == ["AMB", "HIT", "VOICE"], f"Les trois strips sonores sont présents : {sorted(S)}", "Ne supprimez ni n'ajoutez de strip sonore : AMB, HIT, VOICE.", 3):
        return r.finish()
    mk = {m.name: m.frame for m in sc.timeline_markers}
    r.check(not any(s.mute for s in S.values()), "Aucun strip sonore muet", "Désactivez Mute (propriétés du strip).", 4)
    h, v, a = S["HIT"].frame_final_start, S["VOICE"].frame_final_start, S["AMB"]
    r.check(abs(h - mk.get("IMPACT", 49)) <= 2, f"HIT commence à l'image {h} (IMPACT : {mk.get('IMPACT', 49)} ± 2)", "Placez le début du strip HIT sur le marqueur IMPACT.", 8)
    r.check(abs(v - mk.get("LINE", 61)) <= 3, f"VOICE commence à l'image {v} (LINE : {mk.get('LINE', 61)} ± 3)", "Placez le début du strip VOICE sur le marqueur LINE.", 8)
    r.check(a.frame_final_start <= 1 and a.frame_final_end >= 97, f"AMB couvre l'images {a.frame_final_start} à {a.frame_final_end - 1} (1–96 attendu)", "Déplacez/prolongez l'ambiance : elle doit commencer à l'image 1 et durer jusqu'à la 96.", 6)
    out = os.path.join(tempfile.gettempdir(), "bcma_ch1203_val.wav")
    if os.path.exists(out):
        os.remove(out)
    bpy.ops.sound.mixdown(filepath=out, check_existing=False, container="WAV", codec="PCM", format="S16", accuracy=1024, bitrate=192, split_channels=False)
    with wave.open(out, "rb") as w:
        n, ch, sr = w.getnframes(), w.getnchannels(), w.getframerate()
        x = np.frombuffer(w.readframes(n), dtype="<i2").astype(np.float32) / 32768.0
    x = x.reshape(-1, ch).mean(axis=1)
    amb, hit, gap, line, tail, peak = win(x, sr, 40, 47), win(x, sr, 49, 55), win(x, sr, 56, 59), win(x, sr, 61, 72), win(x, sr, 85, 96), float(np.abs(x).max())
    r.check(amb > 1e-4 and hit >= 5 * amb, f"Le coup se détache : énergie 49–55 = {hit:.3f}, ambiance 40–47 = {amb:.4f} (rapport {hit / max(amb, 1e-6):.1f}, ≥ 5)", "HIT doit sonner à partir de l'image 49 et dépasser l'ambiance.", 8)
    r.check(gap <= 0.04, f"Silence relatif entre le coup et la réplique : énergie 56–59 = {gap:.3f} (≤ 0,04)", "Rien d'autre que l'ambiance entre les images 56 et 59 : le coup doit être calé sur IMPACT.", 6)
    r.check(amb > 1e-4 and line >= 5 * amb, f"La réplique domine : énergie 61–72 = {line:.3f} (rapport {line / max(amb, 1e-6):.1f}, ≥ 5)", "VOICE doit sonner à partir de l'image 61.", 6)
    r.check(tail >= 0.5 * amb and amb > 1e-4, f"L'ambiance dure : énergie 85–96 = {tail:.4f} (≥ 0,5 × {amb:.4f})", "Prolongez l'ambiance jusqu'à l'image 96.", 6)
    r.check(peak <= 0.98, f"Pas d'écrêtage : crête du mixage {peak:.2f} (≤ 0,98)", "Baissez le volume du strip trop fort.", 6)
    if debug:
        print("[DEBUG]", {"amb": amb, "hit": hit, "gap": gap, "line": line, "tail": tail, "peak": peak})
    return r.finish()


if __name__ == "__main__":
    L.run(main)
