# CH18.11 — Exercices

## Exercice 1 — Facile : relever un découpage ⏱ 20 min
Une minute de dialogue d'un film : pour chaque plan, notez valeur, qui est cadré, côté de l'écran,
direction du regard. Le côté de chaque personnage change-t-il ?

## Exercice 2 — Moyen : la chasse aux faux raccords ⏱ 15 min
Dans une copie de la solution, déplacez `CAM_SH030` de l'autre côté de l'axe (y = +0,95) : lancez le
correcteur, lisez les messages, regardez le plan. Puis inversez la visée de `CAM_SH040` pour mettre B
à gauche. Notez ce que le spectateur comprendrait.

## Exercice 3 — Difficile : le dialogue (SANS procédure) ⏱ 45 min
6 plans, marqueurs liés, 180° respectés, A à gauche et B à droite partout, planche dessinée.
Validation : `--exercise dialogue` et `--exercise board --render`.

### Grille d'auto-évaluation (sur 20)
| Critère | 0 | 1 | 2 |
|---|---|---|---|
| Master clair (lieu + deux personnages) | non | partiel | oui |
| Champ/contrechamp avec amorces | non | sans amorce | oui |
| 180° respectés | non | — | oui |
| Côtés et regards constants | non | — | oui |
| Variété de valeurs | non | partielle | oui |
| Insert utile | non | — | oui |
| Marqueurs nommés et liés | non | partiel | oui |
| Durées cohérentes (≥ 1 s) | non | — | oui |
| Planche lisible (flèches de regard) | non | partielle | oui |
| Temps < 45 min | > 75 | 45–75 | < 45 |
**≥ 14/20** : acquis.

## Défis
- **Défi 1 :** ajoutez un 3ᵉ personnage C : comment placer les caméras quand A regarde C puis B ?
  (Nouvel axe pour chaque paire.)
- **Défi 2 :** raccord mouvement : B lève la tasse dans SH040 (animez-la) et le geste se termine dans
  SH060.

## Mini-projet — La traversée ⏱ 1 h 30
Un personnage traverse le plateau en 4 plans (sort à droite, entre à gauche…) : caméras, marqueurs,
animation simple de déplacement (clés de position), même sens de déplacement à l'écran dans les 4
plans. Rendu en séquence d'images.
