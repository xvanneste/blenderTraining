"""
test_p6.py — Teste validate_p6.py : la RÉFÉRENCE doit être ACCEPTÉE ; chaque variante fausse doit être REFUSÉE par le contrôle visé.
Variantes (copies de REFERENCE dans un dossier temporaire) :
  no_bind         : modificateur Armature retiré du corps                -> « Armature »
  no_action       : Action de test retirée                               -> « Action de test »
  static_action   : toutes les valeurs de l'Action égales à la première  -> « Action de test »
  one_frame       : images clés de l'image 24 supprimées                 -> « Action de test »
  visible_deform  : collection DEF visible                               -> « Ergonomie »
  partial_weights : poids retirés sous z = 0,5 m                         -> « Sommets pesés »
  offset          : corps détaché, rig décalé de 0,5 m en X                            -> « centré sous le corps »
  no_sheet        : planche supprimée                                    -> « Planche »
  dark_sheet      : planche remplacée par une image noire                -> « Planche »
Usage : python 06_RIGGING/PROJECT_P6/test_p6.py
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
body, rig = bpy.data.objects["CHR_Hero_Body"], bpy.data.objects["RIG_Hero"]
def fcs(act):
    try:
        return list(act.fcurves)
    except AttributeError:
        return [f for l in act.layers for s in l.strips for cb in s.channelbags for f in cb.fcurves]
if kind == "no_bind":
    for m in list(body.modifiers):
        body.modifiers.remove(m)
elif kind == "no_action":
    rig.animation_data.action = None
elif kind == "static_action":
    for fc in fcs(rig.animation_data.action):
        y0 = fc.keyframe_points[0].co[1]
        for kp in fc.keyframe_points:
            kp.co[1] = y0
            kp.handle_left[1] = y0
            kp.handle_right[1] = y0
        fc.update()
elif kind == "one_frame":
    for fc in fcs(rig.animation_data.action):
        for kp in list(fc.keyframe_points):
            if round(kp.co[0]) == 24:
                fc.keyframe_points.remove(kp)
elif kind == "visible_deform":
    rig.data.collections_all["DEF"].is_visible = True
elif kind == "partial_weights":
    idx = [v.index for v in body.data.vertices if v.co.z < 0.5]
    for g in body.vertex_groups:
        g.remove(idx)
elif kind == "offset":
    mw = body.matrix_world.copy()
    body.parent = None
    body.matrix_world = mw
    rig.location.x = 0.5
elif kind == "dark_sheet":
    im = bpy.data.images.new("dark", 1920, 900)
    im.pixels = [0.0, 0.0, 0.0, 1.0] * (1920 * 900)
    im.filepath_raw = os.path.join(os.path.dirname(bpy.data.filepath), "renders", "p6_posetest.png")
    im.file_format = "PNG"
    im.save()
bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath, copy=False)
'''

CASES = [("no_bind", "Armature"), ("no_action", "Action de test"), ("static_action", "Action de test"), ("one_frame", "Action de test"), ("visible_deform", "Ergonomie"),
         ("partial_weights", "Sommets pesés"), ("offset", "centré sous le corps"), ("no_sheet", "Planche"), ("dark_sheet", "Planche")]


def run_validator(blend):
    p = subprocess.run([BLENDER, "-b", "--factory-startup", blend, "--python", os.path.join(HERE, "validate_p6.py"), "--python-exit-code", "1"],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    return p.returncode, [l.strip() for l in p.stdout.splitlines() if "✘" in l]


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    ok_all = True
    tmp = tempfile.mkdtemp(prefix="p6_")
    mut = os.path.join(tmp, "mutate.py")
    open(mut, "w", encoding="utf-8").write(MUTATE)
    code, fails = run_validator(os.path.join(REF, "p6_character_reference.blend"))
    ok = code == 0 and not fails
    print(f"[{'PASS' if ok else 'FAIL'}] référence ACCEPTÉE ({'0 échec' if ok else fails})")
    ok_all &= ok
    for kind, target in CASES:
        d = os.path.join(tmp, kind)
        shutil.copytree(REF, d)
        blend = os.path.join(d, "p6_character_reference.blend")
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
    print("TOUS LES TESTS P6 OK" if ok_all else "ÉCHEC")
    return 0 if ok_all else 1


if __name__ == "__main__":
    sys.exit(main())
