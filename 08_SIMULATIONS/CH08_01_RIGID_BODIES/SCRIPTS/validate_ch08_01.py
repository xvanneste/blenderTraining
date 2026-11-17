"""
validate_ch08_01.py — Correcteur « Rigid Bodies » (CH08.01).
Usage : … --python-exit-code 1 --python validate_ch08_01.py -- --exercise rigid [--debug]
Objets : GEO_Ground, 30 briques BRICK_*, BALL_Impact.
  Configuration : monde de corps rigides, images 1–150, au moins 10 sous-étapes ; GEO_Ground PASSIVE (forme Box ou Mesh) ;
                  briques ACTIVE, masse de 0,5 à 3 kg, friction de 0,3 à 1,0, forme Box ou Convex Hull ; BALL_Impact ACTIVE, masse ≥ 10 kg,
                  « Animated » (kinematic) animé : vrai à l'image 1, faux à l'image 21 ou après (la boule est lâchée).
  Simulation (images 1 à 150 avancées une à une) :
    avant l'impact (image 12) aucune brique ne s'est déplacée de plus de 2 cm ; à l'image 150 au moins 10 briques sont à plus de 0,6 m de leur place ;
    aucune brique sous le sol (z ≥ −0,05 m) ; la boule a avancé d'au moins 3 m ; mur au repos : entre les images 140 et 150 aucune brique ne bouge de plus de 5 cm.
Testé avec : Blender 5.3.0.
"""
import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bpy  # noqa: E402


def fcurves(act):
    try:
        return list(act.fcurves)
    except AttributeError:
        return [f for l in act.layers for st in l.strips for cb in st.channelbags for f in cb.fcurves]


def main():
    debug = L.flag("--debug")
    r = L.Report("CH08.01 — Corps rigides (mur de briques)")
    sc = bpy.context.scene
    ground, ball = bpy.data.objects.get("GEO_Ground"), bpy.data.objects.get("BALL_Impact")
    bricks = sorted([o for o in bpy.data.objects if o.name.startswith("BRICK_")], key=lambda o: o.name)
    if not r.check(ground is not None and ball is not None and len(bricks) == 30, f"GEO_Ground, BALL_Impact et {len(bricks)} briques présents (30)", "Partez du fichier de départ.", 2):
        return r.finish()
    w = sc.rigidbody_world
    r.check(w is not None and w.point_cache.frame_start == 1 and w.point_cache.frame_end >= 150 and w.substeps_per_frame >= 10, f"Monde : images {w.point_cache.frame_start if w else '–'}–{w.point_cache.frame_end if w else '–'}, sous-étapes {w.substeps_per_frame if w else '–'} (≥ 10)", "Scene > Rigid Body World : cache 1–150.", 4)
    g = ground.rigid_body
    r.check(g is not None and g.type == "PASSIVE" and g.collision_shape in ("BOX", "MESH"), f"Sol : {g.type if g else 'sans corps rigide'} / {g.collision_shape if g else '–'} (Passive, Box ou Mesh)", "Physics > Rigid Body > Passive.", 4)
    okb = all(b.rigid_body is not None and b.rigid_body.type == "ACTIVE" and b.rigid_body.collision_shape in ("BOX", "CONVEX_HULL") and 0.5 <= b.rigid_body.mass <= 3 and 0.3 <= b.rigid_body.friction <= 1.0 for b in bricks)
    r.check(okb, f"Briques : Active, Box ou Convex Hull, masse 0,5–3 kg, friction 0,3–1,0 : {'oui' if okb else 'non'}", "Active, masse 1 kg, friction 0,6.", 6)
    bb = ball.rigid_body
    kin = None
    if ball.animation_data and ball.animation_data.action:
        kin = next((f for f in fcurves(ball.animation_data.action) if f.data_path == "rigid_body.kinematic"), None)
    ks = sorted((round(k.co[0]), k.co[1]) for k in kin.keyframe_points) if kin else []
    rel = bool(ks) and ks[0][0] <= 1 and ks[0][1] > 0.5 and ks[-1][1] < 0.5 and ks[-1][0] >= 15
    r.check(bb is not None and bb.type == "ACTIVE" and bb.mass >= 10 and rel, f"Boule : {bb.type if bb else '–'}, masse {bb.mass if bb else '–'} kg (≥ 10) ; Animated par clés {ks} (vrai à l'image 1, faux à l'image 21 ou après)", "Dynamics > Animated coché à 1, décoché à 21 (clés sur la case).", 7)
    if w is None or any(b.rigid_body is None for b in bricks) or bb is None:
        return r.finish()
    p0 = {b.name: b.matrix_world.translation.copy() for b in bricks}
    b0 = ball.matrix_world.translation.copy()
    sc.frame_set(1)
    pos = {}
    for f in range(1, 151):
        sc.frame_set(f)
        bpy.context.view_layer.update()
        if f in (12, 140, 150):
            pos[f] = {b.name: b.matrix_world.translation.copy() for b in bricks}
        if f == 150:
            bend = ball.matrix_world.translation.copy()
    sc.frame_set(1)
    d12 = max((pos[12][n] - p0[n]).length for n in p0)
    moved = sum(1 for n in p0 if (pos[150][n] - p0[n]).length > 0.6)
    zmin = min(pos[150][n].z for n in p0)
    settle = max((pos[150][n] - pos[140][n]).length for n in p0)
    adv = (bend - b0).length
    r.check(d12 <= 0.02, f"Avant l'impact (image 12) : déplacement maximal d'une brique {1000 * d12:.0f} mm (≤ 20)", "Mur stable : sol Passive, marge 0, bonne friction.", 5)
    r.check(moved >= 10, f"Effondrement : {moved} briques sur 30 à plus de 0,6 m de leur place à l'image 150 (≥ 10)", "Boule assez lourde (20 kg) et lâchée ; briques actives.", 6)
    r.check(zmin >= -0.05, f"Aucune brique sous le sol : z minimal {zmin:.2f} m (≥ −0,05)", "Le sol doit être un corps rigide Passive.", 6)
    r.check(adv >= 3.0, f"La boule a avancé de {adv:.1f} m (≥ 3)", "Boule lâchée à l'image 21.", 3)
    r.check(settle <= 0.05, f"Mur au repos : déplacement maximal {1000 * settle:.0f} mm entre les images 140 et 150 (≤ 50)", "Cache jusqu'à l'image 150.", 4)
    if debug:
        print("[DEBUG] d12", round(d12, 4), "moved", moved, "zmin", round(zmin, 2), "adv", round(adv, 2), "settle", round(settle, 3), "ks", ks)
    return r.finish()


if __name__ == "__main__":
    L.run(main)
