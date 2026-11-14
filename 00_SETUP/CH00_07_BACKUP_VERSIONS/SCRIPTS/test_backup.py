"""
test_backup.py — Test automatique de SCRIPTS/bcma_backup.py (CH00.07).
Crée un faux projet dans un dossier temporaire, lance 3 sauvegardes avec --keep 2,
vérifie : 2 archives restantes, .blend1 et renders/ exclus, archive lisible.
Fonctionne avec le Python système ou dans Blender (-b --python).
Testé avec : Python 3.14 et Blender 5.3.0.
"""
import os
import shutil
import subprocess
import sys
import tempfile
import time
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
TOOL = os.path.join(HERE, "..", "..", "..", "SCRIPTS", "bcma_backup.py")


def main():
    tmp = tempfile.mkdtemp(prefix="bcma_bk_")
    try:
        src = os.path.join(tmp, "film_test")
        os.makedirs(os.path.join(src, "03_shots", "renders"))
        open(os.path.join(src, "a_v001.blend"), "wb").write(b"x" * 1000)
        open(os.path.join(src, "a_v001.blend1"), "wb").write(b"y" * 1000)
        open(os.path.join(src, "03_shots", "renders", "img_0001.png"), "wb").write(b"z" * 1000)
        dest = os.path.join(tmp, "backups")
        py = sys.executable if "python" in os.path.basename(sys.executable).lower() else shutil.which("python")
        for _ in range(3):
            subprocess.run([py, TOOL, "--source", src, "--dest", dest, "--keep", "2"], check=True)
            time.sleep(1.1)
        zips = sorted(os.listdir(dest))
        assert len(zips) == 2, zips
        names = zipfile.ZipFile(os.path.join(dest, zips[-1])).namelist()
        assert any(n.endswith("a_v001.blend") for n in names), names
        assert not any(n.endswith(".blend1") for n in names), names
        assert not any("renders" in n for n in names), names
        print("[BCMA] bcma_backup.py : OK", zips)
        return 0
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
