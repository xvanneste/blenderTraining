"""
test_p5.py — Teste validate_p5.py : l'outil de RÉFÉRENCE doit être ACCEPTÉ ; chaque variante fausse doit être REFUSÉE par le contrôle visé.
Variantes (copies de REFERENCE dans un dossier temporaire) :
  no_seed    : Seed débranché des Random Value                -> « Seed + 1 »
  no_density : Density débranchée de la sélection             -> « Density 0,3 → 0,9 »
  no_style   : Style débranché de Instance Index              -> « Style 0 → 2 »
  realized   : Realize Instances ajouté                       -> « Realize »
  unbounded  : Lots avec un maximum de 200                    -> « bornes maximales »
  few_params : entrées Lots et Lot Size supprimées            -> « entrées »
  not_asset  : arbre non marqué comme asset                   -> « marqué comme asset »
  no_cats    : fichier de catalogues supprimé                 -> « Catalogue »
  no_sheet   : planche supprimée                              -> « Planche »
Usage : python 05_GEOMETRY_NODES/PROJECT_P5/test_p5.py
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
ng = bpy.data.node_groups["GN_City"]
def cut(from_name, to_type=None):
    for l in list(ng.links):
        if l.from_node.bl_idname == "NodeGroupInput" and l.from_socket.name == from_name and (to_type is None or l.to_node.bl_idname == to_type or l.to_socket.name == to_type):
            ng.links.remove(l)
if kind == "no_seed":
    cut("Seed")
elif kind == "no_density":
    cut("Density")
elif kind == "no_style":
    cut("Style")
elif kind == "realized":
    io = next(n for n in ng.nodes if n.bl_idname == "GeometryNodeInstanceOnPoints")
    jn = next(n for n in ng.nodes if n.bl_idname == "GeometryNodeJoinGeometry")
    for l in list(ng.links):
        if l.from_node == io and l.to_node == jn:
            ng.links.remove(l)
    rz = ng.nodes.new("GeometryNodeRealizeInstances")
    ng.links.new(io.outputs["Instances"], rz.inputs["Geometry"]); ng.links.new(rz.outputs["Geometry"], jn.inputs["Geometry"])
elif kind == "unbounded":
    next(i for i in ng.interface.items_tree if i.item_type == "SOCKET" and i.name == "Lots").max_value = 200
elif kind == "few_params":
    for n in ("Lots", "Lot Size"):
        ng.interface.remove(next(i for i in ng.interface.items_tree if i.item_type == "SOCKET" and i.name == n))
elif kind == "not_asset":
    ng.asset_clear()
bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath, copy=False)
'''

CASES = [("no_seed", "Seed \\+ 1"), ("no_density", "Density 0,3"), ("no_style", "Style 0"), ("realized", "Realize"), ("unbounded", "bornes maximales"),
         ("few_params", "entrées"), ("not_asset", "marqué comme asset"), ("no_cats", "Catalogue"), ("no_sheet", "Planche")]


def run_validator(blend):
    p = subprocess.run([BLENDER, "-b", "--factory-startup", blend, "--python", os.path.join(HERE, "validate_p5.py"), "--python-exit-code", "1"],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    return p.returncode, [l.strip() for l in p.stdout.splitlines() if "✘" in l]


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    ok_all = True
    tmp = tempfile.mkdtemp(prefix="p5_")
    mut = os.path.join(tmp, "mutate.py")
    open(mut, "w", encoding="utf-8").write(MUTATE)
    code, fails = run_validator(os.path.join(REF, "p5_tool_reference.blend"))
    ok = code == 0 and not fails
    print(f"[{'PASS' if ok else 'FAIL'}] référence ACCEPTÉE ({'0 échec' if ok else fails})")
    ok_all &= ok
    for kind, target in CASES:
        d = os.path.join(tmp, kind)
        shutil.copytree(REF, d)
        blend = os.path.join(d, "p5_tool_reference.blend")
        if kind == "no_cats":
            os.remove(os.path.join(d, "blender_assets.cats.txt"))
        elif kind == "no_sheet":
            shutil.rmtree(os.path.join(d, "renders"))
        else:
            subprocess.run([BLENDER, "-b", "--factory-startup", blend, "--python", mut, "--python-exit-code", "1", "--", kind], capture_output=True)
        code, fails = run_validator(blend)
        hit = [f for f in fails if re.search(target, f)]
        ok = code != 0 and bool(hit)
        print(f"[{'PASS' if ok else 'FAIL'}] {kind} REFUSÉE par « {target} » ({len(fails)} contrôle(s) en échec : {[f[:62] for f in fails]})")
        ok_all &= ok
    shutil.rmtree(tmp, ignore_errors=True)
    print("TOUS LES TESTS P5 OK" if ok_all else "ÉCHEC")
    return 0 if ok_all else 1


if __name__ == "__main__":
    sys.exit(main())
