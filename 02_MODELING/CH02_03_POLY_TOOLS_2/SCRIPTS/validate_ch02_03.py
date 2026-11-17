"""
validate_ch02_03.py — Correcteur de « L'atelier de découpe » (CH02.03).
Usage : blender -b --factory-startup <fichier.blend> --python-exit-code 1 --python validate_ch02_03.py -- --exercise atelier [--render]
Mesures en coordonnées LOCALES de chaque objet (géométrie évaluée pour le ressort). Testé avec : Blender 5.3.0.
"""
import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bmesh  # noqa: E402
import bpy  # noqa: E402


def get_bm(name, evaluated=False):
    ob = L.obj(name)
    if ob is None or ob.type != "MESH":
        return None
    bm = bmesh.new()
    if evaluated:
        bm.from_object(ob, bpy.context.evaluated_depsgraph_get())
    else:
        bm.from_mesh(ob.data)
    bm.normal_update()
    return bm


def main():
    r = L.Report("CH02.03 — L'atelier de découpe")
    bm = get_bm("GEO_Bar")
    if r.check(bm is not None, "GEO_Bar présent", "Ne supprimez pas les objets.", 1):
        zmax = max(v.co.z for v in bm.verts)
        r.check(abs(zmax - 0.8) < 0.02, f"GEO_Bar coupé à z = {zmax:.2f} (attendu 0,80)",
                "Mesh > Bisect, panneau : Plane Point Z 0.8, Plane Normal (0,0,1), Clear Outer.", 3)
        nm = sum(1 for e in bm.edges if not e.is_manifold)
        r.check(nm == 0, f"GEO_Bar : coupe bouchée ({nm} arête(s) ouvertes)", "Cochez Fill dans le panneau de Bisect.", 2)
        bm.free()
    bm = get_bm("GEO_Messy")
    if r.check(bm is not None, "GEO_Messy présent", "", 1):
        dims = [max(v.co[i] for v in bm.verts) - min(v.co[i] for v in bm.verts) for i in range(3)]
        r.check(len(bm.faces) <= 6, f"GEO_Messy nettoyé : {len(bm.faces)} faces (≤ 6)", "A, puis X > Limited Dissolve.", 3)
        r.check(all(abs(d - 0.7) < 0.01 for d in dims), "GEO_Messy : forme intacte (cube de 70 cm)",
                "Dissolve ne doit pas déformer : n'utilisez pas Delete.", 1)
        bm.free()
    bm = get_bm("GEO_Profile")
    if r.check(bm is not None, "GEO_Profile présent", "", 1):
        sectors = {round(((math.degrees(math.atan2(v.co.y, v.co.x)) + 360) % 360) / 15) % 24 for v in bm.verts if v.co.xy.length > 0.05}
        r.check(len(bm.faces) >= 150 and len(sectors) >= 22, f"Vase tourné : {len(bm.faces)} faces, {len(sectors)}/24 secteurs couverts",
                "Curseur au centre (Shift+C), A, Alt+E > Spin : Steps 24, Angle 360°, Axis Z.", 3)
        uniq = {tuple(round(c, 4) for c in v.co) for v in bm.verts}
        r.check(len(uniq) == len(bm.verts), f"Vase sans couture (aucun sommet en double : {len(bm.verts) - len(uniq)})",
                "Cochez Auto Merge dans le panneau de Spin, ou M > By Distance.", 2)
        bnd = [e for e in bm.edges if e.is_boundary]
        r.check(bnd and all(min(v.co.z for v in e.verts) > 0.3 for e in bnd), "Vase fermé au fond, ouvert seulement au col",
                "Le profil doit partir de l'axe (premier sommet en x = 0).", 1)
        bm.free()
    bm = get_bm("GEO_Pyramid")
    if r.check(bm is not None, "GEO_Pyramid présent", "", 1):
        top = max(bm.verts, key=lambda v: v.co.z)
        r.check(len(bm.verts) == 5 and top.co.xy.length < 0.01, f"Pyramide : {len(bm.verts)} sommets, pointe centrée",
                "Sélectionnez les 4 sommets du haut, M > At Center.", 3)
        bm.free()
    sp = L.obj("GEO_Spring")
    if r.check(sp is not None, "GEO_Spring présent", "", 1):
        ms = [m for m in sp.modifiers if m.type == "SCREW"]
        ok = bool(ms) and ms[0].iterations >= 4 and abs(ms[0].screw_offset) >= 0.04
        r.check(ok, "Modificateur Screw (Iterations ≥ 4, Screw ≥ 0,04)", "Add Modifier > Generate > Screw.", 3)
        bm = get_bm("GEO_Spring", evaluated=True)
        h = max(v.co.z for v in bm.verts) - min(v.co.z for v in bm.verts)
        r.check(h >= 0.25, f"Ressort de {h * 100:.0f} cm de haut (≥ 25 cm)", "Augmentez Screw ou Iterations.", 1)
        bm.free()
    bm = get_bm("GEO_Tile")
    if r.check(bm is not None, "GEO_Tile présent", "", 1):
        diag = [e for e in bm.edges if all(abs(v.co.x - v.co.y) < 0.005 for v in e.verts)
                and abs(e.verts[0].co.x - e.verts[1].co.x) > 0.01]
        span = sum(abs(e.verts[0].co.x - e.verts[1].co.x) for e in diag)
        width = max(v.co.x for v in bm.verts) - min(v.co.x for v in bm.verts)
        r.check(span >= 0.97 * width, f"Diagonale coupée au Knife (couverte sur {span:.2f} m / {width:.2f} m)",
                "K, clic sur un coin, clic sur le coin opposé, Entrée.", 3)
        bm.free()
    if L.flag("--render"):
        lum = L.quick_render(15, 4)
        r.check(lum > 0.05, f"Rendu de contrôle non noir ({lum:.3f})", "", 1)
    return r.finish()


if __name__ == "__main__":
    L.run(main)
