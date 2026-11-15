"""
test_p2.py — Teste validate_p2.py : un fichier vide doit être REFUSÉ, une scène d'exemple ACCEPTÉE.
La scène d'exemple (non livrée comme solution : le projet est personnel) lie 6 props de la
bibliothèque de CH02.13 et ajoute une pièce, 4 props locaux, caméra, lumières et rendu.
Usage : python 02_MODELING/PROJECT_P2/test_p2.py  (écrit dans un dossier temporaire)
Testé avec : Blender 5.3.0.
"""
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
BLENDER = r"C:\Program Files\Blender Foundation\Blender 5.3\blender.exe"
LIB = os.path.join(HERE, "..", "CH02_13_ASSETS", "COMPLETED_EXAMPLES", "ch02_13_library_solution.blend")

MAKE = r'''
import bpy, bmesh, math, os, sys
sys.path.insert(0, r"%(scripts)s")
import bcma_lib as L
L.reset("SC_Atelier")
setc, props, lights, cams = (L.collection(n) for n in ("SET", "PROPS", "LIGHTS", "CAMERAS"))
floor = L.plane("GEO_Floor", setc, None, size=6)
w1 = L.cube("GEO_Wall_Back", setc, None, size=1, location=(0, 3, 1.4), scale=(6, 0.2, 2.8))
w2 = L.cube("GEO_Wall_Left", setc, None, size=1, location=(-3, 0, 1.4), scale=(0.2, 6, 2.8))
for o in (w1, w2):
    bpy.context.view_layer.objects.active = o; o.select_set(True)
    bpy.ops.object.transform_apply(scale=True)
    o.select_set(False)
cut = L.cube("GEO_Cut_Window", setc, None, size=1, location=(0, 3, 1.5), scale=(1.2, 0.6, 1.0))
cut.display_type = "WIRE"; cut.hide_render = True
bpy.context.view_layer.objects.active = cut; cut.select_set(True); bpy.ops.object.transform_apply(scale=True); cut.select_set(False)
b = w1.modifiers.new("Window", "BOOLEAN"); b.object = cut
with bpy.data.libraries.load(r"%(lib)s", link=True) as (src, dst):
    dst.objects = [n for n in src.objects if n.startswith("GEO_")]
for i, ob in enumerate(dst.objects):
    inst = ob
    props.objects.link(inst)
x = -2.0
for name in ("GEO_Box_A", "GEO_Box_B"):
    o = L.cube(name, props, None, size=0.4, location=(x, -1, 0.2)); x += 0.8
    o.modifiers.new("Bevel", "BEVEL")
s = L.sphere("GEO_Ball", props, None, radius=0.2, location=(1.5, -1, 0.2))
s.modifiers.new("Subdivision", "SUBSURF")
L.cylinder("GEO_Pot", props, None, radius=0.15, depth=0.3, location=(2.2, -1, 0.15))
for o in [o for o in bpy.context.scene.objects if o.type == "MESH" and o.library is None]:
    bpy.context.view_layer.objects.active = o
    for x in bpy.context.selected_objects: x.select_set(False)
    o.select_set(True)
    bpy.ops.object.mode_set(mode="EDIT"); bpy.ops.mesh.select_all(action="SELECT")
    bpy.ops.uv.smart_project(); bpy.ops.object.mode_set(mode="OBJECT")
L.light("LGT_Key", lights, "AREA", (2, -3, 3), 600)
L.light("LGT_Fill", lights, "AREA", (-2, -3, 2), 200)
cam = L.camera("CAM_Main", cams, (0, -5.5, 1.6), 35)
cam.rotation_euler = (math.radians(85), 0, 0)
L.render_defaults("BLENDER_EEVEE", 10)
p = r"%(out)s"
L.save(p)
os.makedirs(os.path.join(os.path.dirname(p), "renders"), exist_ok=True)
bpy.context.scene.render.filepath = os.path.join(os.path.dirname(p), "renders", "p2_atelier.png")
bpy.ops.render.render(write_still=True)
'''


def run(args):
    return subprocess.run([BLENDER, "-b", "--factory-startup"] + args, capture_output=True, text=True, encoding="utf-8", errors="replace")


def main():
    tmp = tempfile.mkdtemp(prefix="bcma_p2_")
    ok = True
    empty = os.path.join(tmp, "empty.blend")
    run(["--python-expr", f"import bpy; bpy.ops.wm.save_as_mainfile(filepath=r'{empty}')"])
    r = run([empty, "--python", os.path.join(HERE, "validate_p2.py"), "--python-exit-code", "1"])
    print("[test] fichier vide :", "REFUSÉ (attendu)" if r.returncode != 0 else "ACCEPTÉ (ERREUR)")
    ok &= r.returncode != 0
    script = os.path.join(tmp, "make.py")
    out = os.path.join(tmp, "p2_atelier_test_v001.blend")
    open(script, "w", encoding="utf-8").write(MAKE % {"scripts": os.path.join(HERE, "..", "..", "SCRIPTS"),
                                                       "lib": os.path.abspath(LIB), "out": out})
    m = run(["--python", script, "--python-exit-code", "1"])
    if m.returncode != 0:
        print(m.stdout[-2000:], m.stderr[-2000:])
    r = run([out, "--python", os.path.join(HERE, "validate_p2.py"), "--python-exit-code", "1"])
    print("[test] scène d'exemple :", "ACCEPTÉE (attendu)" if r.returncode == 0 else "REFUSÉE (ERREUR)")
    if r.returncode != 0:
        print("\n".join(l for l in r.stdout.splitlines() if "✘" in l or "piste" in l))
    ok &= r.returncode == 0
    print("[test] P2 :", "OK" if ok else "ÉCHEC")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
