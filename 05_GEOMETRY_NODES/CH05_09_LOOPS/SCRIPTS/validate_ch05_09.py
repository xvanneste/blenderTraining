"""
validate_ch05_09.py — Correcteur « Boucles et simulation » (CH05.09, zone de répétition).
Usage : … --python-exit-code 1 --python validate_ch05_09.py -- --exercise loops [--render] [--debug]
GEO_Spiral / outil GN_Spiral :
  Graphe : une zone de répétition (Repeat Input + Repeat Output appariés) ; Iterations alimenté par Steps.
  Interface : Steps (Integer), Angle, Rise, Radius (Float) avec descriptions et bornes cohérentes.
  Mesures sur la géométrie évaluée, DEUX réglages : A (Steps 16 ; Angle 22,5° ; Rise 0,18 ; Radius 1,2) et B (30 ; 15° ; 0,12 ; 2,0) :
    nombre de marches (composantes connexes) = Steps ; centres espacés en hauteur de Rise (± 5 mm) ; première marche à z = 0,05 ;
    écart angulaire entre marches consécutives = Angle (± 0,5°) ; rayon des centres = Radius (± 1 cm).
Testé avec : Blender 5.3.0.
"""
import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bmesh  # noqa: E402
import bpy  # noqa: E402
import numpy as np  # noqa: E402

EXPECT = {"Steps": "NodeSocketInt", "Angle": "NodeSocketFloat", "Rise": "NodeSocketFloat", "Radius": "NodeSocketFloat"}
BOUNDS = {"Steps": (1, 200), "Angle": (1.0, 90.0), "Rise": (0.02, 1.0), "Radius": (0.2, 10.0)}
A = {"Steps": 16, "Angle": 22.5, "Rise": 0.18, "Radius": 1.2}
B = {"Steps": 30, "Angle": 15.0, "Rise": 0.12, "Radius": 2.0}


def steps(ob):
    ob.update_tag()
    bpy.context.view_layer.update()
    ev = ob.evaluated_get(bpy.context.evaluated_depsgraph_get())
    me = ev.to_mesh()
    bm = bmesh.new()
    bm.from_mesh(me)
    ev.to_mesh_clear()
    bm.verts.ensure_lookup_table()
    seen, cents = set(), []
    for v in bm.verts:
        if v.index in seen:
            continue
        stack, pts = [v], []
        seen.add(v.index)
        while stack:
            x = stack.pop()
            pts.append(x.co[:])
            for e in x.link_edges:
                o = e.other_vert(x)
                if o.index not in seen:
                    seen.add(o.index)
                    stack.append(o)
        cents.append(np.mean(np.array(pts), axis=0))
    bm.free()
    return sorted(cents, key=lambda c: c[2])


def check(r, tag, par, cents):
    n = len(cents)
    r.check(n == par["Steps"], f"{tag} : {n} marches (Steps = {par['Steps']})", "Iterations ← Steps ; Join Geometry accumule les marches.", 4)
    if n < 2:
        for k in range(3):
            r.check(False, f"{tag} : mesure impossible", "", 2)
        return
    C = np.array(cents)
    dz = np.diff(C[:, 2])
    r.check(abs(C[0, 2] - 0.05) <= 0.005 and np.abs(dz - par["Rise"]).max() <= 0.005, f"{tag} : première marche à z = {C[0, 2]:.3f} (0,05), contremarche {float(dz.mean()):.3f} m (attendu {par['Rise']})", "Translation z = 0,05 + Iteration × Rise.", 3)
    ang = np.unwrap(np.arctan2(C[:, 1], C[:, 0]))
    da = np.degrees(np.diff(ang))
    r.check(np.abs(da - par["Angle"]).max() <= 0.5, f"{tag} : écart angulaire {float(da.mean()):.2f}° (attendu {par['Angle']}°)", "Rotation z = Iteration × radians(Angle).", 3)
    rad = np.hypot(C[:, 0], C[:, 1])
    r.check(np.abs(rad - par["Radius"]).max() <= 0.01, f"{tag} : rayon {float(rad.mean()):.2f} m (attendu {par['Radius']})", "Translation x = Radius AVANT la rotation.", 3)


def main():
    debug = L.flag("--debug")
    r = L.Report("CH05.09 — Boucles (zone de répétition)")
    ob = bpy.data.objects.get("GEO_Spiral")
    md = next((m for m in ob.modifiers if m.type == "NODES"), None) if ob else None
    if not r.check(md is not None and md.node_group is not None, "GEO_Spiral avec un modificateur Geometry Nodes et un arbre", "Partez du fichier de départ.", 3):
        return r.finish()
    ng = md.node_group
    ris = [n for n in ng.nodes if n.bl_idname == "GeometryNodeRepeatInput"]
    ros = [n for n in ng.nodes if n.bl_idname == "GeometryNodeRepeatOutput"]
    paired = bool(ris) and bool(ros) and ris[0].paired_output == ros[0]
    r.check(paired, "Zone de répétition : Repeat Input et Repeat Output appariés", "Add > Utilities > Repeat Zone.", 4)
    socks = {i.name: i for i in ng.interface.items_tree if i.item_type == "SOCKET" and i.in_out == "INPUT" and i.name != "Geometry"}
    ok_t = all(n in socks and socks[n].socket_type == t for n, t in EXPECT.items())
    r.check(ok_t, f"Interface : Steps (Integer), Angle, Rise, Radius (Float) — trouvées : {sorted(socks)}", "Créer les quatre entrées.", 4)
    if not (paired and ok_t):
        return r.finish()
    r.check(ris[0].inputs["Iterations"].is_linked, "Iterations alimenté (Steps)", "Group Input [Steps] → Iterations.", 3)
    r.check(all((socks[n].description or "").strip() for n in EXPECT), "Chaque entrée a une description", "", 1)
    bad = [n for n, (lo, hi) in BOUNDS.items() if not (socks[n].min_value >= lo and socks[n].max_value <= hi and socks[n].min_value <= socks[n].default_value <= socks[n].max_value)]
    r.check(not bad, f"Bornes et défauts plausibles ({bad or 'tous OK'})", "", 2)
    for tag, par in (("Réglage A", A), ("Réglage B", B)):
        for n, v in par.items():
            md.properties.inputs[socks[n].identifier]["value"] = v
        c = steps(ob)
        check(r, tag, par, c)
    for n, v in A.items():
        md.properties.inputs[socks[n].identifier]["value"] = v
    if debug:
        print("[DEBUG] ok")
    if L.flag("--render"):
        lum = L.quick_render(15, 4)
        r.check(lum > 0.05, f"Rendu de contrôle non noir ({lum:.3f})", "", 1)
    return r.finish()


if __name__ == "__main__":
    L.run(main)
