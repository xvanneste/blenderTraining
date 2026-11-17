"""
validate_ch05_01.py — Correcteur « Geometry Nodes : principes » (CH05.01).
Usage : … --python-exit-code 1 --python validate_ch05_01.py -- --exercise principles [--render] [--debug]
GEO_Terrain / modificateur Geometry Nodes (arbre GN_Terrain) — contrôle du GRAPHE et de la géométrie ÉVALUÉE :
  Graphe : un nœud Grid (≥ 50 × 50 sommets) ; un Set Position dont Offset est alimenté par un CHAMP (Noise Texture en amont) ; Set Shade Smooth ; Set Material ;
           Group Output [Geometry] alimenté ; aucun nœud orphelin ; 5 à 15 nœuds.
  Géométrie évaluée : 2 500 à 20 000 sommets ; emprise X, Y de 9,5 à 10,5 m ; écart-type de Z ≥ 0,05 m ; étendue de Z entre 0,2 et 2,5 m ;
           ≥ 90 % de faces lisses ; matériau MAT_Terrain présent.
Testé avec : Blender 5.3.0.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bpy  # noqa: E402
import numpy as np  # noqa: E402


def upstream_types(sock, seen=None):
    seen = set() if seen is None else seen
    out = set()
    for l in sock.links:
        n = l.from_node
        if n.name not in seen:
            seen.add(n.name)
            out.add(n.type)
            for i in n.inputs:
                out |= upstream_types(i, seen)
    return out


def main():
    debug = L.flag("--debug")
    r = L.Report("CH05.01 — Principes de Geometry Nodes")
    ob = bpy.data.objects.get("GEO_Terrain")
    md = next((m for m in ob.modifiers if m.type == "NODES"), None) if ob else None
    if not r.check(md is not None and md.node_group is not None, "GEO_Terrain avec un modificateur Geometry Nodes et un arbre", "Partez du fichier de départ.", 3):
        return r.finish()
    ng = md.node_group
    N = ng.nodes
    grid = next((n for n in N if n.bl_idname == "GeometryNodeMeshGrid"), None)
    r.check(grid is not None and grid.inputs["Vertices X"].default_value >= 50 and grid.inputs["Vertices Y"].default_value >= 50,
            f"Grid ≥ 50 × 50 sommets ({'absente' if grid is None else (grid.inputs['Vertices X'].default_value, grid.inputs['Vertices Y'].default_value)})", "Grid : Vertices X et Y = 100.", 3)
    sp = next((n for n in N if n.bl_idname == "GeometryNodeSetPosition"), None)
    field = sp is not None and sp.inputs["Offset"].is_linked and "TEX_NOISE" in upstream_types(sp.inputs["Offset"])
    r.check(field, "Set Position : Offset alimenté par un champ (Noise Texture en amont)", "Noise [Fac] -> Math -> Combine XYZ -> Offset.", 4)
    r.check(any(n.bl_idname == "GeometryNodeSetShadeSmooth" for n in N), "Set Shade Smooth présent", "Après le déplacement.", 2)
    r.check(any(n.bl_idname == "GeometryNodeSetMaterial" for n in N), "Set Material présent", "La géométrie générée n'hérite pas des matériaux du maillage d'origine.", 2)
    out = next((n for n in N if n.bl_idname == "NodeGroupOutput"), None)
    r.check(out is not None and out.inputs[0].is_linked, "Group Output [Geometry] alimenté", "Relier la dernière sortie de géométrie.", 3)
    orph = [n.name for n in N if n.bl_idname != "NodeGroupOutput" and n.type != "FRAME" and not any(o.links for o in n.outputs)]
    r.check(not orph, f"Aucun nœud orphelin ({orph or 'aucun'})", "Supprimez ou reliez.", 2)
    nn = len([n for n in N if n.type != "FRAME"])
    r.check(5 <= nn <= 15, f"{nn} nœuds (5–15)", "", 1)
    # Géométrie évaluée
    dg = bpy.context.evaluated_depsgraph_get()
    ev = ob.evaluated_get(dg)
    me = ev.to_mesh()
    nv = len(me.vertices)
    co = np.empty(nv * 3, np.float32)
    me.vertices.foreach_get("co", co)
    co = co.reshape(-1, 3)
    smooth = np.array([p.use_smooth for p in me.polygons]) if len(me.polygons) else np.array([False])
    mats = [m.name for m in me.materials if m]
    ev.to_mesh_clear()
    r.check(2500 <= nv <= 20000, f"Géométrie évaluée : {nv} sommets (2 500–20 000)", "Grid 100 × 100 = 10 000 sommets.", 3)
    if nv:
        ex, ey = np.ptp(co[:, 0]), np.ptp(co[:, 1])
        zs, ze = float(co[:, 2].std()), float(np.ptp(co[:, 2]))
    else:
        ex = ey = zs = ze = 0.0
    r.check(9.5 <= ex <= 10.5 and 9.5 <= ey <= 10.5, f"Emprise {ex:.1f} × {ey:.1f} m (9,5–10,5)", "Grid Size 10 × 10.", 2)
    r.check(zs >= 0.05, f"Relief : écart-type de Z {zs:.3f} m (≥ 0,05)", "Le champ doit varier d'un point à l'autre.", 3)
    r.check(0.2 <= ze <= 2.5, f"Étendue de Z {ze:.2f} m (0,2–2,5)", "Amplitude 2 : ± 0,6 m environ.", 2)
    r.check(float(smooth.mean()) >= 0.9, f"{100 * float(smooth.mean()):.0f} % de faces lisses (≥ 90)", "Set Shade Smooth.", 2)
    r.check("MAT_Terrain" in mats, f"Matériau MAT_Terrain dans la géométrie évaluée ({mats or 'aucun'})", "Set Material.", 2)
    if debug:
        print("[DEBUG] nv", nv, "emprise", round(float(ex), 2), round(float(ey), 2), "z std", round(zs, 3), "z ptp", round(ze, 3), "smooth", round(float(smooth.mean()), 2), "mats", mats)
    if L.flag("--render"):
        lum = L.quick_render(15, 4)
        r.check(lum > 0.05, f"Rendu de contrôle non noir ({lum:.3f})", "", 1)
    return r.finish()


if __name__ == "__main__":
    L.run(main)
