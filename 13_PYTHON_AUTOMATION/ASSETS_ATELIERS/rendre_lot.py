"""Lance Blender en mode batch pour obtenir deux images PNG d’un .blend."""
import argparse
import subprocess
from pathlib import Path
from tempfile import TemporaryDirectory


def rendre(blender, scene, dossier):
    dossier.mkdir(parents=True, exist_ok=True)
    # Un ancien rendu ne peut pas faire croire à la réussite du nouveau calcul.
    with TemporaryDirectory(prefix="rendu_", dir=dossier) as staging:
        buffer = Path(staging)
        names = []
        for image in (1, 25):
            command = [str(blender), "-b", str(scene), "-o", str(buffer / "plan_####"),
                       "-F", "PNG", "-f", str(image)]
            subprocess.run(command, check=True)
            output = buffer / f"plan_{image:04d}.png"
            with output.open("rb") as handle:
                if handle.read(8) != b"\x89PNG\r\n\x1a\n":
                    raise ValueError(f"PNG invalide : {output}")
            names.append(output)
        for output in names:
            output.replace(dossier / output.name)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    for argument in ("blender", "scene", "dossier"):
        parser.add_argument(argument, type=Path)
    args = parser.parse_args()
    rendre(args.blender.resolve(strict=True), args.scene.resolve(strict=True), args.dossier.resolve())
