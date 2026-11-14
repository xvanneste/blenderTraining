"""
validate_p1.py — Correcteur du projet de phase P1 « Nature morte ».
Usage : blender -b --factory-startup <votre_fichier.blend> --python validate_p1.py --python-exit-code 1
Testé avec : Blender 5.3.0 (sur la solution de CH01.14 adaptée et sur un fichier vide).
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bcma_naming_check as N  # noqa: E402
import bpy  # noqa: E402


def main():
    r = L.Report("Projet P1 — Nature morte")
    sc = bpy.context.scene
    cols = {c.name for c in sc.collection.children}
    r.check({"SET", "PROPS", "LIGHTS", "CAMERAS"} <= cols, "Collections SET, PROPS, LIGHTS, CAMERAS", "", 2)
    r.check(not sc.collection.objects, "Aucun objet en vrac", "M pour ranger.", 1)
    N.check(r, 2)
    props = bpy.data.collections.get("PROPS")
    objs = [o for o in props.all_objects if o.type == "MESH"] if props else []
    r.check(len(objs) >= 8, f"≥ 8 objets dans PROPS ({len(objs)})", "", 2)
    shared = any(o.data.users >= 2 for o in objs)
    r.check(shared, "Au moins une duplication liée (Alt+D)", "", 1)
    r.check(any(len(o.modifiers) >= 2 for o in objs), "Un objet avec ≥ 2 modificateurs", "", 1)
    r.check(any(len({p.material_index for p in o.data.polygons}) >= 2 for o in objs), "Un objet multi-matériaux (par faces)", "", 1)
    bad = [o.name for o in sc.objects if o.type == "MESH" and o.parent is None and any(abs(s - 1) > 1e-4 for s in o.scale)]
    r.check(not bad, f"Échelles appliquées ({len(bad)} à appliquer : {', '.join(bad[:4])})", "Ctrl+A > Scale.", 2)
    cam = sc.camera
    r.check(cam and cam.name.startswith("CAM_") and 35 <= cam.data.lens <= 100 and cam.data.dof.use_dof,
            "Caméra active CAM_… 35–100 mm avec profondeur de champ", "", 2)
    lights = [o for o in sc.objects if o.type == "LIGHT" and not o.hide_render]
    r.check(len(lights) >= 3, f"≥ 3 lumières ({len(lights)})", "", 2)
    bg = next((n for n in sc.world.node_tree.nodes if n.type == "BACKGROUND"), None) if sc.world else None
    r.check(bg is None or bg.inputs["Strength"].default_value <= 0.5, "Monde ≤ 0,5", "", 1)
    for name in ("p1_cycles.png", "p1_eevee.png"):
        p = bpy.path.abspath("//renders/" + name)
        ok = os.path.exists(p)
        size = None
        if ok:
            im = bpy.data.images.load(p)
            size = tuple(im.size)
            bpy.data.images.remove(im)
        r.check(ok and size == (1920, 1080), f"renders/{name} en 1920 × 1080", "F12 puis Image > Save As.", 2)
    return r.finish()


if __name__ == "__main__":
    L.run(main)
