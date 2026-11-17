"""
validate_ch02_07.py — Correcteur de « La platine percée » (CH02.07).
Usage : blender -b --factory-startup <fichier.blend> --python-exit-code 1 --python validate_ch02_07.py -- --exercise plate [--render]
Le nombre de trous traversants est mesuré par la caractéristique d'Euler du résultat évalué :
pour une surface fermée d'un seul tenant, V − E + F = 2 − 2g (g = nombre de trous traversants).
Testé avec : Blender 5.3.0.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bmesh  # noqa: E402
import bpy  # noqa: E402


def main():
    r = L.Report("CH02.07 — La platine percée")
    plate = L.obj("GEO_Plate")
    if not r.check(plate is not None, "GEO_Plate présente", "Ne renommez pas la platine.", 1):
        return r.finish()
    col = bpy.data.collections.get("CUTTERS")
    cutters = list(col.objects) if col else []
    r.check(len(cutters) >= 5, f"Collection CUTTERS avec {len(cutters)} cutter(s) (≥ 5)",
            "Collection CUTTERS : 4 cylindres + 1 pavé.", 2)
    if cutters:
        r.check(all(c.display_type in ("WIRE", "BOUNDS") for c in cutters), "Cutters affichés en fil de fer (Wire/Bounds)",
                "Object Properties > Viewport Display > Display As : Wire.", 1)
        r.check(all(c.hide_render for c in cutters), "Cutters désactivés au rendu",
                "Object Properties > Visibility > Show In : Renders décoché.", 2)
    mods = list(plate.modifiers)
    bi = [i for i, m in enumerate(mods) if m.type == "BOOLEAN" and m.operation == "DIFFERENCE"]
    r.check(bi, "Modificateur Boolean (Difference) sur GEO_Plate", "Add Modifier > Generate > Boolean.", 2)
    uses_col = any(mods[i].operand_type == "COLLECTION" and mods[i].collection == col for i in bi) if col else False
    r.check(uses_col, "Boolean en mode Collection sur CUTTERS (un seul modificateur pour tous les cutters)",
            "Operand Type : Collection ; Collection : CUTTERS.", 1, mandatory=False)
    be = [i for i, m in enumerate(mods) if m.type == "BEVEL"]
    r.check(bi and be and min(bi) < max(be), "Bevel placé APRÈS le Boolean (les bords des trous sont biseautés)",
            "Glissez le Bevel sous le Boolean dans la pile.", 2)
    r.check(len(plate.data.vertices) <= 8, f"Rien n'est appliqué (maillage d'origine : {len(plate.data.vertices)} sommets)",
            "N'appliquez pas les modificateurs.", 2)
    dg = bpy.context.evaluated_depsgraph_get()
    bm = bmesh.new()
    bm.from_object(plate, dg)
    nm = sum(1 for e in bm.edges if not e.is_manifold)
    chi = len(bm.verts) - len(bm.edges) + len(bm.faces)
    holes = (2 - chi) // 2
    bm.free()
    r.check(nm == 0, f"Résultat fermé ({nm} arête(s) non-manifold)", "Les cutters doivent TRAVERSER la platine ; Solver Exact.", 2)
    r.check(holes >= 5, f"{holes} trou(s) traversant(s) mesuré(s) (≥ 5)",
            "Cutters plus hauts que la platine (0,1 m) et centrés en z = 0,015.", 3)
    if L.flag("--render"):
        lum = L.quick_render(15, 4)
        r.check(lum > 0.05, f"Rendu de contrôle non noir ({lum:.3f})", "", 1)
    return r.finish()


if __name__ == "__main__":
    L.run(main)
