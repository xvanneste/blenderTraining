"""Contrôles reproductibles du pilote (Python 3, sans dépendance)."""
import argparse
import csv
import hashlib
import json
import re
import struct
import zipfile
from pathlib import Path, PurePosixPath

HERE = Path(__file__).resolve().parent
SHOT_ID = re.compile(r"SQ\d{3}_SH\d{3}")


def read_rows(path):
    with path.open(encoding="utf-8-sig", newline="") as source:
        return list(csv.DictReader(source))


def tokens(text):
    return tuple(part for part in text.split("+") if part)


def valider_plans(rows, assets):
    expected_start = 1
    seen = set()
    for row in rows:
        name = row["plan"]
        if name in seen or not SHOT_ID.fullmatch(name):
            raise ValueError(f"Identifiant invalide ou répété : {name}")
        seen.add(name)
        first, last = int(row["debut"]), int(row["fin"])
        if first != expected_start or last < first:
            raise ValueError(f"Rupture ou chevauchement avant {name} (attendu {expected_start})")
        unknown = set(tokens(row["actifs"])) | {row["lieu"]}
        unknown -= assets
        if unknown:
            raise ValueError(f"Actifs inconnus dans {name} : {sorted(unknown)}")
        expected_start = last + 1
    if not seen:
        raise ValueError("Feuille de plans vide")
    return expected_start - 1


def planifier(rows):
    tasks = {row["tache"]: (int(row["jours"]), tokens(row["parents"])) for row in rows}
    if not tasks or len(tasks) != len(rows):
        raise ValueError("Planning vide ou tâche répétée")
    dates = {}
    pending = set(tasks)
    while pending:
        ready = sorted(name for name in pending if all(parent in dates for parent in tasks[name][1]))
        if not ready:
            raise ValueError(f"Cycle ou parent absent : {sorted(pending)}")
        for name in ready:
            duration, parents = tasks[name]
            if duration <= 0:
                raise ValueError(f"Durée invalide : {name}")
            critical_parent = max(parents, key=lambda p: dates[p]["fin"], default=None)
            start = dates[critical_parent]["fin"] if critical_parent else 0
            dates[name] = {"debut": start, "fin": start + duration, "parent": critical_parent}
        pending.difference_update(ready)
    terminal = max(dates, key=lambda name: dates[name]["fin"])
    delay = dates[terminal]["fin"]
    critical = []
    while terminal:
        critical.append(terminal)
        terminal = dates[terminal]["parent"]
    return {"charge": sum(duration for duration, _ in tasks.values()),
            "delai": delay, "chemin": list(reversed(critical)), "dates": dates}


def verifier_png(path, dimensions):
    with path.open("rb") as stream:
        header = stream.read(24)
    if len(header) != 24 or header[:8] != b"\x89PNG\r\n\x1a\n" or header[12:16] != b"IHDR":
        raise ValueError(f"PNG invalide : {path.name}")
    if struct.unpack(">II", header[16:24]) != dimensions:
        raise ValueError(f"Dimensions incorrectes : {path.name}")


def valider_lots(rows, directory, dimensions):
    seen = set()
    for row in rows:
        first, last, count = (int(row[key]) for key in ("debut_local", "fin_locale", "attendue"))
        template = Path(row["sortie"])
        if count <= 0 or last - first + 1 != count:
            raise ValueError(f"Plage incohérente : {row['lot']}")
        for frame in range(first, last + 1):
            name = template.name.replace("####", f"{frame:04d}")
            target = directory / template.with_name(name)
            if target in seen:
                raise ValueError(f"Produit répété : {target}")
            seen.add(target)
            verifier_png(target, dimensions)
    return len(seen)


def timecode_ms(value):
    h, m, s, ms = (int(piece) for piece in re.split("[:,]", value))
    if m >= 60 or s >= 60 or ms >= 1000:
        raise ValueError(f"Timecode invalide : {value}")
    return ((h * 60 + m) * 60 + s) * 1000 + ms


def verifier_srt(text, duration_ms):
    previous = 0
    entries = re.split(r"\n\s*\n", text.strip())
    for index, entry in enumerate(entries, 1):
        lines = entry.splitlines()
        if len(lines) < 3 or lines[0] != str(index):
            raise ValueError(f"Entrée SRT invalide : {index}")
        first, last = map(timecode_ms, lines[1].split(" --> "))
        if not previous <= first < last <= duration_ms:
            raise ValueError(f"Bornes SRT invalides à l’entrée {index}")
        previous = last
    return len(entries)


def verifier_archive(archive):
    with zipfile.ZipFile(archive) as zipped:
        manifest = json.loads(zipped.read("MANIFEST.json"))
        expected = manifest["fichiers"]
        names = zipped.namelist()
        if len(names) != len(set(names)) or set(names) != set(expected) | {"MANIFEST.json"}:
            raise ValueError("Pièces manquantes ou inattendues")
        for name, digest in expected.items():
            member = PurePosixPath(name)
            if member.is_absolute() or ".." in member.parts or "\\" in name or ":" in name:
                raise ValueError(f"Nom d’archive invalide : {name}")
            if hashlib.sha256(zipped.read(name)).hexdigest() != digest:
                raise ValueError(f"Empreinte incorrecte : {name}")
        cues = verifier_srt(zipped.read(manifest["sous_titres"]).decode("utf-8-sig"), manifest["duree_ms"])
        return {"version": manifest["version"], "pieces": len(expected), "sous_titres": cues}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("controle", choices=("plans", "planning", "rendus", "livraison"))
    parser.add_argument("--archive", type=Path, help="Paquet ZIP à vérifier avec le contrôle livraison")
    args = parser.parse_args()
    selection = args.controle
    if args.archive is not None and selection != "livraison":
        parser.error("--archive s’utilise avec le contrôle livraison")
    if selection == "plans":
        assets = {row["item"] for row in read_rows(HERE / "assets_pilote.csv")}
        result = {"images": valider_plans(read_rows(HERE / "plans_pilote.csv"), assets), "fps": 24}
    elif selection == "planning":
        result = planifier(read_rows(HERE / "charges_pilote.csv"))
    elif selection == "rendus":
        result = {"images_valides":valider_lots(read_rows(HERE / "lots_rendu.csv"), HERE, (640, 360))}
    else:
        result = verifier_archive(args.archive or HERE / "livraison_demo.zip")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
