"""
bcma_backup.py — Sauvegarde datée et vérifiée d'un dossier de projet (CH00.07).

Crée <destination>/<nom>_AAAA-MM-JJ_HHMMSS.zip, vérifie l'archive (CRC de chaque
fichier), conserve les N dernières archives et supprime les plus anciennes
(UNIQUEMENT les archives de ce projet créées par cet outil, reconnues à leur nom).

Exclusions par défaut (régénérables) : renders/, cache/, __pycache__/, *.blend1, *.blend2,
fichiers temporaires. Utilisez --include-renders pour tout garder.

Usage (Python système, aucune dépendance) :
  python SCRIPTS/bcma_backup.py --source "G:/…/PROJECTS/mon_court" --dest "F:/Backups" [--keep 10]
  python SCRIPTS/bcma_backup.py --source … --dest … --dry-run     (liste sans écrire)
Testé avec : Python 3.14 (Windows).
"""
import argparse
import datetime
import fnmatch
import os
import re
import sys
import zipfile

EXCLUDE_DIRS = {"renders", "cache", "__pycache__", ".git"}
EXCLUDE_FILES = ["*.blend1", "*.blend2", "*.blend@", "*.tmp", "Thumbs.db", "desktop.ini"]


def iter_files(src, include_renders):
    for root, dirs, files in os.walk(src):
        dirs[:] = [d for d in dirs if include_renders or d.lower() not in EXCLUDE_DIRS]
        for f in files:
            if any(fnmatch.fnmatch(f, p) for p in EXCLUDE_FILES):
                continue
            yield os.path.join(root, f)


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    ap = argparse.ArgumentParser(description="Sauvegarde zip datée et vérifiée (BCMA)")
    ap.add_argument("--source", required=True)
    ap.add_argument("--dest", required=True)
    ap.add_argument("--keep", type=int, default=10)
    ap.add_argument("--include-renders", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args(sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else sys.argv[1:])
    src = os.path.abspath(a.source)
    if not os.path.isdir(src):
        print(f"[BCMA] source introuvable : {src}")
        return 1
    name = os.path.basename(src.rstrip("\\/"))
    files = list(iter_files(src, a.include_renders))
    size = sum(os.path.getsize(f) for f in files)
    print(f"[BCMA] {len(files)} fichiers, {size / 1e6:.1f} Mo à sauvegarder depuis {src}")
    if a.dry_run:
        for f in files[:50]:
            print("   ", os.path.relpath(f, src))
        return 0
    os.makedirs(a.dest, exist_ok=True)
    stamp = datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S")
    out = os.path.join(a.dest, f"{name}_{stamp}.zip")
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as z:
        for f in files:
            z.write(f, os.path.join(name, os.path.relpath(f, src)))
    with zipfile.ZipFile(out) as z:
        bad = z.testzip()
    if bad:
        print(f"[BCMA] ERREUR : archive corrompue ({bad})")
        return 1
    print(f"[BCMA] archive vérifiée : {out} ({os.path.getsize(out) / 1e6:.1f} Mo)")
    pattern = re.compile(re.escape(name) + r"_\d{4}-\d{2}-\d{2}_\d{6}\.zip$")
    olds = sorted(f for f in os.listdir(a.dest) if pattern.match(f))
    for f in olds[:-a.keep] if a.keep > 0 else []:
        os.remove(os.path.join(a.dest, f))
        print(f"[BCMA] ancienne archive supprimée : {f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
