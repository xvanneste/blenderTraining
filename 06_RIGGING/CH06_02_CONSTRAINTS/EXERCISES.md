# CH06.02 — Exercices

## Exercice 1 — Facile : prévoir ⏱ 15 min
Cible à 60° de l'avant, Influence 0,5, limite ± 35° : rotation de la tête ? Et à 90° ? (Réponses : 30° ; 35° (45° plafonnés).)

## Exercice 2 — Moyen : le regard ⏱ 2 h 30
Partez du starter et posez les contraintes. Validation : `--exercise constraints`.

## Exercice 3 — Difficile : le cou ⏱ 2 h
Ajoutez un bone `neck` parent de head qui suit la cible à 20 % avec une limite de ± 20° ; le correcteur d'origine doit rester vert si head reste à ± 35° en local, ou adaptez-le (rotation totale ≈ somme).

### Grille d'auto-évaluation (sur 10)
| Critère | 0 | 1 | 2 |
|---|---|---|---|
| Yeux : Damped Track, axe Y, bonne cible | non | partiel | oui |
| Tête : suivi à 50 % | non | partiel | oui |
| Limite ± 35° en espace Local, après le suivi | non | partiel | oui |
| Erreur de visée ≤ 1° aux trois cibles | non | partiel | oui |
| Croquis comparé, cible déplacée à la main | non | partiel | oui |
**≥ 7/10** : acquis.

## Défis
- **Défi 1 :** ajoutez un clignement (Copy Rotation limité) sur deux bones de paupière.
- **Défi 2 :** tête qui suit aussi en hauteur (limites X).

## Mini-projet
Le regard du personnage de votre court-métrage.
