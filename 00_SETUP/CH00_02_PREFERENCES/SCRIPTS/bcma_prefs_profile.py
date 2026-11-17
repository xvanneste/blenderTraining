"""
bcma_prefs_profile.py — Audit / application du profil de préférences de l'académie (CH00.02).

Modes :
  (défaut) --audit    compare VOS préférences au profil recommandé, affiche les écarts
  --apply             applique le profil à la session courante
  --apply --save      applique ET enregistre les préférences (userpref.blend)
  --strict            code de retour 1 si des écarts « obligatoires » subsistent
  --no-numpad         ajoute « Emulate Numpad » au profil (clavier sans pavé numérique)
  --no-middle-mouse   ajoute « Emulate 3 Button Mouse » (souris sans bouton du milieu / trackpad)

Exemples :
  blender -b --python bcma_prefs_profile.py -- --audit
  blender -b --python bcma_prefs_profile.py -- --apply --save
Dans Blender : Scripting > Open > Run Script (mode audit) ; les messages sont dans la
console système (Window > Toggle System Console).

Sécurité : --save est refusé si Blender a été lancé avec --factory-startup
(on écraserait vos préférences par celles d'usine modifiées).

Testé avec : Blender 5.3.0.
"""
import sys

import bpy

ARGS = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []

# (chemin, propriété, valeur recommandée, obligatoire ?, explication)
PROFILE = [
    ("inputs", "use_rotate_around_active", True, True,
     "Orbit Around Selection : l'orbite tourne autour de ce que vous avez sélectionné"),
    ("inputs", "use_zoom_to_mouse", True, True,
     "Zoom to Mouse Position : le zoom se dirige vers le curseur"),
    ("inputs", "use_mouse_depth_navigate", True, False,
     "Auto Depth : la navigation s'adapte à la profondeur sous la souris"),
    ("inputs", "use_auto_perspective", True, False,
     "Auto Perspective : vues de face/côté en orthographique, orbite en perspective"),
    ("edit", "undo_steps", 64, False,
     "Undo Steps : 64 retours arrière (plus de mémoire utilisée)"),
    ("filepaths", "use_auto_save_temporary_files", True, True,
     "Auto-Save : sauvegarde automatique de secours"),
    ("filepaths", "auto_save_time", 2, False,
     "Auto-Save Timer : toutes les 2 minutes"),
    ("filepaths", "save_version", 2, False,
     "Save Versions : garder .blend1 et .blend2"),
    ("filepaths", "use_relative_paths", True, True,
     "Relative Paths : chemins relatifs par défaut"),
    ("view", "show_statusbar_stats", True, True,
     "Status Bar > Scene Statistics : nombre d'objets, de faces…"),
    ("view", "show_statusbar_memory", True, False,
     "Status Bar > System Memory"),
    ("view", "show_statusbar_vram", True, False,
     "Status Bar > Video Memory"),
    ("view", "show_statusbar_version", True, False,
     "Status Bar > Blender Version"),
]
if "--no-numpad" in ARGS:
    PROFILE.append(("inputs", "use_emulate_numpad", True, True,
                    "Emulate Numpad : les chiffres du clavier remplacent le pavé numérique"))
if "--no-middle-mouse" in ARGS:
    PROFILE.append(("inputs", "use_mouse_emulate_3_button", True, True,
                    "Emulate 3 Button Mouse : Alt + clic gauche remplace le bouton du milieu"))


def section(prefs, name):
    return getattr(prefs, name)


def cycles_device_ok(prefs):
    addon = prefs.addons.get("cycles")
    if addon is None:
        return False, "add-on Cycles absent"
    t = addon.preferences.compute_device_type
    return t != "NONE", f"Cycles Render Devices = {t}"


def audit(prefs):
    diffs = []
    print("\n========== BCMA — AUDIT DES PRÉFÉRENCES ==========")
    for path, prop, value, mandatory, why in PROFILE:
        cur = getattr(section(prefs, path), prop)
        ok = cur == value
        tag = "✔" if ok else ("✘" if mandatory else "–")
        print(f" {tag} {why}\n      actuel : {cur}   recommandé : {value}")
        if not ok:
            diffs.append((path, prop, value, mandatory))
    ok, msg = cycles_device_ok(prefs)
    print(f" {'✔' if ok else '–'} GPU Cycles configuré ({msg})")
    print(f" {'✔' if prefs.use_preferences_save else '–'} Auto-Save Preferences = {prefs.use_preferences_save}")
    mand = [d for d in diffs if d[3]]
    print(f"--------------------------------------------------\n Écarts : {len(diffs)} "
          f"(dont {len(mand)} obligatoire(s))")
    if bpy.app.factory_startup:
        print(" INFO : lancé avec --factory-startup → ce sont les réglages d'usine, pas les vôtres.")
    print("==================================================\n")
    return diffs


def apply(prefs):
    for path, prop, value, mandatory, _ in PROFILE:
        settings = section(prefs, path)
        if settings.is_property_readonly(prop):
            if mandatory and getattr(settings, prop) != value:
                raise RuntimeError(f"Réglage obligatoire en lecture seule : {path}.{prop}")
            print(f"[BCMA] ignoré dans ce contexte (lecture seule) : {path}.{prop}")
            continue
        setattr(settings, prop, value)
        print(f"[BCMA] appliqué : {path}.{prop} = {value}")


def main():
    prefs = bpy.context.preferences
    if "--apply" in ARGS:
        if "--save" in ARGS and bpy.app.factory_startup:
            print("[BCMA] REFUS : --save interdit avec --factory-startup.")
            return 1
        apply(prefs)
        if "--save" in ARGS:
            if bpy.ops.wm.save_userpref() != {"FINISHED"}:
                print("[BCMA] Blender n’a pas enregistré les préférences.")
                return 1
            print("[BCMA] Préférences enregistrées (userpref.blend).")
    diffs = audit(prefs)
    if "--strict" in ARGS and any(d[3] for d in diffs):
        return 1
    return 0


if __name__ == "__main__":
    code = main()
    if bpy.app.background:
        sys.exit(code)
