"""
validate_ch02_04.py — Correcteur « Les ombrages ratés » (CH02.04).
Usage : blender -b --factory-startup <fichier.blend> --python-exit-code 1 --python validate_ch02_04.py -- --exercise normals [--render]
Mesure les normales de coin (corner normals) du maillage ÉVALUÉ : c'est ce qu'utilise le rendu.
Testé avec : Blender 5.3.0.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bpy  # noqa: E402
from mathutils import Vector  # noqa: E402


def evaluated(ob):
    dg = bpy.context.evaluated_depsgraph_get()
    oe = ob.evaluated_get(dg)
    return oe, oe.to_mesh()


def flat_ratio(me, face_filter, tol=0.9999):
    """Part des faces filtrées dont TOUTES les normales de coin sont égales à la normale de face."""
    cn = me.corner_normals
    faces = [p for p in me.polygons if face_filter(p)]
    if not faces:
        return 0.0, 0
    ok = 0
    for p in faces:
        if all(cn[i].vector.dot(p.normal) > tol for i in p.loop_indices):
            ok += 1
    return ok / len(faces), len(faces)


def main():
    r = L.Report("CH02.04 — Les ombrages ratés")
    ob = L.obj("GEO_Flipped")
    if r.check(ob is not None, "GEO_Flipped présent", "Ne supprimez pas les objets.", 1):
        me = ob.data
        c = sum((v.co for v in me.vertices), Vector()) / len(me.vertices)
        inward = sum(1 for p in me.polygons if p.normal.dot(p.center - c) < 0)
        r.check(inward == 0, f"GEO_Flipped : {inward} face(s) tournée(s) vers l'intérieur (0 attendu)",
                "Edit Mode, A, Shift+N (Recalculate Outside). Contrôle : overlay Face Orientation tout bleu.", 4)
    ob = L.obj("GEO_Can")
    if r.check(ob is not None, "GEO_Can présent", "", 1):
        oe, me = evaluated(ob)
        caps, n = flat_ratio(me, lambda p: abs(p.normal.z) > 0.99)
        sides, m = flat_ratio(me, lambda p: abs(p.normal.z) < 0.1)
        r.check(n and caps > 0.99, f"GEO_Can : couvercles plats ({100 * caps:.0f} % de {n})",
                "Object > Shade Auto Smooth (Angle 30°).", 3)
        r.check(m and sides < 0.1, f"GEO_Can : flancs lissés ({100 * (1 - sides):.0f} % de {m} faces lisses)",
                "Le flanc doit rester lisse : ne passez pas en Shade Flat.", 2)
        oe.to_mesh_clear()
    ob = L.obj("GEO_Block")
    if r.check(ob is not None, "GEO_Block présent", "", 1):
        r.check(any(m.type == "WEIGHTED_NORMAL" for m in ob.modifiers), "GEO_Block : modificateur Weighted Normal",
                "Add Modifier > Normals > Weighted Normal.", 2)
        oe, me = evaluated(ob)
        big_area = max(p.area for p in me.polygons)
        big, n = flat_ratio(me, lambda p: p.area > 0.3 * big_area, tol=0.99)   # mesuré : 0,876 sans, 0,994 Weight 50, 1,0 Weight ≥ 75
        r.check(n and big > 0.99, f"GEO_Block : grandes faces sans dégradé ({100 * big:.0f} % de {n})",
                "Weighted Normal : cochez Face Influence et Keep Sharp ; objet en Shade Smooth.", 3)
        smooth = sum(1 for p in me.polygons if p.use_smooth) / len(me.polygons)
        r.check(smooth > 0.9, f"GEO_Block toujours en Shade Smooth ({100 * smooth:.0f} %)",
                "Weighted Normal n'agit que sur un objet lissé.", 1)
        oe.to_mesh_clear()
    if L.flag("--render"):
        lum = L.quick_render(15, 4)
        r.check(lum > 0.05, f"Rendu de contrôle non noir ({lum:.3f})", "", 1)
    return r.finish()


if __name__ == "__main__":
    L.run(main)
