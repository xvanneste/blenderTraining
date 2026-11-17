"""
validate_ch05_07.py — Correcteur « Décors et végétation » (CH05.07).
Usage : … --python-exit-code 1 --python validate_ch05_07.py -- --exercise scattering [--render] [--debug]
GEO_Forest / outil GN_Forest — le correcteur RÈGLE les paramètres du modificateur et mesure les instances évaluées :
  Interface : Seed (Integer), Density (Float), Max Slope (Float, degrés).
  Réglage par défaut (Seed 0 ; Density 0,5 ; Max Slope 30) : 60 à 600 arbres ; chaque arbre sur la surface du terrain (écart vertical ≤ 0,1 m) et sa base posée sur le point (≤ 5 cm) ;
        ≥ 95 % sur une pente ≤ 33° ; ≥ 3 variantes d'arbres (hauteurs de géométrie distinctes) ; échelles variées (écart-type / moyenne ≥ 0,05).
  Seed 7 : autre répartition (≤ 20 % des arbres à moins de 5 cm d'un arbre du réglage par défaut) et nombre voisin (± 40 %).
  Density 0,25 : de 30 % à 70 % du nombre d'arbres par défaut.
  Max Slope 10 : au plus 80 % du nombre par défaut et toutes les pentes ≤ 13°.
Testé avec : Blender 5.3.0.
"""
import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bpy  # noqa: E402
import numpy as np  # noqa: E402
from mathutils import Vector  # noqa: E402
from mathutils.bvhtree import BVHTree  # noqa: E402
from mathutils.kdtree import KDTree  # noqa: E402

EXPECT = {"Seed": "NodeSocketInt", "Density": "NodeSocketFloat", "Max Slope": "NodeSocketFloat"}


def measure(ob):
    ob.update_tag()
    bpy.context.view_layer.update()
    dg = bpy.context.evaluated_depsgraph_get()
    ev = ob.evaluated_get(dg)
    me = ev.to_mesh()
    mw = ev.matrix_world
    verts = [mw @ v.co for v in me.vertices]
    polys = [tuple(p.vertices) for p in me.polygons]
    bvh = BVHTree.FromPolygons(verts, polys) if polys else None
    ev.to_mesh_clear()
    pts, scl, hts, dz, slope, base = [], [], [], [], [], []
    for inst in dg.object_instances:
        if inst.is_instance and inst.parent is not None and inst.parent.original == ob:
            m = inst.matrix_world
            p = m.translation
            s = (m.to_scale().x + m.to_scale().y + m.to_scale().z) / 3
            pts.append((p.x, p.y, p.z))
            scl.append(s)
            dm = inst.object.data
            co = np.empty(len(dm.vertices) * 3, np.float32)
            dm.vertices.foreach_get("co", co)
            zl = co.reshape(-1, 3)[:, 2]
            hts.append(round(float(zl.max() - zl.min()), 1))          # hauteur de la géométrie instanciée (variante)
            base.append(abs(float(zl.min()) * s))
            if bvh is not None:
                hit = bvh.ray_cast(Vector((p.x, p.y, p.z + 8.0)), Vector((0, 0, -1)))
                if hit[0] is not None:
                    dz.append(abs(hit[0].z - p.z))
                    slope.append(math.degrees(math.acos(max(min(hit[1].z, 1.0), -1.0))))
    measure.base = np.array(base)
    return np.array(pts), np.array(scl), hts, np.array(dz), np.array(slope)


def set_param(md, item, v):
    md.properties.inputs[item.identifier]["value"] = v


def main():
    debug = L.flag("--debug")
    r = L.Report("CH05.07 — Décors et végétation")
    ob = bpy.data.objects.get("GEO_Forest")
    md = next((m for m in ob.modifiers if m.type == "NODES"), None) if ob else None
    if not r.check(md is not None and md.node_group is not None, "GEO_Forest avec un modificateur Geometry Nodes et un arbre", "Partez du fichier de départ.", 3):
        return r.finish()
    ng = md.node_group
    socks = {i.name: i for i in ng.interface.items_tree if i.item_type == "SOCKET" and i.in_out == "INPUT" and i.name != "Geometry"}
    ok_if = all(n in socks and socks[n].socket_type == t for n, t in EXPECT.items())
    r.check(ok_if, f"Interface : Seed (Integer), Density (Float), Max Slope (Float) — trouvées : {sorted(socks)}", "Créer les trois entrées.", 4)
    if not ok_if:
        return r.finish()
    P0, S0, H0, DZ0, SL0 = measure(ob)
    n0 = len(P0)
    r.check(60 <= n0 <= 600, f"Réglage par défaut : {n0} arbres (60–600)", "Density 0,5 sur 400 m² avec masque de pente.", 4)
    r.check(n0 > 0 and float(DZ0.max()) <= 0.1, f"Arbres sur la surface du terrain (écart vertical max {float(DZ0.max()) if n0 else 9:.3f} m ≤ 0,1)", "Points issus de Distribute sur le terrain déplacé ; pas de translation parasite.", 4)
    bmax = float(measure.base.max()) if n0 else 9.0
    r.check(n0 > 0 and bmax <= 0.05, f"Base des arbres posée sur le point (écart max {bmax:.3f} m ≤ 0,05)", "Cônes translatés de Depth ÷ 2 seulement.", 3)
    frac = float((SL0 <= 33).mean()) if n0 else 0.0
    r.check(frac >= 0.95, f"{100 * frac:.0f} % des arbres sur une pente ≤ 33° (≥ 95)", "Masque : Normal Z > cos(Max Slope) → Density Factor.", 4)
    var = len(set(H0))
    r.check(var >= 3, f"{var} variantes d'arbres (hauteurs {sorted(set(H0))}) (≥ 3)", "Geometry to Instance + Pick Instance + Instance Index aléatoire.", 3)
    cv = float(S0.std() / S0.mean()) if n0 else 0.0
    r.check(cv >= 0.05, f"Échelles variées (écart-type / moyenne {cv:.3f} ≥ 0,05)", "Scale ← Random Value 0,8–1,2.", 3)
    # Seed
    set_param(md, socks["Seed"], 7)
    P1, _, _, _, _ = measure(ob)
    n1 = len(P1)
    same = 1.0
    if n0 and n1:
        kd = KDTree(n0)
        for i, p in enumerate(P0):
            kd.insert(p, i)
        kd.balance()
        same = float(np.mean([kd.find(p)[2] < 0.05 for p in P1]))
    r.check(n1 > 0 and abs(n1 - n0) <= 0.4 * n0 and same <= 0.2, f"Seed 7 : {n1} arbres, {100 * same:.0f} % identiques au réglage par défaut (≤ 20)", "Seed → Distribute [Seed].", 4)
    set_param(md, socks["Seed"], 0)
    # Density
    set_param(md, socks["Density"], 0.25)
    n2 = len(measure(ob)[0])
    ratio = n2 / n0 if n0 else 0.0
    r.check(0.3 <= ratio <= 0.7, f"Density 0,25 : {n2} arbres, {100 * ratio:.0f} % du réglage par défaut (30–70)", "Density → Distribute [Density Max].", 3)
    set_param(md, socks["Density"], 0.5)
    # Pente
    set_param(md, socks["Max Slope"], 10.0)
    P3, _, _, _, SL3 = measure(ob)
    n3 = len(P3)
    r.check(n3 <= 0.8 * n0 and (n3 == 0 or float(SL3.max()) <= 13), f"Max Slope 10 : {n3} arbres (≤ 80 % de {n0}), pente max {float(SL3.max()) if n3 else 0:.1f}° (≤ 13)", "Max Slope → Radians → Cosine → comparaison avec Normal Z.", 4)
    set_param(md, socks["Max Slope"], 30.0)
    if debug:
        print("[DEBUG] n0", n0, "dz", round(float(DZ0.max()), 3) if n0 else None, "slope≤33", round(frac, 3), "var", sorted(set(H0)), "cv", round(cv, 3), "seed7", n1, round(same, 3), "dens", n2, round(ratio, 2), "slope10", n3)
    if L.flag("--render"):
        lum = L.quick_render(15, 4)
        r.check(lum > 0.05, f"Rendu de contrôle non noir ({lum:.3f})", "", 1)
    return r.finish()


if __name__ == "__main__":
    L.run(main)
