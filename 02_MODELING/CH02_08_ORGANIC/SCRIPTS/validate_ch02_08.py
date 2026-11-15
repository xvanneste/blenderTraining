"""
validate_ch02_08.py — Correcteur de « L'arbre au modificateur Skin » (CH02.08).
Usage : blender -b --factory-startup <fichier.blend> --python validate_ch02_08.py --python-exit-code 1 -- --exercise tree [--render]
Testé avec : Blender 5.3.0.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bmesh  # noqa: E402
import bpy  # noqa: E402


def main():
    r = L.Report("CH02.08 — L'arbre au modificateur Skin")
    ob = L.obj("GEO_Tree")
    if not r.check(ob is not None and ob.type == "MESH", "GEO_Tree présent", "Ne renommez pas l'objet.", 1):
        return r.finish()
    me = ob.data
    nv, ne = len(me.vertices), len(me.edges)
    r.check(nv >= 10 and len(me.polygons) == 0, f"Squelette d'arêtes : {nv} sommets, {ne} arêtes, {len(me.polygons)} face(s)",
            "Extrudez des sommets (E) : le squelette ne doit contenir que des arêtes.", 2)
    deg = [0] * nv
    for e in me.edges:
        for i in e.vertices:
            deg[i] += 1
    junctions = sum(1 for d in deg if d >= 3)
    r.check(junctions >= 2, f"{junctions} embranchement(s) (sommets reliés à ≥ 3 arêtes ; ≥ 2 : branches + racines)",
            "Extrudez plusieurs fois depuis le même sommet (haut du tronc, base).", 2)
    zs = [v.co.z for v in me.vertices]
    r.check(max(zs) - min(zs) >= 1.5, f"Hauteur du squelette {max(zs) - min(zs):.2f} m (≥ 1,5)", "Tronc + branches ≥ 1,5 m.", 1)
    mods = [m.type for m in ob.modifiers]
    r.check("SKIN" in mods, "Modificateur Skin", "Add Modifier > Generate > Skin.", 2)
    r.check("SKIN" in mods and "SUBSURF" in mods and mods.index("SKIN") < mods.index("SUBSURF"),
            "Subdivision APRÈS le Skin", "Ordre : Skin puis Subdivision Surface.", 2)
    if me.skin_vertices:
        radii = [max(d.radius) for d in me.skin_vertices[0].data]
        ratio = max(radii) / max(min(radii), 1e-6)
        r.check(ratio >= 2.5, f"Rayons variés : base {max(radii) * 100:.0f} cm / pointe {min(radii) * 100:.1f} cm (rapport {ratio:.1f} ≥ 2,5)",
                "Edit Mode, Ctrl+A (Skin Resize) : épaissir la base, affiner les pointes.", 3)
    else:
        r.check(False, "Rayons Skin définis", "Ajoutez le modificateur Skin.", 3)
    if "SKIN" in mods:
        bm = bmesh.new()
        bm.from_object(ob, bpy.context.evaluated_depsgraph_get())
        nm = sum(1 for e in bm.edges if not e.is_manifold)
        r.check(nm == 0 and len(bm.faces) > 100, f"Surface générée fermée ({len(bm.faces)} faces, {nm} arête(s) ouvertes)",
                "Évitez les arêtes en double et les sommets superposés (M > By Distance).", 2)
        bm.free()
    if L.flag("--render"):
        lum = L.quick_render(15, 4)
        r.check(lum > 0.05, f"Rendu de contrôle non noir ({lum:.3f})", "", 1)
    return r.finish()


if __name__ == "__main__":
    L.run(main)
