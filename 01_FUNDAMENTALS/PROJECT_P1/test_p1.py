"""Vérifie le corrigé et deux variantes fautives du projet P1 dans Blender 5.3."""
from pathlib import Path
import shutil
import subprocess
import tempfile


PROJECT = Path(__file__).resolve().parent
BLENDER = r"C:\Program Files\Blender Foundation\Blender 5.3\blender.exe"
REFERENCE = PROJECT / "REFERENCE"
BLEND_FILE = "p1_nature_morte_reference.blend"


def blender(blend, *args):
    return subprocess.run(
        [BLENDER, "-b", "--factory-startup", str(blend), "--python-exit-code", "1", *args],
        capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=60,
    )


def validate(blend):
    return blender(blend, "--python", str(PROJECT / "validate_p1.py"))


def main():
    result = validate(REFERENCE / BLEND_FILE)
    assert result.returncode == 0 and "RÉSULTAT : VALIDÉ" in result.stdout, result.stdout + result.stderr
    print("[PASS] Référence acceptée.")

    cases = (
        ("partagent un maillage", "apple = bpy.data.objects['GEO_Apple_2']; apple.data = apple.data.copy()"),
        ("multi-matériaux", "book = bpy.data.objects['GEO_Book_3']\n"
         "for face in book.data.polygons:\n    face.material_index = 0"),
    )
    for expected, change in cases:
        with tempfile.TemporaryDirectory(prefix="bcma_p1_") as directory:
            copy = Path(directory) / "reference"
            shutil.copytree(REFERENCE, copy)
            blend = copy / BLEND_FILE
            expression = (
                f"import bpy\n{change}\nbpy.context.preferences.filepaths.save_version = 0\n"
                "bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath)"
            )
            result = blender(blend, "--python-expr", expression)
            result.check_returncode()
            result = validate(blend)
            failures = [line for line in result.stdout.splitlines() if line.strip().startswith("✘")]
            assert result.returncode == 1 and len(failures) == 1 and expected in failures[0], result.stdout + result.stderr
            print(f"[PASS] Variante refusée par le contrôle {expected}.")


if __name__ == "__main__":
    main()
