"""
validate_ch02_06.py — Correcteur « Garder la forme sous la subdivision » (CH02.06).
Usage : blender -b --factory-startup <fichier.blend> --python-exit-code 1 --python validate_ch02_06.py -- --exercise subdiv [--render]
Mesures sur le maillage ÉVALUÉ (après subdivision). Testé avec : Blender 5.3.0.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bmesh  # noqa: E402
import bpy  # noqa: E402


def evaluated_bm(ob):
    bm = bmesh.new()
    bm.from_object(ob, bpy.context.evaluated_depsgraph_get())
    bm.normal_update()
    return bm


def fill_ratio(bm):
    """Volume réel / volume de la boîte englobante : 1 = cube parfait ; cube 8 sommets subdivisé (Levels 2) = 0,52 (mesuré)."""
    xs = [v.co.x for v in bm.verts]; ys = [v.co.y for v in bm.verts]; zs = [v.co.z for v in bm.verts]
    box = (max(xs) - min(xs)) * (max(ys) - min(ys)) * (max(zs) - min(zs))
    return bm.calc_volume() / box if box else 0


def subsurf(ob):
    return next((m for m in ob.modifiers if m.type == "SUBSURF"), None)


def main():
    r = L.Report("CH02.06 — Garder la forme sous la subdivision")
    for name in ("GEO_Support", "GEO_Crease", "GEO_Pebble"):
        ob = L.obj(name)
        if not r.check(ob is not None and subsurf(ob) is not None, f"{name} avec son modificateur Subdivision",
                       "Ne supprimez pas et n'appliquez pas le modificateur.", 1):
            return r.finish()
    sup = L.obj("GEO_Support")
    bm = evaluated_bm(sup)
    fr = fill_ratio(bm)
    bm.free()
    r.check(len(sup.data.vertices) > 8, f"GEO_Support : boucles ajoutées ({len(sup.data.vertices)} sommets dans la cage)",
            "Ctrl+R, 2 coupes dans chaque direction.", 1)
    r.check(fr >= 0.9, f"GEO_Support : forme cubique conservée (remplissage {fr:.2f} ≥ 0,90 ; sans boucles 0,52, solution 0,99)",
            "Rapprochez les boucles de maintien des arêtes (≈ 5 cm).", 3)
    cr = L.obj("GEO_Crease")
    att = cr.data.attributes.get("crease_edge")
    n = sum(1 for d in att.data if d.value > 0.9) if att else 0
    r.check(n >= 4, f"GEO_Crease : {n} arête(s) avec crease = 1 (≥ 4)", "Arêtes du dessus, Shift+E puis 1.", 2)
    bm = evaluated_bm(cr)
    top = max(v.co.z for v in bm.verts)
    flat = sum(f.calc_area() for f in bm.faces if f.normal.z > 0.999 and f.calc_center_median().z > top - 0.002)
    low = min(v.co.z for v in bm.verts)
    bottom = sum(f.calc_area() for f in bm.faces if f.normal.z < -0.999 and f.calc_center_median().z < low + 0.002)
    bm.free()
    r.check(flat >= 0.35, f"GEO_Crease : dessus plat ({flat:.2f} m² ; sans crease 0, solution 0,42 : coins arrondis en plan)", "Crease = 1 sur les 4 arêtes du dessus.", 3)
    r.check(bottom < flat * 0.6, f"GEO_Crease : le dessous reste arrondi ({bottom:.2f} m² plats)",
            "Ne creasez que le dessus.", 1)
    pm = subsurf(L.obj("GEO_Pebble"))
    r.check(pm.levels <= 1 and pm.render_levels >= 3, f"GEO_Pebble : Levels Viewport {pm.levels} (≤ 1), Render {pm.render_levels} (≥ 3)",
            "Modificateur : Levels Viewport 1, Render 3.", 2)
    if L.flag("--render"):
        lum = L.quick_render(15, 4)
        r.check(lum > 0.05, f"Rendu de contrôle non noir ({lum:.3f})", "", 1)
    return r.finish()


if __name__ == "__main__":
    L.run(main)
