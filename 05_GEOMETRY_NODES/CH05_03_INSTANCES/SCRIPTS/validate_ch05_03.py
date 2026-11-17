"""
validate_ch05_03.py — Correcteur « Instances » (CH05.03).
Usage : … --python-exit-code 1 --python validate_ch05_03.py -- --exercise instances [--render] [--debug]
GEO_Posts / arbre GN_Posts — graphe et INSTANCES évaluées (depsgraph.object_instances) :
  Graphe : Instance on Points (Points et Instance reliés) ; Rotation ET Scale alimentés par des Random Value ; Set Material ; PAS de Realize Instances ;
           Group Output alimenté ; aucun nœud orphelin.
  Évalué : 100 à 1 600 instances ; emprise X et Y de 7 à 8,5 m ; échelle uniforme dans [0,4 ; 1,8] avec écart-type/moyenne ≥ 0,1 ;
           orientations réparties (longueur du vecteur moyen des angles ≤ 0,3) ; base des piquets à z = 0 (±2 cm) ; matériau MAT_Post.
Testé avec : Blender 5.3.0.
"""
import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bpy  # noqa: E402
import numpy as np  # noqa: E402


def upstream_nodes(sock, seen=None):
    seen = set() if seen is None else seen
    out = []
    for l in sock.links:
        n = l.from_node
        if n.name not in seen:
            seen.add(n.name)
            out.append(n)
            for i in n.inputs:
                out += upstream_nodes(i, seen)
    return out


def main():
    debug = L.flag("--debug")
    r = L.Report("CH05.03 — Instances")
    ob = bpy.data.objects.get("GEO_Posts")
    md = next((m for m in ob.modifiers if m.type == "NODES"), None) if ob else None
    if not r.check(md is not None and md.node_group is not None, "GEO_Posts avec un modificateur Geometry Nodes et un arbre", "Partez du fichier de départ.", 3):
        return r.finish()
    N = md.node_group.nodes
    io = next((n for n in N if n.bl_idname == "GeometryNodeInstanceOnPoints"), None)
    r.check(io is not None and io.inputs["Points"].is_linked and io.inputs["Instance"].is_linked, "Instance on Points avec Points et Instance reliés", "Grid → Points ; piquet → Instance.", 4)
    rot_ok = io is not None and any(n.bl_idname == "FunctionNodeRandomValue" for n in upstream_nodes(io.inputs["Rotation"]))
    sc_ok = io is not None and any(n.bl_idname == "FunctionNodeRandomValue" for n in upstream_nodes(io.inputs["Scale"]))
    r.check(rot_ok, "Rotation alimentée par un Random Value", "Random Value (Vector, Max z = 6,283) → Rotation.", 3)
    r.check(sc_ok, "Scale alimenté par un Random Value", "Random Value (Float 0,6–1,4) → Scale.", 3)
    r.check(any(n.bl_idname == "GeometryNodeSetMaterial" for n in N), "Set Material présent", "", 1)
    r.check(not any(n.bl_idname == "GeometryNodeRealizeInstances" for n in N), "Pas de Realize Instances (on garde des instances)", "Realize Instances multiplie la géométrie : à éviter ici.", 3)
    out = next((n for n in N if n.bl_idname == "NodeGroupOutput"), None)
    r.check(out is not None and out.inputs[0].is_linked, "Group Output alimenté", "", 2)
    orph = [n.name for n in N if n.bl_idname != "NodeGroupOutput" and n.type != "FRAME" and not any(o.links for o in n.outputs)]
    r.check(not orph, f"Aucun nœud orphelin ({orph or 'aucun'})", "", 2)
    # Instances évaluées
    bpy.context.view_layer.update()
    dg = bpy.context.evaluated_depsgraph_get()
    pos, scl, yaw, zmins, mats = [], [], [], [], set()
    for inst in dg.object_instances:
        if inst.is_instance and inst.parent is not None and inst.parent.original == ob:
            m = inst.matrix_world
            s = m.to_scale()
            pos.append(tuple(m.translation))
            scl.append((s.x + s.y + s.z) / 3)
            yaw.append(m.to_euler().z)
            lz = min(v[2] for v in inst.object.bound_box)
            zmins.append(m.translation.z + lz * s.z)
            for mt in inst.object.data.materials:
                if mt:
                    mats.add(mt.name)
    n = len(pos)
    r.check(100 <= n <= 1600, f"{n} instances (100–1 600)", "Grid 21 × 21 = 441 points.", 4)
    if n:
        P = np.array(pos)
        ex, ey = float(np.ptp(P[:, 0])), float(np.ptp(P[:, 1]))
        S_ = np.array(scl)
        cv = float(S_.std() / S_.mean())
        resultant = float(abs(np.mean(np.exp(1j * np.array(yaw)))))
        zm = float(np.max(np.abs(zmins)))
    else:
        ex = ey = cv = zm = 0.0
        resultant = 1.0
        S_ = np.array([1.0])
    r.check(7.0 <= ex <= 8.5 and 7.0 <= ey <= 8.5, f"Emprise {ex:.1f} × {ey:.1f} m (7–8,5)", "Grid Size 8 × 8.", 2)
    r.check(0.4 <= float(S_.min()) and float(S_.max()) <= 1.8 and cv >= 0.1, f"Échelles {float(S_.min()):.2f}–{float(S_.max()):.2f}, variation relative {cv:.2f} (≥ 0,1)", "Scale aléatoire 0,6–1,4.", 3)
    r.check(resultant <= 0.3, f"Orientations réparties (vecteur moyen {resultant:.2f} ≤ 0,3)", "Rotation aléatoire autour de Z.", 3)
    r.check(n > 0 and zm <= 0.02, f"Bases des piquets sur z = 0 (écart max {zm:.3f} m)", "Transform z = 0,5 avant d'instancier.", 3)
    r.check("MAT_Post" in mats, f"Matériau des instances : {sorted(mats) or 'aucun'}", "Set Material sur le piquet.", 2)
    if debug:
        print("[DEBUG] n", n, "emprise", round(ex, 2), round(ey, 2), "scale", round(float(S_.min()), 2), round(float(S_.max()), 2), "cv", round(cv, 3), "R", round(resultant, 3), "zmax", round(zm, 4), mats)
    if L.flag("--render"):
        lum = L.quick_render(15, 4)
        r.check(lum > 0.05, f"Rendu de contrôle non noir ({lum:.3f})", "", 1)
    return r.finish()


if __name__ == "__main__":
    L.run(main)
