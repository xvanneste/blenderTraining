# CH02.04 — Solutions

<!-- QUIZ_ANSWERS_START -->
## Réponses du quiz

| Q | Réponse | Explication |
|---|---|---|
| Q1 | — | Un vecteur perpendiculaire à la surface indiquant l'extérieur ; le rendu s'en sert pour calculer la réflexion de la lumière. |
| Q2 | **b** — vue de l'intérieur (normale inversée) | Bleu = extérieur, rouge = intérieur. |
| Q3 | **a** — Shift+N | Shift+N ; Shift+Ctrl+N pour Inside ; Alt+N ouvre le menu Normals. |
| Q4 | — | Elle casse d'autres opérations : Solidify, Weighted Normal, Backface Culling, exports vers moteurs, booléens, simulations. |
| Q5 | — | Par l'opérateur Object → Shade Auto Smooth, qui ajoute un modificateur Smooth by Angle (Geometry Nodes) réglable. |
| Q6 | **b** — Shade Auto Smooth (≈ 30°) | Les arêtes au-delà de l'angle restent vives, le flanc reste lisse. |
| Q7 | — | Edit Mode, sélectionner l'arête, Edge → Mark Sharp (respectée par Smooth by Angle tant que Ignore Sharpness est décoché). |
| Q8 | — | Sur un objet chanfreiné et lissé, il pondère les normales par la surface des faces pour que les grandes faces restent parfaitement planes (plus de dégradés). |
| Q9 | **b** — En dernier | Il doit voir la géométrie finale (après Bevel, Mirror…). |
| Q10 | — | Que l'objet est en Shade Smooth (sinon les normales restent plates par face). |
<!-- QUIZ_ANSWERS_END -->

## Exercice 1
Avec *Recalculate Inside*, les faces « regardent » l'intérieur de la pièce. Avec le *Backface
Culling*, les murs entre la caméra et l'intérieur deviennent transparents vus de l'extérieur : pratique
pour travailler dans une pièce fermée, et indispensable pour certains moteurs temps réel.

## Exercice 3
Référence : `COMPLETED_EXAMPLES/ch02_04_normals_solution.blend`, rendus `ch02_04_normals_starter_view.png`
(avant) et `ch02_04_normals_reference.png` (après).
- GEO_Flipped : *Recalculate Outside* → 0 face tournée vers l'intérieur (le rendu avant/après est
  identique : défaut invisible au rendu, visible avec Face Orientation).
- GEO_Can : *Shade Auto Smooth* 30° (modificateur Smooth by Angle) → couvercles 100 % plats, flanc
  100 % lisse (32 faces).
- GEO_Block : *Weighted Normal* (Face Area, Weight 100, Keep Sharp, Face Influence) → les 6 grandes
  faces parfaitement planes (produit scalaire 1,000 ; 0,876 sans modificateur).
