"""
test_p10.py — Teste validate_p10.py : la RÉFÉRENCE doit être ACCEPTÉE ; chaque variante fausse doit être REFUSÉE par le contrôle visé.
Variantes (copies de REFERENCE dans un dossier temporaire) :
  heavy_meshes : 200 maillages différents (niveau 0)                 -> « Géométrie »
  high_tris    : un maillage partagé, Subdivision Surface niveau 2   -> « Géométrie »
  big_texture  : Simplify désactivé (texture 4 096 sans limite)      -> « Textures »
  noisy        : 4 échantillons, sans débruitage ni adaptatif        -> « Cycles »
  no_exr       : EXR supprimé                                        -> « EXR »
  half_exr     : EXR réécrit en 16 bits                              -> « EXR »
  no_crypto    : EXR réécrit sans passe Cryptomatte                  -> « EXR »
  lying_report : triangles du rapport faux (100)                     -> « Rapport cohérent »
  no_report    : rapport supprimé                                    -> « Rapport renders »
  few_props    : 100 accessoires supprimés                           -> « Accessoires »
Usage : python 10_RENDERING/PROJECT_P10/test_p10.py
Testé avec : Blender 5.3.0.
"""
import json
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
import bpy, sys, os, json, bmesh
kind = sys.argv[sys.argv.index("--") + 1]
sc = bpy.context.scene
here = os.path.dirname(bpy.data.filepath)
def unique_meshes(level):
    mat = bpy.data.materials["MA_Rock"]
    for o in [o for o in bpy.data.objects if o.name.startswith("Prop_") and o.name != "Prop_src"]:
        loc = o.location.copy()
        bpy.data.objects.remove(o)
        bm = bmesh.new(); bmesh.ops.create_icosphere(bm, subdivisions=2, radius=0.4)
        me = bpy.data.meshes.new("ME_u"); bm.to_mesh(me); bm.free(); me.materials.append(mat)
        e = bpy.data.objects.new(o.name if False else "Prop_x", me); e.location = loc
        md = e.modifiers.new("S", "SUBSURF"); md.levels = md.render_levels = level
        sc.collection.objects.link(e)
def rerender_exr(depth="32", crypto=True):
    ims = sc.render.image_settings
    if not crypto:
        sc.view_layers[0].use_pass_cryptomatte_object = False
    ims.media_type = "MULTI_LAYER_IMAGE"
    ims.color_depth, ims.exr_codec = depth, "ZIP"
    sc.render.filepath = os.path.join(here, "renders", "p10_master.exr")
    bpy.ops.render.render(write_still=True)
if kind == "heavy_meshes":
    unique_meshes(0)
elif kind == "high_tris":
    shared = bpy.data.meshes["ME_Rock"]
    for o in [o for o in bpy.data.objects if o.name.startswith("Prop_") and o.name != "Prop_src"]:
        loc = o.location.copy(); nm = o.name
        bpy.data.objects.remove(o)
        e = bpy.data.objects.new(nm, shared); e.location = loc
        md = e.modifiers.new("S", "SUBSURF"); md.levels = md.render_levels = 2
        sc.collection.objects.link(e)
elif kind == "big_texture":
    sc.render.use_simplify = False
elif kind == "noisy":
    sc.cycles.samples = 4; sc.cycles.use_denoising = False; sc.cycles.use_adaptive_sampling = False
elif kind == "half_exr":
    rerender_exr("16")
elif kind == "no_crypto":
    rerender_exr("32", crypto=False)
elif kind == "few_props":
    for o in [o for o in bpy.data.objects if o.name.startswith("Prop_") and o.name != "Prop_src"][100:]:
        bpy.data.objects.remove(o)
bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath, copy=False)
'''

CASES = [("heavy_meshes", "Géométrie"), ("high_tris", "Géométrie"), ("big_texture", "Textures"), ("noisy", "Cycles"), ("no_exr", "EXR"), ("half_exr", "EXR"), ("no_crypto", "EXR"),
         ("lying_report", "Rapport cohérent"), ("no_report", "Rapport renders"), ("few_props", "Accessoires")]


def run_validator(blend):
    p = subprocess.run([BLENDER, "-b", "--factory-startup", blend, "--python", os.path.join(HERE, "validate_p10.py"), "--python-exit-code", "1"],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    return p.returncode, [l.strip() for l in p.stdout.splitlines() if "✘" in l]


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    ok_all = True
    tmp = tempfile.mkdtemp(prefix="p10_")
    mut = os.path.join(tmp, "mutate.py")
    open(mut, "w", encoding="utf-8").write(MUTATE)
    code, fails = run_validator(os.path.join(REF, "p10_scene_reference.blend"))
    ok = code == 0 and not fails
    print(f"[{'PASS' if ok else 'FAIL'}] référence ACCEPTÉE ({'0 échec' if ok else fails})")
    ok_all &= ok
    for kind, target in CASES:
        d = os.path.join(tmp, kind)
        shutil.copytree(REF, d)
        blend = os.path.join(d, "p10_scene_reference.blend")
        rep = os.path.join(d, "renders", "p10_report.json")
        if kind == "no_exr":
            os.remove(os.path.join(d, "renders", "p10_master.exr"))
        elif kind == "no_report":
            os.remove(rep)
        elif kind == "lying_report":
            data = json.load(open(rep, encoding="utf-8"))
            data["after"]["triangles"] = 100
            json.dump(data, open(rep, "w", encoding="utf-8"))
        else:
            subprocess.run([BLENDER, "-b", "--factory-startup", blend, "--python", mut, "--python-exit-code", "1", "--", kind], capture_output=True)
        code, fails = run_validator(blend)
        hit = [f for f in fails if re.search(target, f)]
        ok = code != 0 and bool(hit)
        print(f"[{'PASS' if ok else 'FAIL'}] {kind} REFUSÉE par « {target} » ({len(fails)} contrôle(s) en échec : {[f[:62] for f in fails]})")
        ok_all &= ok
    shutil.rmtree(tmp, ignore_errors=True)
    print("TOUS LES TESTS P10 OK" if ok_all else "ÉCHEC")
    return 0 if ok_all else 1


if __name__ == "__main__":
    sys.exit(main())
