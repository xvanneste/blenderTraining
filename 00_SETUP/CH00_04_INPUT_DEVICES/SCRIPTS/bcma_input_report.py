"""
bcma_input_report.py — Rapport des réglages de périphériques d'entrée (CH00.04).

Affiche, pour chaque catégorie (clavier, souris, trackpad, tablette, NDOF), les réglages
actuels et une recommandation selon votre matériel, déclaré en option :
  --profile mouse3     souris 3 boutons + clavier complet (défaut)
  --profile laptop     trackpad, clavier sans pavé numérique
  --profile tablet     tablette graphique (dessin, sculpture)
Usage : blender -b --python bcma_input_report.py -- --profile laptop
Testé avec : Blender 5.3.0.
"""
import sys

import bpy

ARGS = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
PROFILE = ARGS[ARGS.index("--profile") + 1] if "--profile" in ARGS else "mouse3"

RECO = {
    "mouse3": {"use_emulate_numpad": False, "use_mouse_emulate_3_button": False},
    "laptop": {"use_emulate_numpad": True, "use_mouse_emulate_3_button": True,
               "use_multitouch_gestures": True},
    "tablet": {"use_mouse_emulate_3_button": True, "tablet_api": "AUTOMATIC"},
}
SHOW = ["use_emulate_numpad", "use_mouse_emulate_3_button", "mouse_emulate_3_button_modifier",
        "use_mouse_continuous", "drag_threshold_mouse", "drag_threshold_tablet",
        "use_multitouch_gestures", "touchpad_scroll_direction", "tablet_api",
        "pressure_threshold_max", "pressure_softness", "ndof_navigation_mode",
        "view_zoom_method", "invert_zoom_wheel"]


def main():
    if PROFILE not in RECO:
        print(f"[BCMA] profil inconnu : {PROFILE} (mouse3 | laptop | tablet)")
        return 1
    inp = bpy.context.preferences.inputs
    reco = RECO[PROFILE]
    print(f"\n====== BCMA — PÉRIPHÉRIQUES D'ENTRÉE (profil {PROFILE}) ======")
    for k in SHOW:
        prop = inp.bl_rna.properties[k]
        cur = getattr(inp, k)
        line = f" {prop.name:28s} = {cur}"
        if k in reco:
            line += "   ✔" if cur == reco[k] else f"   → recommandé : {reco[k]}"
        print(line)
    print("============================================================\n")
    return 0


if __name__ == "__main__":
    code = main()
    if bpy.app.background:
        sys.exit(code)
