"""
validate_ch18_09.py — Correcteur CH18.09 (décor dessiné en profondeur).
Usage : blender -b --factory-startup <fichier.blend> --python-exit-code 1 --python validate_ch18_09.py -- --exercise set [--render]
Testé avec : Blender 5.3.0.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bpy  # noqa: E402
from bpy_extras.object_utils import world_to_camera_view  # noqa: E402


def layer_points(ob, lay):
    pts, n = [], 0
    for fr in lay.frames:
        n += len(fr.drawing.strokes)
        for s in fr.drawing.strokes:
            for p in s.points:
                pts.append(ob.matrix_world @ lay.matrix_local @ p.position)
    return pts, n


def main():
    r = L.Report("CH18.09 — Décor dessiné en profondeur")
    sc = bpy.context.scene
    ob, cam = L.obj("GP_Set"), L.obj("CAM_Layout")
    if not r.check(ob is not None and ob.type == "GREASEPENCIL" and cam is not None,
                   "GP_Set et CAM_Layout présents", "Ne renommez pas l'objet ni la caméra.", 1):
        return r.finish()
    lay = {l.name: l for l in ob.data.layers}
    cpos = cam.matrix_world.translation
    dist, allpts = {}, []
    for name, mn in (("BG", 4), ("MID", 4), ("FG", 4), ("GROUND", 3)):
        if not r.check(name in lay, f"Calque {name} présent", "Ne supprimez pas les calques fournis.", 1):
            continue
        pts, n = layer_points(ob, lay[name])
        allpts += pts
        r.check(n >= mn, f"{name} : {n} traits (≥ {mn})", f"Dessinez sur le calque {name}.", 2)
        if pts:
            dist[name] = sum((p - cpos).length for p in pts) / len(pts)
    if all(k in dist for k in ("FG", "MID", "BG")):
        r.check(dist["MID"] - dist["FG"] >= 3.0, f"FG nettement devant MID ({dist['FG']:.1f} m / {dist['MID']:.1f} m)",
                "Dessinez FG près de la caméra (Y ≈ -5) : curseur 3D + Stroke Placement 3D Cursor.", 2)
        r.check(dist["BG"] - dist["MID"] >= 4.0, f"BG nettement derrière MID ({dist['MID']:.1f} m / {dist['BG']:.1f} m)",
                "Dessinez BG loin (Y ≈ 14) : déplacez le curseur 3D avant de dessiner.", 2)
    if "GROUND" in lay:
        pts, _ = layer_points(ob, lay["GROUND"])
        if pts:
            zs, ys = [p.z for p in pts], [p.y for p in pts]
            r.check(max(zs) - min(zs) <= 0.3 and abs(sum(zs) / len(zs)) <= 0.3,
                    f"GROUND dessiné à plat sur le sol (Z de {min(zs):.2f} à {max(zs):.2f})",
                    "Drawing Plane : Top (X-Y), curseur 3D à Z = 0.", 2)
            r.check(max(ys) - min(ys) >= 6.0, f"GROUND s'étend en profondeur ({max(ys) - min(ys):.1f} m en Y ≥ 6)",
                    "Dessinez la route de l'avant vers le fond.", 1)
    if allpts:
        inside = sum(1 for p in allpts if (lambda v: 0 <= v.x <= 1 and 0 <= v.y <= 1 and v.z > 0)(world_to_camera_view(sc, cam, p)))
        r.check(inside / len(allpts) >= 0.5, f"Décor visible dans CAM_Layout ({100 * inside / len(allpts):.0f} % des points)",
                "Vérifiez en vue caméra (Num 0).", 1)
    r.check(bpy.context.view_layer.use_pass_z, "Passe Z activée", "View Layer > Passes > Data > Z.", 1)
    ref = L.obj("REF_Concept")
    r.check(ref is not None and ref.type == "EMPTY" and ref.empty_display_type == "IMAGE",
            "Image de référence REF_Concept conservée", "Ne supprimez pas la référence.", 1, mandatory=False)
    if L.flag("--render"):
        lum = L.quick_render(15, 4)
        r.check(lum > 0.1, f"Rendu de contrôle non noir ({lum:.3f})", "", 1)
    return r.finish()


if __name__ == "__main__":
    L.run(main)
