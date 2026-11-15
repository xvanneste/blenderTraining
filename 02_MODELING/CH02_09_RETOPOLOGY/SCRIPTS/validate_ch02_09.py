"""
validate_ch02_09.py — Correcteur « Retopologiser un rocher » (CH02.09).
Usage : blender -b --factory-startup <fichier.blend> --python validate_ch02_09.py --python-exit-code 1 -- --exercise retopo [--render]
Écarts mesurés avec des arbres BVH (mathutils.bvhtree) entre la cage évaluée et la sculpture.
Testé avec : Blender 5.3.0.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bmesh  # noqa: E402
import bpy  # noqa: E402
from mathutils.bvhtree import BVHTree  # noqa: E402


def world_bm(ob):
    bm = bmesh.new()
    bm.from_object(ob, bpy.context.evaluated_depsgraph_get())
    bm.transform(ob.matrix_world)
    bm.normal_update()
    return bm


def main():
    r = L.Report("CH02.09 — Retopologiser un rocher")
    sc, rt = L.obj("GEO_Sculpt"), L.obj("GEO_Retopo")
    if not r.check(sc is not None and len(sc.data.polygons) == 20480, "GEO_Sculpt intacte (20 480 faces)",
                   "Ne modifiez pas la sculpture : elle sert de référence.", 2):
        return r.finish()
    if not r.check(rt is not None and rt.type == "MESH", "Objet GEO_Retopo présent", "Créez la cage et nommez-la GEO_Retopo.", 2):
        return r.finish()
    bm_r = world_bm(rt)
    nf = len(bm_r.faces)
    q = sum(1 for f in bm_r.faces if len(f.verts) == 4) / max(1, nf)
    r.check(100 <= nf <= 3000, f"Cage légère : {nf} faces (100–3 000 ; sculpture 20 480)", "Moins de faces : c'est le but.", 2)
    r.check(q >= 0.9, f"{100 * q:.0f} % de quads (≥ 90 %)", "Cube subdivisé, Poly Build : restez en quads.", 2)
    nm = sum(1 for e in bm_r.edges if not e.is_manifold)
    r.check(nm == 0, f"Cage fermée ({nm} arête(s) ouvertes)", "Bouchez les trous ; fusionnez les doublons.", 1)
    bm_s = world_bm(sc)
    t_s = BVHTree.FromBMesh(bm_s)
    t_r = BVHTree.FromBMesh(bm_r)
    d1 = [t_s.find_nearest(v.co)[3] for v in bm_r.verts]
    mean1 = sum(d1) / len(d1)
    r.check(mean1 < 0.02, f"La cage épouse la surface (écart moyen {mean1 * 100:.2f} cm < 2 cm)",
            "Shrinkwrap (Nearest Surface Point) ou snapping Face Project.", 3)
    d2 = [t_r.find_nearest(v.co)[3] for v in list(bm_s.verts)[::20]]
    cover = sum(1 for d in d2 if d < 0.06) / len(d2)
    r.check(cover >= 0.95, f"La cage couvre toute la sculpture ({100 * cover:.0f} % des points à < 6 cm)",
            "Aucune zone oubliée : la cage doit entourer tout le rocher.", 3)
    bm_r.free()
    bm_s.free()
    r.check(sc.hide_render, "Sculpture masquée au rendu", "Outliner : caméra de GEO_Sculpt décochée.", 1, mandatory=False)
    if L.flag("--render"):
        lum = L.quick_render(15, 4)
        r.check(lum > 0.05, f"Rendu de contrôle non noir ({lum:.3f})", "", 1)
    return r.finish()


if __name__ == "__main__":
    L.run(main)
