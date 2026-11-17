"""
validate_ch05_04.py — Correcteur « Distribution » (CH05.04).
Usage : … --python-exit-code 1 --python validate_ch05_04.py -- --exercise distribution [--render] [--debug]
GEO_Field / arbre GN_Field — graphe et instances évaluées :
  Graphe : Distribute Points on Faces en méthode POISSON, Mesh relié, Density Factor alimenté (champ : masque) ; Instance on Points relié aux points distribués ;
           Group Output alimenté ; aucun nœud orphelin.
  Évalué : 40 à 400 instances ; ≥ 95 % avec x > 0 (masque) ; distance minimale entre instances ≥ 0,45 m (Poisson, Distance Min 0,5) ;
           toutes dans le sol (|x|, |y| ≤ 5,05 m) ; matériau MAT_Tree sur les instances.
Testé avec : Blender 5.3.0.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bpy  # noqa: E402
import numpy as np  # noqa: E402
from mathutils.kdtree import KDTree  # noqa: E402


def main():
    debug = L.flag("--debug")
    r = L.Report("CH05.04 — Distribution")
    ob = bpy.data.objects.get("GEO_Field")
    md = next((m for m in ob.modifiers if m.type == "NODES"), None) if ob else None
    if not r.check(md is not None and md.node_group is not None, "GEO_Field avec un modificateur Geometry Nodes et un arbre", "Partez du fichier de départ.", 3):
        return r.finish()
    N = md.node_group.nodes
    ds = next((n for n in N if n.bl_idname == "GeometryNodeDistributePointsOnFaces"), None)
    r.check(ds is not None and ds.inputs["Mesh"].is_linked, "Distribute Points on Faces avec Mesh relié", "Grid → Mesh.", 3)
    r.check(ds is not None and ds.distribute_method == "POISSON", f"Méthode : {ds.distribute_method if ds else 'absent'} (POISSON exigé)", "Poisson Disk impose une distance minimale entre points.", 3)
    r.check(ds is not None and "Density Factor" in ds.inputs and ds.inputs["Density Factor"].is_linked, "Density Factor alimenté par un champ (masque)", "Position → Separate XYZ → Math → Density Factor.", 4)
    io = next((n for n in N if n.bl_idname == "GeometryNodeInstanceOnPoints"), None)
    ok_io = io is not None and io.inputs["Points"].is_linked and io.inputs["Points"].links[0].from_node == ds and io.inputs["Instance"].is_linked
    r.check(ok_io, "Instance on Points : Points ← Distribute, Instance relié", "Distribute [Points] → Points.", 3)
    out = next((n for n in N if n.bl_idname == "NodeGroupOutput"), None)
    r.check(out is not None and out.inputs[0].is_linked, "Group Output alimenté", "", 2)
    orph = [n.name for n in N if n.bl_idname != "NodeGroupOutput" and n.type != "FRAME" and not any(o.links for o in n.outputs)]
    r.check(not orph, f"Aucun nœud orphelin ({orph or 'aucun'})", "", 2)
    bpy.context.view_layer.update()
    dg = bpy.context.evaluated_depsgraph_get()
    pts, mats = [], set()
    for inst in dg.object_instances:
        if inst.is_instance and inst.parent is not None and inst.parent.original == ob:
            pts.append(tuple(inst.matrix_world.translation))
            for mt in inst.object.data.materials:
                if mt:
                    mats.add(mt.name)
    n = len(pts)
    r.check(40 <= n <= 400, f"{n} instances (40–400)", "Density Max 3 sur la moitié du sol.", 4)
    if n:
        P = np.array(pts)
        frac = float((P[:, 0] > 0).mean())
        inside = bool((np.abs(P[:, 0]) <= 5.05).all() and (np.abs(P[:, 1]) <= 5.05).all())
        kd = KDTree(n)
        for i, p in enumerate(P):
            kd.insert(p, i)
        kd.balance()
        dmin = min(kd.find_n(p, 2)[1][2] for p in P) if n > 1 else 0.0
    else:
        frac, inside, dmin = 0.0, False, 0.0
    r.check(frac >= 0.95, f"{100 * frac:.0f} % des arbres sur la moitié x > 0 (≥ 95)", "Masque Greater Than 0 sur X.", 4)
    r.check(n > 1 and dmin >= 0.45, f"Distance minimale entre arbres {dmin:.2f} m (≥ 0,45)", "Méthode Poisson, Distance Min 0,5.", 3)
    r.check(inside, "Tous les arbres sont dans le sol", "", 1)
    r.check("MAT_Tree" in mats, f"Matériau des instances : {sorted(mats) or 'aucun'}", "Set Material sur l'arbre.", 2)
    if debug:
        print("[DEBUG] n", n, "frac x>0", round(frac, 3), "dmin", round(dmin, 3), "mats", mats)
    if L.flag("--render"):
        lum = L.quick_render(15, 4)
        r.check(lum > 0.05, f"Rendu de contrôle non noir ({lum:.3f})", "", 1)
    return r.finish()


if __name__ == "__main__":
    L.run(main)
