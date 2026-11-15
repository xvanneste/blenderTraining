# CH18.14 — Solutions

<!-- QUIZ_ANSWERS_START -->
## Réponses du quiz

| Q | Réponse | Explication |
|---|---|---|
| Q1 | **c** — 36 | 1,5 × 24 = 36. |
| Q2 | — | 73 (72 images de 1 à 72). |
| Q3 | — | C'est le premier film complet : on y juge rythme, clarté et durée quand un changement coûte encore peu. |
| Q4 | **b** — Shift+I | Insert Blank Keyframe (Active Layer). |
| Q5 | — | Jusqu'à l'image clé suivante du même calque. |
| Q6 | **a** — F2 | Rename Marker. |
| Q7 | — | Output Properties > Metadata (Marker, Frame) + Burn Into Image. |
| Q8 | **b** — Bind Camera to Markers | Marker > Bind Camera to Markers (Ctrl+B). |
| Q9 | — | Resserrer le cadre : rapprocher la caméra ou allonger la focale jusqu'à couper à la poitrine. |
| Q10 | — | Pour lire ensemble liste de plans, timeline et Outliner, et permettre une vérification automatique. |
<!-- QUIZ_ANSWERS_END -->

## Exercice 1
| Plan | Durée | Images | Début | Fin |
|---|---|---|---|---|
| SH0010 | 3 s | 72 | 1 | 72 |
| SH0020 | 1,5 s | 36 | 73 | 108 |
| SH0030 | 1 s | 24 | 109 | 132 |
| SH0040 | 0,8 s | 19 | 133 | 151 |
| SH0050 | 0,5 s | 12 | 152 | 163 |
| SH0060 | 1 s | 24 | 164 | 187 |
| SH0070 | 0,7 s | 17 | 188 | 204 |
| SH0080 | 1 s | 24 | 205 | 228 |
| SH0090 | 2 s | 48 | 229 | 276 |
| SH0100 | 2 s | 48 | 277 | 324 |
| SH0110 | 1,5 s | 36 | 325 | 360 |
| SH0120 | 4 s | 96 | 361 | 456 |

## Exercice 2
`COMPLETED_EXAMPLES/ch18_14_animatic_solution.blend` (+ `_contact.png`) : les 12 cases de la planche
CH18.13 recopiées par script et agrandies au cadre, une clé GP par plan, 12 marqueurs, *End* 456,
Orthographic Scale 10 → 12 entre les images 361 et 456, incrustation Marker + Frame.
Contre-épreuve : marqueur SH0050 décalé d'une image, caméra non animée et fin à 480 → refusé (12/19).

## Exercice 3
`COMPLETED_EXAMPLES/ch18_14_layout_solution.blend` (+ `_contact.png`). Débuts : 1, 73, 121, 169, 217,
253 ; *End* 324. Focales trouvées par le script de construction (valeur mesurée) : PE 33 mm à 14 m,
PM 35 mm à ~4 m, PRP 109 mm à ~2,2 m, GP 114 mm à ~1,2 m, PE 32 mm. Contre-épreuve : focale de
CAM_SH0030 passée à 35 mm et CAM_SH0050 passée en y = +1 → refusé (valeurs 4/6, règle des 180°).
