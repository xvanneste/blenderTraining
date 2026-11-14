# CH00.07 — Solutions

<!-- QUIZ_ANSWERS_START -->
## Réponses du quiz

| Q | Réponse | Explication |
|---|---|---|
| Q1 | **b** — File > Recover > Auto Save | Recover > Auto Save liste les sauvegardes automatiques. |
| Q2 | — | File > Recover > Last Session (quit.blend). |
| Q3 | — | L'état du fichier avant le dernier enregistrement (copie automatique, écrasée à chaque Ctrl+S). |
| Q4 | — | Il n'enregistre pas les changements en cours en Sculpt Mode, Texture Paint et Edit Mode. |
| Q5 | — | L'historique d'annulation est en mémoire et disparaît à la fermeture/réouverture. |
| Q6 | **b** — Crée scene_v008.blend | Save Incremental. |
| Q7 | — | Avant une modification risquée, après une étape validée, en fin de séance, avant d'envoyer le fichier. |
| Q8 | — | 3 copies, sur 2 supports différents, dont 1 hors site. |
| Q9 | **b** — Non : une suppression ou un chiffrement se synchronise aussi | Synchronisation ≠ sauvegarde versionnée. |
| Q10 | — | Une restauration réussie (testée). |
| Q11 | **b** — Alembic | Alembic (ou USD). |
| Q12 | **b** — OpenEXR | OpenEXR : virgule flottante, multicouche. |
| Q13 | — | Compression avec perte et 8 bits : artefacts cumulatifs, pas de données au-delà du blanc, pas de transparence. |
| Q14 | — | USD (OpenUSD). |
<!-- QUIZ_ANSWERS_END -->

## Exercice 3
Le `.blend1` à côté du fichier contient l'état **précédent** l'enregistrement fautif.
Copier-renommer le `.blend1` en `ch00_07_hero_scene_v002.blend`, l'ouvrir, enregistrer.
Fichier de référence : `COMPLETED_EXAMPLES/ch00_07_hero_scene_v002.blend`.
Alternative : ajouter le héros depuis le `.blend1` avec *File → Append* (naviguer dans le
`.blend1`, dossier `Object`, `GEO_Hero`) dans le fichier v001, puis `Ctrl+Alt+S`.

## Exercice 4
(a) **FBX** (ou glTF si le moteur le gère) ; (b) **Alembic** (ou USD) : géométrie cuite ;
(c) **OpenEXR** multicouche ; (d) **glTF/GLB** ; (e) **USD** ; (f) **STL** (ou 3MF/OBJ selon
l'imprimante).
