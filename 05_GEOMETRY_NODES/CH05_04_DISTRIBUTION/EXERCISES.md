# CH05.04 — Exercices

## Exercice 1 — Facile : estimer ⏱ 15 min
Un sol de 10 × 10 m, Random, Density 3 par m² : combien de points environ ? Et sur la moitié du sol ? (Réponses : ≈ 300 ; ≈ 150.)

## Exercice 2 — Moyen : le demi-sol boisé ⏱ 2 h
Partez du starter et construisez la distribution. Validation : `--exercise distribution --render`.

## Exercice 3 — Difficile : une clairière ⏱ 2 h
Remplacez le masque par un cercle : aucun arbre à moins de 2 m du centre, arbres au-delà (Density Factor = Greater Than de la distance au centre). Adaptez les mesures du correcteur (au moins 95 % des arbres à plus de 2 m).

### Grille d'auto-évaluation (sur 10)
| Critère | 0 | 1 | 2 |
|---|---|---|---|
| Poisson, distance minimale respectée | non | partiel | oui |
| Masque par un champ | non | partiel | oui |
| Rotation transmise, instances posées | non | partiel | oui |
| Nombre d'arbres plausible (40–400) | non | partiel | oui |
| Rendu regardé, arbre propre | non | partiel | oui |
**≥ 7/10** : acquis.

## Défis
- **Défi 1 :** variez la densité par un Noise (bosquets).
- **Défi 2 :** exposez Seed comme paramètre (préparation de CH05.06).

## Mini-projet
Un semis de pierres ou de buissons sur le terrain de CH05.01.
