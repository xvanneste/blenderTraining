"""Publication locale d’un lot déjà planifié. Python 3, sans dépendance."""
import argparse
import hashlib
import json
import os
import re
import subprocess
import tempfile
from pathlib import Path


def publier(destination, version, renders, worker, verify):
    """Publie la version complète. worker écrit dans un emplacement provisoire."""
    if not re.fullmatch(r"v\d{3,}", version):
        raise ValueError(f"Nomenclature de version invalide : {version}")
    names = tuple(renders)
    if (not names or len(set(names)) != len(names)
            or any(not re.fullmatch(r"[A-Za-z0-9_-]+\.png", name) for name in names)):
        raise ValueError("Noms d’images invalides")
    destination.mkdir(parents=True, exist_ok=True)
    target = destination / version
    lock = destination / f".{version}.reservation"
    try:
        fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    except FileExistsError as error:
        raise FileExistsError(f"La publication {version} est réservée") from error
    os.close(fd)
    try:
        if target.exists():
            raise FileExistsError(f"La version {version} est déjà publiée")
        with tempfile.TemporaryDirectory(prefix=f"travail_{version}_", dir=destination) as work:
            candidate = Path(work) / version
            candidate.mkdir()
            worker(candidate)
            hashes = {}
            for name in names:
                image = candidate / name
                verify(image)
                hashes[name] = hashlib.sha256(image.read_bytes()).hexdigest()
            if {artifact.name for artifact in candidate.iterdir()} != set(hashes):
                raise ValueError("Produits inattendus dans le lot")
            (candidate / "manifest.json").write_text(
                json.dumps({"version": version, "images": hashes}, indent=2) + "\n",
                encoding="utf-8",
            )
            candidate.rename(target)
    finally:
        lock.unlink()
    return target


def verifier_png(path):
    with path.open("rb") as image:
        header = image.read(24)
    if len(header) != 24 or header[:8] != b"\x89PNG\r\n\x1a\n" or header[12:16] != b"IHDR":
        raise ValueError(f"PNG invalide : {path.name}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("blender", type=Path)
    ap.add_argument("scene", type=Path)
    ap.add_argument("sortie", type=Path)
    ap.add_argument("version")
    args = ap.parse_args()
    blender = args.blender.resolve(strict=True)
    scene = args.scene.resolve(strict=True)

    def render(directory):
        for frame in (1, 25):
            subprocess.run([str(blender), "-b", str(scene), "-o", str(directory / "plan_####"),
                            "-F", "PNG", "-f", str(frame)], check=True)

    result = publier(args.sortie.resolve(), args.version, ("plan_0001.png", "plan_0025.png"),
                     render, verifier_png)
    print(result)


if __name__ == "__main__":
    main()
