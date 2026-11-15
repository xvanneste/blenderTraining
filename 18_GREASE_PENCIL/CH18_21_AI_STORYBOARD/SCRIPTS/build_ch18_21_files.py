"""
build_ch18_21_files.py — « Storyboard assisté, contrôlé » (CH18.21, phase 18 module G).

  STARTER_FILES/ch18_21_assist_starter.blend
      Décor de dialogue de CH18.11 (A à gauche, B à droite), aucune caméra ; textes :
      SHOTLIST = proposition « faite par une IA » contenant 4 erreurs (code en double, plan qui franchit
      l'axe, durée nulle, durée totale ≠ cible) ; AI_LOG = journal d'usage de l'IA à remplir ;
      shot_prep.py = le script de préparation des plans (copie de SCRIPTS/shot_prep.py).
  COMPLETED_EXAMPLES/ch18_21_assist_solution.blend (+ _contact.png)
      SHOTLIST corrigée, plans générés par shot_prep.py (6 caméras, marqueurs, boards, notes),
      AI_LOG complété (outil, demandes, ce qui a été accepté / refusé / corrigé).
Dépend de : SCRIPTS/build_ch18_11_files.py (décor).
Usage : blender -b --factory-startup --python build_ch18_21_files.py --python-exit-code 1
Testé avec : Blender 5.3.0.
"""
import importlib.util
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bpy  # noqa: E402
import numpy as np  # noqa: E402

CH = L.chapter_dir(__file__)
SRC_SET = os.path.join(os.path.dirname(CH), "CH18_11_CONTINUITY", "SCRIPTS", "build_ch18_11_files.py")
PREP = os.path.join(HERE, "shot_prep.py")

PROPOSAL = """# Proposition IA — séquence « La tasse partagée » — durée cible : 12 s
# code;valeur;sujet;côté;durée_s;note
SQ040_SH0010;PE;A;face;3;Installation : A et B à table, la tasse entre eux
SQ040_SH0020;PRP;B;face;2;B pousse la tasse vers A
SQ040_SH0030;PRP;A;face;2;A hésite
SQ040_SH0030;GP;B;dos;1.5;B sourit, encourageant
SQ040_SH0050;TGP;A;face;0;Les yeux de A se posent sur la tasse
SQ040_SH0060;PM;A;face;2;A prend la tasse
"""
CORRECTED = """# Liste contrôlée — séquence « La tasse partagée » — durée cible : 12 s
# code;valeur;sujet;côté;durée_s;note
SQ040_SH0010;PE;A;face;3;Installation : A et B à table, la tasse entre eux
SQ040_SH0020;PRP;B;face;2;B pousse la tasse vers A
SQ040_SH0030;PRP;A;face;2;A hésite
SQ040_SH0040;GP;B;face;1.5;B sourit, encourageant
SQ040_SH0050;TGP;A;face;1.5;Les yeux de A se posent sur la tasse
SQ040_SH0060;PM;A;face;2;A prend la tasse
"""
LOG_TEMPLATE = """# JOURNAL D'USAGE DE L'IA (à compléter)
# Outil utilisé (nom, version, date) :
# Ce qui a été demandé :
# Proposition ACCEPTÉE telle quelle :
# Proposition REFUSÉE ou CORRIGÉE (et pourquoi) :
# Droits / sources des images de référence éventuelles :
"""
LOG_SOLUTION = """# JOURNAL D'USAGE DE L'IA
Outil : assistant conversationnel (modèle de langage), session du 14/11/2026.
Demande : « propose un découpage de 6 plans, 12 s, dialogue A/B autour d'une tasse ».
Accepté : l'ordre des plans, les valeurs PE → PRP → GP → TGP → PM, les notes d'intention.
Corrigé : code SQ040_SH0030 en double → le 4e plan devient SQ040_SH0040.
Refusé : le plan SH0040 « dos » (caméra de l'autre côté de l'axe A–B, faux raccord) → côté face.
Corrigé : durée 0 s du TGP → 1,5 s ; total 10,5 s → 12 s (cible).
Accepté avec contrôle : script shot_prep.py (écrit avec l'IA), vérifié par validate_ch18_21.py.
Droits : aucune image générée ni importée ; tous les dessins sont de ma main.
"""
NOTE = """CH18.21 — STORYBOARD ASSISTÉ, CONTRÔLÉ
Le texte SHOTLIST est une proposition « faite par une IA ». Elle contient des ERREURS.
1. Relisez-la avec les règles des chapitres précédents (codes uniques, règle des 180° : A à gauche,
   B à droite, toutes les caméras côté « face » ; durées > 0 ; total = durée cible de l'en-tête).
2. Corrigez SHOTLIST directement dans le Text Editor.
3. Lancez le script : Text Editor > shot_prep.py > Run Script (enregistrez d'abord votre fichier dans
   STARTER_FILES : le script y retrouve les outils de l'académie). Il crée caméras, marqueurs, boards.
4. Vérifiez les plans en vue caméra (flèches haut/bas = marqueurs). Dessinez vos boards si vous voulez.
5. Complétez AI_LOG : outil, demande, ce que vous avez ACCEPTÉ, REFUSÉ ou CORRIGÉ et pourquoi.
Vérification : SCRIPTS/validate_ch18_21.py -- --exercise assist
"""


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def build(sol):
    sc = load(SRC_SET, "b1811").scene(False)
    sc.name = "SC_Assist"
    sc.render.fps = 24
    sc.frame_start, sc.frame_end = 1, 288
    L.instructions(CORRECTED if sol else PROPOSAL, "SHOTLIST")
    L.instructions(LOG_SOLUTION if sol else LOG_TEMPLATE, "AI_LOG")
    t = L.instructions(open(PREP, encoding="utf-8").read(), "shot_prep.py")
    t.use_module = False
    if sol:
        load(PREP, "shot_prep").build(sc)
    L.instructions(NOTE)
    return sc


def contact(sc, out):
    sc.render.resolution_percentage = 25
    W, H = sc.render.resolution_x // 4, sc.render.resolution_y // 4
    mks = sorted(sc.timeline_markers, key=lambda m: m.frame)
    sheet = np.zeros((2 * H, 3 * W, 4), dtype=np.float32)
    for i, m in enumerate(mks[:6]):
        sc.frame_set(m.frame)
        sc.camera = m.camera
        p = os.path.join(bpy.app.tempdir, f"assist_{i}.png")
        sc.render.filepath = p
        bpy.ops.render.render(write_still=True)
        im = bpy.data.images.load(p)
        sheet[(1 - i // 3) * H:(2 - i // 3) * H, (i % 3) * W:(i % 3 + 1) * W] = np.array(im.pixels[:], dtype=np.float32).reshape(H, W, 4)
        bpy.data.images.remove(im)
    img = bpy.data.images.new("assist_contact", 3 * W, 2 * H)
    img.pixels = sheet.ravel()
    img.filepath_raw = out
    img.file_format = "PNG"
    img.save()


def main():
    out = os.path.join(CH, "COMPLETED_EXAMPLES")
    build(False)
    L.save(os.path.join(CH, "STARTER_FILES", "ch18_21_assist_starter.blend"))
    sc = build(True)
    L.save(os.path.join(out, "ch18_21_assist_solution.blend"))
    contact(sc, os.path.join(out, "ch18_21_assist_contact.png"))


if __name__ == "__main__":
    L.run(main)
