# CH04.01 — Exercices

## Exercice 1 — Facile : lire un damier ⏱ 20 min
Sur le starter, décrivez en deux phrases où le damier est étiré et pourquoi (projection plane). Puis comparez avec `ch04_01_chest_reference.png`.

## Exercice 2 — Moyen : UV propres ⏱ 2 h
Partez du starter : seams, Unwrap, Average Islands Scale, Pack Islands. Validation : `--exercise uv --render`.

## Exercice 3 — Difficile : plus de densité sur le couvercle ⏱ 2 h
Donnez au couvercle une densité 2× supérieure à celle du corps (pour une gravure) tout en restant dans [0, 1], sans chevauchement. Le correcteur refusera la densité uniforme : relevez la valeur de
l'écart-type et expliquez pourquoi c'est ici un choix volontaire (c'est l'occasion de comprendre la limite du correcteur).

### Grille d'auto-évaluation (sur 10)
| Critère | 0 | 1 | 2 |
|---|---|---|---|
| Seams sur les arêtes vives, aucune coupure inutile | non | partiel | oui |
| Damier régulier, sans bandes | non | partiel | oui |
| Même densité de texels partout (ou choix justifié) | non | partiel | oui |
| Pas de chevauchement, tout dans [0, 1] | non | partiel | oui |
| Bonne occupation, marges suffisantes | non | partiel | oui |
**≥ 7/10** : acquis.

## Défis
- **Défi 1 :** orientez les îlots pour que les veines d'une texture de bois suivent la longueur du coffre.
- **Défi 2 :** sur un autre objet de CH02 (le tabouret, la lampe…), obtenez les mêmes mesures.

## Mini-projet
Dépliez trois accessoires de votre court-métrage et fournissez pour chacun la disposition UV et la fiche de mesures.
