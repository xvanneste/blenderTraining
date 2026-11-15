# CH02.09 — Solutions

<!-- QUIZ_ANSWERS_START -->
## Réponses du quiz

| Q | Réponse | Explication |
|---|---|---|
| Q1 | — | Son maillage dense et désordonné est inutilisable pour l'animation, les UV et la subdivision ; on reconstruit une cage légère en quads. |
| Q2 | — | Là où la forme plie ou se déforme : articulations, bouche, yeux ; peu ailleurs. |
| Q3 | **b** — Par textures (normal map, baking) ou Multiresolution | Détails fins → textures ou multirésolution. |
| Q4 | — | Sphère de quads (cube subdivisé + To Sphere) mise à l'échelle pour envelopper la forme, puis modificateur Shrinkwrap (Nearest Surface Point) avec la sculpture comme cible. |
| Q5 | — | Les sommets se collent au point le plus proche, sur le « ventre » de la forme : les extrémités ne sont pas couvertes (63 % seulement dans l'essai du chapitre). |
| Q6 | **b** — Garder la cage légèrement au-dessus de la surface | Quelques millimètres évitent que la cage soit cachée dans la sculpture. |
| Q7 | — | Nearest Surface Point, Project, Nearest Vertex, Target Normal Project (deux parmi celles-ci). |
| Q8 | **b** — Face Project | Snap Target for Individual Elements : Face Project (ou Face Nearest). |
| Q9 | — | Sinon les sommets s'aimantent aussi à la cage en cours d'édition au lieu de la sculpture. |
| Q10 | — | Clic : extruder au curseur ; Ctrl+clic : créer une face ; Shift+clic : supprimer. |
<!-- QUIZ_ANSWERS_END -->

## Exercice 1
Monkey : 500 faces ; Subdivision niveau 3 : **31 488 faces** mesurées (et non 32 000 = 500 × 64 : les
triangles de Suzanne donnent 3 quads au premier niveau, pas 4). Une cage de quelques centaines à
milliers de faces suffit dès que les petits détails
(rides, pores) passent dans une *normal map* (phase 4).

## Exercice 3
Référence : `COMPLETED_EXAMPLES/ch02_09_retopo_solution.blend`, rendus `ch02_09_retopo_reference.png`
et `ch02_09_retopo_wire.png`. Cage : cube subdivisé (5 coupes) → To Sphere → mise à l'échelle pour
**envelopper** le rocher → Shrinkwrap *Nearest Surface Point*, offset 5 mm. Mesures du correcteur :
**216 quads**, écart moyen **0,50 cm**, couverture **100 %**. Avec une sphère de 50 cm non mise à
l'échelle, la couverture tombe à **63 %** (essai mesuré lors de la création du chapitre).
