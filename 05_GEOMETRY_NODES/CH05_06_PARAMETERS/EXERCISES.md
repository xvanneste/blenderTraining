# CH05.06 — Exercices

## Exercice 1 — Facile : concevoir ⏱ 15 min
Pour un outil « escalier », listez cinq entrées avec type, défaut et bornes (par exemple Steps Integer 12, 2–60 ; Step Height Float 0,18, 0,1–0,3). Aucune réponse unique : vérifiez la cohérence des bornes.

## Exercice 2 — Moyen : l'outil ⏱ 2 h 30
Partez du starter et créez l'interface, les panneaux et les branchements. Validation : `--exercise parameters --render`.

## Exercice 3 — Difficile : un cinquième paramètre ⏱ 2 h
Ajoutez Seed (Integer) qui randomise légèrement la hauteur de chaque pilier (Random Value de 0,9 à 1,1 × Height, seed = Seed). Le correcteur d'origine doit rester vert (désactivez la variation par défaut : Variation = 0).

### Grille d'auto-évaluation (sur 10)
| Critère | 0 | 1 | 2 |
|---|---|---|---|
| Entrées typées avec défauts, bornes et descriptions | non | partiel | oui |
| Panneaux « Dimensions » et « Layout » | non | partiel | oui |
| Toutes les entrées branchées | non | partiel | oui |
| La géométrie suit les paramètres (réglage B) | non | partiel | oui |
| Rendu des deux réglages regardé | non | partiel | oui |
**≥ 7/10** : acquis.

## Défis
- **Défi 1 :** ajoutez une entrée Material (objet matériau) pour choisir le matériau.
- **Défi 2 :** ajoutez un Bool « Realize » qui réalise les instances.

## Mini-projet
Un outil paramétrable pour votre décor (clôture, escalier, rangée d'arbres) avec une fiche d'utilisation.
