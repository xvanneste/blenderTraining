"""
test_p9.py — Teste validate_p9.py : la RÉFÉRENCE doit être ACCEPTÉE ; chaque variante fausse doit être REFUSÉE par le contrôle visé.
Variantes (copies de REFERENCE dans un dossier temporaire) :
  bright_sadness : monde de SH_SADNESS à la force 0,5            -> « SADNESS »
  cold_joy       : monde et lampe de SH_JOY bleutés              -> « JOY »
  centered_joy   : Shift X de la caméra de SH_JOY à 0            -> « JOY »
  pale_anger     : monde et lampe de SH_ANGER blancs             -> « ANGER »
  contrasty_calm : lampe de 3 000 W ajoutée à SH_CALM            -> « CALM »
  big_fear       : caméra de SH_FEAR avancée à y = 0             -> « FEAR »
  moved_hero     : Hero déplacé de 1 m                           -> « Hero présent »
  missing_scene  : SH_CALM supprimée                             -> « Les cinq scènes »
  no_sheet       : planche supprimée                             -> « Planche »
  dark_sheet     : planche remplacée par une image noire         -> « Planche »
Usage : python 09_CINEMATOGRAPHY/PROJECT_P9/test_p9.py
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
S = bpy.data.scenes
def bg(scene):
    return S[scene].world.node_tree.nodes["Background"]
if kind == "bright_sadness":
    bg("SH_SADNESS").inputs["Strength"].default_value = 0.5
elif kind == "cold_joy":
    bg("SH_JOY").inputs["Color"].default_value = (0.5, 0.7, 1.0, 1)
    for o in S["SH_JOY"].objects:
        if o.type == "LIGHT":
            o.data.color = (0.5, 0.7, 1.0)
elif kind == "centered_joy":
    bpy.data.objects["CAM_JOY"].data.shift_x = 0.0
elif kind == "pale_anger":
    bg("SH_ANGER").inputs["Color"].default_value = (1, 1, 1, 1)
    for o in S["SH_ANGER"].objects:
        if o.type == "LIGHT":
            o.data.color = (1, 1, 1)
elif kind == "contrasty_calm":
    ld = bpy.data.lights.new("EXTRA", "POINT")
    ld.energy = 3000
    ob = bpy.data.objects.new("EXTRA", ld)
    S["SH_CALM"].collection.objects.link(ob)
    ob.location = (-2, 3, 3)
elif kind == "big_fear":
    bpy.data.objects["CAM_FEAR"].location.y = 0.0
elif kind == "moved_hero":
    bpy.data.objects["Hero"].location.x = 1.0
elif kind == "missing_scene":
    S.remove(S["SH_CALM"])
elif kind == "dark_sheet":
    im = bpy.data.images.new("dark", 2000, 225)
    im.pixels = [0.0, 0.0, 0.0, 1.0] * (2000 * 225)
    im.filepath_raw = os.path.join(os.path.dirname(bpy.data.filepath), "renders", "p9_contact_sheet.png")
    im.file_format = "PNG"
    im.save()
bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath, copy=False)
'''

CASES = [("bright_sadness", "SADNESS :"), ("cold_joy", "JOY :"), ("centered_joy", "JOY :"), ("pale_anger", "ANGER :"), ("contrasty_calm", "CALM :"), ("big_fear", "FEAR :"),
         ("moved_hero", "Hero présent"), ("missing_scene", "Les cinq scènes"), ("no_sheet", "Planche"), ("dark_sheet", "Planche")]


def run_validator(blend):
    p = subprocess.run([BLENDER, "-b", "--factory-startup", blend, "--python", os.path.join(HERE, "validate_p9.py"), "--python-exit-code", "1"],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    return p.returncode, [l.strip() for l in p.stdout.splitlines() if "✘" in l]


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    ok_all = True
    tmp = tempfile.mkdtemp(prefix="p9_")
    mut = os.path.join(tmp, "mutate.py")
    open(mut, "w", encoding="utf-8").write(MUTATE)
    code, fails = run_validator(os.path.join(REF, "p9_scene_reference.blend"))
    ok = code == 0 and not fails
    print(f"[{'PASS' if ok else 'FAIL'}] référence ACCEPTÉE ({'0 échec' if ok else fails})")
    ok_all &= ok
    for kind, target in CASES:
        d = os.path.join(tmp, kind)
        shutil.copytree(REF, d)
        blend = os.path.join(d, "p9_scene_reference.blend")
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
    print("TOUS LES TESTS P9 OK" if ok_all else "ÉCHEC")
    return 0 if ok_all else 1


if __name__ == "__main__":
    sys.exit(main())
