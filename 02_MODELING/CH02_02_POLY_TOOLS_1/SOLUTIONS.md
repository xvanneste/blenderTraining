# CH02.02 — Solutions

<!-- QUIZ_ANSWERS_START -->
## Réponses du quiz

| Q | Réponse | Explication |
|---|---|---|
| Q1 | **b** — Ctrl+R | Ctrl+R ; molette pour le nombre de coupes. |
| Q2 | — | Clic gauche pour valider la coupe, puis clic droit pour annuler le glissement : elle reste centrée. |
| Q3 | — | Pour créer des boucles intermédiaires qui servent ensuite à brancher des éléments (traverses) ou à plier. |
| Q4 | **b** — Extrude (Faces, Along Normals, Individual, Manifold, Edges, Vertices) | Menu Extrude avec ses variantes. |
| Q5 | — | Il relie deux boucles d'arêtes (ou deux faces) par un tube de faces ; les deux côtés doivent avoir le même nombre de sommets. |
| Q6 | — | Twist, dans le panneau de l'opération Bridge Edge Loops. |
| Q7 | **a** — 1 | 1 segment = chanfrein ; 2–3 = arrondi léger. |
| Q8 | — | Inset (I) avec Depth 0 pour un rebord plat, puis Extrude (E) vers l'intérieur. |
| Q9 | — | Blocking des volumes à l'échelle, découpes (Loop Cut), construction (Extrude, Bridge), puis finitions (Bevel, Inset, détails). |
| Q10 | **b** — Rouvrir le panneau de la dernière opération pour la régler | Adjust Last Operation. |
<!-- QUIZ_ANSWERS_END -->

## Exercice 2
Pavé : `N` → *Dimensions* 0,8 × 0,25 × 1,2. Loop Cut `Ctrl+R` à 3 coupes horizontales (4 niveaux).
Face avant : sélection des 4 faces de façade → `I` avec *Individual* (épaisseur 2 cm) → `E −0.23`.
Bevel des arêtes de façade : `Ctrl+B`, *Width* 0,005. Attention : régler *Dimensions* en Object Mode change l'échelle de l'objet ; appliquez-la (`Ctrl+A` → *Scale*) avant Inset et Bevel, sinon les épaisseurs sont déformées.

## Exercice 3
Référence : `COMPLETED_EXAMPLES/ch02_02_stool_solution.blend` et `ch02_02_stool_reference.png`.
Valeurs de la solution : coupes à ±15 cm (`S X 2.25` après 2 Loop Cuts au tiers), pieds de 5 × 5 cm
extrudés de 0,20 + 0,05 + 0,17 m, 4 traverses dans le tronçon de 5 cm (z 0,17–0,22), bevel 1 cm
2 segments sur le pourtour supérieur, inset 2 cm et creux de 5 mm. Résultat mesuré : 134 faces,
maillage fermé, 100 % quads. Les zones sombres visibles sur le rendu sous l'assise sont les ombres
des pieds (géométrie vérifiée : traverses rectangulaires, normales correctes).
