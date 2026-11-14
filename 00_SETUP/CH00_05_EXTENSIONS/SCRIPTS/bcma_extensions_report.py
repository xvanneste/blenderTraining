"""
bcma_extensions_report.py — Inventaire des extensions et add-ons (CH00.05).

Affiche : accès en ligne autorisé ou non, dépôts d'extensions (nom, URL, activé),
add-ons/extensions activés (module, origine : cœur, extension, ancien add-on utilisateur).
Usage : blender -b --python bcma_extensions_report.py
        (sans --factory-startup pour voir VOTRE configuration)
Testé avec : Blender 5.3.0.
"""
import sys

import addon_utils
import bpy


def origin(mod_name):
    if mod_name.startswith("bl_ext."):
        return "extension (" + mod_name.split(".")[1] + ")"
    for m in addon_utils.modules(refresh=False):
        if m.__name__ == mod_name:
            path = getattr(m, "__file__", "") or ""
            return "cœur (addons_core)" if "addons_core" in path else "add-on utilisateur (ancien système)"
    return "inconnu"


def main():
    prefs = bpy.context.preferences
    print("\n====== BCMA — EXTENSIONS ET ADD-ONS ======")
    print(f" Accès en ligne (session) : {'autorisé' if bpy.app.online_access else 'refusé'}")
    print(f" Préférence Allow Online Access : {prefs.system.use_online_access}")
    print(" Dépôts :")
    for r in prefs.extensions.repos:
        print(f"   - {r.name:28s} activé={r.enabled}  {r.remote_url or '(local)'}")
    print(" Activés :")
    for a in sorted(prefs.addons.keys()):
        print(f"   - {a:40s} {origin(a)}")
    print("==========================================\n")
    return 0


if __name__ == "__main__":
    code = main()
    if bpy.app.background:
        sys.exit(code)
