"""
validate_ch08_03.py — Correcteur « Cloth » (CH08.03).
Usage : … --python-exit-code 1 --python validate_ch08_03.py -- --exercise cloth [--debug]
Objets : CLOTH_Sheet (grille 2,4 × 2,4 m à z = 1,2), COL_Ball (sphère de rayon 0,5 à l'origine), COL_Floor (plan à z = −0,5).
  Configuration : CLOTH_Sheet porte un modificateur Cloth (Quality ≥ 8) avec collisions (Quality ≥ 3, Distance ≤ 1 cm, auto-collision décochée) ; COL_Ball et COL_Floor portent un modificateur Collision.
  Simulation (images 1 à 120 avancées une à une) :
    sommet central du drap à z entre 0,50 et 0,58 m (posé sur la sphère) ; aucun sommet à moins de 0,49 m du centre de la sphère ; point le plus bas ≥ −0,505 m (pas de traversée du sol) ;
    drap au repos : aucun sommet ne bouge de plus de 2 cm entre les images 110 et 120.
Testé avec : Blender 5.3.0.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bpy  # noqa: E402


def main():
    debug = L.flag("--debug")
    r = L.Report("CH08.03 — Cloth (drap sur une sphère)")
    cl, ball, floor = (bpy.data.objects.get(n) for n in ("CLOTH_Sheet", "COL_Ball", "COL_Floor"))
    if not r.check(cl is not None and ball is not None and floor is not None, "CLOTH_Sheet, COL_Ball et COL_Floor présents", "Partez du fichier de départ.", 2):
        return r.finish()
    md = next((m for m in cl.modifiers if m.type == "CLOTH"), None)
    if not r.check(md is not None, "Modificateur Cloth sur CLOTH_Sheet", "Physics > Cloth.", 4):
        return r.finish()
    c = md.collision_settings
    r.check(md.settings.quality >= 8, f"Cloth Quality {md.settings.quality} (≥ 8)", "Quality 12.", 3)
    r.check(c.use_collision and c.collision_quality >= 3 and c.distance_min <= 0.01 and not c.use_self_collision, f"Collisions du tissu : {'actives' if c.use_collision else 'inactives'}, Quality {c.collision_quality} (≥ 3), Distance {1000 * c.distance_min:.0f} mm (≤ 10), auto-collision {'non' if not c.use_self_collision else 'oui'}", "Collisions : Quality 5, Distance 0,005, Self Collisions décoché.", 5)
    has = lambda o: any(m.type == "COLLISION" for m in o.modifiers)  # noqa: E731
    r.check(has(ball) and has(floor), f"Obstacles : COL_Ball {'Collision' if has(ball) else 'sans collision'}, COL_Floor {'Collision' if has(floor) else 'sans collision'}", "Physics > Collision sur la sphère et sur le sol.", 5)
    sc = bpy.context.scene
    sc.frame_set(1)
    snap = {}
    for f in range(1, 121):
        sc.frame_set(f)
        bpy.context.view_layer.update()
        if f in (110, 120):
            ev = cl.evaluated_get(bpy.context.evaluated_depsgraph_get())
            m = ev.to_mesh()
            snap[f] = [v.co.copy() for v in m.vertices]
            ev.to_mesh_clear()
    sc.frame_set(1)
    c1, c0 = snap[120], snap[110]
    mid = min(range(len(c1)), key=lambda i: c1[i].x ** 2 + c1[i].y ** 2)
    center = c1[mid].z
    inside = min(v.length for v in c1)
    zmin = min(v.z for v in c1)
    settle = max((a - b).length for a, b in zip(c0, c1))
    r.check(0.50 <= center <= 0.58, f"Drap posé sur la sphère : sommet central à z = {center:.3f} m (0,50–0,58)", "Gravité active, collision de la sphère.", 6)
    r.check(inside >= 0.49, f"Pas de pénétration de la sphère : distance minimale au centre {inside:.3f} m (≥ 0,49)", "Collision sur la sphère ; Quality et Distance du drap.", 5)
    r.check(zmin >= -0.505, f"Pas de traversée du sol : point le plus bas {zmin:.3f} m (≥ −0,505)", "Collision sur le sol.", 5)
    r.check(settle <= 0.02, f"Drap au repos : déplacement maximal {1000 * settle:.0f} mm entre les images 110 et 120 (≤ 20)", "Quality 12 et Collisions Quality 5 : le drap se stabilise.", 5)
    if debug:
        print("[DEBUG] center", round(center, 3), "inside", round(inside, 3), "zmin", round(zmin, 3), "settle", round(settle, 4))
    return r.finish()


if __name__ == "__main__":
    L.run(main)
