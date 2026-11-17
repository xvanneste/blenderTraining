"""
test_p12.py — Teste validate_p12.py : la RÉFÉRENCE doit être ACCEPTÉE ; chaque variante fausse doit être REFUSÉE par le contrôle visé.
Variantes (copies de REFERENCE dans un dossier temporaire) :
  jump_cut      : SH4 et SH5 permutés (deux gros plans de suite)       -> « Montage »
  slow_rhythm   : SH3 raccourci à 10 images (le rythme ralentit)       -> « Montage »
  no_crossfade  : strip Crossfade supprimé                             -> « Plans, titre, sons »
  subtitle_typo : « Bonjour » sans point                               -> « Sous-titres (SRT »
  late_hit      : HIT à l'image 60                                     -> « Son : »
  muted_voice   : VOICE muet                                           -> « Son : »
  no_duck       : volume de la musique sans animation                  -> « Mixage »
  no_web        : p12_web.mp4 supprimé                                 -> « Livraison renders/p12_web »
  small_master  : p12_master.mp4 remplacé par la version web          -> « p12_master.mp4 »
  no_audio_web  : p12_web.mp4 réexporté sans audio                     -> « p12_web.mp4 »
Usage : python 12_EDITING_SOUND/PROJECT_P12/test_p12.py
Testé avec : Blender 5.3.0.
"""
import os
import re
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
BLENDER = r"C:\Program Files\Blender Foundation\Blender 5.3\blender.exe"
REF = os.path.join(HERE, "REFERENCE")

MUTATE = r'''
import bpy, sys, os
kind = sys.argv[sys.argv.index("--") + 1]
sc = bpy.context.scene
se = sc.sequence_editor
S = {s.name: s for s in se.strips_all}
if kind == "jump_cut":
    a, b = S["SH4_medium"], S["SH5_close"]
    sa, sb = a.frame_start, b.frame_start
    a.frame_start = sb + 1000; b.frame_start = sa; a.frame_start = sb
elif kind == "slow_rhythm":
    S["SH3_close"].frame_final_duration = 10
elif kind == "no_crossfade":
    se.strips.remove(next(s for s in se.strips_all if s.type == "CROSS"))
elif kind == "subtitle_typo":
    S["SUB1"].text = "Bonjour"
elif kind == "late_hit":
    S["HIT"].frame_start = 60
elif kind == "muted_voice":
    S["VOICE"].mute = True
elif kind == "no_duck":
    sc.animation_data_clear()
    S["MUSIC"].volume = 0.3
elif kind == "no_audio_web":
    here = os.path.dirname(bpy.data.filepath)
    sc.render.ffmpeg.audio_codec = "NONE"
    sc.render.resolution_x, sc.render.resolution_y = 640, 360
    sc.render.filepath = os.path.join(here, "renders", "x_")
    bpy.ops.render.render(animation=True)
    for f in os.listdir(os.path.join(here, "renders")):
        if f.startswith("x_") and f.endswith(".mp4"):
            os.replace(os.path.join(here, "renders", f), os.path.join(here, "renders", "p12_web.mp4"))
bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath, copy=False)
'''

CASES = [("jump_cut", "Montage"), ("slow_rhythm", "Montage"), ("no_crossfade", "Plans, titre, sons"), ("subtitle_typo", "Sous-titres \\(SRT"), ("late_hit", "Son :"), ("muted_voice", "Son :"), ("no_duck", "Mixage"),
         ("no_web", "Livraison renders/p12_web"), ("small_master", "p12_master.mp4"), ("no_audio_web", "p12_web.mp4")]


def run_validator(blend):
    p = subprocess.run([BLENDER, "-b", "--factory-startup", blend, "--python-exit-code", "1", "--python", os.path.join(HERE, "validate_p12.py")],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    return p.returncode, [l.strip() for l in p.stdout.splitlines() if "✘" in l]


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    ok_all = True
    tmp = tempfile.mkdtemp(prefix="p12_")
    mut = os.path.join(tmp, "mutate.py")
    open(mut, "w", encoding="utf-8").write(MUTATE)
    # dossier temporaire à la même profondeur que REFERENCE pour les chemins relatifs des sons (//../ASSETS/…)
    work = os.path.join(tmp, "PROJECT_P12")
    os.makedirs(work)
    shutil.copytree(os.path.join(HERE, "ASSETS"), os.path.join(work, "ASSETS"))
    code, fails = run_validator(os.path.join(REF, "p12_scene_reference.blend"))
    ok = code == 0 and not fails
    print(f"[{'PASS' if ok else 'FAIL'}] référence ACCEPTÉE ({'0 échec' if ok else fails})")
    ok_all &= ok
    for kind, target in CASES:
        d = os.path.join(work, "V_" + kind)
        shutil.copytree(REF, d)
        blend = os.path.join(d, "p12_scene_reference.blend")
        rd = os.path.join(d, "renders")
        if kind == "no_web":
            os.remove(os.path.join(rd, "p12_web.mp4"))
        elif kind == "small_master":
            shutil.copy(os.path.join(rd, "p12_web.mp4"), os.path.join(rd, "p12_master.mp4"))
        else:
            subprocess.run([BLENDER, "-b", "--factory-startup", blend, "--python-exit-code", "1", "--python", mut, "--", kind], capture_output=True)
        code, fails = run_validator(blend)
        hit = [f for f in fails if re.search(target, f)]
        ok = code != 0 and bool(hit)
        print(f"[{'PASS' if ok else 'FAIL'}] {kind} REFUSÉE par « {target} » ({len(fails)} contrôle(s) en échec : {[f[:60] for f in fails]})")
        ok_all &= ok
    shutil.rmtree(tmp, ignore_errors=True)
    print("TOUS LES TESTS P12 OK" if ok_all else "ÉCHEC")
    return 0 if ok_all else 1


if __name__ == "__main__":
    sys.exit(main())
