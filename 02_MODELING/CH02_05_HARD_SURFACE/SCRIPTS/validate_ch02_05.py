"""
validate_ch02_05.py — Correcteur du boîtier de commande (CH02.05).
Usage : blender -b --factory-startup <fichier.blend> --python validate_ch02_05.py --python-exit-code 1 -- --exercise device [--render]
Testé avec : Blender 5.3.0.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bmesh  # noqa: E402
import bpy  # noqa: E402

H = 0.50


def main():
    r = L.Report("CH02.05 — Le boîtier de commande")
    ob = L.obj("GEO_Device")
    if not r.check(ob is not None and ob.type == "MESH", "GEO_Device présent", "Ne renommez pas l'objet.", 1):
        return r.finish()
    me = ob.data
    r.check(all(abs(s - 1) < 1e-4 for s in ob.scale), "Échelle d'objet à 1 (biseaux réguliers)",
            "Ctrl+A > Scale si vous avez mis l'objet à l'échelle.", 1)
    att = me.attributes.get("bevel_weight_edge")
    nw = sum(1 for d in att.data if d.value > 0.5) if att else 0
    r.check(nw >= 4, f"{nw} arête(s) avec un Bevel Weight (≥ 4 : les arêtes verticales)",
            "Edit Mode, arêtes verticales, Edge > Edge Bevel Weight = 1.", 2)
    bev = [m for m in ob.modifiers if m.type == "BEVEL"]
    r.check(any(m.limit_method == "WEIGHT" and m.segments >= 3 for m in bev), "Bevel « Weight » (≥ 3 segments) pour les coins",
            "Add Modifier > Generate > Bevel, Limit Method : Weight.", 2)
    r.check(any(m.limit_method == "ANGLE" and m.segments >= 2 and m.width <= 0.006 for m in bev),
            "Bevel « Angle » fin (≤ 6 mm, ≥ 2 segments) pour les autres arêtes",
            "2e Bevel : Limit Method : Angle, Width 0.003, Segments 2.", 2)
    r.check(any(m.harden_normals for m in bev) or any(m.type == "WEIGHTED_NORMAL" for m in ob.modifiers),
            "Harden Normals (ou Weighted Normal) activé", "Bevel > Shading > Harden Normals.", 1)
    r.check(sum(p.use_smooth for p in me.polygons) / len(me.polygons) > 0.9, "Shade Smooth", "Object > Shade Smooth.", 1)
    bm = bmesh.new()
    bm.from_mesh(me)
    bm.normal_update()
    ymin = min(v.co.y for v in bm.verts)
    recess = sum(f.calc_area() for f in bm.faces if f.normal.y < -0.99 and f.calc_center_median().y > ymin + 0.005)
    r.check(recess >= 0.02, f"Écran en creux sur la face avant ({recess * 1e4:.0f} cm², ≥ 200)",
            "Face avant : I 0.03 puis E -0.01.", 2)
    tops = [f for f in bm.faces if f.normal.z > 0.99 and f.calc_center_median().z > H + 0.005]
    r.check(len(tops) >= 3, f"{len(tops)} bouton(s) sur le dessus (≥ 3)", "3 cylindres joints (Ctrl+J) ou extrudés.", 2)
    bm.free()
    dg = bpy.context.evaluated_depsgraph_get()
    bm = bmesh.new()
    bm.from_object(ob, dg)
    nm = sum(1 for e in bm.edges if not e.is_manifold)
    r.check(nm == 0, f"Résultat évalué fermé ({nm} arête(s) ouvertes)", "Pas de trou ; boutons fermés (Cap Fill).", 1)
    r.check(len(bm.faces) > len(me.polygons) * 2, f"Biseaux visibles dans le résultat ({len(bm.faces)} faces évaluées)",
            "Modificateurs Bevel actifs (icônes écran et appareil photo).", 1)
    bm.free()
    if L.flag("--render"):
        lum = L.quick_render(15, 4)
        r.check(lum > 0.05, f"Rendu de contrôle non noir ({lum:.3f})", "", 1)
    return r.finish()


if __name__ == "__main__":
    L.run(main)
