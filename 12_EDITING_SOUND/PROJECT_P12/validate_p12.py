"""
validate_p12.py — Correcteur du projet P12 « Une séquence finalisée » (montage, titre, sous-titres, son, mixage, export master + web).
Usage : blender -b --factory-startup <fichier.blend> --python-exit-code 1 --python validate_p12.py [-- --debug]
Données : strips COLOR SH1_wide … SH6_wide (couleurs de plans), strip effet Crossfade, strips de texte (TITLE et sous-titres), strips sonores AMB, HIT, VOICE, MUSIC ; marqueurs IMPACT (image 55) et LINE (image 85) ; 24 i/s. Le correcteur contrôle :
  1. montage (CH12.01–02) : les six plans, échelles (suffixe du nom) jamais identiques à deux plans consécutifs ; durées des cinq premiers plans (par début) non croissantes ; SH6 ≥ 2 × le cinquième ; Crossfade (CROSS) entre le cinquième plan et SH6 (recouvrement de 8 à 16 images) ; plage de la scène 1–dernière image du montage ;
  2. titres (CH12.05) : strip TITLE de texte non vide, centré (location (0,5 ; 0,5)), taille ≥ 40, commençant à l'image 1 ; sous-titres : export SRT (Sequencer > Export Subtitles) : entrées « Bonjour. » 1,250→2,250 s et « Il fait nuit. » 3,500→4,333 s à ± 2 images ; en bas (y ≤ 0,2) ;
  3. son (CH12.03) : HIT commence à IMPACT ± 2 ; VOICE à LINE ± 3 ; AMB couvre 1 à la fin ; aucun strip muet ;
  4. mixage (CH12.04, mixdown de chaque strip seul) : MUSIC (images 20–40) de 0,03 à 0,09 ; ducking : MUSIC pendant la réplique (85–104) / avant ≤ 0,5 ; VOICE ≥ 2 × MUSIC pendant la réplique ; mixage complet : RMS de 0,03 à 0,15, crête ≤ 0,9 ;
  5. livraison (CH12.06) : renders/p12_web.mp4 : H.264 (avc1) + AAC (mp4a), 640 × 360 ; renders/p12_master.mp4 : H.264 + AAC, au moins 1 280 × 720 ; durée de chaque fichier égale à la durée de la scène (± 0,15 s) ; poids de la version web ≤ 1,5 Mo.
Testé avec : Blender 5.3.0.
"""
import os
import re
import sys
import tempfile
import wave

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "SCRIPTS"))
sys.path.insert(0, os.path.join(HERE, "..", "CH12_06_EXPORT", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bpy  # noqa: E402
import mp4probe  # noqa: E402
import numpy as np  # noqa: E402

FPS = 24
SHOTS = ["SH1_wide", "SH2_medium", "SH3_close", "SH4_medium", "SH5_close", "SH6_wide"]
REF_SUBS = [("Bonjour.", 1.25, 2.25), ("Il fait nuit.", 3.5, 4.3333)]


def parse_srt(s):
    out = []
    for blk in re.split(r"\n\s*\n", s.strip()):
        lines = [l for l in blk.strip().splitlines() if l.strip()]
        if len(lines) < 3:
            continue
        m = re.match(r"(\d+):(\d+):(\d+),(\d+) --> (\d+):(\d+):(\d+),(\d+)", lines[1])
        if m:
            g = [int(v) for v in m.groups()]
            out.append((" ".join(lines[2:]), g[0] * 3600 + g[1] * 60 + g[2] + g[3] / 1000.0, g[4] * 3600 + g[5] * 60 + g[6] + g[7] / 1000.0))
    return out


def export_srt(sc, texts):
    se = sc.sequence_editor
    for s in se.strips_all:
        s.select = s in texts
    se.active_strip = texts[0]
    win = bpy.context.window_manager.windows[0]
    area = win.screen.areas[0]
    keep = area.type
    area.type = "SEQUENCE_EDITOR"
    sp = area.spaces.active
    reg = [r for r in area.regions if r.type == "WINDOW"][0]
    out = os.path.join(tempfile.gettempdir(), "bcma_p12_val.srt")
    if os.path.exists(out):
        os.remove(out)
    try:
        with bpy.context.temp_override(window=win, area=area, region=reg, space_data=sp, scene=sc, sequencer_scene=sc):
            bpy.ops.sequencer.export_subtitles(filepath=out)
    finally:
        area.type = keep
    return open(out, encoding="utf-8").read()


def mix(solo=None):
    se = bpy.context.scene.sequence_editor
    keep = {s.name: s.mute for s in se.strips_all}
    for s in se.strips_all:
        s.mute = False if solo is None else s.name != solo
    p = os.path.join(tempfile.gettempdir(), "bcma_p12_mix.wav")
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


def rms(x, sr, f0, f1):
    a, b = int((f0 - 1) / FPS * sr), int(f1 / FPS * sr)
    seg = x[a:b]
    return float(np.sqrt((seg ** 2).mean())) if seg.size else 0.0


def main():
    debug = L.flag("--debug")
    r = L.Report("P12 — Une séquence finalisée")
    sc = bpy.context.scene
    se = sc.sequence_editor
    allst = list(se.strips_all) if se else []
    S = {s.name: s for s in allst}
    need = SHOTS + ["TITLE", "AMB", "HIT", "VOICE", "MUSIC"]
    if not r.check(all(n in S for n in need) and sum(1 for s in allst if s.type == "CROSS") == 1, "Plans, titre, sons et un Crossfade présents", "Partez de la scène fournie : ne supprimez aucun strip.", 4):
        return r.finish()
    r.check(sc.render.fps == 24, f"Cadence : {sc.render.fps} i/s", "24 i/s.", 2)
    # 1. montage
    others = sorted((S[n] for n in SHOTS if n != "SH6_wide"), key=lambda s: s.frame_final_start)
    six = S["SH6_wide"]
    seq = others + [six]
    size = lambda s: s.name.rsplit("_", 1)[1]
    jumps = [f"{a.name}→{b.name}" for a, b in zip(seq, seq[1:]) if size(a) == size(b)]
    d = [s.frame_final_duration for s in others]
    cross = [s for s in allst if s.type == "CROSS"][0]
    ov = others[-1].frame_final_end - six.frame_final_start
    last = max(S[n].frame_final_end for n in SHOTS) - 1
    ok = not jumps and all(d[i] >= d[i + 1] for i in range(len(d) - 1)) and six.frame_final_duration >= 2 * d[-1]
    r.check(ok, f"Montage : échelles alternées, durées {d}, résolution SH6 {six.frame_final_duration}" if ok else f"Montage : faux raccords {jumps or 'aucun'} ; durées {d} ; SH6 {six.frame_final_duration}", "Alternez les échelles ; durées non croissantes ; SH6 ≥ 2 × le cinquième plan.", 10)
    ok = cross.input_1 == others[-1] and cross.input_2 == six and 8 <= ov <= 16
    r.check(ok, f"Fondu : Crossfade (cinquième plan → SH6), recouvrement {ov} images", "Crossfade entre le cinquième plan et SH6 avec 8 à 16 images de recouvrement.", 8)
    r.check(sc.frame_start == 1 and sc.frame_end == last, f"Plage de la scène : 1–{sc.frame_end} (dernière image du montage {last})", "Frame End = dernière image du dernier plan.", 6)
    # 2. titres
    t = S["TITLE"]
    r.check(t.type == "TEXT" and t.text.strip() != "" and tuple(round(v, 2) for v in t.location) == (0.5, 0.5) and t.font_size >= 40 and t.frame_final_start <= 2, f"Titre : « {t.text} », centré, taille {t.font_size:.0f}", "TITLE : texte non vide, location (0,5 ; 0,5), taille ≥ 40, début à l'image 1.", 6)
    subs = [s for s in allst if s.type == "TEXT" and s.name != "TITLE"]
    if subs:
        ent = [e for e in parse_srt(export_srt(sc, subs)) if e[0] != t.text]
        ent = sorted(ent, key=lambda e: e[1])
        ok = len(ent) == 2 and all(e[0] == w[0] and abs(e[1] - w[1]) <= 2 / FPS and abs(e[2] - w[2]) <= 2 / FPS for e, w in zip(ent, REF_SUBS))
        detail = " ; ".join(f"« {e[0]} » {e[1]:.2f}→{e[2]:.2f}" for e in ent)
        r.check(ok, f"Sous-titres (SRT exporté) : {detail}", "« Bonjour. » 1,25→2,25 s ; « Il fait nuit. » 3,50→4,33 s (± 2 images) ; textes exacts.", 10)
        r.check(all(s.location[1] <= 0.2 for s in subs), "Sous-titres en bas de l'image (y ≤ 0,2)", "location y ≤ 0,2.", 4)
    else:
        r.check(False, "Sous-titres : aucun strip de texte en dehors de TITLE", "Créez les deux sous-titres.", 14)
    # 3. son
    mk = {m.name: m.frame for m in sc.timeline_markers}
    r.check(abs(S["HIT"].frame_final_start - mk.get("IMPACT", 55)) <= 2 and abs(S["VOICE"].frame_final_start - mk.get("LINE", 85)) <= 3 and S["AMB"].frame_final_start <= 1 and S["AMB"].frame_final_end >= last + 1 and not any(S[n].mute for n in ("AMB", "HIT", "VOICE", "MUSIC")),
            f"Son : HIT à {S['HIT'].frame_final_start} (IMPACT {mk.get('IMPACT', 55)} ± 2), VOICE à {S['VOICE'].frame_final_start} (LINE {mk.get('LINE', 85)} ± 3), AMB {S['AMB'].frame_final_start}–{S['AMB'].frame_final_end - 1}", "Calez HIT sur IMPACT, VOICE sur LINE, AMB sur toute la durée, rien de muet.", 8)
    # 4. mixage
    mu, sr = mix("MUSIC")
    vo, _ = mix("VOICE")
    full, _ = mix()
    ref, duck, voice = rms(mu, sr, 20, 40), rms(mu, sr, 85, 104), rms(vo, sr, 85, 104)
    total, peak = rms(full, sr, 1, last), float(np.abs(full).max())
    r.check(0.03 <= ref <= 0.09 and ref > 1e-4 and duck / ref <= 0.5 and voice >= 2 * duck, f"Mixage : musique {ref:.3f}, ducking {duck / max(ref, 1e-6):.2f} (≤ 0,5), voix / musique {voice / max(duck, 1e-6):.1f} (≥ 2)", "MUSIC ≈ 0,3 avec ducking pendant la réplique ; VOICE dominante.", 10)
    r.check(0.03 <= total <= 0.15 and peak <= 0.9, f"Niveau global : RMS {total:.3f} (0,03–0,15), crête {peak:.2f} (≤ 0,9)", "Ni trop faible ni écrêté.", 6)
    # 5. livraison
    here = os.path.dirname(bpy.data.filepath)
    dur = last / float(FPS)
    for fname, minw, minh, mb in (("p12_web.mp4", 640, 360, 1.5), ("p12_master.mp4", 1280, 720, 40.0)):
        fp = os.path.join(here, "renders", fname)
        if not os.path.exists(fp):
            r.check(False, f"Livraison renders/{fname}", "Exportez le fichier (CH12.06).", 8)
            continue
        res = mp4probe.analyse(fp)
        v = next((x for x in res["tracks"] if x["kind"] == "vide"), None)
        a = next((x for x in res["tracks"] if x["kind"] == "soun"), None)
        size_mb = os.path.getsize(fp) / 1048576.0
        ok = v is not None and v["codec"] == "avc1" and a is not None and a["codec"] == "mp4a" and v["width"] >= minw and v["height"] >= minh and abs(res["duration"] - dur) <= 0.15 and size_mb <= mb
        what = f"{v['codec'] if v else '—'}/{a['codec'] if a else '—'} {v['width'] if v else 0}×{v['height'] if v else 0}, {res['duration']:.2f} s, {size_mb:.2f} Mo"
        r.check(ok, f"{fname} : {what} (H.264 + AAC, ≥ {minw} × {minh}, durée {dur:.2f} s ± 0,15)", "MP4 H.264 + AAC, résolution et durée corrects.", 8)
    if debug:
        print("[DEBUG]", {"ref": ref, "duck": duck, "voice": voice, "total": total, "peak": peak, "last": last})
    return r.finish()


if __name__ == "__main__":
    L.run(main)
