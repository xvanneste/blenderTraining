"""
build_ch01_09_files.py — La chasse aux propriétés (CH01.09).

  STARTER_FILES/ch01_09_hunt_starter.blend
      Scène de plan « sq010_sh0010 » avec les réglages par défaut à corriger dans
      10 onglets différents de l'éditeur Properties (liste dans README_EXERCICE).
  COMPLETED_EXAMPLES/ch01_09_hunt_solution.blend
      Tous les réglages faits.
Usage : blender -b --factory-startup --python build_ch01_09_files.py --python-exit-code 1
Testé avec : Blender 5.3.0.
"""
import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bpy  # noqa: E402

CH = L.chapter_dir(__file__)
NOTE = """CH01.09 — LA CHASSE AUX PROPRIÉTÉS (une consigne = un onglet de Properties)
 1. Render   : moteur EEVEE, Sampling > Render > Samples = 32.
 2. Output   : résolution 1280 × 720, 100 %, Frame Rate 25 fps, Frame Start 1, End 120.
 3. Scene    : caméra active = CAM_Shot ; Units > Length = Centimeters.
 4. World    : Surface > Color = bleu nuit (0,02 ; 0,03 ; 0,08 environ), Strength 1.
 5. Object   : GEO_Guide en affichage Wire (Viewport Display > Display As) et
               non rendu (Visibility > Renders décoché).
 6. Object   : GEO_Hero : Viewport Display > Name coché.
 7. Data     : CAM_Shot : Focal Length 35 mm.
 8. Data     : LGT_Key : Power 250 W, couleur chaude (R > G > B).
 9. Material : MAT_Hero : Base Color rouge (R ≥ 0,6 ; G et B ≤ 0,2).
10. Scene    : Custom Properties > New : nom « shot », valeur texte « sq010_sh0010 ».
11. MAT_Library_Gold est posé sur GEO_Guide par erreur : protégez-le (Fake User, bouclier)
    PUIS retirez-le de GEO_Guide (Material > slot > bouton −). Il doit survivre à l'enregistrement.
"""


def build(solution):
    L.reset("SC_Shot")
    st = L.studio(subject_height=1.2)
    col = L.collection("PROPS")
    hero = L.mesh(bpy.ops.mesh.primitive_monkey_add, "GEO_Hero", col, L.material("MAT_Hero", (0.8, 0.8, 0.8), 0.5),
                  size=1.2, location=(0, 0, 0.8))
    guide = L.cube("GEO_Guide", L.collection("HELPERS"), size=0.3, location=(1.5, -1, 0.15))
    gold = L.material("MAT_Library_Gold", (1.0, 0.75, 0.3), 0.25, 1.0)
    guide.data.materials.append(gold)
    cam = L.camera("CAM_Shot", L.collection("CAMERAS"), (2.5, -4.5, 1.6), 50, st["target"], make_active=False)
    sc = bpy.context.scene
    sc.camera = st["camera"]
    L.render_defaults("CYCLES", 100, 128)
    if solution:
        sc.render.engine = "BLENDER_EEVEE"
        sc.eevee.taa_render_samples = 32
        sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage = 1280, 720, 100
        sc.render.fps, sc.render.fps_base = 25, 1.0
        sc.frame_start, sc.frame_end = 1, 120
        sc.camera = cam
        sc.unit_settings.length_unit = "CENTIMETERS"
        bg = next(n for n in sc.world.node_tree.nodes if n.type == "BACKGROUND")
        bg.inputs["Color"].default_value = (0.02, 0.03, 0.08, 1)
        bg.inputs["Strength"].default_value = 1.0
        guide.display_type = "WIRE"
        guide.hide_render = True
        hero.show_name = True
        cam.data.lens = 35
        key = bpy.data.objects["LGT_Key"]
        key.data.energy = 250
        key.data.color = (1.0, 0.85, 0.65)
        bsdf = next(n for n in hero.active_material.node_tree.nodes if n.type == "BSDF_PRINCIPLED")
        bsdf.inputs["Base Color"].default_value = (0.8, 0.05, 0.05, 1)
        sc["shot"] = "sq010_sh0010"
        gold.use_fake_user = True
        guide.data.materials.clear()
    L.instructions(NOTE)


def main():
    build(False)
    L.save(os.path.join(CH, "STARTER_FILES", "ch01_09_hunt_starter.blend"))
    build(True)
    L.save(os.path.join(CH, "COMPLETED_EXAMPLES", "ch01_09_hunt_solution.blend"))


if __name__ == "__main__":
    L.run(main)
