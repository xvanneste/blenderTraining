"""Contre-épreuves reproductibles du protocole de publication."""
import json
import shutil
import sys
import tempfile
from contextlib import contextmanager
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.dont_write_bytecode = True
from publier_lot import publier, verifier_png

SOURCE = HERE.parents[1] / "16_FEATURE_FILMS/ASSETS_ATELIERS/RENDUS_TEST/v001"
IMAGES = ("plan_0001.png", "plan_0025.png")


@contextmanager
def refus(kind, text):
    try:
        yield
    except kind as error:
        assert text in str(error), error
    else:
        raise AssertionError(f"Erreur attendue : {text}")


def complet(directory):
    for name in IMAGES:
        shutil.copy2(SOURCE / name, directory / name)


def incomplet(directory):
    shutil.copy2(SOURCE / IMAGES[0], directory / IMAGES[0])


def corrompu(directory):
    incomplet(directory)
    (directory / IMAGES[1]).write_text("invalide", encoding="utf-8")


def main():
    with tempfile.TemporaryDirectory(prefix="bcma_publish_") as tmp:
        root = Path(tmp)
        old = publier(root, "v001", IMAGES, complet, verifier_png)
        manifest = old / "manifest.json"
        contents = manifest.read_bytes()
        assert set(json.loads(contents)["images"]) == set(IMAGES)
        with refus(FileNotFoundError, IMAGES[1]):
            publier(root, "v002", IMAGES, incomplet, verifier_png)
        with refus(ValueError, "PNG invalide"):
            publier(root, "v002", IMAGES, corrompu, verifier_png)
        lock = root / ".v002.reservation"
        lock.touch()
        with refus(FileExistsError, "réservée"):
            publier(root, "v002", IMAGES, complet, verifier_png)
        lock.unlink()
        assert sorted(path.name for path in root.iterdir()) == ["v001"]
        new = publier(root, "v002", IMAGES, complet, verifier_png)
        assert new.is_dir() and manifest.read_bytes() == contents
        with refus(FileExistsError, "déjà publiée"):
            publier(root, "v001", IMAGES, complet, verifier_png)
        assert not any(root.glob(".*.reservation"))
    print("Publication, refus, réservation et reprise vérifiés")


if __name__ == "__main__":
    main()
