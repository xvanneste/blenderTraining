"""
validate_ch01_10.py — Correcteur du petit pont (CH01.10).
Vérifie la présence, les réglages et l'ORDRE des modificateurs, et la géométrie évaluée.
Usage : blender -b --factory-startup <fichier.blend> --python-exit-code 1 --python validate_ch01_10.py -- --exercise bridge [--render]
Testé avec : Blender 5.3.0.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bpy  # noqa: E402


def ev_bbox(o):
    dg = bpy.context.evaluated_depsgraph_get()
    ev = o.evaluated_get(dg)
    me = ev.to_mesh()
    pts = [o.matrix_world @ v.co for v in me.vertices]
    nv = len(me.vertices)
    ev.to_mesh_clear()
    return (min(p.x for p in pts), max(p.x for p in pts), min(p.z for p in pts), max(p.z for p in pts)), nv


def mods(o, t):
    return [m for m in o.modifiers if m.type == t]


def main():
    r = L.Report("CH01.10 — Le petit pont")
    plank, rail, pillar, bucket = (L.obj(n) for n in ("GEO_Plank", "GEO_Railing", "GEO_Pillar", "GEO_Bucket"))
    if not r.check(all((plank, rail, pillar, bucket)), "Objets présents", "", 1):
        return r.finish()
    a = mods(plank, "ARRAY")
    r.check(a and a[0].count == 10, f"Planche : Array de 10 ({a[0].count if a else 0})", "Add Modifier > Generate > Array, Count 10.", 2)
    (x0, x1, _, _), nv = ev_bbox(plank)
    r.check(x1 - x0 > 2.4, f"Tablier long de {x1 - x0:.2f} m (> 2,4 m)", "Relative Offset X ≈ 1,05 (léger espace entre planches).", 1)
    r.check(len(plank.data.vertices) == 8, "Planche : modificateur non appliqué (8 sommets dans le maillage)",
            "N'appliquez pas le modificateur : la pile doit rester modifiable.", 1)
    m = mods(rail, "MIRROR")
    (rx0, rx1, _, _), _ = ev_bbox(rail)
    r.check(m and m[0].use_axis[0] and abs(rx0 + rx1) < 0.05 and rx1 - rx0 > 4.9,
            f"Rambarde symétrique de {rx0:.2f} à {rx1:.2f} m", "Add Modifier > Generate > Mirror, axe X.", 2)
    b = mods(pillar, "BEVEL")
    r.check(b and 0.01 <= b[0].width <= 0.04 and b[0].segments >= 2, "Pilier : Bevel ~0,02 m, ≥ 2 segments",
            "Add Modifier > Generate > Bevel ; Amount 0.02 ; Segments 3.", 2)
    types = [md.type for md in bucket.modifiers]
    ok_order = "SOLIDIFY" in types and "SUBSURF" in types and types.index("SOLIDIFY") < types.index("SUBSURF")
    r.check(ok_order, f"Seau : Solidify AVANT Subdivision (pile : {types})",
            "Glissez la poignée (::::) d'un modificateur pour changer l'ordre, ou menu ˅ > Move to First/Last.", 3)
    s = mods(bucket, "SOLIDIFY")
    r.check(s and 0.01 <= abs(s[0].thickness) <= 0.04, "Seau : épaisseur 1–4 cm", "Solidify > Thickness 0.02.", 1)
    sd = mods(bucket, "SUBSURF")
    r.check(sd and sd[0].render_levels >= 2, "Seau : Subdivision Render ≥ 2", "Levels Viewport 1, Render 2.", 1)
    if L.flag("--render"):
        lum = L.quick_render(15, 4)
        r.check(lum > 0.02, f"Rendu de contrôle non noir ({lum:.3f})", "", 1)
    return r.finish()


if __name__ == "__main__":
    L.run(main)
