# CH01.02 — Solutions

<!-- QUIZ_ANSWERS_START -->
## Réponses du quiz

| Q | Réponse | Explication |
|---|---|---|
| Q1 | **c** — Z | Z vers le haut (Z-up). |
| Q2 | **b** — Vert | X rouge, Y vert, Z bleu. |
| Q3 | — | Non, c'est le point de vue qui se déplace autour de la scène. |
| Q4 | — | Shift + clic du milieu glissé (ou Ctrl+Num 2/4/6/8). |
| Q5 | **c** — De dessus | Dessus (Top). |
| Q6 | — | Vers +Y (on se tient du côté -Y). |
| Q7 | — | Pas de déformation de perspective : les parallèles restent parallèles, alignements et mesures précis. |
| Q8 | **b** — Num 5 | Num 5. |
| Q9 | **b** — Num / | Vue locale : Num / (même touche pour sortir). |
| Q10 | — | Clipping Region : n'afficher qu'une région rectangulaire de la scène (Alt+B pour annuler). |
| Q11 | — | Frame Selected (Num .). |
| Q12 | **b** — Aligne la caméra active sur la vue actuelle | Align Active Camera to View. |
| Q13 | — | En vue caméra, chaque navigation déplace la caméra : on dérègle le cadrage du plan. |
| Q14 | — | Orthographic Scale (la distance de la caméra n'a pas d'effet sur la taille). |
<!-- QUIZ_ANSWERS_END -->

## Exercice 2
`GEO_Coin` : posée au sol vers (4,2 ; −3,1). Vue de dessus `Num 7`, zoom vers ce coin, ou
`Shift+B` (zoom sur rectangle). `GEO_Hidden` : derrière le mur à (−5,6 ; 2) : vue de dessus,
`Alt+B` autour, ou vue locale après sélection dans l'Outliner.

## Exercice 3 — valeurs de référence
| Caméra | Position | Rotation (X, Y, Z) | Ortho Scale |
|---|---|---|---|
| CAM_Front | (0, −10, 1,2) | (90°, 0, 0) | 3,2 |
| CAM_Right | (10, 0, 1,2) | (90°, 0, 90°) | 3,2 |
| CAM_Top | (0, 0, 12) | (0, 0, 0) | 3,2 |
Fichier : `COMPLETED_EXAMPLES/ch01_02_museum_solution.blend`. En vue orthographique, la
distance de la caméra n'influence pas la taille de l'objet à l'image : seule
*Orthographic Scale* compte (il faut seulement que la caméra soit hors de l'objet et que
*Clip End* l'atteigne).
