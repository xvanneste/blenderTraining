"""
validate_p5.py — Correcteur du projet P5 « Un outil procédural paramétrable » (ville ou forêt).
Usage : blender -b --factory-startup <p5_tool_<prenom>.blend> --python-exit-code 1 --python validate_p5.py [-- --debug]
Objet GEO_City (ou GEO_Forest) portant UN modificateur Geometry Nodes. Le correcteur RÈGLE les paramètres et mesure les instances évaluées.
  Interface : Seed (Integer, min ≥ 0), Density (Float, 0–1, défaut entre 0,2 et 0,9), Style (Integer, 0 à ≥ 2) + au moins 2 autres entrées ; descriptions ; bornes finies ≤ 1 000 ;
              défauts dans les bornes.
  Arbre     : pas de Realize Instances ; la géométrie d'entrée est conservée ; ≤ 60 nœuds.
  Comportement (instances évaluées) : au réglage par défaut 20 à 5 000 instances ;
      Seed → Seed + 1 : ≤ 50 % des instances identiques (position, hauteur) ;
      Density 0,3 → 0,9 : plus d'instances (× 1,8 au moins) ;
      Style 0 → 2 : les hauteurs de géométrie instanciée changent (ensembles distincts) ;
      les instances restent dans une emprise bornée (≤ 500 m) ; budget : ≤ 20 000 instances aux bornes max de tous les paramètres entiers et flottants sauf Seed/Style.
  Publication : l'arbre est un asset (description, auteur, licence, ≥ 2 tags, catalogue présent dans blender_assets.cats.txt à côté du .blend) ; is_modifier ;
              planche renders/p5_turnaround.png ≥ 1 600 px de large, non noire et contrastée.
Testé avec : Blender 5.3.0.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "SCRIPTS"))
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


def inst_sig(ob):
    ob.update_tag()
    bpy.context.view_layer.update()
    dg = bpy.context.evaluated_depsgraph_get()
    sigs, heights, pts = [], set(), []
    for inst in dg.object_instances:
        if inst.is_instance and inst.parent is not None and inst.parent.original == ob:
            m = inst.matrix_world
            dm = inst.object.data
            co = np.empty(len(dm.vertices) * 3, np.float32)
            dm.vertices.foreach_get("co", co)
            z = co.reshape(-1, 3)[:, 2]
            h = float(z.max() - z.min())
            heights.add(round(h, 1))
            sigs.append((round(m.translation.x, 1), round(m.translation.y, 1), round(h * m.to_scale().z, 1)))
            pts.append((m.translation.x, m.translation.y))
    return sigs, heights, np.array(pts).reshape(-1, 2)


def setp(md, item, v):
    md.properties.inputs[item.identifier]["value"] = v


def main():
    debug = L.flag("--debug")
    r = L.Report("Projet P5 — Un outil procédural paramétrable")
    ob = bpy.data.objects.get("GEO_City") or bpy.data.objects.get("GEO_Forest")
    md = next((m for m in ob.modifiers if m.type == "NODES"), None) if ob else None
    if not r.check(md is not None and md.node_group is not None, "Objet GEO_City (ou GEO_Forest) avec un modificateur Geometry Nodes et un arbre", "Nommage : GEO_City / GEO_Forest.", 6):
        return r.finish()
    ng = md.node_group
    socks = {i.name: i for i in ng.interface.items_tree if i.item_type == "SOCKET" and i.in_out == "INPUT" and i.socket_type != "NodeSocketGeometry"}
    ok_i = (socks.get("Seed") is not None and socks["Seed"].socket_type == "NodeSocketInt" and socks["Seed"].min_value >= 0
            and socks.get("Density") is not None and socks["Density"].socket_type == "NodeSocketFloat" and socks["Density"].min_value >= 0 and socks["Density"].max_value <= 1
            and socks.get("Style") is not None and socks["Style"].socket_type == "NodeSocketInt" and socks["Style"].min_value == 0 and socks["Style"].max_value >= 2)
    r.check(ok_i, f"Interface : Seed (Integer), Density (Float 0–1), Style (Integer 0–2+) — trouvées : {sorted(socks)}", "Trois entrées obligatoires.", 6)
    r.check(len(socks) >= 5, f"{len(socks)} entrées (≥ 5 : Seed, Density, Style + 2 autres)", "Ajoutez deux paramètres propres à votre outil.", 3)
    r.check(all((s.description or "").strip() for s in socks.values()), "Chaque entrée a une description", "", 2)
    bad = [n for n, s in socks.items() if not (s.min_value <= s.default_value <= s.max_value and abs(s.max_value) <= 1000)]
    r.check(not bad, f"Bornes finies (≤ 1 000) et défauts dans les bornes ({bad or 'tous OK'})", "", 3)
    N = ng.nodes
    r.check(not any(n.bl_idname == "GeometryNodeRealizeInstances" for n in N), "Pas de Realize Instances", "", 4)
    gi = next((n for n in N if n.bl_idname == "NodeGroupInput"), None)
    jn = [n for n in N if n.bl_idname == "GeometryNodeJoinGeometry"]
    uses = bool(gi and any(l.from_node == gi and l.from_socket.name == "Geometry" for j in jn for l in j.inputs[0].links))
    r.check(uses, "La géométrie d'entrée est conservée (Group Input → Join Geometry)", "", 2)
    r.check(len([n for n in N if n.type != "FRAME"]) <= 60, "≤ 60 nœuds", "Groupez ou simplifiez.", 1)
    r.check(ng.is_modifier, "Arbre utilisable comme modificateur (is_modifier)", "", 2)
    if not ok_i:
        return r.finish()
    S, D, St = socks["Seed"], socks["Density"], socks["Style"]
    base = {n: s.default_value for n, s in socks.items()}
    for n, v in base.items():
        setp(md, socks[n], v)
    sig0, h0, _ = inst_sig(ob)
    n0 = len(sig0)
    r.check(20 <= n0 <= 5000, f"Réglage par défaut : {n0} instances (20–5 000)", "", 4)
    setp(md, S, int(base["Seed"]) + 1)
    sig1, _, _ = inst_sig(ob)
    same = len(set(sig0) & set(sig1)) / max(len(set(sig0)), 1)
    r.check(n0 > 0 and same <= 0.5, f"Seed + 1 : {100 * same:.0f} % d'instances identiques (≤ 50)", "Seed → tirages aléatoires.", 5)
    setp(md, S, base["Seed"])
    setp(md, D, 0.3)
    nl = len(inst_sig(ob)[0])
    setp(md, D, 0.9)
    nh = len(inst_sig(ob)[0])
    r.check(nl > 0 and nh >= 1.8 * nl, f"Density 0,3 → 0,9 : {nl} → {nh} instances (× {nh / max(nl, 1):.1f} ≥ 1,8)", "Density → probabilité / densité.", 5)
    setp(md, D, base["Density"])
    setp(md, St, 0)
    _, hs0, _ = inst_sig(ob)
    setp(md, St, 2)
    _, hs2, _ = inst_sig(ob)
    r.check(bool(hs0) and bool(hs2) and hs0 != hs2, f"Style 0 → 2 : hauteurs de géométrie {sorted(hs0)} → {sorted(hs2)} (différentes)", "Style → Instance Index (Pick Instance).", 5)
    setp(md, St, base["Style"])
    # emprise et budget aux bornes
    _, _, pts = inst_sig(ob)
    ext = float(np.ptp(pts, axis=0).max()) if len(pts) else 0.0
    r.check(len(pts) > 0 and ext <= 500, f"Emprise {ext:.0f} m (≤ 500)", "", 2)
    for n, s in socks.items():
        if n not in ("Seed", "Style") and s.socket_type in ("NodeSocketInt", "NodeSocketFloat") and n != "Density":
            pass
    mx = dict(base)
    for n, s in socks.items():
        if n not in ("Seed", "Style"):
            mx[n] = s.max_value
    for n, v in mx.items():
        setp(md, socks[n], v)
    nmax = len(inst_sig(ob)[0])
    r.check(nmax <= 20000, f"Aux bornes maximales : {nmax} instances (≤ 20 000)", "Bornez les paramètres de quantité.", 4)
    for n, v in base.items():
        setp(md, socks[n], v)
    # publication
    a = ng.asset_data
    r.check(a is not None, "L'arbre est marqué comme asset", "Mark as Asset.", 4)
    if a is not None:
        r.check((a.description or "").strip() and (a.author or "").strip() and (a.license or "").strip() and len(a.tags) >= 2, f"Métadonnées : description, auteur, licence, {len(a.tags)} tag(s) (≥ 2)", "", 3)
        cats = read_catalogs()
        r.check(a.catalog_id in cats, f"Catalogue « {cats.get(a.catalog_id, '—')} » présent dans blender_assets.cats.txt", "", 3)
    else:
        r.check(False, "Métadonnées", "", 3)
        r.check(False, "Catalogue", "", 3)
    sheet = os.path.join(os.path.dirname(bpy.data.filepath), "renders", "p5_turnaround.png")
    ok_img, msg = False, "absente"
    if os.path.exists(sheet):
        im = bpy.data.images.load(sheet)
        W, H = im.size
        px = np.array(im.pixels[:], np.float32).reshape(H, W, 4)[..., :3]
        ok_img = W >= 1600 and px.mean() > 0.05 and px.std() > 0.03
        msg = f"{W} × {H}, moyenne {px.mean():.2f}, écart-type {px.std():.2f}"
        bpy.data.images.remove(im)
    r.check(ok_img, f"Planche renders/p5_turnaround.png : {msg}", "Trois réglages côte à côte, ≥ 1 600 px de large.", 3)
    if debug:
        print("[DEBUG] n0", n0, "same", round(same, 3), "nl/nh", nl, nh, "h0/h2", sorted(hs0), sorted(hs2), "ext", round(ext, 1), "nmax", nmax)
    return r.finish()


if __name__ == "__main__":
    L.run(main)
