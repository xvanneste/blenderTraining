"""
validate_ch07_03.py — Correcteur « Dope Sheet et Action » (CH07.03).
Usage : … --python-exit-code 1 --python validate_ch07_03.py -- --exercise dopesheet [--debug]
Objets : GEO_CrateA et GEO_CrateB.
  Actions : GEO_CrateA porte l'action « Slide » ; GEO_CrateB porte une AUTRE action « Slide_Late » (blocs de données distincts) ; chaque objet a un slot actif.
  « Slide » : clés de position X aux images exactement [1, 25, 49], valeurs 0, 2, 4 (± 0,01) ; une seule utilisation (A).
  « Slide_Late » : clés aux images [25, 49, 73], valeurs 0, 2, 4 (± 0,01).
  Évalué : A : X = 2 à l'image 25, 4 à l'image 49 ; B : X = 0 à l'image 25, 2 à l'image 49, 4 à l'image 73 (± 0,02) ; plage de la scène 1–73.
Testé avec : Blender 5.3.0.
"""
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


def kx(act):
    fc = next((f for f in fcurves(act) if f.data_path == "location" and f.array_index == 0), None)
    return [(round(k.co[0]), k.co[1]) for k in fc.keyframe_points] if fc else []


def ok_keys(keys, frames):
    return [f for f, v in keys] == list(frames) and all(abs(v - e) <= 0.01 for (f, v), e in zip(keys, (0, 2, 4)))


def main():
    debug = L.flag("--debug")
    r = L.Report("CH07.03 — Dope Sheet et Action")
    a, b = bpy.data.objects.get("GEO_CrateA"), bpy.data.objects.get("GEO_CrateB")
    if not r.check(a is not None and b is not None and a.animation_data is not None and a.animation_data.action is not None, "GEO_CrateA (animée) et GEO_CrateB présentes", "Partez du fichier de départ.", 2):
        return r.finish()
    aa = a.animation_data.action
    ba = b.animation_data.action if b.animation_data else None
    r.check(aa.name == "Slide", f"GEO_CrateA porte l'action « {aa.name} » (attendu : Slide)", "Ne renommez pas l'action.", 2)
    r.check(ba is not None and ba.name == "Slide_Late" and ba != aa, f"GEO_CrateB porte une action distincte « {ba.name if ba else None} » (attendu : Slide_Late, différente de Slide)", "Dupliquez l'action, renommez-la, assignez-la à B.", 5)
    sa = a.animation_data.action_slot
    sb = b.animation_data.action_slot if b.animation_data else None
    r.check(sa is not None and sb is not None, "Chaque objet a un slot d'action actif", "Un slot relie une action à un objet.", 2)
    ka = kx(aa)
    r.check(ok_keys(ka, (1, 25, 49)), f"« Slide » : clés {[(f, round(v, 2)) for f, v in ka]} (images 1, 25, 49 ; valeurs 0, 2, 4)", "Dope Sheet : toutes les clés, curseur à l'image 1, S ×2.", 6)
    kb = kx(ba) if ba else []
    r.check(ok_keys(kb, (25, 49, 73)), f"« Slide_Late » : clés {[(f, round(v, 2)) for f, v in kb]} (images 25, 49, 73 ; valeurs 0, 2, 4)", "Décaler l'action dupliquée de 24 images (G).", 6)
    r.check(aa.users == 1, f"« Slide » n'a qu'un utilisateur ({aa.users})", "Ne partagez pas l'action entre les deux caisses.", 2)
    sc = bpy.context.scene

    def x(ob, f):
        sc.frame_set(f)
        bpy.context.view_layer.update()
        return ob.location.x
    va = (x(a, 25), x(a, 49))
    vb = (x(b, 25), x(b, 49), x(b, 73))
    r.check(abs(va[0] - 2) <= 0.02 and abs(va[1] - 4) <= 0.02, f"A évaluée : X = {va[0]:.2f} (image 25) et {va[1]:.2f} (image 49) = 2 et 4", "", 3)
    r.check(abs(vb[0]) <= 0.02 and abs(vb[1] - 2) <= 0.02 and abs(vb[2] - 4) <= 0.02, f"B évaluée : X = {vb[0]:.2f}, {vb[1]:.2f}, {vb[2]:.2f} aux images 25, 49, 73 = 0, 2, 4", "", 3)
    r.check(sc.frame_start == 1 and sc.frame_end == 73, f"Plage de la scène : {sc.frame_start}–{sc.frame_end} (1–73)", "End = 73.", 2)
    sc.frame_set(1)
    if debug:
        print("[DEBUG] ka", ka, "kb", kb, "va", va, "vb", vb, "users", aa.users)
    return r.finish()


if __name__ == "__main__":
    L.run(main)
