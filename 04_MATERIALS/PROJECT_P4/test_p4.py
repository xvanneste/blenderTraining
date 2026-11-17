"""
test_p4.py — Teste validate_p4.py : la bibliothèque de RÉFÉRENCE doit être ACCEPTÉE ; chaque variante fausse doit être REFUSÉE par le contrôle visé.
Variantes (copies de REFERENCE dans un dossier temporaire) :
  few        : 3 matériaux retirés du statut d'asset (22 assets)              -> « matériaux marqués asset »
  no_desc    : une description vidée                                          -> « description »
  metal_half : Metallic 0,5 sur MAT_Metal_Copper                              -> « Metallic proche de 0 ou 1 »
  orphan     : un nœud Noise sans sortie utilisée                             -> « nœud orphelin »
  image      : un nœud Image Texture ajouté et relié                          -> « aucune image »
  no_cats    : fichier de catalogues supprimé                                 -> « catalogues »
  no_sheet   : planche contact supprimée                                      -> « Planche contact »
  glass_opaque : verre sans transmission                                      -> « Verres transmissifs »
Usage : python 04_MATERIALS/PROJECT_P4/test_p4.py
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
import bpy, sys
kind = sys.argv[sys.argv.index("--") + 1]
M = bpy.data.materials
if kind == "few":
    for n in ("MAT_Wood_Oak", "MAT_Wood_Walnut", "MAT_Wood_Plywood"):
        M[n].asset_clear()
elif kind == "no_desc":
    M["MAT_Stone_Brick"].asset_data.description = ""
elif kind == "metal_half":
    M["MAT_Metal_Copper"].node_tree.nodes["Principled BSDF"].inputs["Metallic"].default_value = 0.5
elif kind == "orphan":
    M["MAT_Plastic_RedGloss"].node_tree.nodes.new("ShaderNodeTexNoise")
elif kind == "image":
    nt = M["MAT_Plastic_WhiteABS"].node_tree
    t = nt.nodes.new("ShaderNodeTexImage"); t.image = bpy.data.images.new("X", 8, 8)
    nt.links.new(t.outputs["Color"], nt.nodes["Principled BSDF"].inputs["Base Color"])
elif kind == "glass_opaque":
    M["MAT_Glass_Clear"].node_tree.nodes["Principled BSDF"].inputs["Transmission Weight"].default_value = 0.0
bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath, copy=False)
'''

CASES = [("few", "matériaux marqués asset"), ("no_desc", "description"), ("metal_half", "Metallic proche"), ("orphan", "nœud orphelin"),
         ("image", "aucune image"), ("no_cats", "catalogue"), ("no_sheet", "Planche contact"), ("glass_opaque", "Verres transmissifs")]


def run_validator(blend):
    p = subprocess.run([BLENDER, "-b", "--factory-startup", blend, "--python", os.path.join(HERE, "validate_p4.py"), "--python-exit-code", "1"],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    fails = [l.strip() for l in p.stdout.splitlines() if "✘" in l]
    return p.returncode, fails


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    ok_all = True
    tmp = tempfile.mkdtemp(prefix="p4_")
    mut = os.path.join(tmp, "mutate.py")
    open(mut, "w", encoding="utf-8").write(MUTATE)
    code, fails = run_validator(os.path.join(REF, "p4_library_reference.blend"))
    ok = code == 0 and not fails
    print(f"[{'PASS' if ok else 'FAIL'}] référence ACCEPTÉE ({'0 échec' if ok else fails})")
    ok_all &= ok
    for kind, target in CASES:
        d = os.path.join(tmp, kind)
        shutil.copytree(REF, d)
        blend = os.path.join(d, "p4_library_reference.blend")
        if kind == "no_cats":
            os.remove(os.path.join(d, "blender_assets.cats.txt"))
        elif kind == "no_sheet":
            shutil.rmtree(os.path.join(d, "renders"))
        else:
            subprocess.run([BLENDER, "-b", "--factory-startup", blend, "--python", mut, "--python-exit-code", "1", "--", kind], capture_output=True)
        code, fails = run_validator(blend)
        hit = [f for f in fails if re.search(target, f)]
        ok = code != 0 and bool(hit)
        print(f"[{'PASS' if ok else 'FAIL'}] {kind} REFUSÉE par « {target} » ({len(fails)} contrôle(s) en échec : {[f[:70] for f in fails]})")
        ok_all &= ok
    shutil.rmtree(tmp, ignore_errors=True)
    print("TOUS LES TESTS P4 OK" if ok_all else "ÉCHEC")
    return 0 if ok_all else 1


if __name__ == "__main__":
    sys.exit(main())
