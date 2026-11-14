# CH01.13 — Solutions

<!-- QUIZ_ANSWERS_START -->
## Réponses du quiz

| Q | Réponse | Explication |
|---|---|---|
| Q1 | **d** — Sun | Sun. |
| Q2 | — | L'éclairement diminue avec le carré de la distance : deux fois plus loin = quatre fois moins de lumière. |
| Q3 | **b** — Grande | Grande source = ombres douces. |
| Q4 | — | Bougie ~1900–2700 K (chaude) ; ciel bleu ~7000–10000 K (froide). |
| Q5 | — | Une teinte (Tint) qui se combine à la couleur de la température. |
| Q6 | — | Devant elle, selon son axe -Z local (il faut l'orienter vers le sujet). |
| Q7 | — | Lumière principale : donne la forme, la direction et l'ambiance. |
| Q8 | **b** — Derrière le sujet, en hauteur | Contre-jour : détache la silhouette. |
| Q9 | — | 8:1, ambiance contrastée/dramatique. |
| Q10 | — | Une ambiance uniforme aplatit les formes et supprime la direction et le contraste voulus. |
<!-- QUIZ_ANSWERS_END -->

## Exercice 1
Inverse du carré : à 2 m il faut 4 × 100 = **400 W** ; à 4 m, 16 × 100 = **1 600 W**.

## Exercice 3
Fichier : `COMPLETED_EXAMPLES/ch01_13_bust_solution.blend` ; rendu
`COMPLETED_EXAMPLES/ch01_13_bust_reference.png` (luminance moyenne mesurée ≈ 0,31).
| Lumière | Type | Position | Puissance | Taille | Température |
|---|---|---|---|---|---|
| LGT_Key | Area | (−2,2 ; −2,2 ; 2,8) | 450 W | 0,8 m | 4500 K |
| LGT_Fill | Area | (2,5 ; −2 ; 1,6) | 70 W | 2 m | 7000 K |
| LGT_Rim | Spot | (1 ; 2,5 ; 3) | 900 W | — | blanc |
Toutes visent `EMP_Target` (Track To). Ratio key/fill ≈ 6,4 : éclairage naturel à légèrement
contrasté.
