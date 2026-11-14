# CH01.08 — Exercices

## Exercice 1 — Facile : SET et LIGHTS ⏱ 3 min
Rangez le décor dans `SET` et les lumières dans `LIGHTS`.

## Exercice 2 — Moyen : « où est passé le canapé ? » ⏱ 10 min
Un camarade a manipulé votre fichier : le canapé est visible dans la vue mais absent du rendu,
la table est invisible dans la vue mais présente au rendu, le vase ne se sélectionne plus.
Reproduisez ces trois situations avec les interrupteurs, puis remettez tout en ordre en
expliquant chaque icône.

## Exercice 3 — Difficile : le grand rangement (SANS procédure) ⏱ 8 min
Rangement complet en 5 collections, HELPERS désactivée au rendu, abat-jour parenté au pied
sans bouger. Validez (`--exercise organize --render`).
Barème (23 pts) : 5 collections × (1 + 2) · rien en vrac 2 · HELPERS hors rendu 3 · parent 3 ·
abat-jour en place 2 · rendu 1 (+ 1 facultatif : HELPERS visible au viewport).

## Défis
- **Défi 1 :** transformez `PROPS` en **instance** : *Add → Collection Instance → PROPS*,
  déplacez l'instance : un deuxième salon apparaît pour presque rien (CH01.04, CH00.03).
- **Défi 2 :** utilisez la colonne *Holdout* sur une collection et observez le rendu
  (trou transparent — vu en compositing, phase 11).

## Mini-projet — Fichier « propre » ⏱ 20 min
Reprenez votre nature morte (CH01.03) ou votre chambre (CH01.06) : collections conformes,
repères en HELPERS hors rendu, parentages logiques, noms conformes (`bcma_naming_check.py`
sans problème). Grille : structure 40 · visibilités 20 · parentage 20 · contrôle de nommage 20.

## Tests chronométrés
| Test | Cible |
|---|---|
| Ranger 15 objets en 4 collections | 1 min |
| Exclure une collection du rendu | 3 s |
| Parenter puis déparenter en gardant la position | 10 s |
