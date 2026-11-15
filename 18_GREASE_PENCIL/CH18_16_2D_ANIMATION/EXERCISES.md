# CH18.16 — Exercices

## Exercice 1 — Facile : les poses clés ⏱ 30 min
Starter : départ au sommet, 4 contacts écrasés, 3 sommets décroissants, avancée vers la droite ;
types Keyframe/Extreme. Validation : `--exercise keys`.

## Exercice 2 — Moyen : la balle complète ⏱ 2 h
Intervalles « en deux », ralenti aux sommets, étirement/écrasement, volume constant, intervalles en
Breakdown. Validation : `--exercise bounce --render`.

## Exercice 3 — Difficile : trois matières ⏱ 2 h
Dans trois copies du fichier : balle de **bowling** (lourde : 1 seul petit rebond, presque pas
d'écrasement), balle de **ping-pong** (légère : rebonds hauts et nombreux, rapides), **ballon de
baudruche** (flotte : chute lente, rebonds mous et très écrasés). Le correcteur valide la mécanique
générale ; la différence de matière est jugée par la grille.

### Grille d'auto-évaluation (sur 10)
| Critère | 0 | 1 | 2 |
|---|---|---|---|
| Arcs réguliers (onion skin) | non | partiel | oui |
| Ralenti aux sommets lisible | non | partiel | oui |
| Squash & stretch dosés selon l'énergie | non | partiel | oui |
| Volume constant (pas de « gonflement ») | non | partiel | oui |
| Matière reconnaissable (exercice 3) | non | partiel | oui |
**≥ 7/10** : acquis.

## Défis
- **Défi 1 :** la balle rebondit contre un mur puis revient.
- **Défi 2 :** ajoutez une ombre au sol (ellipse sur un calque séparé) qui grossit quand la balle descend.

## Mini-projet
Une balle avec un caractère : elle hésite au bord d'une marche, saute, rebondit et s'arrête en
« regardant » la caméra (étirement anticipé avant le saut). 3 à 5 secondes, en deux.
