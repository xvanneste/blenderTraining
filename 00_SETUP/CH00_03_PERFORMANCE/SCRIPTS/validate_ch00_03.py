"""
validate_ch00_03.py — Correcteur de l'exercice « optimiser la scène lourde » (CH00.03).

Usage :
  blender -b --factory-startup <fichier.blend> --python-exit-code 1 --python validate_ch00_03.py -- --exercise optimize [--render]
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


def enabled_objects(layer_collection):
    if layer_collection.exclude or layer_collection.collection.hide_render:
        return set()
    enabled = {obj for obj in layer_collection.collection.objects if not obj.hide_render}
    for child in layer_collection.children:
        enabled.update(enabled_objects(child))
    return enabled


def main():
    r = L.Report("CH00.03 — Optimiser la scène lourde")
    pebbles = [o for o in bpy.context.scene.objects if o.type == "MESH" and o.name.startswith("GEO_Pebble_")]
    enabled = enabled_objects(bpy.context.view_layer.layer_collection)
    r.check(len(pebbles) == 200 and all(obj in enabled for obj in pebbles),
            f"200 galets présents et activés pour le rendu ({sum(obj in enabled for obj in pebbles)})",
            "Gardez chaque galet et activez son rendu ainsi que celui de sa collection.", 2)
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
