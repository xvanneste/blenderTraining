# CH10.03 — Exercices

## Exercice 1 — Facile : lire un compromis ⏱ 15 min
4 échantillons débruités ou 64 échantillons bruts ? Justifiez par le coût et l'EQM.

## Exercice 2 — Moyen : débruiter ⏱ 2 h
Partez du starter. Validation : `--exercise denoising`.

## Exercice 3 — Difficile : passes et préfiltre ⏱ 4 h
Comparez RGB, Albedo, Albedo+Normal avec Fast et Accurate : tableau d'EQM ; sur une scène avec un motif plus fin, un avantage apparaît-il ?

### Grille d'auto-évaluation (sur 10)
| Critère | 0 | 1 | 2 |
|---|---|---|---|
| Débruitage activé | non | partiel | oui |
| Préfiltre | non | partiel | oui |
| EQM | non | partiel | oui |
| Contraste conservé | non | partiel | oui |
| Budget respecté | non | partiel | oui |
**≥ 7/10** : acquis.

## Défis
- **Défi 1 :** trouvez le nombre d'échantillons minimal qui passe EQM ≤ 0,065.
- **Défi 2 :** testez le débruitage sur une animation de 10 images et cherchez le scintillement.

## Mini-projet
Un tableau EQM / temps pour 1, 2, 4, 8, 16, 64 échantillons avec et sans débruitage.
