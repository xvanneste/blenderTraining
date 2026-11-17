"""Vérifie la sauvegarde et la restauration dans un profil Blender temporaire."""
import os
import subprocess
import tempfile
from pathlib import Path

import bpy

SCRIPT = Path(__file__).with_name("bcma_prefs_profile.py")


def main():
    with tempfile.TemporaryDirectory(prefix="bcma_preferences_") as folder:
        env = dict(os.environ, BLENDER_USER_RESOURCES=folder)
        base = [bpy.app.binary_path, "-b", "--python-exit-code", "1"]

        def run(*args):
            result = subprocess.run([*base, *args], env=env,
                                  capture_output=True, text=True, encoding="utf-8", errors="replace")
            if result.returncode:
                print(result.stdout, result.stderr)
            result.check_returncode()

        # Ajouter deux choix personnels avant d’appliquer le profil de référence.
        run("--python-expr", "import bpy; p=bpy.context.preferences; "
            "p.inputs.use_rotate_around_active=False; p.view.ui_scale=1.25; "
            "bpy.ops.wm.save_userpref()")
        preferences_file = Path(folder) / "config/userpref.blend"
        archived = preferences_file.read_bytes()

        run("--python", str(SCRIPT), "--", "--apply", "--save", "--no-numpad", "--strict")
        run("--python", str(SCRIPT), "--", "--audit", "--no-numpad", "--strict")
        assert preferences_file.read_bytes() != archived

        preferences_file.write_bytes(archived)
        run("--python-expr", "import bpy; p=bpy.context.preferences; "
            "assert p.inputs.use_rotate_around_active is False; "
            "assert abs(p.view.ui_scale-1.25) < 0.01")
        print("Profil isolé : audit et restauration vérifiés.")


if __name__ == "__main__":
    main()
