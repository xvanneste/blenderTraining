"""
validate_ch07_05.py — Correcteur « Timing et spacing » (CH07.05).
Usage : … --python-exit-code 1 --python validate_ch07_05.py -- --exercise bounce [--debug]
Objet : GEO_Ball (origine à sa base, position Z animée, 72 images à 24 i/s ; plage 1–72).
  Mesures sur la hauteur Z ÉVALUÉE à chaque image :
    Lâcher : Z(1) entre 2,5 et 3,0 m ; jamais sous le sol : Z ≥ −0,02 m partout ;
    Contacts : au moins 3 contacts (premières images d'une série où Z ≤ 0,02 m) ;
    Décroissance : h1/h0 et h2/h1 entre 0,35 et 0,65 (h0 = hauteur du lâcher, h1 et h2 = sommets des deux vols) ; durées de vol : T2/T1 entre 0,55 et 0,85 (T = images entre deux contacts) ;
    Gravité : accélération a = 2·h0/τ0² (chute de τ0 images) et a = 8·h/T² (vols) entre 0,0128 et 0,0213 m/image² (g = 0,01703) ;
    Espacement : accélération médiane (différence seconde de Z) de la chute et de chaque vol, bords exclus, entre −0,0238 et −0,0102 m/image² ;
    Repos : Z ≤ 0,02 m aux images 66 à 72 ; au plus 12 clés sur la courbe Z.
Testé avec : Blender 5.3.0.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bpy  # noqa: E402
import numpy as np  # noqa: E402


def fcurves(act):
    try:
        return list(act.fcurves)
    except AttributeError:
        return [f for l in act.layers for st in l.strips for cb in st.channelbags for f in cb.fcurves]


def main():
    debug = L.flag("--debug")
    r = L.Report("CH07.05 — Timing et spacing (balle rebondissante)")
    ob = bpy.data.objects.get("GEO_Ball")
    if not r.check(ob is not None and ob.animation_data is not None and ob.animation_data.action is not None, "GEO_Ball animée présente", "Partez du fichier de départ.", 2):
        return r.finish()
    sc = bpy.context.scene
    r.check(sc.frame_start == 1 and sc.frame_end == 72 and sc.render.fps == 24, f"Plage {sc.frame_start}–{sc.frame_end} à {sc.render.fps} i/s (1–72 à 24)", "Ne changez pas la plage.", 1)
    fc = next((f for f in fcurves(ob.animation_data.action) if f.data_path == "location" and f.array_index == 2), None)
    if not r.check(fc is not None, "Courbe de position Z présente", "Animez la position Z.", 2):
        return r.finish()
    z = np.zeros(73)
    for f in range(1, 73):
        sc.frame_set(f)
        bpy.context.view_layer.update()
        z[f] = ob.location.z
    sc.frame_set(1)
    r.check(2.5 <= z[1] <= 3.0 and z[1:].min() >= -0.02, f"Lâcher à {z[1]:.2f} m (2,5–3,0) ; point le plus bas {z[1:].min():.3f} m (≥ −0,02)", "Pas de rebond sous le sol : Z ≥ 0.", 3)
    contacts = []
    for f in range(2, 73):
        if z[f] <= 0.02 and (f == 1 or z[f - 1] > 0.02):
            contacts.append(f)
    r.check(len(contacts) >= 3, f"Contacts aux images {contacts} (au moins 3)", "Trois rebonds.", 5)
    if len(contacts) < 3:
        return r.finish()
    c1, c2, c3 = contacts[:3]
    h0 = float(z[1])
    h1 = float(z[c1:c2 + 1].max())
    h2 = float(z[c2:c3 + 1].max())
    T0, T1, T2 = c1 - 1, c2 - c1, c3 - c2
    r.check(0.35 <= h1 / h0 <= 0.65 and 0.35 <= h2 / h1 <= 0.65, f"Décroissance des hauteurs : {h0:.2f} → {h1:.2f} → {h2:.2f} m (rapports {h1 / h0:.2f} et {h2 / h1:.2f}, attendus 0,35–0,65)", "Chaque rebond monte moins haut.", 5)
    r.check(0.55 <= T2 / T1 <= 0.85, f"Décroissance des durées de vol : {T1} puis {T2} images (rapport {T2 / T1:.2f}, attendu 0,55–0,85)", "Chaque vol dure moins longtemps.", 4)
    ag = [2 * h0 / T0 ** 2, 8 * h1 / T1 ** 2, 8 * h2 / T2 ** 2]
    r.check(all(0.0128 <= a <= 0.0213 for a in ag), f"Gravité : accélérations {[round(a, 4) for a in ag]} m/image² (0,0128–0,0213 ; g = 0,0170)", "Hauteur et durée doivent respecter h = g·T²/8.", 6)
    d2 = z[2:] - 2 * z[1:-1] + z[:-2]                                 # d2[i] correspond à l'image i + 2

    def med(a, b):
        a, b = a + 2, b - 2
        return float(np.median(d2[a - 2:b - 1])) if b > a else 0.0
    meds = [med(1, c1), med(c1, c2), med(c2, c3)]
    r.check(all(-0.0238 <= m <= -0.0102 for m in meds), f"Espacement parabolique : accélérations médianes {[round(m, 4) for m in meds]} m/image² (−0,0238 à −0,0102)", "Sommets en poignées horizontales, contacts en poignées raides (Vector) : pas de courbe flottante ni linéaire.", 6)
    r.check(float(z[66:73].max()) <= 0.02, f"Repos : Z max aux images 66–72 = {1000 * float(z[66:73].max()):.0f} mm (≤ 20)", "La balle s'arrête au dernier contact.", 3)
    nk = len(fc.keyframe_points)
    r.check(nk <= 12, f"{nk} clés sur la courbe Z (≤ 12)", "Peu de clés : le Graph Editor fait le reste.", 2)
    if debug:
        print("[DEBUG] contacts", contacts, "h", round(h0, 3), round(h1, 3), round(h2, 3), "T", T0, T1, T2, "ag", [round(a, 4) for a in ag], "meds", [round(m, 4) for m in meds], "rest", round(float(z[66:73].max()), 4), "nk", nk)
    return r.finish()


if __name__ == "__main__":
    L.run(main)
