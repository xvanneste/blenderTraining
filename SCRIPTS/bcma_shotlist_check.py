"""
bcma_shotlist_check.py — Vérifie une liste de plans (shot list) au format CSV BCMA.

Colonnes obligatoires (séparateur ;) :
  sequence;shot;duration_frames;shot_size;camera_move;description;characters;assets;status
Règles :
  - sequence = sqNNN, shot = shNNNN, couple unique, ordre croissant
  - duration_frames entier > 0
  - shot_size ∈ {EWS, WS, FS, MS, MCU, CU, ECU, OTS, POV, INSERT}
  - status ∈ {todo, board, animatic, layout, anim, lighting, render, comp, done}
Affiche durée totale (à --fps, défaut 24) et nombre de plans.

Usage : python bcma_shotlist_check.py fichier.csv [--fps 24] [--target-seconds 30 --tolerance 3]
        (fonctionne aussi dans Blender : blender -b --python … -- fichier.csv)
Code de retour 1 si erreur bloquante.
Testé avec : Python 3.14 et Blender 5.3.0.
"""
import csv
import re
import sys

COLS = ["sequence", "shot", "duration_frames", "shot_size", "camera_move", "description",
        "characters", "assets", "status"]
SIZES = {"EWS", "WS", "FS", "MS", "MCU", "CU", "ECU", "OTS", "POV", "INSERT"}
STATUS = {"todo", "board", "animatic", "layout", "anim", "lighting", "render", "comp", "done"}


def check(path, fps=24, target=None, tol=3.0):
    errors, rows = [], []
    with open(path, encoding="utf-8-sig", newline="") as f:
        rd = csv.DictReader(f, delimiter=";")
        missing = [c for c in COLS if c not in (rd.fieldnames or [])]
        if missing:
            return [f"colonnes manquantes : {missing}"], 0, 0
        for i, r in enumerate(rd, start=2):
            rows.append(r)
            if not re.fullmatch(r"sq\d{3}", r["sequence"] or ""):
                errors.append(f"ligne {i}: séquence '{r['sequence']}' (attendu sqNNN)")
            if not re.fullmatch(r"sh\d{4}", r["shot"] or ""):
                errors.append(f"ligne {i}: plan '{r['shot']}' (attendu shNNNN)")
            try:
                if int(r["duration_frames"]) <= 0:
                    raise ValueError
            except ValueError:
                errors.append(f"ligne {i}: durée '{r['duration_frames']}' invalide")
            if r["shot_size"] not in SIZES:
                errors.append(f"ligne {i}: valeur de plan '{r['shot_size']}' ∉ {sorted(SIZES)}")
            if r["status"] not in STATUS:
                errors.append(f"ligne {i}: statut '{r['status']}' ∉ {sorted(STATUS)}")
            if not (r["description"] or "").strip():
                errors.append(f"ligne {i}: description vide")
    keys = [(r["sequence"], r["shot"]) for r in rows]
    if len(set(keys)) != len(keys):
        errors.append("doublons sequence/shot")
    if keys != sorted(keys):
        errors.append("plans non triés")
    frames = sum(int(r["duration_frames"]) for r in rows if r["duration_frames"].isdigit())
    secs = frames / fps
    if target is not None and abs(secs - target) > tol:
        errors.append(f"durée totale {secs:.1f} s hors cible {target} ± {tol} s")
    return errors, len(rows), secs


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    a = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else sys.argv[1:]
    if not a:
        print(__doc__)
        return 1
    fps = float(a[a.index("--fps") + 1]) if "--fps" in a else 24
    target = float(a[a.index("--target-seconds") + 1]) if "--target-seconds" in a else None
    tol = float(a[a.index("--tolerance") + 1]) if "--tolerance" in a else 3.0
    errors, n, secs = check(a[0], fps, target, tol)
    print(f"\n====== BCMA — SHOT LIST {a[0]} ======")
    print(f" {n} plans, durée totale {secs:.1f} s à {fps:g} i/s")
    for e in errors:
        print(" ✘", e)
    print(" RÉSULTAT :", "VALIDÉ" if not errors else f"À CORRIGER ({len(errors)})")
    return 1 if errors else 0


if __name__ == "__main__":
    code = main()
    sys.exit(code)
