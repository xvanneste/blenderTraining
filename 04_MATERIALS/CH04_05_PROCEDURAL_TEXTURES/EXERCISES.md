# CH04.05 — Exercices

## Exercice 1 — Facile : choisir ⏱ 15 min
Pour chaque cas, procédural ou image ? Brique, étiquette de bouteille, marbre, visage tatoué, sable. (Réponses : procédural ; image ; procédural ; image ; procédural.)

## Exercice 2 — Moyen : mur de briques ⏱ 2 h
Partez du starter et construisez le matériau. Validation : `--exercise procedural --render`.

## Exercice 3 — Difficile : variation ⏱ 2 h
Ajoutez un Noise qui assombrit certaines briques (via un Mix sur Color) sans nœud orphelin ; le correcteur doit rester vert (Color de la Brick doit rester relié, directement, à Base Color : cherchez une autre voie, par exemple varier Color1/Color2 ou ajouter une salissure via Roughness).

### Grille d'auto-évaluation (sur 10)
| Critère | 0 | 1 | 2 |
|---|---|---|---|
| Réglages de la Brick plausibles (Scale, joint, Offset) | non | partiel | oui |
| Variation de couleur visible | non | partiel | oui |
| Joint plus clair que les briques | non | partiel | oui |
| Bump piloté par Fac, joints en creux | non | partiel | oui |
| Rendu regardé, aucun nœud orphelin | non | partiel | oui |
**≥ 7/10** : acquis.

## Défis
- **Défi 1 :** un carrelage avec Checker Texture et joints.
- **Défi 2 :** briques de tailles différentes (Brick Width, Row Height).

## Mini-projet
Un mur ou un sol procédural pour un décor de votre court-métrage.
