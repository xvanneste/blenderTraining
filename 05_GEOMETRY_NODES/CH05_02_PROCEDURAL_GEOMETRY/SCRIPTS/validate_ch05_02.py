"""
validate_ch05_02.py — Correcteur « Géométrie procédurale » (CH05.02).
Usage : … --python-exit-code 1 --python validate_ch05_02.py -- --exercise procedural [--render] [--debug]
GEO_Column / arbre GN_Column — graphe et géométrie ÉVALUÉE :
  Graphe : ≥ 1 Cylinder, ≥ 2 Cube, ≥ 1 Curve to Mesh (avec un Curve Circle en profil), ≥ 3 Transform, un Join Geometry, Set Shade Smooth, Set Material ;
           Group Output alimenté ; aucun nœud orphelin.
  Géométrie évaluée : 4 pièces (composantes connexes) dont un fût de ≥ 2,4 m de haut ; hauteur 2,8–3,6 m ; pieds sur z = 0 (±1 cm) ; emprise X et Y entre 0,8 et 1,0 m ;
           centrée sur l'axe Z (±1 cm) ; maillage fermé (aucune arête non manifold) ; matériau MAT_Column ; ≥ 90 % de faces lisses.
Testé avec : Blender 5.3.0.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bmesh  # noqa: E402
import bpy  # noqa: E402
import numpy as np  # noqa: E402


def count(N, idname):
    return len([n for n in N if n.bl_idname == idname])


def main():
    debug = L.flag("--debug")
    r = L.Report("CH05.02 — Géométrie procédurale")
    ob = bpy.data.objects.get("GEO_Column")
    md = next((m for m in ob.modifiers if m.type == "NODES"), None) if ob else None
    if not r.check(md is not None and md.node_group is not None, "GEO_Column avec un modificateur Geometry Nodes et un arbre", "Partez du fichier de départ.", 3):
        return r.finish()
    N = md.node_group.nodes
    r.check(count(N, "GeometryNodeMeshCylinder") >= 1, "Un nœud Cylinder (fût)", "", 1)
    r.check(count(N, "GeometryNodeMeshCube") >= 2, f"Deux nœuds Cube ou plus ({count(N, 'GeometryNodeMeshCube')}) : base et chapiteau", "", 1)
    cm = [n for n in N if n.bl_idname == "GeometryNodeCurveToMesh"]
    prof = any(n.inputs["Profile Curve"].is_linked and n.inputs["Profile Curve"].links[0].from_node.bl_idname == "GeometryNodeCurvePrimitiveCircle" for n in cm)
    r.check(bool(cm) and prof, "Curve to Mesh avec un Curve Circle en profil (anneau)", "Curve Circle -> Profile Curve.", 3)
    r.check(count(N, "GeometryNodeTransform") >= 3, f"Au moins 3 Transform ({count(N, 'GeometryNodeTransform')})", "Placer chaque pièce.", 2)
    r.check(count(N, "GeometryNodeJoinGeometry") >= 1, "Join Geometry présent", "Rassembler les pièces.", 3)
    r.check(count(N, "GeometryNodeSetShadeSmooth") >= 1 and count(N, "GeometryNodeSetMaterial") >= 1, "Set Shade Smooth et Set Material présents", "", 2)
    out = next((n for n in N if n.bl_idname == "NodeGroupOutput"), None)
    r.check(out is not None and out.inputs[0].is_linked, "Group Output alimenté", "", 3)
    orph = [n.name for n in N if n.bl_idname != "NodeGroupOutput" and n.type != "FRAME" and not any(o.links for o in n.outputs)]
    r.check(not orph, f"Aucun nœud orphelin ({orph or 'aucun'})", "", 2)
    # évalué
    dg = bpy.context.evaluated_depsgraph_get()
    ev = ob.evaluated_get(dg)
    me = ev.to_mesh()
    bm = bmesh.new()
    bm.from_mesh(me)
    mats = [m.name for m in me.materials if m]
    smooth = float(np.mean([p.use_smooth for p in me.polygons])) if len(me.polygons) else 0.0
    ev.to_mesh_clear()
    bm.verts.ensure_lookup_table()
    seen, comps, boxes = set(), 0, []
    for v in bm.verts:
        if v.index in seen:
            continue
        comps += 1
        stack = [v]
        seen.add(v.index)
        pts = []
        while stack:
            x = stack.pop()
            pts.append(x.co[:])
            for e in x.link_edges:
                o = e.other_vert(x)
                if o.index not in seen:
                    seen.add(o.index)
                    stack.append(o)
        a = np.array(pts)
        boxes.append((float(np.ptp(a[:, 0])), float(np.ptp(a[:, 1])), float(np.ptp(a[:, 2]))))
    shaft = [b for b in boxes if 0.55 <= b[0] <= 0.65 and 0.55 <= b[1] <= 0.65 and b[2] > 0.5]
    shaft_h = max((b[2] for b in shaft), default=0.0)
    nonman = sum(1 for e in bm.edges if len(e.link_faces) != 2)
    co = np.array([v.co[:] for v in bm.verts]) if bm.verts else np.zeros((1, 3))
    bm.free()
    zmin, zmax = float(co[:, 2].min()), float(co[:, 2].max())
    ex, ey = float(np.ptp(co[:, 0])), float(np.ptp(co[:, 1]))
    cx, cy = float((co[:, 0].min() + co[:, 0].max()) / 2), float((co[:, 1].min() + co[:, 1].max()) / 2)
    r.check(comps == 4, f"{comps} pièce(s) connexe(s) (4 attendues : fût, base, chapiteau, anneau)", "Join Geometry sur les quatre pièces.", 3)
    r.check(shaft_h >= 2.4, f"Fût de {shaft_h:.2f} m de haut (≥ 2,4 : il relie la base au chapiteau)", "Cylinder : Depth 2,6.", 3)
    r.check(2.8 <= zmax - zmin <= 3.6, f"Hauteur {zmax - zmin:.2f} m (2,8–3,6)", "Fût de 2,6 m + base + chapiteau.", 3)
    r.check(abs(zmin) <= 0.01, f"Pieds sur z = 0 (z min {zmin:+.3f} m)", "Base : translation z = 0,1.", 3)
    r.check(0.8 <= ex <= 1.0 and 0.8 <= ey <= 1.0, f"Emprise {ex:.2f} × {ey:.2f} m (0,8–1,0)", "Base et chapiteau de 0,9 m.", 2)
    r.check(abs(cx) <= 0.01 and abs(cy) <= 0.01, f"Centrée sur l'axe Z ({cx:+.3f}, {cy:+.3f})", "Aucune translation en X ou Y.", 3)
    r.check(nonman == 0, f"Maillage fermé ({nonman} arête(s) non manifold)", "Chaque pièce doit être fermée.", 2)
    r.check("MAT_Column" in mats and smooth >= 0.9, f"Matériau {mats or 'aucun'} ; {100 * smooth:.0f} % de faces lisses", "Set Material et Set Shade Smooth.", 2)
    if debug:
        print("[DEBUG] comps", comps, "h", round(zmax - zmin, 3), "zmin", round(zmin, 3), "ex/ey", round(ex, 3), round(ey, 3), "c", round(cx, 3), round(cy, 3), "nonman", nonman, "smooth", round(smooth, 2))
    if L.flag("--render"):
        lum = L.quick_render(15, 4)
        r.check(lum > 0.05, f"Rendu de contrôle non noir ({lum:.3f})", "", 1)
    return r.finish()


if __name__ == "__main__":
    L.run(main)
