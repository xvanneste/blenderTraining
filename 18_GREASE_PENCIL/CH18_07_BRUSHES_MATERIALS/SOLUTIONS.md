# CH18.07 — Solutions

<!-- QUIZ_ANSWERS_START -->
## Réponses du quiz

| Q | Réponse | Explication |
|---|---|---|
| Q1 | — | L'outil définit ce que fait le clic (dessiner, remplir, gommer) ; le pinceau comment le trait est tracé (taille, force, pression, type) ; le matériau de quoi il est fait (couleurs, style). |
| Q2 | **b** — Ink Pen | Ink Pen : trait net à épaisseur variable selon la pression. |
| Q3 | — | Dans l'étagère d'assets en bas du viewport ou le sélecteur de pinceau de l'en-tête : les pinceaux sont des assets. |
| Q4 | **b** — Stroke Mode Fill/Both du pinceau, outil Fill, ou Set Stroke Type | Le remplissage est porté par chaque trait ; le matériau fournit seulement la couleur. |
| Q5 | — | La forme n'est pas fermée : annuler, fermer le trait, tracer un guide (Alt+glisser) ou régler Gap Closure. |
| Q6 | — | À étendre (ou réduire) légèrement l'aplat sous le trait pour éviter les liserés blancs. |
| Q7 | **b** — sous le calque d'encrage | Sous l'encrage, pour que les traits restent visibles par-dessus les couleurs. |
| Q8 | — | Pour pouvoir modifier une couleur partout d'un coup (tout le personnage, tout le film) et garder une palette cohérente. |
| Q9 | **c** — Stroke | Stroke supprime le trait entier ; Point coupe ; Dissolve atténue. |
| Q10 | — | SKETCH (recherche au crayon, pâle et verrouillé) → LINE (encre, formes fermées) → COLOR sous LINE (Fill) → SHADE (ombres). |
<!-- QUIZ_ANSWERS_END -->

## Exercice 2
Modifier la *Base Color* du panneau **Fill** de `MAT_GP_Cloth` met à jour instantanément tous
les traits qui utilisent ce matériau, sur toutes les images : c'est l'intérêt d'une palette par
matériaux plutôt que de couleurs « peintes » une à une.

## Exercice 3
Référence : `COMPLETED_EXAMPLES/ch18_07_brushes_solution.blend` et
`ch18_07_brushes_reference.png`, générée par script :
- bande 1 : traits fins à opacité 0,7 et pression irrégulière (imitation crayon) ; bande 2 :
  pression fin → épais → fin (encre) ; bande 3 : trait large et régulier (marqueur) ;
- 8 matériaux (`MAT_GP_Wall`, `Roof`, `Wood`, `Glass`, `Cup`, `Coffee`, `Fish`, `White`) ;
- 9 aplats **sans contour** (Stroke Mode *Fill*) sur `USER_Fills`, calque placé **sous** le GUIDE :
  l'encrage reste par-dessus les couleurs.
Dans l'interface, vous obtenez le même résultat avec l'outil Fill (Layer Mode : Visible).
