"""
validate_ch18_21.py — Correcteur « Storyboard assisté, contrôlé » (CH18.21).
Usage : … --python validate_ch18_21.py --python-exit-code 1 -- --exercise assist [--render]
1. CONTRÔLE de la liste SHOTLIST (proposition d'IA corrigée) : ≥ 5 plans, codes uniques, valeurs et
   sujets connus, toutes les caméras côté « face » (règle des 180°), durées > 0, total = durée cible
   annoncée dans l'en-tête (« durée cible : 12 s »).
2. SCÈNE conforme à la liste : un marqueur par plan à l'image de début, lié à une caméra côté y < 0,
   valeur mesurée (bcma_shots.classify) = valeur demandée, note portée par la caméra, fin de scène.
3. JOURNAL AI_LOG : outil, éléments acceptés et refusés/corrigés (≥ 4 lignes renseignées).
Testé avec : Blender 5.3.0.
"""
import os
import re
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bcma_shots as S  # noqa: E402
import bpy  # noqa: E402

SUBJECTS = {"A": (-1.0, 0.0, 0.0), "B": (1.0, 0.0, 0.0)}
VALUES = {"PE", "PM", "PA", "PRT", "PRP", "GP", "TGP"}


def main():
    sc = bpy.context.scene
    r = L.Report("CH18.21 — Storyboard assisté, contrôlé")
    t = bpy.data.texts.get("SHOTLIST")
    txt = t.as_string() if t else ""
    m = re.search(r"durée cible\s*:\s*(\d+(?:[.,]\d+)?)\s*s", txt, re.I)
    target = float(m.group(1).replace(",", ".")) if m else None
    rows = []
    for line in txt.splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            p = [x.strip() for x in line.split(";")]
            if len(p) >= 6:
                try:
                    rows.append((p[0], p[1].upper(), p[2].upper(), p[3].lower(), float(p[4].replace(",", ".")), p[5]))
                except ValueError:
                    rows.append((p[0], p[1].upper(), p[2].upper(), p[3].lower(), -1.0, p[5]))
    if not r.check(len(rows) >= 5, f"Liste de plans lue ({len(rows)} plans)", "Gardez le format code;valeur;sujet;côté;durée_s;note.", 1):
        return r.finish()
    codes = [x[0] for x in rows]
    dup = sorted({c for c in codes if codes.count(c) > 1})
    r.check(not dup, "Contrôle : codes de plans uniques", f"En double : {dup}", 2)
    bad_v = [x[0] for x in rows if x[1] not in VALUES or x[2] not in SUBJECTS]
    r.check(not bad_v, "Contrôle : valeurs et sujets valides", f"À revoir : {bad_v}", 1)
    axis = [x[0] for x in rows if x[3] != "face"]
    r.check(not axis, "Contrôle : règle des 180° (toutes les caméras côté « face »)", f"Franchissement d'axe : {axis}", 2)
    zero = [x[0] for x in rows if x[4] <= 0]
    r.check(not zero, "Contrôle : durées strictement positives", f"Durée nulle ou invalide : {zero}", 2)
    tot = sum(max(0, x[4]) for x in rows)
    r.check(target is not None and abs(tot - target) < 1e-6, f"Contrôle : total {tot:g} s = durée cible {target} s",
            "Ajustez les durées pour atteindre la cible annoncée en en-tête.", 2)
    # scène générée
    mk = {m.name: m for m in sc.timeline_markers}
    f, wrong = sc.frame_start, []
    for code, val, subj, _side, dur, _note in rows:
        m = mk.get(code)
        if m is None or m.frame != f or m.camera is None:
            wrong.append(f"{code} : marqueur/caméra absent ou pas à l'image {f}")
        else:
            cam = m.camera
            got = S.classify(sc, cam, SUBJECTS.get(subj, SUBJECTS["A"]))[0]
            if got != val:
                wrong.append(f"{code} : {got} au lieu de {val}")
            if cam.matrix_world.translation.y >= 0:
                wrong.append(f"{code} : caméra côté y ≥ 0")
            if not str(cam.get("note", "")).strip():
                wrong.append(f"{code} : note absente")
        f += max(1, round(max(dur, 0) * 24))
    r.check(not wrong, f"Plans générés conformes à la liste ({len(rows) - len({w.split(' ')[0] for w in wrong})}/{len(rows)})",
            " ; ".join(wrong[:4]) + " — relancez shot_prep.py après correction.", 4)
    r.check(sc.frame_end == f - 1, f"Fin de scène {sc.frame_end} (attendu {f - 1})", "shot_prep.py règle la fin de scène.", 1)
    # journal
    log = bpy.data.texts.get("AI_LOG")
    lines = [x for x in (log.as_string().splitlines() if log else []) if x.strip() and not x.strip().startswith("#")]
    low = " ".join(lines).lower()
    ok_log = len(lines) >= 4 and "outil" in low and "accept" in low and ("refus" in low or "corrig" in low)
    r.check(ok_log, f"Journal d'usage de l'IA renseigné ({len(lines)} ligne(s))",
            "AI_LOG : outil, demande, ce qui est accepté, refusé ou corrigé (lignes sans « # »).", 2)
    if L.flag("--render"):
        sc.frame_set(sc.frame_start)
        lum = L.quick_render(15, 4)
        r.check(lum > 0.05, f"Rendu de contrôle non noir ({lum:.3f})", "", 1)
    return r.finish()


if __name__ == "__main__":
    L.run(main)
