"""
validate_ch05_06.py — Correcteur « Paramètres et interfaces » (CH05.06).
Usage : … --python-exit-code 1 --python validate_ch05_06.py -- --exercise parameters [--render] [--debug]
GEO_Row / outil GN_PillarRow :
  Interface : entrées Height (Float), Radius (Float), Count (Integer), Spacing (Float) ; Height et Radius dans un panneau « Dimensions », Count et Spacing dans un panneau « Layout » ;
              chaque entrée a une description ; bornes plausibles (Height min ≥ 0,1, max ≤ 20 ; Radius min > 0, max ≤ 2 ; Count min ≥ 1, max ≤ 100 ; Spacing min ≥ 0,1, max ≤ 10) et défaut dans les bornes ;
              aucune entrée inutilisée (chaque sortie de Group Input est reliée).
  Comportement (le correcteur CHANGE les paramètres du modificateur) :
              réglage par défaut : 8 piliers, hauteur 2,0 m, entraxe 1,2 m (étendue 8,4 m) ;
              réglage B (Height 3,5 ; Radius 0,3 ; Count 12 ; Spacing 1,0) : 12 piliers, hauteur 3,5 m, largeur 0,6 m, étendue 11,0 m.
Testé avec : Blender 5.3.0.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bpy  # noqa: E402
import numpy as np  # noqa: E402

EXPECT = {"Height": "NodeSocketFloat", "Radius": "NodeSocketFloat", "Count": "NodeSocketInt", "Spacing": "NodeSocketFloat"}
PANEL = {"Height": "Dimensions", "Radius": "Dimensions", "Count": "Layout", "Spacing": "Layout"}
BOUNDS = {"Height": (0.1, 20.0), "Radius": (1e-3, 2.0), "Count": (1, 100), "Spacing": (0.1, 10.0)}


def measure(ob):
    ob.update_tag()
    bpy.context.view_layer.update()
    dg = bpy.context.evaluated_depsgraph_get()
    xs, tops, widths = [], [], []
    for inst in dg.object_instances:
        if inst.is_instance and inst.parent is not None and inst.parent.original == ob:
            m = inst.matrix_world
            bb = [m @ __import__("mathutils").Vector(v) for v in inst.object.bound_box]
            xs.append(m.translation.x)
            tops.append(max(v.z for v in bb))
            widths.append(max(v.x for v in bb) - min(v.x for v in bb))
    n = len(xs)
    return n, (max(tops) if n else 0.0), (float(np.ptp(xs)) if n else 0.0), (float(np.mean(widths)) if n else 0.0)


def main():
    debug = L.flag("--debug")
    r = L.Report("CH05.06 — Paramètres et interfaces")
    ob = bpy.data.objects.get("GEO_Row")
    md = next((m for m in ob.modifiers if m.type == "NODES"), None) if ob else None
    if not r.check(md is not None and md.node_group is not None, "GEO_Row avec un modificateur Geometry Nodes et un arbre", "Partez du fichier de départ.", 3):
        return r.finish()
    ng = md.node_group
    items = [i for i in ng.interface.items_tree]
    socks = {i.name: i for i in items if i.item_type == "SOCKET" and i.in_out == "INPUT" and i.name != "Geometry"}
    ok_types = all(n in socks and socks[n].socket_type == t for n, t in EXPECT.items())
    r.check(ok_types, f"Entrées Height, Radius (Float), Count (Integer), Spacing (Float) — trouvées : {sorted(socks)}", "Interface de l'arbre : Group > +.", 4)
    ok_pan = all(n in socks and socks[n].parent is not None and socks[n].parent.name == p for n, p in PANEL.items())
    r.check(ok_pan, "Panneaux : Height et Radius dans « Dimensions », Count et Spacing dans « Layout »", "Interface > nouveau panneau, glisser les entrées.", 3)
    r.check(all(n in socks and (socks[n].description or "").strip() for n in EXPECT), "Chaque entrée a une description", "Interface : champ Description de l'entrée.", 3)
    bad = []
    for n, (lo, hi) in BOUNDS.items():
        s = socks.get(n)
        if s is None or not (s.min_value >= lo and s.max_value <= hi and s.min_value <= s.default_value <= s.max_value):
            bad.append(n)
    r.check(not bad, f"Bornes et défauts plausibles ({bad or 'tous OK'})", "Ex. Count 1–50 défaut 8 ; Height 0,2–10 défaut 2.", 3)
    gi = next((n for n in ng.nodes if n.bl_idname == "NodeGroupInput"), None)
    unused = [n for n in EXPECT if n in socks and gi is not None and not gi.outputs[n].is_linked]
    r.check(gi is not None and not unused, f"Chaque entrée est utilisée (inutilisées : {unused or 'aucune'})", "Brancher la sortie de Group Input.", 3)
    # comportement
    nA, topA, extA, wA = measure(ob)
    r.check(nA == 8 and abs(topA - 2.0) <= 0.02 and abs(extA - 8.4) <= 0.05, f"Réglage par défaut : {nA} piliers, hauteur {topA:.2f} m, étendue {extA:.2f} m (8 ; 2,0 ; 8,4)", "Valeurs par défaut de l'interface.", 3)
    try:
        for n, v in (("Height", 3.5), ("Radius", 0.3), ("Count", 12), ("Spacing", 1.0)):
            md.properties.inputs[socks[n].identifier]["value"] = v
        nB, topB, extB, wB = measure(ob)
    except Exception as e:  # noqa: BLE001
        nB, topB, extB, wB = 0, 0.0, 0.0, 0.0
        print("[DEBUG] erreur réglage B :", e)
    r.check(nB == 12, f"Réglage B : Count 12 → {nB} piliers", "Count → Mesh Line [Count].", 3)
    r.check(abs(topB - 3.5) <= 0.02, f"Réglage B : Height 3,5 → hauteur {topB:.2f} m", "Height → Cylinder Depth ET Transform z (÷ 2).", 4)
    r.check(abs(wB - 0.6) <= 0.02, f"Réglage B : Radius 0,3 → largeur {wB:.2f} m", "Radius → Cylinder Radius.", 3)
    r.check(abs(extB - 11.0) <= 0.05, f"Réglage B : Spacing 1,0 → étendue {extB:.2f} m (11,0)", "Spacing → Offset X du Mesh Line.", 3)
    if debug:
        print("[DEBUG] A", nA, round(topA, 3), round(extA, 3), round(wA, 3), "B", nB, round(topB, 3), round(extB, 3), round(wB, 3))
    if L.flag("--render"):
        lum = L.quick_render(15, 4)
        r.check(lum > 0.05, f"Rendu de contrôle non noir ({lum:.3f})", "", 1)
    return r.finish()


if __name__ == "__main__":
    L.run(main)
