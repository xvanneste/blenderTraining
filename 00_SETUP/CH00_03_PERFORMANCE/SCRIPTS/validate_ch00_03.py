"""
validate_ch00_03.py — Correcteur de l'exercice « optimiser la scène lourde » (CH00.03).

Usage :
  blender -b --factory-startup <fichier.blend> --python validate_ch00_03.py --python-exit-code 1 -- --exercise optimize [--render]
Testé avec : Blender 5.3.0.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "SCRIPTS"))
sys.path.insert(0, HERE)
import bcma_lib as L  # noqa: E402
import bcma_scene_cost as C  # noqa: E402
import bpy  # noqa: E402


def main():
    r = L.Report("CH00.03 — Optimiser la scène lourde")
    pebbles = [o for o in bpy.context.scene.objects if o.name.startswith("GEO_Pebble_")]
    r.check(len(pebbles) == 200, f"200 galets toujours présents ({len(pebbles)})",
            "Optimiser ne veut pas dire supprimer : gardez les 200 galets.", 2)
    meshes = {o.data.name for o in pebbles}
    r.check(len(meshes) <= 5, f"Maillages partagés ({len(meshes)} maillage(s) distinct(s) ≤ 5)",
            "Sélectionnez tous les galets, puis le galet de référence en dernier (actif), Ctrl+L > Link Object Data.", 3)
    c = C.scene_cost()
    r.check(c["render_faces_est"] < 2_000_000,
            f"Faces estimées au rendu : {c['render_faces_est']:,} < 2 000 000".replace(",", " "),
            "Baissez Levels Render du modificateur Subdivision, ou activez Render > Simplify > Max Subdivision.", 3)
    smooth = all(any(m.type == "SUBSURF" and m.show_render for m in o.modifiers) for o in pebbles)
    r.check(smooth, "Les galets restent lisses (Subdivision active au rendu)",
            "Ne supprimez pas le modificateur : réduisez ses niveaux.", 2)
    r.check(c["render_faces_est"] > 50_000, "Qualité conservée (pas d'optimisation destructrice)",
            "Au moins 1 niveau de subdivision au rendu.", 1)
    if L.flag("--render"):
        lum = L.quick_render(15, 4)
        r.check(lum > 0.02, f"Rendu de contrôle non noir ({lum:.3f})", "", 1)
    return r.finish()


if __name__ == "__main__":
    L.run(main)
