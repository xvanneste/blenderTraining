"""
validate_ch02_02.py — Correcteur du tabouret (CH02.02).
Usage : blender -b --factory-startup <fichier.blend> --python validate_ch02_02.py --python-exit-code 1 -- --exercise stool [--render]
Mesures sur la géométrie évaluée (coordonnées monde). Testé avec : Blender 5.3.0.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bmesh  # noqa: E402
import bpy  # noqa: E402


def main():
    r = L.Report("CH02.02 — Le tabouret")
    ob = L.obj("GEO_Stool")
    if not r.check(ob is not None and ob.type == "MESH", "GEO_Stool présent (un seul objet maillage)",
                   "Modélisez dans l'objet GEO_Stool fourni.", 1):
        return r.finish()
    dg = bpy.context.evaluated_depsgraph_get()
    bm = bmesh.new()
    bm.from_object(ob, dg)
    bm.transform(ob.matrix_world)
    bm.normal_update()
    xs = [v.co.x for v in bm.verts]; ys = [v.co.y for v in bm.verts]; zs = [v.co.z for v in bm.verts]
    w, d, h = max(xs) - min(xs), max(ys) - min(ys), max(zs) - min(zs)
    r.check(0.35 <= w <= 0.5 and 0.35 <= d <= 0.5, f"Assise de {w * 100:.0f} × {d * 100:.0f} cm (35–50 cm)",
            "Ne mettez pas l'objet à l'échelle en Object Mode ; gardez l'assise de 40 cm.", 1)
    r.check(0.42 <= h <= 0.55 and abs(min(zs)) <= 0.02, f"Hauteur {h * 100:.0f} cm, pieds au sol (z min = {min(zs) * 100:.1f} cm)",
            "Extrudez les pieds jusqu'à z = 0 (total 0,20 + 0,05 + 0,17).", 2)
    feet = {(v.co.x > 0, v.co.y > 0) for v in bm.verts if v.co.z < 0.02}
    r.check(len(feet) == 4, f"{len(feet)} pied(s) touchent le sol (4 attendus)", "Extrudez les 4 carrés d'angle du dessous.", 3)
    sides = set()
    for f in bm.faces:
        c = f.calc_center_median()
        if 0.08 < c.z < 0.32:
            if abs(c.x) < 0.08 and abs(c.y) > 0.1:
                sides.add("Y+" if c.y > 0 else "Y-")
            if abs(c.y) < 0.08 and abs(c.x) > 0.1:
                sides.add("X+" if c.x > 0 else "X-")
    r.check(len(sides) >= 2, f"Traverses entre les pieds : {len(sides)} côté(s) (≥ 2)",
            "Faces du tronçon du milieu en vis-à-vis → Edge > Bridge Edge Loops.", 3)
    bev = sum(1 for f in bm.faces if 0.2 < abs(f.normal.z) < 0.95 and f.calc_center_median().z > 0.44)
    r.check(bev >= 8, f"Chanfrein de l'assise : {bev} faces inclinées (≥ 8)", "Pourtour supérieur : Alt+clic, Ctrl+B, 2 segments.", 2)
    top = [f for f in bm.faces if f.normal.z > 0.99 and f.calc_center_median().z > 0.44]
    levels = {round(f.calc_center_median().z, 3) for f in top}
    r.check(len(top) >= 5 and len(levels) >= 2, f"Dessus inséré et creusé ({len(top)} faces, {len(levels)} niveaux)",
            "Faces du dessus : I (Inset), puis E -0.005.", 2)
    nm = sum(1 for e in bm.edges if not e.is_manifold)
    r.check(nm == 0, f"Maillage fermé ({nm} arête(s) non-manifold)", "Pas de trou : Bridge supprime les faces en vis-à-vis.", 2)
    q = sum(1 for f in bm.faces if len(f.verts) == 4) / max(1, len(bm.faces))
    r.check(q >= 0.85, f"{100 * q:.0f} % de quads (≥ 85 %)", "Évitez Fill/n-gons ; utilisez Loop Cut, Extrude, Bridge.", 1)
    bm.free()
    if L.flag("--render"):
        lum = L.quick_render(15, 4)
        r.check(lum > 0.05, f"Rendu de contrôle non noir ({lum:.3f})", "", 1)
    return r.finish()


if __name__ == "__main__":
    L.run(main)
