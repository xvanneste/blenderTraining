"""
test_p8.py — Teste validate_p8.py : la RÉFÉRENCE doit être ACCEPTÉE ; chaque variante fausse doit être REFUSÉE par le contrôle visé.
Variantes (copies de REFERENCE dans un dossier temporaire) :
  no_breaking   : contraintes non cassables                     -> « Contraintes »
  light_ball    : boulet de 5 kg                                -> « Destruction : monde »
  no_wind       : FORCE_Wind supprimé                           -> « Vent »
  cloth_unpinned: groupe d'épinglage retiré du tissu            -> « Tissu »
  cloth_deaf    : poids de champ « wind » du tissu à 0          -> « le bas est poussé »
  no_dust       : système de particules supprimé                -> « Particules »
  dust_blown    : poids de champ « wind » de la poussière à 1   -> « Poussière »
  short_scene   : plage 1–100                                   -> « Durée »
  no_sheet      : planche supprimée                             -> « Planche »
  dark_sheet    : planche remplacée par une image noire         -> « Planche »
Usage : python 08_SIMULATIONS/PROJECT_P8/test_p8.py
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
if kind == "no_breaking":
    for o in bpy.data.objects:
        if o.rigid_body_constraint:
            o.rigid_body_constraint.use_breaking = False
elif kind == "light_ball":
    bpy.data.objects["Wreck_Ball"].rigid_body.mass = 5.0
elif kind == "no_wind":
    bpy.data.objects.remove(bpy.data.objects["FORCE_Wind"], do_unlink=True)
elif kind == "cloth_unpinned":
    cm = next(m for m in bpy.data.objects["Flag"].modifiers if m.type == "CLOTH")
    cm.settings.vertex_group_mass = ""
elif kind == "cloth_deaf":
    cm = next(m for m in bpy.data.objects["Flag"].modifiers if m.type == "CLOTH")
    cm.settings.effector_weights.wind = 0.0
elif kind == "no_dust":
    d = bpy.data.objects["Dust"]
    d.modifiers.remove(next(m for m in d.modifiers if m.type == "PARTICLE_SYSTEM"))
elif kind == "dust_blown":
    bpy.data.objects["Dust"].particle_systems[0].settings.effector_weights.wind = 1.0
elif kind == "short_scene":
    sc.frame_end = 100
elif kind == "dark_sheet":
    im = bpy.data.images.new("dark", 1920, 270)
    im.pixels = [0.0, 0.0, 0.0, 1.0] * (1920 * 270)
    im.filepath_raw = os.path.join(os.path.dirname(bpy.data.filepath), "renders", "p8_contact_sheet.png")
    im.file_format = "PNG"
    im.save()
bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath, copy=False)
'''

CASES = [("no_breaking", "Contraintes"), ("light_ball", "Destruction : monde"), ("no_wind", "Vent"), ("cloth_unpinned", "Tissu"), ("cloth_deaf", "le bas est poussé"),
         ("no_dust", "Particules"), ("dust_blown", "Poussière"), ("short_scene", "Durée"), ("no_sheet", "Planche"), ("dark_sheet", "Planche")]


def run_validator(blend):
    p = subprocess.run([BLENDER, "-b", "--factory-startup", blend, "--python", os.path.join(HERE, "validate_p8.py"), "--python-exit-code", "1"],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    return p.returncode, [l.strip() for l in p.stdout.splitlines() if "✘" in l]


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    ok_all = True
    tmp = tempfile.mkdtemp(prefix="p8_")
    mut = os.path.join(tmp, "mutate.py")
    open(mut, "w", encoding="utf-8").write(MUTATE)
    code, fails = run_validator(os.path.join(REF, "p8_scene_reference.blend"))
    ok = code == 0 and not fails
    print(f"[{'PASS' if ok else 'FAIL'}] référence ACCEPTÉE ({'0 échec' if ok else fails})")
    ok_all &= ok
    for kind, target in CASES:
        d = os.path.join(tmp, kind)
        shutil.copytree(REF, d)
        blend = os.path.join(d, "p8_scene_reference.blend")
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
    print("TOUS LES TESTS P8 OK" if ok_all else "ÉCHEC")
    return 0 if ok_all else 1


if __name__ == "__main__":
    sys.exit(main())
