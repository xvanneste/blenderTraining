"""
validate_ch08_09.py — Correcteur « Forces » (CH08.09).
Usage : … --python-exit-code 1 --python validate_ch08_09.py -- --exercise forces [--debug]
Objets : EMITTER (300 particules), FORCE_Wind, FORCE_Turb.
  Configuration : FORCE_Wind avec un champ de type Wind, force de 2 à 10, axe local Z orienté vers +X (composante x ≥ 0,9) ;
                  FORCE_Turb avec un champ de type Turbulence, force ≥ 2, taille ≤ 1 ; poids de champ (Field Weights) du système : wind et turbulence ≥ 0,5.
  Simulation (images 1 à 60 avancées une à une) : au moins 280 particules vivantes ; x moyen de 2,5 à 8 m (le vent pousse) ; écart-type en y d'au moins 0,25 m (la turbulence brasse).
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
    r = L.Report("CH08.09 — Forces (vent et turbulence)")
    sc = bpy.context.scene
    em = bpy.data.objects.get("EMITTER")
    if not r.check(em is not None and em.particle_systems, "EMITTER et son système de particules présents", "Partez du fichier de départ.", 2):
        return r.finish()
    w, t = bpy.data.objects.get("FORCE_Wind"), bpy.data.objects.get("FORCE_Turb")
    fw = w.field if w and w.field and w.field.type == "WIND" else None
    ft = t.field if t and t.field and t.field.type == "TURBULENCE" else None
    r.check(fw is not None, f"FORCE_Wind : champ {w.field.type if w and w.field else 'absent'} (Wind)", "Add > Force Field > Wind.", 5)
    if fw is not None:
        zx = w.matrix_world.to_3x3().col[2].normalized().x
        r.check(2 <= fw.strength <= 10, f"Vent : force {fw.strength:.1f} (2–10)", "Strength 5.", 4)
        r.check(zx >= 0.9, f"Vent : direction x = {zx:.2f} (≥ 0,9 : l'axe Z local pointe vers +X)", "Rotation 90° autour de Y.", 5)
    r.check(ft is not None, f"FORCE_Turb : champ {t.field.type if t and t.field else 'absent'} (Turbulence)", "Add > Force Field > Turbulence.", 5)
    if ft is not None:
        r.check(ft.strength >= 2 and ft.size <= 1.0, f"Turbulence : force {ft.strength:.1f} (≥ 2), taille {ft.size:.2f} (≤ 1)", "Strength 5, Size 0,5.", 4)
    ew = em.particle_systems[0].settings.effector_weights
    r.check(ew.wind >= 0.5 and ew.turbulence >= 0.5, f"Field Weights : wind {ew.wind:.1f}, turbulence {ew.turbulence:.1f} (≥ 0,5)", "Field Weights : 1 pour le vent et la turbulence.", 5)
    sc.frame_set(1)
    for f in range(1, 61):
        sc.frame_set(f)
        bpy.context.view_layer.update()
    ev = em.evaluated_get(bpy.context.evaluated_depsgraph_get())
    P = np.array([p.location[:] for p in ev.particle_systems[0].particles if p.alive_state == "ALIVE"])
    sc.frame_set(1)
    n = len(P)
    mx = float(P[:, 0].mean()) if n else 0.0
    sy = float(P[:, 1].std()) if n else 0.0
    r.check(n >= 280, f"Particules vivantes à l'image 60 : {n} (≥ 280)", "Ne changez pas l'émetteur.", 3)
    r.check(2.5 <= mx <= 8, f"Dérive : x moyen {mx:.2f} m (2,5–8)", "Un vent de force 5 vers +X.", 7)
    r.check(sy >= 0.25, f"Brassage : écart-type en y {sy:.2f} m (≥ 0,25)", "Turbulence de force 5, taille 0,5.", 7)
    if debug:
        print("[DEBUG] n", n, "mx", round(mx, 2), "sy", round(sy, 3))
    return r.finish()


if __name__ == "__main__":
    L.run(main)
