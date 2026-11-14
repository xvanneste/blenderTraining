# CH01.03 — Exercices

## Exercice 1 — Facile : sélections imposées ⏱ 5 min
Dans `PEBBLES` : (a) tous ; (b) aucun ; (c) les 10 premiers par motif de nom ; (d) l'inverse
de (c) ; (e) un groupe au lasso. Faites-le deux fois de suite sans hésiter.

## Exercice 2 — Moyen : le rangement ⏱ 10 min
Alignez les 30 cailloux sur une ligne : même Y = 0, même Z = 0,12, X réparti librement.
Indices : sélection multiple, `S Y 0` (échelle 0 sur Y aligne les **positions** des objets
si le point de pivot est *Median Point*… essayez et observez), ou la sidebar avec *Copy to Selected* (clic droit sur le champ).

## Exercice 3 — Difficile : le puzzle (SANS procédure) ⏱ cible 3 min
Rangez les 4 pièces dans leurs silhouettes avec les valeurs du `README_EXERCICE`, puis
validez (`--exercise puzzle`). Barème (17 pts) : 4 × (présence 1 + placement 3) + cailloux 1.

## Défis
- **Défi 1 :** refaites le puzzle uniquement avec les gizmos (outils de la barre `T`) et
  le snapping `Ctrl` : quelle précision obtenez-vous ?
- **Défi 2 :** placez la pièce D en tournant de 45° sur son **axe local** X après sa
  rotation Z : quelle différence avec une rotation globale ?

## Mini-projet — Nature morte de primitives ⏱ 20 min
Composez une nature morte (6–10 primitives : livres = cubes aplatis, tasse = cylindre…)
**uniquement** par saisie numérique, avec au moins une rotation locale. Rendu `F12` sauvé
dans `RENDERS/`. Grille : précision (objets posés, pas d'interpénétration) 40 · composition
30 · nommage 30.

## Tests chronométrés
| Test | Cible |
|---|---|
| Puzzle complet | 3 min |
| Sélection par motif de nom | 10 s |
| Remise à zéro des transformations de 5 objets | 5 s |
