"""
build_ch00_03_files.py — Scène « trop lourde » à optimiser (CH00.03).

  STARTER_FILES/ch00_03_heavy_scene_starter.blend
     Un champ de 200 « galets » : 200 copies INDÉPENDANTES du même maillage (données
     dupliquées), chacune avec une Subdivision Surface de niveau 2 (viewport) et 5 (rendu).
     Estimation au rendu : ~16,4 millions de faces.
  COMPLETED_EXAMPLES/ch00_03_heavy_scene_solution.blend
     Même image : maillage PARTAGÉ (duplications liées), Subdivision 1 / 2, Simplify activé
     comme garde-fou  ; ~0,26 million de faces au rendu (64 fois moins).

Usage : blender -b --factory-startup --python build_ch00_03_files.py --python-exit-code 1
Testé avec : Blender 5.3.0.
"""
import math
import os
import random
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bpy  # noqa: E402

CH = L.chapter_dir(__file__)

NOTE = """CH00.03 — SCÈNE TROP LOURDE
Cette scène rend la même image que la solution, mais elle est ~64 fois plus lourde au rendu (16,4 M de faces contre 0,26 M).
Objectif : estimation de faces au rendu < 2 000 000 et au plus 5 maillages distincts
pour les galets, sans changer l'aspect (forme lisse, même placement).
Outils : Statistiques (barre d'état), Object > Link/Transfer Data > Link Object Data (Ctrl+L),
modificateur Subdivision (Levels Viewport / Render), Render > Simplify.
Vérification : SCRIPTS/validate_ch00_03.py --exercise optimize
"""


def build(optimized):
    L.reset("SC_Pebbles")
    random.seed(7)
    L.studio(subject_height=0.6)
    col = L.collection("PROPS")
    mat = L.material("MAT_Pebble", (0.45, 0.42, 0.38), 0.55)
    src = L.mesh(bpy.ops.mesh.primitive_ico_sphere_add, "GEO_Pebble_000", col, mat,
                 subdivisions=2, radius=0.12, location=(0, 0, 0))
    for p in src.data.polygons:
        p.use_smooth = True
    for i in range(200):
        if i == 0:
            o = src
        else:
            data = src.data if optimized else src.data.copy()
            o = bpy.data.objects.new(f"GEO_Pebble_{i:03d}", data)
            col.objects.link(o)
        a = random.uniform(0, 2 * math.pi)
        r = math.sqrt(random.uniform(0, 1)) * 3.0
        o.location = (r * math.cos(a), r * math.sin(a) - 0.5, 0.05)
        o.rotation_euler = (random.uniform(0, 3), random.uniform(0, 3), random.uniform(0, 3))
        s = random.uniform(0.6, 1.4)
        o.scale = (s * 1.4, s, s * 0.55)
        m = o.modifiers.new("Subdivision", "SUBSURF")
        m.levels = 1 if optimized else 2
        m.render_levels = 2 if optimized else 5
    sc = L.render_defaults("CYCLES", 50, 64, "//renders/pebbles_")
    if optimized:
        sc.render.use_simplify = True
        sc.render.simplify_subdivision = 1
        sc.render.simplify_subdivision_render = 2
    L.instructions(NOTE)


def main():
    build(False)
    L.save(os.path.join(CH, "STARTER_FILES", "ch00_03_heavy_scene_starter.blend"))
    build(True)
    L.save(os.path.join(CH, "COMPLETED_EXAMPLES", "ch00_03_heavy_scene_solution.blend"))


if __name__ == "__main__":
    L.run(main)
