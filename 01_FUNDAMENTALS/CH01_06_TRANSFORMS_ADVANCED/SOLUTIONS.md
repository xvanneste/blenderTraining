# CH01.06 — Solutions

<!-- QUIZ_ANSWERS_START -->
## Réponses du quiz

| Q | Réponse | Explication |
|---|---|---|
| Q1 | — | Scale est un multiplicateur appliqué à l'objet ; Dimensions est la taille réelle résultante en mètres. |
| Q2 | **b** — (1, 1, 1) | La transformation est cuite dans les sommets ; l'échelle revient à 1. |
| Q3 | — | Bevel, Solidify, textures procédurales, simulations (tissu, rigid body), rigging, export. |
| Q4 | — | Parce qu'on perd l'orientation locale de l'objet (axes locaux) ; un objet orienté ou animé doit garder sa rotation. |
| Q5 | **b** — Local | Local. |
| Q6 | — | La virgule (,). |
| Q7 | — | Normal. |
| Q8 | **a** — Shift+Tab | Shift+Tab (Ctrl+Shift+Tab : panneau de réglages). |
| Q9 | — | Maintenir Ctrl pendant la transformation. |
| Q10 | — | Snap Base : passer de Center à Closest. |
<!-- QUIZ_ANSWERS_END -->

## Leçon 1 moyen
Après *Apply Rotation*, *Rotation* = 0 et l'axe local X de la planche redevient parallèle au
X global : `G X X` déplacerait alors le long du X global. Il faut donc appliquer la rotation
**après** les opérations qui utilisent l'axe local — ou ne pas l'appliquer du tout (on
n'applique pas les rotations d'objets animés ou orientés volontairement).

## Exercice 3 — valeurs de référence
| Objet | Résultat |
|---|---|
| GEO_Crate | Scale (1, 1, 1), Dimensions (2, 1, 0,5) |
| GEO_Book | Location Z = 0,82 (dessous à 0,80) |
| GEO_Shelf | Location Y = 1,85 (dos à 2,00) ; X = −1,5 ; Z = 1,2 |
| GEO_Plank | Location = (3 + cos 30°, sin 30°, 0,05) = (3,866 ; 0,5 ; 0,05) |
Fichier : `COMPLETED_EXAMPLES/ch01_06_moving_solution.blend`.
