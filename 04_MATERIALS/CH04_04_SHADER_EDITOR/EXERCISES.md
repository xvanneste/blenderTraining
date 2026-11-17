# CH04.04 — Exercices

## Exercice 1 — Facile : lire ⏱ 15 min
Sur le schéma de THEORY.md §3, nommez les trois entrées du Principled BSDF alimentées par le bruit (directement ou non) et dites pourquoi la rouille ne doit pas être métallique.

## Exercice 2 — Moyen : acier rouillé ⏱ 2 h
Partez du starter et construisez le graphe. Validation : `--exercise nodes --render`.

## Exercice 3 — Difficile : variantes ⏱ 2 h
Ajoutez un second masque (autre Noise, échelle différente) qui assombrit la rouille par endroits, sans nœud orphelin et en restant ≤ 18 nœuds ; le correcteur doit rester vert.

### Grille d'auto-évaluation (sur 10)
| Critère | 0 | 1 | 2 |
|---|---|---|---|
| Chaîne Coordinate → Mapping → Noise | non | partiel | oui |
| Rampe resserrée, plaques nettes | non | partiel | oui |
| Couleur, Metallic et Roughness pilotés | non | partiel | oui |
| Aucun nœud orphelin, graphe lisible | non | partiel | oui |
| Rendu regardé (taches lisibles à l'échelle) | non | partiel | oui |
**≥ 7/10** : acquis.

## Défis
- **Défi 1 :** remplacez le Noise par une texture Voronoi pour un aspect « écaillé ».
- **Défi 2 :** ajoutez un Frame étiqueté autour des nœuds de masque.

## Mini-projet
Un matériau usé (métal, bois ou pierre) pour un accessoire de votre court-métrage, avec capture du graphe.
