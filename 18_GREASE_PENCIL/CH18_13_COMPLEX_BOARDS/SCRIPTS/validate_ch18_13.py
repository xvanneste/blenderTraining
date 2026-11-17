"""
validate_ch18_13.py — Correcteur « Storyboard d'action et d'émotion » (CH18.13 ; projet n° 1 de la phase 18).
Usage : … --python-exit-code 1 --python validate_ch18_13.py -- --exercise action [--render]
Lecture de la planche par SCRIPTS/bcma_board.py ; vérifie dessin, flèches, notes normées, variété des
valeurs, présence d'insert et de gros plan, rythme (durées).
Testé avec : Blender 5.3.0.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "SCRIPTS"))
import bcma_board as B  # noqa: E402
import bcma_lib as L  # noqa: E402
import bpy  # noqa: E402


def main():
    r = L.Report("CH18.13 — Storyboard d'action et d'émotion (12 cases)")
    info = B.read(bpy.context.scene)
    n = len(info["rects"])
    if not r.check(n == 12, f"Gabarit de 12 cases ({n})", "Repartez du starter.", 1):
        return r.finish()
    pp = info["per_panel"]
    r.check(all(c >= 3 for c in pp), f"Dessin dans les 12 cases (min {min(pp)} traits)", "Remplissez chaque case.", 3)
    r.check(info["arrows"] >= 6, f"{info['arrows']} trait(s) de flèches (≥ 6)", "L'action se lit par les flèches.", 2)
    notes = info["notes"]
    complete = [x for x in notes if x["value"] and x["move"] and x["duration"] is not None]
    r.check(len(complete) >= 12, f"{len(complete)} note(s) complètes (≥ 12)", "Format : SQ020_SH0010 · PE · fixe · 3 s", 3)
    panels = {x["panel"] for x in complete if x["panel"] is not None}
    r.check(len(panels) == 12, f"Une note sous chaque case ({len(panels)}/12)", "Placez chaque note sous sa case.", 2)
    codes = [x["code"] for x in notes]
    r.check(len(codes) == len(set(codes)), "Codes de plans uniques", "", 1)
    vals = {x["value"] for x in complete}
    r.check(len(vals) >= 5, f"{len(vals)} valeurs de plans différentes (≥ 5) : {', '.join(sorted(vals))}", "Variez les valeurs.", 2)
    r.check("INS" in vals and ({"GP", "TGP"} & vals), "Un insert et un gros plan (ou TGP) au moins", "L'objet de l'action et l'émotion.", 2)
    durs = [x["duration"] for x in complete]
    if durs:
        mean, tot = sum(durs) / len(durs), sum(durs)
        r.check(mean <= 2.5, f"Rythme : durée moyenne {mean:.2f} s (≤ 2,5 s pour une action)", "Raccourcissez les plans d'action.", 2)
        r.check(min(durs) <= 1.0 and max(durs) >= 3.0, f"Variation : plan le plus court {min(durs)} s (≤ 1), le plus long {max(durs)} s (≥ 3)",
                "Alternez plans très courts (action) et plans longs (installation, résolution).", 2)
        r.check(10 <= tot <= 40, f"Durée totale {tot:.1f} s (10–40 s)", "", 1)
    r.check(info["header"], "En-tête de page", "Texte « … Page 01 » en haut.", 1)
    if L.flag("--render"):
        lum = L.quick_render(15, 4)
        r.check(lum > 0.05, f"Rendu de contrôle non noir ({lum:.3f})", "", 1)
    return r.finish()


if __name__ == "__main__":
    L.run(main)
