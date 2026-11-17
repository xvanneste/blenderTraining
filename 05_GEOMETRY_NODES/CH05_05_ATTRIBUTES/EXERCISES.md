# CH05.05 — Exercices

## Exercice 1 — Facile : choisir ⏱ 15 min
Domaine et type pour : la hauteur d'un sommet ; le matériau d'une face ; un masque d'érosion par sommet ; la couleur d'un sommet. (Réponses : Point/Float ; Face/Integer ; Point/Float ; Point/Color.)

## Exercice 2 — Moyen : terrain colorié ⏱ 2 h
Partez du starter et réalisez le stockage et la lecture. Validation : `--exercise attributes --render`.

## Exercice 3 — Difficile : la pente ⏱ 2 h
Stockez un second attribut « steep » (1 − Normal.z) et mélangez la couleur de roche dans le shader sur les pentes fortes ; le correcteur doit rester vert.

### Grille d'auto-évaluation (sur 10)
| Critère | 0 | 1 | 2 |
|---|---|---|---|
| Store Named Attribute (Float, Point, nom) | non | partiel | oui |
| Valeur = Position Z après déplacement | non | partiel | oui |
| Nœud Attribute (Geometry) avec le même nom | non | partiel | oui |
| Map Range et Color Ramp réglés | non | partiel | oui |
| Rendu regardé, arbre propre | non | partiel | oui |
**≥ 7/10** : acquis.

## Défis
- **Défi 1 :** stockez la distance au centre et dessinez une zone circulaire.
- **Défi 2 :** lisez l'attribut dans l'arbre avec Named Attribute pour poser des arbres sur les basses altitudes.

## Mini-projet
Un terrain de votre décor colorié par altitude et pente.
