"""
validate_ch02_01.py — Correcteur de « La clinique de la topologie » (CH02.01).
Usage : blender -b --factory-startup <fichier.blend> --python-exit-code 1 --python validate_ch02_01.py -- --exercise clinic [--render]
Tout est mesuré sur la géométrie (bmesh) : aucune valeur codée en dur sauf les seuils.
Testé avec : Blender 5.3.0.
"""
import os
import re
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bmesh  # noqa: E402
import bpy  # noqa: E402


def get_bm(name):
    ob = L.obj(name)
    if ob is None or ob.type != "MESH":
        return None
    bm = bmesh.new()
    bm.from_mesh(ob.data)
    return bm


def main():
    r = L.Report("CH02.01 — Clinique de la topologie")
    # 1. n-gon
    bm = get_bm("GEO_Ngon")
    if r.check(bm is not None, "GEO_Ngon présent", "Ne supprimez pas les objets.", 1):
        sides = [len(f.verts) for f in bm.faces]
        r.check(len(sides) >= 3 and max(sides) <= 4, f"GEO_Ngon : plus de n-gon (max {max(sides) if sides else 0} côtés, {len(sides)} faces)",
                "Supprimez la face (X > Only Faces), sélectionnez le contour, Face > Grid Fill.", 3)
        rad = [round(v.co.length, 3) for v in bm.verts]
        r.check(sum(1 for x in rad if abs(x - 0.8) < 0.01) >= 8, "GEO_Ngon : contour d'origine conservé (8 sommets à 0,8 m)",
                "Ne déplacez pas le contour : remplissez-le.", 1)
        bm.free()
    # 2. triangles
    bm = get_bm("GEO_Tris")
    if r.check(bm is not None, "GEO_Tris présent", "", 1):
        q = sum(1 for f in bm.faces if len(f.verts) == 4)
        ratio = q / max(1, len(bm.faces))
        r.check(ratio >= 0.80, f"GEO_Tris : {100 * ratio:.0f} % de quads (≥ 80 % ; maximum possible 83 % : 48 triangles aux pôles)", "Edit Mode, A, Alt+J (Triangles to Quads).", 3)
        bm.free()
    # 3. doublons
    bm = get_bm("GEO_Doubles")
    if r.check(bm is not None, "GEO_Doubles présent", "", 1):
        uniq = {tuple(round(c, 4) for c in v.co) for v in bm.verts}
        r.check(len(uniq) == len(bm.verts), f"GEO_Doubles : aucun sommet superposé ({len(bm.verts)} sommets, {len(uniq)} positions)",
                "Edit Mode, A, M > By Distance.", 3)
        r.check(not any(e.is_boundary for e in bm.edges), "GEO_Doubles : surface fermée (aucune arête de bord)",
                "Après la fusion, les faces doivent être reliées.", 1)
        bm.free()
    # 4. trou
    bm = get_bm("GEO_Hole")
    if r.check(bm is not None, "GEO_Hole présent", "", 1):
        nm = sum(1 for e in bm.edges if not e.is_manifold)
        r.check(nm == 0, f"GEO_Hole : {nm} arête(s) non-manifold (attendu 0)",
                "Select > Select All by Trait > Non Manifold, puis Alt+F ou F.", 3)
        bm.free()
    # 5. diagnostic des pôles
    bm = get_bm("GEO_Poles")
    txt = bpy.data.texts.get("DIAGNOSTIC")
    if r.check(bm is not None and txt is not None, "GEO_Poles et texte DIAGNOSTIC présents", "", 1):
        poles = sum(1 for v in bm.verts if not any(e.is_boundary for e in v.link_edges) and len(v.link_edges) != 4)
        m = re.search(r"POLES\s*=\s*(\d+)", txt.as_string())
        ans = int(m.group(1)) if m else None
        r.check(ans == poles, f"Diagnostic des pôles : réponse {ans}, valeur mesurée {'(cachée)' if ans != poles else poles}",
                "Un pôle = sommet relié à 3 arêtes ou à 5 et plus. Comptez-les sur GEO_Poles.", 3)
        bm.free()
    if L.flag("--render"):
        lum = L.quick_render(15, 4)
        r.check(lum > 0.05, f"Rendu de contrôle non noir ({lum:.3f})", "", 1)
    return r.finish()


if __name__ == "__main__":
    L.run(main)
