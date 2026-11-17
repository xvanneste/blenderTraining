"""
validate_ch08_04.py — Correcteur « Particules et distribution » (CH08.04).
Usage : … --python-exit-code 1 --python validate_ch08_04.py -- --exercise particles [--debug]
Objets : EMITTER (grille de 0,5 m de côté à z = 1 m) et COL_Floor (plan à z = 0).
  Configuration : un système de particules sur EMITTER : Newtonien, émission depuis les faces, 150 à 400 particules, début à l'image 1, fin entre 20 et 40, durée de vie de 40 à 80 images, vitesse normale de 2 à 5, gravité ≥ 0,5 ;
                  COL_Floor porte un modificateur Collision.
  Simulation (images 1 à 100 avancées une à une ; particules vivantes) :
    émission étalée : à l'image 15 entre 35 % et 65 % des particules sont nées, à l'image 30 au moins 95 % ;
    sommet de la fontaine (z maximal sur toute la simulation) entre 1,3 et 3,0 m ;
    aucune particule sous le sol : z ≥ −0,05 m aux images 35 à 85 ;
    toutes mortes à l'image 95 (durée de vie).
Testé avec : Blender 5.3.0.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bpy  # noqa: E402


def main():
    debug = L.flag("--debug")
    r = L.Report("CH08.04 — Particules (fontaine)")
    em, floor = bpy.data.objects.get("EMITTER"), bpy.data.objects.get("COL_Floor")
    if not r.check(em is not None and floor is not None, "EMITTER et COL_Floor présents", "Partez du fichier de départ.", 2):
        return r.finish()
    if not r.check(len(em.particle_systems) >= 1, "Système de particules sur EMITTER", "Physics > Particles > +.", 4):
        return r.finish()
    st = em.particle_systems[0].settings
    ok = st.physics_type == "NEWTON" and st.emit_from == "FACE" and 150 <= st.count <= 400 and st.frame_start == 1 and 20 <= st.frame_end <= 40 and 40 <= st.lifetime <= 80 and 2 <= st.normal_factor <= 5 and st.effector_weights.gravity >= 0.5
    r.check(ok, f"Particules : {st.physics_type}, depuis {st.emit_from}, {st.count} (150–400), images {st.frame_start:.0f}–{st.frame_end:.0f} (1 ; 20–40), vie {st.lifetime:.0f} (40–80), vitesse normale {st.normal_factor:.1f} (2–5), gravité {st.effector_weights.gravity:.1f} (≥ 0,5)", "Newtonian, Faces, 200, 1–30, vie 60, Normal 3, gravité 1.", 8)
    r.check(any(m.type == "COLLISION" for m in floor.modifiers), "COL_Floor porte un modificateur Collision", "Physics > Collision sur le sol.", 4)
    sc = bpy.context.scene
    sc.frame_set(1)
    n15 = n30 = n95 = 0
    zmax, zmin = -9e9, 9e9
    total = st.count
    for f in range(1, 101):
        sc.frame_set(f)
        bpy.context.view_layer.update()
        if f in (15, 30, 95) or f > 0:
            ev = em.evaluated_get(bpy.context.evaluated_depsgraph_get())
            ps = ev.particle_systems[0].particles
            alive = [q for q in ps if q.alive_state == "ALIVE"]
            for q in alive:
                zmax = max(zmax, q.location.z)
                if 35 <= f <= 85:
                    zmin = min(zmin, q.location.z)
            if f == 15:
                n15 = sum(1 for q in ps if q.alive_state != "UNBORN")
            if f == 30:
                n30 = sum(1 for q in ps if q.alive_state != "UNBORN")
            if f == 95:
                n95 = len(alive)
    sc.frame_set(1)
    r.check(0.35 * total <= n15 <= 0.65 * total and n30 >= 0.95 * total, f"Émission étalée : {n15} nées à l'image 15 ({100 * n15 / total:.0f} %, attendu 35–65 %), {n30} à l'image 30 (≥ 95 %)", "Frame Start 1, End 30.", 6)
    r.check(1.3 <= zmax <= 3.0, f"Sommet de la fontaine : z = {zmax:.2f} m (1,3–3,0)", "Vitesse normale 3, gravité 1.", 6)
    r.check(zmin >= -0.05, f"Aucune particule sous le sol : z minimal {zmin:.2f} m aux images 35–85 (≥ −0,05)", "Collision sur le sol.", 6)
    r.check(n95 == 0, f"Durée de vie : {n95} particules vivantes à l'image 95 (0)", "Lifetime 60 : la dernière née (image 30) meurt à l'image 90.", 4)
    if debug:
        print("[DEBUG] n15", n15, "n30", n30, "zmax", round(zmax, 2), "zmin", round(zmin, 2), "n95", n95)
    return r.finish()


if __name__ == "__main__":
    L.run(main)
