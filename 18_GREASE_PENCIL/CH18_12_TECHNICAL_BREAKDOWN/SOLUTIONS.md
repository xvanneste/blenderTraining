# CH18.12 — Solutions

<!-- QUIZ_ANSWERS_START -->
## Réponses du quiz

| Q | Réponse | Explication |
|---|---|---|
| Q1 | — | La traduction d'une scène en plans numérotés, avec pour chacun valeur, angle, mouvement, durée, action, dialogue et son. |
| Q2 | **b** — Pour pouvoir insérer des plans (SH0015) sans tout renuméroter | On insère SH0015 entre SH0010 et SH0020. |
| Q3 | — | Projet, séquence, numéro de page, version, date. |
| Q4 | **b** — Le format de l'image finale (16:9, 2,39:1…) | Toutes identiques, au format du film. |
| Q5 | **b** — un mouvement de caméra | Tirets = caméra ; plein = personnage. |
| Q6 | — | Des flèches des coins de la case vers le centre (ou un cadre d'arrivée dessiné dans le cadre de départ). |
| Q7 | — | Environ une seconde : silhouette lisible, composition simple, 3 valeurs. |
| Q8 | — | SQ020_SH0030 · PRT · fixe · 2 s |
| Q9 | **a** — Il est couché (face vers le haut) : le tourner de 90° sur X | R X 90 pour le mettre face à la caméra (−Y). |
| Q10 | — | Une animatique : chaque case devient un plan dans la timeline, avec sa durée et son son. |
<!-- QUIZ_ANSWERS_END -->

## Exercice 1 (exemple)
| Code | Valeur | Angle | Mouvement | Durée | Action |
|---|---|---|---|---|---|
| SQ010_SH0010 | PE | normal | fixe | 3 s | L'entrée, A entre |
| SQ010_SH0020 | PM | normal | panoramique droite | 3 s | A fouille ses poches |
| SQ010_SH0030 | INS | plongée | fixe | 1,5 s | Poches vides |
| SQ010_SH0040 | GP | normal | fixe | 2 s | A s'inquiète |
| SQ010_SH0050 | PRT | normal | travelling avant | 4 s | A soulève le coussin |
| SQ010_SH0060 | INS | plongée | fixe | 2 s | Les clés |

## Exercice 2
Travelling avant : flèches en tirets des coins vers le centre ; arrière : du centre vers les coins ;
panoramique gauche : flèche en tirets au-dessus, pointant à gauche ; suivi : flèche pleine (personnage)
dans la case + flèche en tirets (caméra) au-dessus, même sens.

## Exercice 3
Référence : `COMPLETED_EXAMPLES/ch18_12_board_solution.blend` et `ch18_12_board_reference.png`
(séquence « La tasse » : PE fixe, PM travelling avant, PRP panoramique droite, insert, GP, PE grue
montante ; 6 notes `TXT_SH0010`–`TXT_SH0060`, en-tête `TXT_Header`). Contre-épreuve : une note sans
durée est refusée par le correcteur.
