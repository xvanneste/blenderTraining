"""
test_p3.py — Teste validate_p3.py : le personnage de RÉFÉRENCE doit être ACCEPTÉ ; chaque variante fausse doit être REFUSÉE par le contrôle visé.
Variantes (copies de REFERENCE dans un dossier temporaire) :
  no_uv      : calque UV supprimé                                  -> « UV présents »
  low_sculpt : HIGH décimé à 20 % (≈ 5 500 faces)                  -> « Sculpt »
  unbaked    : normal map remise à plat                            -> « Bake : relief »
  triangles  : basse définition triangulée (9 362 triangles)       -> « de quads »
  scaled     : échelle 1,1 non appliquée                           -> « Transformations appliquées »
  floating   : personnage décalé de 20 cm en Z                     -> « Pieds au sol »
  srgb       : normal map marquée sRGB                             -> « Non-Color »
  opaque     : peau sans sous-surface                              -> « Peau »
  no_sheet   : planche de rotation supprimée                       -> « Planche »
Usage : python 03_SCULPTING/PROJECT_P3/test_p3.py
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
import bpy, bmesh, sys
kind = sys.argv[sys.argv.index("--") + 1]
hi, lo = bpy.data.objects["HIGH_Hero"], bpy.data.objects["CHR_Hero_Body"]
if kind == "no_uv":
    while lo.data.uv_layers:
        lo.data.uv_layers.remove(lo.data.uv_layers[0])
elif kind == "low_sculpt":
    bm = bmesh.new(); bm.from_mesh(hi.data)
    bmesh.ops.triangulate(bm, faces=bm.faces)
    bm.to_mesh(hi.data); bm.free()
    md = hi.modifiers.new("D", "DECIMATE"); md.ratio = 0.2
    bpy.context.view_layer.objects.active = hi
    bpy.ops.object.modifier_apply(modifier="D")
elif kind == "unbaked":
    import numpy as np
    img = bpy.data.images["T_Hero_N"]
    n = img.size[0] * img.size[1]
    px = np.tile(np.array([0.5, 0.5, 1.0, 1.0], np.float32), n)
    img.pixels = px
    img.pack()
elif kind == "triangles":
    bm = bmesh.new(); bm.from_mesh(lo.data)
    bmesh.ops.triangulate(bm, faces=bm.faces)
    bm.to_mesh(lo.data); bm.free()
elif kind == "scaled":
    lo.scale = (1.1, 1.1, 1.1)
elif kind == "floating":
    lo.location = (0, 0, 0.2)
elif kind == "srgb":
    bpy.data.images["T_Hero_N"].colorspace_settings.name = "sRGB"
elif kind == "opaque":
    bpy.data.materials["MAT_CHR_Hero"].node_tree.nodes["Principled BSDF"].inputs["Subsurface Weight"].default_value = 0.0
bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath, copy=False)
'''

CASES = [("no_uv", "UV présents"), ("low_sculpt", "Sculpt"), ("unbaked", "Bake : relief"), ("triangles", "de quads"), ("scaled", "Transformations appliquées"),
         ("floating", "Pieds au sol"), ("srgb", "Non-Color"), ("opaque", "Peau"), ("no_sheet", "Planche")]


def run_validator(blend):
    p = subprocess.run([BLENDER, "-b", "--factory-startup", blend, "--python-exit-code", "1", "--python", os.path.join(HERE, "validate_p3.py")],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    return p.returncode, [l.strip() for l in p.stdout.splitlines() if "✘" in l]


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    ok_all = True
    tmp = tempfile.mkdtemp(prefix="p3_")
    mut = os.path.join(tmp, "mutate.py")
    open(mut, "w", encoding="utf-8").write(MUTATE)
    code, fails = run_validator(os.path.join(REF, "p3_character_reference.blend"))
    ok = code == 0 and not fails
    print(f"[{'PASS' if ok else 'FAIL'}] référence ACCEPTÉE ({'0 échec' if ok else fails})")
    ok_all &= ok
    for kind, target in CASES:
        d = os.path.join(tmp, kind)
        shutil.copytree(REF, d)
        blend = os.path.join(d, "p3_character_reference.blend")
        if kind == "no_sheet":
            shutil.rmtree(os.path.join(d, "renders"))
        else:
            subprocess.run([BLENDER, "-b", "--factory-startup", blend, "--python-exit-code", "1", "--python", mut, "--", kind], capture_output=True)
        code, fails = run_validator(blend)
        hit = [f for f in fails if re.search(target, f)]
        ok = code != 0 and bool(hit)
        print(f"[{'PASS' if ok else 'FAIL'}] {kind} REFUSÉE par « {target} » ({len(fails)} contrôle(s) en échec : {[f[:60] for f in fails]})")
        ok_all &= ok
    shutil.rmtree(tmp, ignore_errors=True)
    print("TOUS LES TESTS P3 OK" if ok_all else "ÉCHEC")
    return 0 if ok_all else 1


if __name__ == "__main__":
    sys.exit(main())
