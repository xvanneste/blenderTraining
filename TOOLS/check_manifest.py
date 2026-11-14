"""
check_manifest.py — Vérifie ASSET_MANIFEST.json.

Contrôles : champs obligatoires, identifiants uniques, chemin local existant,
licence renseignée. Avec --update-hashes, recalcule et enregistre l'empreinte
SHA-256 et la taille de chaque fichier (sinon, signale les empreintes divergentes).

Note : un .blend régénéré n'a jamais exactement les mêmes octets (horodatages
internes) ; après une régénération volontaire, relancez avec --update-hashes.
TOOLS/run_all_tests.ps1 le fait automatiquement après reconstruction.

Usage (Python système 3.9+, aucune dépendance) :
  python TOOLS/check_manifest.py
  python TOOLS/check_manifest.py --update-hashes
"""
import hashlib
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MANIFEST = os.path.join(ROOT, "ASSET_MANIFEST.json")
REQUIRED = ["id", "name", "description", "chapter", "type", "source", "license",
            "local_path", "version", "verification_status"]


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    update = "--update-hashes" in sys.argv
    with open(MANIFEST, encoding="utf-8") as f:
        manifest = json.load(f)
    errors, warnings, ids = [], [], set()
    for a in manifest["assets"]:
        aid = a.get("id", "?")
        for k in REQUIRED:
            if not a.get(k):
                errors.append(f"{aid}: champ manquant '{k}'")
        if aid in ids:
            errors.append(f"{aid}: identifiant dupliqué")
        ids.add(aid)
        path = os.path.join(ROOT, a.get("local_path", ""))
        if not os.path.exists(path):
            errors.append(f"{aid}: fichier introuvable {a.get('local_path')}")
            continue
        if os.path.isfile(path):
            digest = sha256(path)
            if update:
                a["sha256"] = digest
                a["size_bytes"] = os.path.getsize(path)
            elif a.get("sha256") and a["sha256"] != digest:
                warnings.append(f"{aid}: empreinte modifiée (fichier régénéré ? relancez --update-hashes)")
    if update:
        with open(MANIFEST, "w", encoding="utf-8") as f:
            json.dump(manifest, f, indent=2, ensure_ascii=False)
            f.write("\n")
        print(f"[manifest] empreintes mises à jour pour {len(manifest['assets'])} assets")
    for w in warnings:
        print("[manifest][WARN]", w)
    for e in errors:
        print("[manifest][ERROR]", e)
    print(f"[manifest] {len(manifest['assets'])} assets, {len(errors)} erreur(s), {len(warnings)} avertissement(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
