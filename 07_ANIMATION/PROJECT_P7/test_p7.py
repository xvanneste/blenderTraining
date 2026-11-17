"""
test_p7.py — Teste validate_p7.py : la RÉFÉRENCE doit être ACCEPTÉE ; chaque variante fausse doit être REFUSÉE par le contrôle visé.
Variantes (copies de REFERENCE dans un dossier temporaire) :
  no_crossfade    : Blend In = 0 sur tous les strips              -> « Montage NLA »
  active_action   : une action laissée active sur le rig          -> « Montage NLA »
  one_camera      : CAM_B supprimée (et son marqueur)             -> « Caméras »
  unbound_markers : marqueurs de caméra déliés                    -> « Caméras »
  no_dialogue     : texte DIALOGUE supprimé                       -> « Dialogue »
  late_lines      : réplique 1 déplacée à l'image 150             -> « Dialogue »
  short_scene     : plage 1–200                                   -> « Durée »
  no_sheet        : planche supprimée                             -> « Planche »
  dark_sheet      : planche remplacée par une image noire         -> « Planche »
Usage : python 07_ANIMATION/PROJECT_P7/test_p7.py
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
rig = bpy.data.objects["RIG_Mannequin"]
if kind == "no_crossfade":
    for t in rig.animation_data.nla_tracks:
        for s in t.strips:
            s.blend_in = 0.0
elif kind == "active_action":
    a = bpy.data.actions["ACT_acting"]
    rig.animation_data.action = a
    rig.animation_data.action_slot = a.slots[0]
elif kind == "one_camera":
    for m in list(sc.timeline_markers):
        if m.camera and m.camera.name == "CAM_B":
            sc.timeline_markers.remove(m)
    bpy.data.objects.remove(bpy.data.objects["CAM_B"], do_unlink=True)
elif kind == "unbound_markers":
    for m in sc.timeline_markers:
        m.camera = None
elif kind == "no_dialogue":
    bpy.data.texts.remove(bpy.data.texts["DIALOGUE"])
elif kind == "late_lines":
    for m in sc.timeline_markers:
        if m.name == "line_1":
            m.frame = 150
    t = bpy.data.texts["DIALOGUE"]
    t.clear()
    t.write("image 150 : Tiens, qu'est-ce que c'est ?\nimage 253 : Je crois qu'on peut y aller.\n")
elif kind == "short_scene":
    sc.frame_end = 200
elif kind == "dark_sheet":
    im = bpy.data.images.new("dark", 1920, 270)
    im.pixels = [0.0, 0.0, 0.0, 1.0] * (1920 * 270)
    im.filepath_raw = os.path.join(os.path.dirname(bpy.data.filepath), "renders", "p7_contact_sheet.png")
    im.file_format = "PNG"
    im.save()
bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath, copy=False)
'''

CASES = [("no_crossfade", "Montage NLA"), ("active_action", "Montage NLA"), ("one_camera", "Caméras"), ("unbound_markers", "Caméras"), ("no_dialogue", "Dialogue"),
         ("late_lines", "Dialogue"), ("short_scene", "Durée"), ("no_sheet", "Planche"), ("dark_sheet", "Planche")]


def run_validator(blend):
    p = subprocess.run([BLENDER, "-b", "--factory-startup", blend, "--python", os.path.join(HERE, "validate_p7.py"), "--python-exit-code", "1"],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    return p.returncode, [l.strip() for l in p.stdout.splitlines() if "✘" in l]


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    ok_all = True
    tmp = tempfile.mkdtemp(prefix="p7_")
    mut = os.path.join(tmp, "mutate.py")
    open(mut, "w", encoding="utf-8").write(MUTATE)
    code, fails = run_validator(os.path.join(REF, "p7_scene_reference.blend"))
    ok = code == 0 and not fails
    print(f"[{'PASS' if ok else 'FAIL'}] référence ACCEPTÉE ({'0 échec' if ok else fails})")
    ok_all &= ok
    for kind, target in CASES:
        d = os.path.join(tmp, kind)
        shutil.copytree(REF, d)
        blend = os.path.join(d, "p7_scene_reference.blend")
        if kind == "no_sheet":
            shutil.rmtree(os.path.join(d, "renders"))
        else:
            subprocess.run([BLENDER, "-b", "--factory-startup", blend, "--python", mut, "--python-exit-code", "1", "--", kind], capture_output=True)
        code, fails = run_validator(blend)
        hit = [f for f in fails if re.search(target, f)]
        ok = code != 0 and bool(hit)
        print(f"[{'PASS' if ok else 'FAIL'}] {kind} REFUSÉE par « {target} » ({len(fails)} contrôle(s) en échec : {[f[:62] for f in fails]})")
        ok_all &= ok
    shutil.rmtree(tmp, ignore_errors=True)
    print("TOUS LES TESTS P7 OK" if ok_all else "ÉCHEC")
    return 0 if ok_all else 1


if __name__ == "__main__":
    sys.exit(main())
