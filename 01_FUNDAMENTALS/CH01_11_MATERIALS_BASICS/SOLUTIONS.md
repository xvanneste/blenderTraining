# CH01.11 — Solutions

<!-- QUIZ_ANSWERS_START -->
## Réponses du quiz

| Q | Réponse | Explication |
|---|---|---|
| Q1 | **a** — 0 | Non-métal : 0. |
| Q2 | **b** — Parfaitement lisse et réfléchissante | 0 = miroir/verni ; 1 = mat. |
| Q3 | — | Transmission Weight 1, Roughness 0 (IOR ~1,45–1,5). |
| Q4 | — | Emission Color + Emission Strength (5 à 20). |
| Q5 | — | Aucun matériau réel n'absorbe ou ne renvoie 100 % de la lumière : les valeurs extrêmes paraissent artificielles et faussent l'éclairage. |
| Q6 | — | Ajouter un emplacement (+), New (ou choisir le matériau), Edit Mode, sélectionner les faces, Assign. |
| Q7 | — | Le premier emplacement (index 0). |
| Q8 | — | Sélectionner les cibles puis la source (active), Ctrl+L > Link Materials. |
| Q9 | **c** — Material Preview | Material Preview (HDRI de test). |
| Q10 | — | Créer une copie du matériau (bouton copie de la ligne de datablock), la renommer et l'assombrir. |
<!-- QUIZ_ANSWERS_END -->

## Exercice 1 (valeurs de départ)
| Matière | Base Color | Metallic | Roughness | Autre |
|---|---|---|---|---|
| Plastique rouge brillant | (0,7 ; 0,05 ; 0,05) | 0 | 0,15 | |
| Caoutchouc noir | (0,03 ; 0,03 ; 0,03) | 0 | 0,85 | |
| Or | (1 ; 0,77 ; 0,34) | 1 | 0,2 | |
| Verre | blanc | 0 | 0 | Transmission Weight 1 |
| Néon cyan | noir | 0 | 0,5 | Emission cyan, Strength 15 |

## Exercice 2
Sur le cube à modifier : ligne de datablock du matériau → bouton **copie** (nouvel
utilisateur unique `MAT_Wood.001`) → renommer `MAT_Wood_Dark` → assombrir.

## Exercice 3
Fichier : `COMPLETED_EXAMPLES/ch01_11_house_colors_solution.blend` ; rendu de référence
`COMPLETED_EXAMPLES/ch01_11_house_colors_reference.png`. Emplacements de GEO_House : 0
MAT_Wall, 1 MAT_Roof (2 pans), 2 MAT_Door (face de porte).
