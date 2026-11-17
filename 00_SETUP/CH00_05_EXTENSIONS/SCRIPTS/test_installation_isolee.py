"""Installe le paquet d’exercice dans un profil sans dépôt ni préférence utilisateur."""
import os
import subprocess
import tempfile
from pathlib import Path

import bpy

PACKAGE = Path(__file__).resolve().parent.parent / "ASSETS/bcma_hello-1.0.0.zip"


def main():
    with tempfile.TemporaryDirectory(prefix="bcma_extension_locale_") as directory:
        env = dict(os.environ, BLENDER_USER_RESOURCES=directory)
        blender = bpy.app.binary_path
        subprocess.run([blender, "--command", "extension", "install-file",
                        "-r", "user_default", "-e", str(PACKAGE)], env=env, check=True)
        proof = (
            "import bpy; assert not bpy.app.online_access; "
            "assert hasattr(bpy.types, 'BCMA_PT_hello'); "
            "[obj.select_set(True) for obj in bpy.context.scene.objects]; "
            "assert bpy.ops.bcma.prefix_names() == {'FINISHED'}; "
            "assert sorted(bpy.context.scene.objects.keys()) == ['CAM_Camera', 'GEO_Cube', 'LGT_Light']; "
            "addon = next(a.module for a in bpy.context.preferences.addons if a.module.endswith('.bcma_hello')); "
            "assert bpy.ops.preferences.addon_disable(module=addon) == {'FINISHED'}; "
            "assert not hasattr(bpy.types, 'BCMA_PT_hello')"
        )
        subprocess.run([blender, "-b", "--python-exit-code", "1", "--python-expr", proof], env=env, check=True)


if __name__ == "__main__":
    main()
