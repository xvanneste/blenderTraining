"""
validate_ch01_13.py — Correcteur de l'éclairage trois points (CH01.13).
Analyse le placement et la puissance des lumières, puis (avec --render) l'exposition de
l'image (luminance moyenne entre 0,08 et 0,6) avec un rendu EEVEE rapide.
Usage : blender -b --factory-startup <fichier.blend> --python-exit-code 1 --python validate_ch01_13.py -- --exercise threepoint [--render]
Testé avec : Blender 5.3.0.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bpy  # noqa: E402

SUBJECT = (0.0, 0.0, 1.4)


def main():
    r = L.Report("CH01.13 — Éclairage trois points")
    lights = [o for o in bpy.context.scene.objects if o.type == "LIGHT" and not o.hide_render]
    r.check(len(lights) >= 3, f"Au moins 3 lumières rendues ({len(lights)})", "Shift+A > Light (Area, Spot, Point).", 2)
    key, fill, rim = L.obj("LGT_Key"), L.obj("LGT_Fill"), L.obj("LGT_Rim")
    r.check(key and fill and rim, "Lumières nommées LGT_Key, LGT_Fill, LGT_Rim", "F2 pour renommer.", 1)
    if key and fill and rim:
        k, f, m = (o.matrix_world.translation for o in (key, fill, rim))
        r.check(k.y < SUBJECT[1] and k.z > SUBJECT[2], "Key devant le sujet et au-dessus de la tête",
                "La key vient du côté de la caméra (y négatif) et d'en haut.", 2)
        r.check(f.y < SUBJECT[1] and (f.x * k.x) < 0, "Fill devant, du côté opposé à la key",
                "Si la key est à gauche (x < 0), la fill est à droite (x > 0).", 2)
        r.check(m.y > SUBJECT[1], "Rim derrière le sujet", "Placez-la derrière (y positif), en hauteur.", 2)
        if key.data.type != "SUN" and fill.data.type != "SUN":
            ratio = key.data.energy / max(fill.data.energy, 1e-6)
            r.check(2 <= ratio <= 8, f"Rapport key/fill = {ratio:.1f} (entre 2 et 8)",
                    "La fill est 2 à 8 fois moins puissante que la key.", 2)
    wo = bpy.context.scene.world
    bg = next((n for n in wo.node_tree.nodes if n.type == "BACKGROUND"), None) if wo else None
    r.check(bg is None or bg.inputs["Strength"].default_value <= 0.3, "Monde resté sombre (Strength ≤ 0,3)",
            "Ne compensez pas avec le monde : éclairez avec les lumières.", 1)
    if L.flag("--render"):
        lum = L.quick_render(20, 16)
        r.check(0.08 <= lum <= 0.6, f"Exposition correcte (luminance moyenne {lum:.3f} entre 0,08 et 0,6)",
                "Trop sombre : augmentez la key ; trop clair : baissez les puissances.", 3)
    return r.finish()


if __name__ == "__main__":
    L.run(main)
