# CH09.09 — Cours théorique : Profondeur de champ

## 1. Le plan net
Un seul plan est parfaitement net (Focus Distance). Devant et derrière, le flou croît avec l'écart : c'est le cercle de confusion.

## 2. L'ouverture
F-Stop petit = grande ouverture = flou fort ; F-Stop grand = presque tout net. Mesuré : f/1,0 → pic lointain 0,31 ; f/16 → 0,97.

## 3. Focale et distance
Une focale longue et un sujet proche augmentent le flou (CH09.08). L'exercice fixe 200 mm.

## 4. Activation
Camera > Depth of Field (propriété `use_dof`). Sans elle, aucun effet (mesuré).

## 5. Mesure
Barres émissives fines sur fond noir ; pic = maximum du profil moyenné sur les lignes centrales moins le fond.

## 6. L'exercice
Near à 5 m, Far à 30 m. Solution : DOF activée, Focus Distance 5, F-Stop 1,0.

## 7. Pièges
- F-Stop sans activer la DOF.
- Mise au point sur l'arrière-plan (sujet flou).
- Ouverture trop fermée.
- Mise au point entre les deux : tout est flou.

## 8. Limites
Pas de forme de bokeh (lames), pas de flou en post-production, deux objets seulement ; le moteur de contrôle est Cycles.
