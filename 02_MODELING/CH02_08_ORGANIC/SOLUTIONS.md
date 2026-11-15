# CH02.08 — Solutions

<!-- QUIZ_ANSWERS_START -->
## Réponses du quiz

| Q | Réponse | Explication |
|---|---|---|
| Q1 | — | Construire rapidement la forme avec des volumes simples pour valider proportions et silhouette avant tout détail. |
| Q2 | **b** — La silhouette et les proportions | Du gros au fin. |
| Q3 | — | Rythme épais/fin, asymétrie maîtrisée, lignes d'action courbes, échelle cohérente (deux parmi ceux-ci). |
| Q4 | — | Pour ne modéliser qu'une moitié symétrique, les sommets du plan de symétrie restant collés au plan (pas de trou au milieu). |
| Q5 | **a** — Shift+Alt+S | Shift+Alt+S arrondit la sélection. |
| Q6 | **b** — O | O (molette pour le rayon pendant la transformation). |
| Q7 | — | Sur un squelette d'arêtes (sommets reliés, sans faces), avec un rayon par sommet. |
| Q8 | **b** — redimensionne le rayon Skin (Skin Resize) | Skin Resize ; en Object Mode, Ctrl+A ouvre Apply. |
| Q9 | — | Subdivision Surface : le Skin produit une cage grossière en quads que la subdivision lisse. |
| Q10 | — | Générer une armature qui suit le squelette, pour un rig rapide (déformer branches, tentacules…). |
<!-- QUIZ_ANSWERS_END -->

## Exercice 1
Proportions de référence (CH18.03) : 7,5 têtes ; bassin à mi-hauteur ; épaules ≈ 2 têtes de
large. Une silhouette réussie se reconnaît en aplat noir sans aucun détail.

## Exercice 2
Ordre conseillé : cube subdivisé → faces du haut `E` + `S` (chapeau) → *To Sphere* sur le chapeau →
faces du bas `E Z` (pied) → Inset des faces sous le chapeau (lamelles) → édition proportionnelle pour
incliner légèrement le chapeau.

## Exercice 3
Référence : `COMPLETED_EXAMPLES/ch02_08_tree_solution.blend`, rendus `ch02_08_tree_reference.png`
et `ch02_08_tree_skeleton.png`. Squelette de 16 sommets (tronc 0 → 0,8 → 1,5 m, 4 branches dont une
flèche centrale, 2 rameaux, 3 racines) ; rayons 18 cm (base) → 2,5 cm (pointes) ; Skin
(*Branch Smoothing* 0,6) puis Subdivision (1 / 2) ; Shade Smooth. Le correcteur vérifie : arêtes sans
faces, embranchements, hauteur, ordre de la pile, rapport des rayons, surface générée fermée.
