"""
validate_ch02_10.py — Correcteur « Alléger sans abîmer » (CH02.10).
Usage : blender -b --factory-startup <fichier.blend> --python validate_ch02_10.py --python-exit-code 1 -- --exercise optim [--render]
L'écart visuel est mesuré entre GEO_Statue évaluée et la référence cachée GEO_Statue_REF (BVH),
en coordonnées locales (les deux objets ont la même transformation d'origine).
Testé avec : Blender 5.3.0.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bmesh  # noqa: E402
import bpy  # noqa: E402
from mathutils.bvhtree import BVHTree  # noqa: E402


def eval_faces(ob):
    """Nombre de TRIANGLES évalués : c'est l'unité du Decimate (Ratio) et des moteurs de rendu."""
    oe = ob.evaluated_get(bpy.context.evaluated_depsgraph_get())
    me = oe.to_mesh()
    me.calc_loop_triangles()
    n = len(me.loop_triangles)
    oe.to_mesh_clear()
    return n


def main():
    r = L.Report("CH02.10 — Alléger sans abîmer")
    st, ref = L.obj("GEO_Statue"), L.obj("GEO_Statue_REF")
    if not r.check(st is not None and ref is not None and len(ref.data.polygons) == 31488,
                   "GEO_Statue et la référence intacte (31 488 faces)", "Ne modifiez pas GEO_Statue_REF.", 2):
        return r.finish()
    base = eval_faces(ref)
    n0 = eval_faces(st)
    r.check(n0 <= 0.25 * base, f"GEO_Statue allégée : {n0} triangles ({100 * n0 / base:.0f} % de {base} ; ≤ 25 %)",
            "Decimate (Collapse) Ratio 0.2.", 3)
    r.check(len(st.data.polygons) == 31488 and any(m.type == "DECIMATE" for m in st.modifiers),
            "Réduction non destructive (modificateur Decimate)", "Gardez le Decimate en modificateur.", 1, mandatory=False)
    bm_r = bmesh.new(); bm_r.from_mesh(ref.data)
    tree = BVHTree.FromBMesh(bm_r)
    bm_s = bmesh.new(); bm_s.from_object(st, bpy.context.evaluated_depsgraph_get())
    d = [tree.find_nearest(v.co)[3] for v in bm_s.verts]
    xs = [v.co for v in bm_r.verts]
    diag = (max(x.x for x in xs) - min(x.x for x in xs)) ** 2 + (max(x.y for x in xs) - min(x.y for x in xs)) ** 2 + (max(x.z for x in xs) - min(x.z for x in xs)) ** 2
    diag **= 0.5
    err = (sum(d) / len(d)) / diag if d else 1
    r.check(err < 0.004, f"Silhouette conservée : écart moyen {100 * err:.3f} % de la taille (< 0,4 %)",
            "Ratio trop agressif : remontez-le (0,2–0,3).", 3)
    bm_r.free(); bm_s.free()
    lod1, lod2 = L.obj("GEO_Statue_LOD1"), L.obj("GEO_Statue_LOD2")
    col = bpy.data.collections.get("LOD")
    r.check(lod1 is not None and lod2 is not None and col is not None and lod1.name in col.objects and lod2.name in col.objects,
            "GEO_Statue_LOD1 et LOD2 dans la collection LOD", "Alt+D, F2, M > LOD.", 2)
    if lod1 and lod2:
        n1, n2 = eval_faces(lod1), eval_faces(lod2)
        r.check(n1 <= 0.1 * base and n2 <= 0.02 * base and n2 < n1 < n0,
                f"LOD dégressifs : {n0} > {n1} > {n2} triangles (LOD1 ≤ 10 %, LOD2 ≤ 2 %)", "Ratios 0,08 et 0,015 par exemple.", 3)
        r.check(lod1.data == st.data and lod2.data == st.data, "LOD en copies liées (même maillage, Alt+D)",
                "Alt+D partage le maillage : une correction de la statue se propage aux LOD.", 2)
    im = L.obj("GEO_Imported")
    if r.check(im is not None, "GEO_Imported présent", "", 1):
        me = im.data
        pos = {tuple(round(c, 4) for c in v.co) for v in me.vertices}
        r.check(len(pos) == len(me.vertices), f"Aucun sommet en double ({len(me.vertices) - len(pos)} restant(s))",
                "Edit Mode, A, M > By Distance.", 2)
        used = {i for p in me.polygons for i in p.vertices}
        r.check(len(used) == len(me.vertices), f"Aucun élément isolé ({len(me.vertices) - len(used)} sommet(s) hors faces)",
                "Mesh > Clean Up > Delete Loose.", 2)
    if L.flag("--render"):
        lum = L.quick_render(15, 4)
        r.check(lum > 0.05, f"Rendu de contrôle non noir ({lum:.3f})", "", 1)
    return r.finish()


if __name__ == "__main__":
    L.run(main)
