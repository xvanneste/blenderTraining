"""
test_p11.py — Teste validate_p11.py : la RÉFÉRENCE doit être ACCEPTÉE ; chaque variante fausse doit être REFUSÉE par le contrôle visé.
Variantes (copies de REFERENCE dans un dossier temporaire) :
  no_catcher   : Floor n'est plus un shadow catcher            -> « Sol lointain »
  no_transparent: film non transparent                          -> « Sol lointain »
  wrong_side   : SUN avec Z +50° (ombre à gauche)               -> « Ombre à droite »
  bright_cube  : nœud Exposure contourné                        -> « Exposition »
  neutral_cube : Gain du Color Balance neutre                   -> « Dominante »
  clean_cube   : 128 échantillons                               -> « Grain »
  no_final     : image finale supprimée                         -> « Image finale »
  lying_qc     : rapport avec ratio 2,0                         -> « Rapport cohérent »
  no_report    : rapport supprimé                               -> « Rapport renders »
  moved_cube   : Cube déplacé de 0,5 m                          -> « Scène inchangée »
Usage : python 11_COMPOSITING_VFX/PROJECT_P11/test_p11.py
Testé avec : Blender 5.3.0.
"""
import json
import math
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
import bpy, sys, math
kind = sys.argv[sys.argv.index("--") + 1]
sc = bpy.context.scene
O = bpy.data.objects
ng = sc.compositing_node_group
if kind == "no_catcher":
    O["Floor"].is_shadow_catcher = False
elif kind == "no_transparent":
    sc.render.film_transparent = False
elif kind == "wrong_side":
    O["SUN"].rotation_euler = (math.radians(50), 0, math.radians(50))
elif kind == "bright_cube":
    rl = next(n for n in ng.nodes if n.bl_idname == "CompositorNodeRLayers")
    cb = next(n for n in ng.nodes if n.bl_idname == "CompositorNodeColorBalance")
    ng.links.new(rl.outputs["Image"], cb.inputs["Image"])
elif kind == "neutral_cube":
    cb = next(n for n in ng.nodes if n.bl_idname == "CompositorNodeColorBalance")
    cb.inputs[8].default_value = (1.0, 1.0, 1.0, 1)
elif kind == "clean_cube":
    sc.cycles.samples = 128
elif kind == "moved_cube":
    O["Cube"].location.x = 0.5
bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath, copy=False)
'''

CASES = [("no_catcher", "Sol lointain"), ("no_transparent", "Sol lointain"), ("wrong_side", "Ombre à droite"), ("bright_cube", "Exposition"), ("neutral_cube", "Dominante"), ("clean_cube", "Grain"),
         ("no_final", "Image finale"), ("lying_qc", "Rapport cohérent"), ("no_report", "Rapport renders"), ("moved_cube", "Scène inchangée")]


def run_validator(blend):
    p = subprocess.run([BLENDER, "-b", "--factory-startup", blend, "--python", os.path.join(HERE, "validate_p11.py"), "--python-exit-code", "1"],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    return p.returncode, [l.strip() for l in p.stdout.splitlines() if "✘" in l]


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    ok_all = True
    tmp = tempfile.mkdtemp(prefix="p11_")
    mut = os.path.join(tmp, "mutate.py")
    open(mut, "w", encoding="utf-8").write(MUTATE)
    code, fails = run_validator(os.path.join(REF, "p11_scene_reference.blend"))
    ok = code == 0 and not fails
    print(f"[{'PASS' if ok else 'FAIL'}] référence ACCEPTÉE ({'0 échec' if ok else fails})")
    ok_all &= ok
    for kind, target in CASES:
        d = os.path.join(tmp, kind)
        shutil.copytree(REF, d)
        blend = os.path.join(d, "p11_scene_reference.blend")
        rep = os.path.join(d, "renders", "p11_qc.json")
        if kind == "no_final":
            os.remove(os.path.join(d, "renders", "p11_final.png"))
        elif kind == "no_report":
            os.remove(rep)
        elif kind == "lying_qc":
            data = json.load(open(rep, encoding="utf-8"))
            data["ratio"] = 2.0
            json.dump(data, open(rep, "w", encoding="utf-8"))
        else:
            subprocess.run([BLENDER, "-b", "--factory-startup", blend, "--python", mut, "--python-exit-code", "1", "--", kind], capture_output=True)
        code, fails = run_validator(blend)
        hit = [f for f in fails if re.search(target, f)]
        ok = code != 0 and bool(hit)
        print(f"[{'PASS' if ok else 'FAIL'}] {kind} REFUSÉE par « {target} » ({len(fails)} contrôle(s) en échec : {[f[:60] for f in fails]})")
        ok_all &= ok
    shutil.rmtree(tmp, ignore_errors=True)
    print("TOUS LES TESTS P11 OK" if ok_all else "ÉCHEC")
    return 0 if ok_all else 1


if __name__ == "__main__":
    sys.exit(main())
