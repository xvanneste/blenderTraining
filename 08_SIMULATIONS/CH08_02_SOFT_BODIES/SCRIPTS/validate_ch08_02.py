"""
validate_ch08_02.py — Correcteur « Soft Bodies » (CH08.02).
Usage : … --python-exit-code 1 --python validate_ch08_02.py -- --exercise softbody [--debug]
Objet : GEO_Plate (grille de 2 × 2 m à z = 2, groupe de sommets « pin » : poids 1 sur le bord x = −1, poids 0 ailleurs).
  Configuration : modificateur Soft Body ; Goal coché avec le groupe « pin » ; Goal Max ≥ 0,9 ; Edges coché, Pull et Push ≥ 0,5 ; masse de 0,5 à 5 kg.
  Simulation (images 1 à 100 avancées une à une) :
    bord accroché : aucun sommet du groupe ne s'écarte de plus de 2 cm de sa place ;
    bord libre (x = +1) : z moyen entre −0,2 et 0,8 m à l'image 100 (il pend sous le bord accroché sans disparaître) ;
    arêtes : aucune ne dépasse 1,15 fois sa longueur de repos ; rien en dessous de −0,5 m.
Testé avec : Blender 5.3.0.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bpy  # noqa: E402


def main():
    debug = L.flag("--debug")
    r = L.Report("CH08.02 — Soft Body (plaque accrochée)")
    ob = bpy.data.objects.get("GEO_Plate")
    if not r.check(ob is not None and "pin" in ob.vertex_groups, "GEO_Plate et son groupe « pin » présents", "Partez du fichier de départ.", 2):
        return r.finish()
    md = next((m for m in ob.modifiers if m.type == "SOFT_BODY"), None)
    if not r.check(md is not None, "Modificateur Soft Body présent", "Physics > Soft Body.", 4):
        return r.finish()
    s = md.settings
    r.check(s.use_goal and s.vertex_group_goal == "pin" and s.goal_max >= 0.9, f"Goal : {'coché' if s.use_goal else 'décoché'}, groupe « {s.vertex_group_goal} » (pin), Max {s.goal_max:.2f} (≥ 0,9)", "Soft Body Goal : coché, groupe pin, Max 1.", 7)
    r.check(s.use_edges and s.pull >= 0.5 and s.push >= 0.5, f"Edges : {'coché' if s.use_edges else 'décoché'}, Pull {s.pull:.2f}, Push {s.push:.2f} (≥ 0,5)", "Soft Body Edges : coché, Pull et Push à 0,9.", 5)
    r.check(0.5 <= s.mass <= 5.0, f"Masse {s.mass:.1f} kg (0,5–5)", "Une masse modeste.", 3)
    me = ob.data
    rest = [v.co.copy() for v in me.vertices]
    ed = [(e.vertices[0], e.vertices[1]) for e in me.edges]
    rl = [(rest[a] - rest[b]).length for a, b in ed]
    gi = ob.vertex_groups["pin"].index
    pin = [v.index for v in me.vertices if any(g.group == gi and g.weight > 0.5 for g in v.groups)]
    xmax = max(c.x for c in rest)
    free = [i for i, c in enumerate(rest) if c.x > xmax - 1e-4]
    sc = bpy.context.scene
    sc.frame_set(1)
    co = None
    for f in range(1, 101):
        sc.frame_set(f)
        bpy.context.view_layer.update()
    ev = ob.evaluated_get(bpy.context.evaluated_depsgraph_get())
    m = ev.to_mesh()
    co = [v.co.copy() for v in m.vertices]
    ev.to_mesh_clear()
    sc.frame_set(1)
    drift = max((co[i] - rest[i]).length for i in pin) if pin else 9.0
    fz = sum(co[i].z for i in free) / len(free)
    ratio = max((co[a] - co[b]).length / x for (a, b), x in zip(ed, rl))
    zmin = min(c.z for c in co)
    r.check(drift <= 0.02, f"Bord accroché immobile : écart maximal {1000 * drift:.0f} mm (≤ 20)", "Goal avec le groupe pin ; Default 1.", 6)
    r.check(-0.2 <= fz <= 0.8, f"Bord libre : z moyen {fz:.2f} m à l'image 100 (−0,2 à 0,8 : la plaque pend)", "Le bord libre doit tomber et pendre ; pas de goal sur les sommets libres.", 6)
    r.check(ratio <= 1.15 and zmin >= -0.5, f"Arêtes non étirées : {ratio:.2f} fois (≤ 1,15) ; point le plus bas {zmin:.2f} m (≥ −0,5)", "Edges : Pull et Push élevés, masse modeste.", 6)
    if debug:
        print("[DEBUG] drift", round(drift, 4), "fz", round(fz, 3), "ratio", round(ratio, 3), "zmin", round(zmin, 2))
    return r.finish()


if __name__ == "__main__":
    L.run(main)
