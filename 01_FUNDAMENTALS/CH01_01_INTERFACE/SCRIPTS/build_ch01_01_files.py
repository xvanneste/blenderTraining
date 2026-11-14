"""
build_ch01_01_files.py — Fichiers du chapitre CH01.01 (interface).

  STARTER_FILES/ch01_01_interface_starter.blend
      Scène par défaut + consignes (Text Editor : README_EXERCICE) + objets à retrouver.
  COMPLETED_EXAMPLES/ch01_01_interface_solution.blend
      Contient un workspace « BCMA_Study » avec 3D Viewport, Outliner, Properties et
      Text Editor (référence de l'exercice 3).
Note technique : en mode arrière-plan, Blender ne permet pas de diviser des zones ; la
solution renomme donc un workspace existant qui possède déjà ces éditeurs. À la main,
l'apprenant construit le sien (voir SOLUTIONS.md).
Usage : blender -b --factory-startup --python build_ch01_01_files.py --python-exit-code 1
Testé avec : Blender 5.3.0.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bpy  # noqa: E402

CH = L.chapter_dir(__file__)
NOTE = """CH01.01 — CHASSE AU TRÉSOR DE L'INTERFACE
Répondez dans vos notes (corrigé : SOLUTIONS.md).
1. Dans quel workspace êtes-vous ? Citez 3 autres workspaces.
2. Combien de zones (areas) compte le workspace Layout ? Nommez chaque éditeur.
3. Ouvrez puis fermez la barre d'outils (T) et la sidebar (N) de la vue 3D.
4. Trouvez l'objet GEO_Clue_A dans l'Outliner : dans quelle collection est-il ?
5. Avec F3, trouvez et lancez « Add Cube ».
6. Maximisez la vue 3D (Ctrl+Space), puis revenez.
7. Changez l'éditeur de la Timeline en Text Editor, puis remettez-le.
8. Quelle est la valeur de la propriété personnalisée « secret » de GEO_Clue_B ?
   (Properties > Object > Custom Properties)
EXERCICE 3 : créez un workspace nommé BCMA_Study contenant au moins :
3D Viewport, Outliner, Properties et Text Editor. Enregistrez en v001.
"""


def build(solution):
    bpy.ops.wm.read_factory_settings(use_empty=False)  # scène et workspaces par défaut
    hunt = L.collection("HUNT")
    a = L.sphere("GEO_Clue_A", hunt, L.material("MAT_Clue", (0.9, 0.6, 0.1)), radius=0.3, location=(3, 2, 0.3))
    b = L.cube("GEO_Clue_B", hunt, size=0.4, location=(-3, 2, 0.2))
    b["secret"] = 42
    L.instructions(NOTE)
    if solution:
        bpy.data.workspaces["Scripting"].name = "BCMA_Study"


def main():
    build(False)
    L.save(os.path.join(CH, "STARTER_FILES", "ch01_01_interface_starter.blend"))
    build(True)
    L.save(os.path.join(CH, "COMPLETED_EXAMPLES", "ch01_01_interface_solution.blend"))


if __name__ == "__main__":
    L.run(main)
