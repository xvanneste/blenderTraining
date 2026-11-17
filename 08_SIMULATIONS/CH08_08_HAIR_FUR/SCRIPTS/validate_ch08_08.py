"""
validate_ch08_08.py — Correcteur « Cheveux et fourrure » (CH08.08).
Usage : … --python-exit-code 1 --python validate_ch08_08.py -- --exercise hair [--debug]
Objet : Head (sphère de 1 m, groupe de sommets « scalp »).
  Configuration : un système de particules de type Hair ; Number de 200 à 600 ; Hair Length de 0,4 à 0,6 m ; densité par le groupe « scalp » ; Children Interpolated avec Display Amount ≥ 8 ;
                  Clumping ≥ 0,3 ; Hair Dynamics activée.
  Mesures (images 1 à 30 avancées une à une, données évaluées) : racines de tous les cheveux à z ≥ 0,15 (calotte) ; longueur d'un cheveu (parent 0, le long des clés) de 0,4 à 0,6 m ;
          au moins 2 000 enfants ; mèches : distance moyenne entre l'extrémité (5e étape, co_hair) d'un enfant sur 5 et l'extrémité du parent le plus proche ≤ 0,055 m ;
          dynamique : la hauteur moyenne des pointes baisse d'au moins 0,3 m entre l'image 1 et l'image 30.
Testé avec : Blender 5.3.0.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bpy  # noqa: E402
import numpy as np  # noqa: E402


def main():
    debug = L.flag("--debug")
    r = L.Report("CH08.08 — Cheveux (particules Hair)")
    sc = bpy.context.scene
    ob = bpy.data.objects.get("Head")
    if not r.check(ob is not None and ob.vertex_groups.get("scalp") is not None, "Head et son groupe « scalp » présents", "Partez du fichier de départ.", 2):
        return r.finish()
    ps = ob.particle_systems[0] if ob.particle_systems else None
    if not r.check(ps is not None and ps.settings.type == "HAIR", f"Système de particules : {ps.settings.type if ps else 'aucun'} (Hair)", "Particles > + ; Type Hair.", 5):
        return r.finish()
    s = ps.settings
    r.check(200 <= s.count <= 600 and 0.4 <= s.hair_length <= 0.6, f"Number {s.count} (200–600), Hair Length {s.hair_length:.2f} m (0,4–0,6)", "300 cheveux de 0,5 m.", 5)
    r.check(ps.vertex_group_density == "scalp", f"Densité par le groupe : « {ps.vertex_group_density} » (« scalp »)", "Vertex Groups > Density.", 5)
    r.check(s.child_type == "INTERPOLATED" and s.child_percent >= 8, f"Enfants : {s.child_type}, Display Amount {s.child_percent} (Interpolated, ≥ 8)", "Children : Interpolated, 10.", 5)
    r.check(s.clump_factor >= 0.3, f"Clumping : {s.clump_factor:.2f} (≥ 0,3)", "Children > Clumping 0,5.", 4)
    r.check(ps.use_hair_dynamics, f"Hair Dynamics : {'oui' if ps.use_hair_dynamics else 'non'}", "Hair Dynamics coché.", 4)
    sc.frame_set(1)
    tz = {}
    for f in range(1, 31):
        sc.frame_set(f)
        bpy.context.view_layer.update()
        if f in (1, 30):
            eps = ob.evaluated_get(bpy.context.evaluated_depsgraph_get()).particle_systems[0]
            tz[f] = float(np.mean([p.hair_keys[-1].co[2] for p in eps.particles]))
    eps = ob.evaluated_get(bpy.context.evaluated_depsgraph_get()).particle_systems[0]
    n, nc = len(eps.particles), len(eps.child_particles)
    sc.frame_set(1)
    # racines et longueur : à l'image 1, avant la chute (refait en rejouant)
    sc.frame_set(1)
    bpy.context.view_layer.update()
    e1 = ob.evaluated_get(bpy.context.evaluated_depsgraph_get()).particle_systems[0]
    zroot = min(p.hair_keys[0].co[2] for p in e1.particles)
    k = [np.array(x.co[:]) for x in e1.particles[0].hair_keys]
    length = sum(float(np.linalg.norm(k[i + 1] - k[i])) for i in range(len(k) - 1))
    # mèches (image 30 : les parents ont la même géométrie relative)
    for f in range(1, 31):
        sc.frame_set(f)
        bpy.context.view_layer.update()
    ev = ob.evaluated_get(bpy.context.evaluated_depsgraph_get()).particle_systems[0]
    par = np.array([list(ev.co_hair(ob, particle_no=i, step=4)) for i in range(n)])
    kid = np.array([list(ev.co_hair(ob, particle_no=n + j, step=4)) for j in range(0, nc, 5)]) if nc else np.zeros((0, 3))
    dist = float(np.linalg.norm(kid[:, None, :] - par[None, :, :], axis=2).min(axis=1).mean()) if len(kid) else 9.0
    drop = tz[1] - tz[30]
    sc.frame_set(1)
    r.check(zroot >= 0.15, f"Racines sur la calotte : z minimal {zroot:.2f} m (≥ 0,15)", "Densité : groupe « scalp ».", 6)
    r.check(0.4 <= length <= 0.6, f"Longueur d'un cheveu : {length:.2f} m (0,4–0,6)", "Hair Length 0,5.", 4)
    r.check(nc >= 2000, f"Enfants : {nc} (≥ 2 000)", "Children : Interpolated, 10.", 5)
    r.check(dist <= 0.055, f"Mèches : distance moyenne enfant–parent {1000 * dist:.0f} mm (≤ 55)", "Clumping 0,5.", 5)
    r.check(drop >= 0.3, f"Dynamique : les pointes descendent de {drop:.2f} m entre les images 1 et 30 (≥ 0,3)", "Hair Dynamics coché ; lecture depuis l'image 1.", 6)
    if debug:
        print("[DEBUG] n", n, "nc", nc, "zroot", round(zroot, 2), "len", round(length, 3), "dist", round(dist, 4), "drop", round(drop, 3))
    return r.finish()


if __name__ == "__main__":
    L.run(main)
