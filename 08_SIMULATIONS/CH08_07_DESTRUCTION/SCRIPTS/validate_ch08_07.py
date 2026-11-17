"""
validate_ch08_07.py — Correcteur « Destruction » (CH08.07).
Usage : … --python-exit-code 1 --python validate_ch08_07.py -- --exercise destruction [--debug]
Objets : Ground, 24 briques Brick_i_k (6 × 4), Wreck_Ball.
  Configuration : monde de corps rigides (images 1–120, au moins 20 sous-étapes) ; Ground PASSIVE ; briques ACTIVE ; Wreck_Ball ACTIVE de 20 kg ou plus ;
                  au moins 30 contraintes de type Fixed entre deux briques, au moins 90 % avec Breaking coché et un seuil de 0,3 à 3.
  Simulation (images 1 à 120 avancées une à une) : une liaison est « cassée » si la distance entre deux briques voisines (24 briques, 38 paires voisines) diffère de plus de 10 cm
                  de la distance au repos ; à l'image 120 : de 8 à 30 liaisons cassées (le mur se fracture sans être pulvérisé ni poussé d'un bloc) ;
                  aucune brique sous le sol (z ≥ 0,05 m au centre) ; aucune brique à plus de 15 m de l'origine.
Testé avec : Blender 5.3.0.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bpy  # noqa: E402


def main():
    debug = L.flag("--debug")
    r = L.Report("CH08.07 — Destruction (mur à contraintes cassables)")
    sc = bpy.context.scene
    ground, ball = bpy.data.objects.get("Ground"), bpy.data.objects.get("Wreck_Ball")
    grid = {}
    for i in range(6):
        for k in range(4):
            o = bpy.data.objects.get(f"Brick_{i}_{k}")
            if o:
                grid[(i, k)] = o
    if not r.check(ground is not None and ball is not None and len(grid) == 24, f"Ground, Wreck_Ball et {len(grid)} briques présents (24)", "Partez du fichier de départ.", 2):
        return r.finish()
    w = sc.rigidbody_world
    r.check(w is not None and w.point_cache.frame_start == 1 and w.point_cache.frame_end >= 120 and w.substeps_per_frame >= 20, f"Monde : images {w.point_cache.frame_start if w else '–'}–{w.point_cache.frame_end if w else '–'}, sous-étapes {w.substeps_per_frame if w else '–'} (≥ 20)", "Ne touchez pas au monde du fichier de départ.", 3)
    g = ground.rigid_body
    r.check(g is not None and g.type == "PASSIVE", f"Sol : {g.type if g else 'sans corps rigide'} (Passive)", "Physics > Rigid Body > Passive.", 4)
    okb = all(b.rigid_body is not None and b.rigid_body.type == "ACTIVE" for b in grid.values())
    r.check(okb, f"Briques : toutes Active : {'oui' if okb else 'non'}", "Rigid Body Active.", 3)
    bb = ball.rigid_body
    r.check(bb is not None and bb.type == "ACTIVE" and bb.mass >= 20, f"Boulet : {bb.type if bb else '–'}, {bb.mass if bb else '–'} kg (≥ 20)", "Ne touchez pas au boulet.", 3)
    names = {b.name for b in grid.values()}
    cons = [o.rigid_body_constraint for o in bpy.data.objects if o.rigid_body_constraint and o.rigid_body_constraint.type == "FIXED"
            and o.rigid_body_constraint.object1 and o.rigid_body_constraint.object2 and o.rigid_body_constraint.object1.name in names and o.rigid_body_constraint.object2.name in names]
    r.check(len(cons) >= 30, f"Contraintes Fixed entre deux briques : {len(cons)} (≥ 30 ; 38 voisines)", "Physics > Rigid Body > Connect, une paire de voisines à la fois.", 6)
    brk = sum(1 for c in cons if c.use_breaking and 0.3 <= c.breaking_threshold <= 3)
    r.check(cons and brk >= 0.9 * len(cons), f"Contraintes cassables avec seuil de 0,3 à 3 : {brk} sur {len(cons)} (≥ 90 %)", "Settings : Breaking coché, Threshold 1.", 6)
    if w is None or any(b.rigid_body is None for b in grid.values()) or bb is None:
        return r.finish()
    rest = {key: b.matrix_world.translation.copy() for key, b in grid.items()}
    pairs = [((i, k), (i + di, k + dk)) for (i, k) in grid for di, dk in ((1, 0), (0, 1)) if (i + di, k + dk) in grid]
    sc.frame_set(1)
    for f in range(1, 121):
        sc.frame_set(f)
        bpy.context.view_layer.update()
    end = {key: b.matrix_world.translation.copy() for key, b in grid.items()}
    sc.frame_set(1)
    broken = sum(1 for a, b in pairs if abs((end[a] - end[b]).length - (rest[a] - rest[b]).length) > 0.1)
    zmin = min(p.z for p in end.values())
    far = max(p.length for p in end.values())
    r.check(broken >= 8, f"Fracture : {broken} liaisons cassées sur {len(pairs)} (≥ 8)", "Seuil de 1 : le choc casse des contraintes ; un seuil trop haut pousse le mur d'un bloc.", 8)
    r.check(broken <= 30, f"Le mur n'est pas pulvérisé : {broken} liaisons cassées (≤ 30)", "Seuil non nul : des morceaux restent liés.", 5)
    r.check(zmin >= 0.05, f"Aucune brique sous le sol : z minimal {zmin:.2f} m (≥ 0,05)", "Le sol doit être un corps rigide Passive.", 4)
    r.check(far <= 15, f"Aucune brique n'est partie à l'infini : distance maximale {far:.1f} m (≤ 15)", "Mur stable : monde et boulet inchangés.", 3)
    if debug:
        print("[DEBUG] cons", len(cons), "brk", brk, "broken", broken, "zmin", round(zmin, 2), "far", round(far, 1))
    return r.finish()


if __name__ == "__main__":
    L.run(main)
