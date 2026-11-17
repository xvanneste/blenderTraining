"""
validate_ch05_10.py — Correcteur « Optimisation et outils » (CH05.10).
Usage : … --python-exit-code 1 --python validate_ch05_10.py -- --exercise tools [--render] [--debug]
GEO_Base / outil GN_ScatterCones :
  Optimisation : pas de Realize Instances ; géométrie instanciée ≤ 40 sommets ; Density : défaut ≤ 1, borne max ≤ 5 ; entrée utilisée (la grille de base subsiste, 441 sommets) ;
                 par défaut 20 à 500 instances ; à Density = max : ≤ 3 000 instances et ≤ 50 000 triangles instanciés .
  Outil        : node_group.is_modifier = True ; interface Density (Float), Seed (Integer), Scale (Float).
  Publication  : l'arbre est un asset : description, auteur, licence, ≥ 2 tags, catalogue présent dans blender_assets.cats.txt (même dossier que le .blend).
Testé avec : Blender 5.3.0.
"""
import os
import sys
import time

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bpy  # noqa: E402
import numpy as np  # noqa: E402


def read_catalogs():
    path = os.path.join(os.path.dirname(bpy.data.filepath), "blender_assets.cats.txt")
    cats = {}
    if os.path.exists(path):
        for line in open(path, encoding="utf-8"):
            line = line.strip()
            if line and not line.startswith("#") and not line.startswith("VERSION"):
                p = line.split(":")
                if len(p) >= 2:
                    cats[p[0]] = p[1]
    return cats


def measure(ob):
    ob.update_tag()
    bpy.context.view_layer.update()
    dg = bpy.context.evaluated_depsgraph_get()
    ev = ob.evaluated_get(dg)
    me = ev.to_mesh()
    nv = len(me.vertices)
    ev.to_mesh_clear()
    dt = 0.0
    n, iv, it = 0, 0, 0
    for inst in dg.object_instances:
        if inst.is_instance and inst.parent is not None and inst.parent.original == ob:
            n += 1
            dm = inst.object.data
            iv = max(iv, len(dm.vertices))
            dm.calc_loop_triangles()
            it = max(it, len(dm.loop_triangles))
    return n, iv, it, nv, dt


def main():
    debug = L.flag("--debug")
    r = L.Report("CH05.10 — Optimisation et outils")
    ob = bpy.data.objects.get("GEO_Base")
    md = next((m for m in ob.modifiers if m.type == "NODES"), None) if ob else None
    if not r.check(md is not None and md.node_group is not None, "GEO_Base avec un modificateur Geometry Nodes et un arbre", "Partez du fichier de départ.", 3):
        return r.finish()
    ng = md.node_group
    N = ng.nodes
    socks = {i.name: i for i in ng.interface.items_tree if i.item_type == "SOCKET" and i.in_out == "INPUT" and i.name != "Geometry"}
    ok_i = all(n in socks for n in ("Density", "Seed", "Scale")) and socks["Density"].socket_type == "NodeSocketFloat" and socks["Seed"].socket_type == "NodeSocketInt"
    r.check(ok_i, f"Interface : Density (Float), Seed (Integer), Scale (Float) — trouvées : {sorted(socks)}", "", 3)
    if not ok_i:
        return r.finish()
    r.check(not any(n.bl_idname == "GeometryNodeRealizeInstances" for n in N), "Pas de Realize Instances", "Garder les instances : elles partagent la géométrie.", 4)
    dn = socks["Density"]
    r.check(dn.default_value <= 1.0 and dn.max_value <= 5.0, f"Density : défaut {dn.default_value}, borne max {dn.max_value} (défaut ≤ 1, max ≤ 5)", "Une borne protège de millions d'instances.", 4)
    gi = next((n for n in N if n.bl_idname == "NodeGroupInput"), None)
    jn = next((n for n in N if n.bl_idname == "GeometryNodeJoinGeometry"), None)
    uses_in = bool(gi and jn and any(l.from_node == gi and l.from_socket.name == "Geometry" for l in jn.inputs[0].links))
    r.check(uses_in, "La géométrie d'entrée est conservée (Group Input → Join Geometry)", "Un outil modificateur enrichit la géométrie reçue.", 3)
    r.check(ng.is_modifier, "Arbre utilisable comme modificateur (is_modifier)", "Options de l'arbre : Modifier.", 3)
    for n, v in (("Density", 0.5), ("Seed", 0), ("Scale", 1.0)):
        md.properties.inputs[socks[n].identifier]["value"] = v
    n0, iv, it, nv0, dt = measure(ob)
    r.check(0 < iv <= 40, f"Géométrie instanciée : {iv} sommets (≤ 40)", "Cône à 8 côtés.", 4)
    r.check(20 <= n0 <= 500, f"Réglage par défaut : {n0} instances (20–500)", "Density 0,5 sur 400 m².", 3)
    r.check(nv0 >= 441, f"Réglage par défaut : la grille de base subsiste ({nv0} sommets évalués ≥ 441)", "Join Geometry avec l'entrée.", 2)
    md.properties.inputs[socks["Density"].identifier]["value"] = float(dn.max_value) if dn.max_value <= 1000 else 5.0
    n1, iv1, it1, nv1, dt1 = measure(ob)
    r.check(n1 <= 3000 and n1 * it1 <= 50000, f"Density au maximum ({md.properties.inputs[socks['Density'].identifier]['value']}) : {n1} instances, {n1 * it1} triangles instanciés (≤ 3 000 ; ≤ 50 000)", "Borner Density à 5.", 4)
    md.properties.inputs[socks["Density"].identifier]["value"] = 0.5
    # publication
    a = ng.asset_data
    r.check(a is not None, "L'arbre est marqué comme asset", "Mark as Asset sur l'arbre.", 4)
    if a is not None:
        r.check((a.description or "").strip() and (a.author or "").strip() and (a.license or "").strip() and len(a.tags) >= 2, f"Métadonnées : description, auteur, licence, {len(a.tags)} tag(s) (≥ 2)", "Panneau d'asset.", 3)
        cats = read_catalogs()
        r.check(a.catalog_id in cats, f"Catalogue « {cats.get(a.catalog_id, '—')} » présent dans blender_assets.cats.txt", "Ranger l'asset dans un catalogue.", 3)
    else:
        r.check(False, "Métadonnées d'asset", "", 3)
        r.check(False, "Catalogue", "", 3)
    if debug:
        print("[DEBUG] n0", n0, "iv", iv, "it", it, "nv0", nv0, "dt", round(dt, 3), "n1", n1, "it1", it1)
    if L.flag("--render"):
        lum = L.quick_render(15, 4)
        r.check(lum > 0.05, f"Rendu de contrôle non noir ({lum:.3f})", "", 1)
    return r.finish()


if __name__ == "__main__":
    L.run(main)
