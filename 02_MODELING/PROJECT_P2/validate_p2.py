"""
validate_p2.py — Correcteur du décor du projet de phase P2 « L'atelier ».
Usage : blender -b --factory-startup <p2_atelier_xxx.blend> --python-exit-code 1 --python validate_p2.py
La bibliothèque se vérifie avec 02_MODELING/CH02_13_ASSETS/SCRIPTS/validate_ch02_13.py.
Testé avec : Blender 5.3.0 (test_p2.py : fichier vide refusé, scène d'exemple acceptée).
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bcma_naming_check as N  # noqa: E402
import bmesh  # noqa: E402
import bpy  # noqa: E402


def is_linked(o):
    return o.library is not None or (o.data is not None and getattr(o.data, "library", None) is not None) \
        or o.override_library is not None or (o.instance_type == "COLLECTION" and o.instance_collection is not None
                                              and o.instance_collection.library is not None)


def main():
    r = L.Report("Projet P2 — L'atelier (décor)")
    sc = bpy.context.scene
    cols = {c.name for c in sc.collection.children}
    r.check({"SET", "PROPS", "LIGHTS", "CAMERAS"} <= cols, "Collections SET, PROPS, LIGHTS, CAMERAS", "", 2)
    r.check(not sc.collection.objects, "Aucun objet en vrac", "M pour ranger.", 1)
    N.check(r, 1)
    setc = bpy.data.collections.get("SET")
    set_meshes = [o for o in setc.all_objects if o.type == "MESH"] if setc else []
    zs = [(o.matrix_world @ v.co).z for o in set_meshes for v in o.data.vertices] if set_meshes else [0]
    h = max(zs) - min(zs)
    r.check(set_meshes and 2.4 <= h <= 3.5, f"Pièce : hauteur {h:.2f} m (2,4–3,5)", "Murs à hauteur réelle.", 2)
    props = bpy.data.collections.get("PROPS")
    pobjs = [o for o in props.all_objects if o.type in ("MESH", "EMPTY")] if props else []
    r.check(len(pobjs) >= 10, f"≥ 10 props dans PROPS ({len(pobjs)})", "", 2)
    linked = [o for o in pobjs if is_linked(o)]
    r.check(len(linked) >= 5, f"≥ 5 props liés depuis la bibliothèque ({len(linked)})", "File > Link… ou Asset Browser en mode Link.", 3)
    local = [o for o in sc.objects if o.type == "MESH" and not is_linked(o)]
    mods = {m.type for o in sc.objects if o.type == "MESH" for m in o.modifiers}
    r.check("BEVEL" in mods or "WEIGHTED_NORMAL" in mods, "Un objet avec Bevel ou Weighted Normal", "Hard surface (CH02.05).", 1)
    r.check("SUBSURF" in mods, "Un objet avec Subdivision Surface", "CH02.06.", 1)
    r.check("BOOLEAN" in mods, "Un objet avec Boolean", "Porte/fenêtre ou perçage (CH02.07).", 1)
    bad = [o.name for o in local if o.parent is None and any(abs(s - 1) > 1e-4 for s in o.scale)]
    r.check(not bad, f"Échelles appliquées ({len(bad)} à appliquer : {', '.join(bad[:4])})", "Ctrl+A > Scale.", 2)
    with_uv = [o for o in local if o.data.uv_layers]
    r.check(local and len(with_uv) / len(local) >= 0.8, f"UV présentes ({len(with_uv)}/{len(local)} maillages locaux ≥ 80 %)",
            "U > Unwrap / Smart UV Project (CH02.11).", 2)
    broken = []
    for o in local:
        if len(o.data.polygons) <= 6:
            continue                      # plans et boîtes simples (sol, murs) tolérés
        bm = bmesh.new()
        bm.from_mesh(o.data)
        if any(not e.is_manifold and not e.is_boundary for e in bm.edges):
            broken.append(o.name)
        bm.free()
    r.check(not broken, f"Aucune arête non-manifold anormale ({', '.join(broken[:4])})", "Select All by Trait > Non Manifold.", 1)
    cam = sc.camera
    r.check(cam and cam.name.startswith("CAM_") and 24 <= cam.data.lens <= 85, "Caméra active CAM_… 24–85 mm", "", 1)
    lights = [o for o in sc.objects if o.type == "LIGHT" and not o.hide_render]
    r.check(len(lights) >= 2, f"≥ 2 lumières ({len(lights)})", "", 1)
    p = bpy.path.abspath("//renders/p2_atelier.png")
    r.check(os.path.exists(p), "Rendu renders/p2_atelier.png", "F12 puis Image > Save As.", 2)
    return r.finish()


if __name__ == "__main__":
    L.run(main)
