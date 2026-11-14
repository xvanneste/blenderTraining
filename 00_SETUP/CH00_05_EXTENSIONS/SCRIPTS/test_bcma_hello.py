"""
test_bcma_hello.py — Teste l'extension d'exemple ASSETS/bcma_hello sans l'installer.

Importe le module, appelle register(), crée des objets, exécute l'opérateur
bcma.prefix_names, vérifie les noms, puis unregister(). Aucune préférence n'est modifiée.
Usage : blender -b --factory-startup --python test_bcma_hello.py --python-exit-code 1
Testé avec : Blender 5.3.0.
"""
import importlib.util
import os
import sys

import bpy

HERE = os.path.dirname(os.path.abspath(__file__))
PKG = os.path.join(HERE, "..", "ASSETS", "bcma_hello", "__init__.py")


def main():
    spec = importlib.util.spec_from_file_location("bcma_hello", PKG)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    mod.register()
    try:
        assert hasattr(bpy.types, "BCMA_PT_hello"), "panneau non enregistré"
        bpy.ops.wm.read_factory_settings(use_empty=False)
        mod.register() if not hasattr(bpy.types, "BCMA_PT_hello") else None
        for o in bpy.context.scene.objects:
            o.select_set(True)
        with bpy.context.temp_override(selected_objects=list(bpy.context.scene.objects)):
            res = bpy.ops.bcma.prefix_names()
        names = sorted(o.name for o in bpy.context.scene.objects)
        print("[BCMA] résultat :", res, names)
        assert names == ["CAM_Camera", "GEO_Cube", "LGT_Light"], names
        print("[BCMA] extension bcma_hello : OK")
        return 0
    finally:
        try:
            mod.unregister()
        except Exception:
            pass


if __name__ == "__main__":
    try:
        code = main()
    except Exception:
        import traceback
        traceback.print_exc()
        code = 1
    sys.exit(code)
