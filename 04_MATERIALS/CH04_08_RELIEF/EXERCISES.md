# CH04.08 — Exercices

## Exercice 1 — Facile : choisir ⏱ 15 min
Pour chaque cas, bump, normal map ou displacement ? Grain de cuir ; rochers vus de profil ; vis d'un modèle de jeu bakées d'un modèle sculpté ; dunes de sable. (Réponses : bump ; displacement ; normal map ; displacement.)

## Exercice 2 — Moyen : le sol ⏱ 2 h
Partez du starter et réalisez le displacement. Validation : `--exercise relief`.

## Exercice 3 — Difficile : deux échelles ⏱ 2 h
Ajoutez un second Noise (échelle plus fine) en bump (nœud Bump → Normal du Principled) et gardez « Displacement and Bump » ; le correcteur doit rester vert.

### Grille d'auto-évaluation (sur 10)
| Critère | 0 | 1 | 2 |
|---|---|---|---|
| Cycles + méthode du matériau correcte | non | partiel | oui |
| Displacement relié, Height pilotée par une texture | non | partiel | oui |
| Scale plausible (quelques cm à 30 cm) | non | partiel | oui |
| Maillage subdivisé | non | partiel | oui |
| Rendu regardé en lumière rasante, silhouette qui ondule | non | partiel | oui |
**≥ 7/10** : acquis.

## Défis
- **Défi 1 :** remplacez le bruit par une Voronoi pour un sol fissuré.
- **Défi 2 :** mesurez le temps de rendu avec 6 niveaux de rendu et avec l'adaptatif.

## Mini-projet
Un sol de terrain ou de pierre pour un décor de votre court-métrage.
