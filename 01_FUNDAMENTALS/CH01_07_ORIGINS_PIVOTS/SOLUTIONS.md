# CH01.07 — Solutions

<!-- QUIZ_ANSWERS_START -->
## Réponses du quiz

| Q | Réponse | Explication |
|---|---|---|
| Q1 | — | Le point qui représente l'objet : sa Location, et le centre de ses rotations et mises à l'échelle par défaut. |
| Q2 | — | Au sol, entre les pieds. |
| Q3 | **b** — Origin to 3D Cursor | On place d'abord le curseur 3D, puis Origin to 3D Cursor. |
| Q4 | — | L'animation est faite sur la transformation de l'objet (autour de l'origine) : déplacer l'origine fausse toutes les clés. |
| Q5 | **b** — Au curseur 3D | Au curseur 3D. |
| Q6 | — | En Edit Mode : Shift+S > Cursor to Selected. |
| Q7 | — | Shift+S > Cursor to World Origin (ou Shift+C). |
| Q8 | **c** — Individual Origins | Individual Origins. |
| Q9 | — | Le point (.). |
| Q10 | — | Curseur au centre de la roue (Shift+S > Cursor to Selected), pivot = 3D Cursor, sélectionner les boulons, R + axe + angle. |
<!-- QUIZ_ANSWERS_END -->

## Exercice 3
Porte : origine en (−0,45 ; 0 ; 0), rotation Z = 90° (ou −90° : les deux sont acceptés).
Boulons : départ à 0°, 120°, 200° → arrivée à 45°, 165°, 245° autour de (2 ; 0), rayon 0,3 m.
Fichier : `COMPLETED_EXAMPLES/ch01_07_door_solution.blend`.

## Exercice 2
Edit Mode → sommet(s) du haut du fil → `Shift+S` *Cursor to Selected* → Object Mode →
*Set Origin → Origin to 3D Cursor* → `R Y 20`.

## Défi 2 (escalier)
Avec le pivot sur *3D Cursor* et le curseur sur l'axe, `Shift+D` puis `R Z 20` (rotation) —
mais `Shift+D` enchaîne un déplacement : validez-le par `Entrée` sans bouger, puis `R Z 20`,
puis `G Z 0.18`. `Shift+R` ne répète que la **dernière** action : il est plus simple d'utiliser
le modificateur Array avec un Empty (CH01.10).
