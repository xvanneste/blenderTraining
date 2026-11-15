"""
validate_ch18_19.py — Correcteur « Personnage 2D dans un décor 3D » (CH18.19).
Usage : … --python validate_ch18_19.py --python-exit-code 1 -- --exercise hybrid [--render]
Vérifie : un objet GP avec modificateur Line Art sur le décor (traits réellement générés) ; le
personnage GP_Character debout DANS le décor (pieds au sol, taille humaine, profondeur entre l'avant
et le mur) et en partie caché par un objet 3D vu de la caméra (lancer de rayons) ; les traits de
GP_Decal posés SUR une surface du décor ; la passe Z activée (occlusion au rendu final).
Testé avec : Blender 5.3.0.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bpy  # noqa: E402
from mathutils import Vector  # noqa: E402


def gp_points(ob):
    mw = ob.matrix_world
    pts, n = [], 0
    for lay in ob.data.layers:
        for fr in lay.frames:
            for s in fr.drawing.strokes:
                n += 1
                pts.extend(mw @ Vector(p.position) for p in s.points)
    return pts, n


def set_meshes():
    col = bpy.data.collections.get("SET")
    return [o for o in (col.all_objects if col else []) if o.type == "MESH"]


def dist_to_set(p, meshes):
    best = 1e9
    for o in meshes:
        inv = o.matrix_world.inverted()
        ok, loc, _n, _i = o.closest_point_on_mesh(inv @ p)
        if ok:
            best = min(best, ((o.matrix_world @ loc) - p).length)
    return best


def main():
    sc = bpy.context.scene
    r = L.Report("CH18.19 — Personnage 2D dans un décor 3D")
    dg = bpy.context.evaluated_depsgraph_get()
    meshes = set_meshes()
    r.check(len(meshes) >= 4, f"Décor 3D présent ({len(meshes)} maillages dans SET)", "Repartez du starter.", 1)
    # Line Art
    la = [o for o in sc.objects if o.type == "GREASEPENCIL" and any(m.type == "LINEART" for m in o.modifiers)]
    n_la = 0
    for o in la:
        ev = o.evaluated_get(dg)
        n_la += sum(len(fr.drawing.strokes) for lay in ev.data.layers for fr in lay.frames)
    src_ok = any(m.type == "LINEART" and (m.source_type == "SCENE" or (m.source_type == "COLLECTION" and m.source_collection
                 and m.source_collection.name == "SET")) for o in la for m in o.modifiers)
    r.check(bool(la) and src_ok, f"Line Art sur le décor ({len(la)} objet(s), source scène ou collection SET)",
            "Add > Grease Pencil > Collection Line Art avec SET active.", 2)
    r.check(n_la >= 15, f"Contours générés : {n_la} trait(s) (≥ 15)", "Vérifiez Target Layer / Target Material du modificateur.", 2)
    # personnage
    ch = bpy.data.objects.get("GP_Character")
    pts, n = gp_points(ch) if ch else ([], 0)
    if not r.check(n >= 8, f"Personnage dessiné : {n} trait(s) (≥ 8)", "Calque USER_Char de GP_Character.", 2):
        return r.finish()
    zs, ys = [p.z for p in pts], [p.y for p in pts]
    hgt = max(zs) - min(zs)
    r.check(-0.1 <= min(zs) <= 0.15, f"Pieds au sol (point le plus bas z = {min(zs):.2f} m)", "Curseur 3D au sol pour dessiner.", 2)
    r.check(1.2 <= hgt <= 2.2, f"Taille humaine dans le décor ({hgt:.2f} m)", "Dessinez à l'échelle du décor (1,2–2,2 m).", 2)
    ymean = sum(ys) / len(ys)
    r.check(0.3 <= ymean <= 3.6, f"Placé DANS la pièce (profondeur moyenne y = {ymean:.2f} m)",
            "Pas collé à la caméra ni au mur : déplacez le curseur 3D en profondeur.", 2)
    # occlusion vue caméra
    cam = sc.camera
    origin = cam.matrix_world.translation
    hidden = 0
    sample = pts[::3]
    for p in sample:
        d = p - origin
        hit, loc, _n, _i, obj, _m = sc.ray_cast(dg, origin, d.normalized(), distance=d.length - 0.05)
        if hit and obj and obj.type == "MESH":
            hidden += 1
    frac = hidden / len(sample)
    r.check(0.05 <= frac <= 0.9, f"Partiellement caché par le décor vu de la caméra ({100 * frac:.0f} % des points)",
            "Placez le personnage derrière un objet 3D (la caisse avant) sans qu'il disparaisse.", 2)
    # décor dessiné sur surface
    dc = bpy.data.objects.get("GP_Decal")
    dp, dn = gp_points(dc) if dc else ([], 0)
    on = sum(1 for p in dp[::2] if dist_to_set(p, meshes) <= 0.05)
    tot = len(dp[::2])
    r.check(dn >= 3 and tot and on >= 0.9 * tot, f"Dessin SUR une surface : {dn} trait(s), {on}/{tot} points à moins de 5 cm",
            "Stroke Placement : Surface, en dessinant sur le mur.", 3)
    r.check(bpy.context.view_layer.use_pass_z, "Passe Z activée (occlusion GP/3D au rendu final)",
            "View Layer Properties > Passes > Data > Z.", 2)
    if L.flag("--render"):
        lum = L.quick_render(15, 4)
        r.check(lum > 0.05, f"Rendu de contrôle non noir ({lum:.3f})", "", 1)
    return r.finish()


if __name__ == "__main__":
    L.run(main)
