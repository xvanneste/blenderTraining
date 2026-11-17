# CH04.07 — Exercices

## Exercice 1 — Facile : encoder ⏱ 15 min
Quelle couleur (RVB) code une normale (0, 0, 1) ? Et (1, 0, 0) ? (Réponses : (0,5 ; 0,5 ; 1) ; (1 ; 0,5 ; 0,5).)

## Exercice 2 — Moyen : baker le rocher ⏱ 2 h
Partez du starter et suivez les tutoriels. Validation : `--exercise baking --render`.

## Exercice 3 — Difficile : bake d'occlusion ⏱ 2 h
Bakez en plus une carte d'AO (Bake Type Ambient Occlusion) dans une seconde image et multipliez-la avec la couleur de base ; le correcteur doit rester vert.

### Grille d'auto-évaluation (sur 10)
| Critère | 0 | 1 | 2 |
|---|---|---|---|
| Relief présent sur tous les îlots | non | partiel | oui |
| Image en Non-Color | non | partiel | oui |
| Image → Normal Map (Tangent) → Normal | non | partiel | oui |
| HIGH caché au rendu, image empaquetée | non | partiel | oui |
| Rendu regardé, pas de couture visible | non | partiel | oui |
**≥ 7/10** : acquis.

## Défis
- **Défi 1 :** comparez avec LOW_Rock sans normal map : qu'est-ce qui change à la silhouette et à l'ombrage ?
- **Défi 2 :** passez l'image en 1024 × 1024 et mesurez le gain.

## Mini-projet
Baker le détail d'un accessoire sculpté (CH03) vers une version basse définition.
