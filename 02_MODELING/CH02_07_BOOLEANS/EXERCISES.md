# CH02.07 — Exercices

## Exercice 1 — Facile : les trois opérations ⏱ 10 min
Un cube et une sphère qui se chevauchent : essayez Difference, Union, Intersect. Puis placez la
sphère pour que sa surface affleure exactement une face du cube : observez les défauts avec le
solver Float, puis Exact.

## Exercice 2 — Moyen : cutters parentés ⏱ 15 min
Parentez tous les cutters de la platine à `GEO_Plate` (`Ctrl+P` → *Object*, CH01.08). Tournez la
platine de 30° : les trous suivent. Pourquoi est-ce indispensable pour une pièce animée ?

## Exercice 3 — Difficile : la platine (SANS procédure) ⏱ 25 min
5 trous traversants, cutters rangés et invisibles au rendu, Boolean puis Bevel, rien d'appliqué.
Validation : `--exercise plate --render`.

### Grille d'auto-évaluation (sur 20)
| Critère | 0 | 1 | 2 |
|---|---|---|---|
| Collection CUTTERS, noms CUT_* | non | partiel | oui |
| Cutters en Wire, invisibles au rendu | non | un des deux | oui |
| Un seul Boolean en mode Collection | non | un par cutter | oui |
| Solver adapté, résultat sans défaut | non | — | oui |
| Bevel après le Boolean | non | — | oui |
| Bords des trous biseautés au rendu | non | — | oui |
| Rien d'appliqué | non | — | oui |
| Cutters modifiables (test de déplacement) | non | — | oui |
| Cotes respectées | non | approx. | oui |
| Temps < 25 min | > 40 | 25–40 | < 25 |
**≥ 14/20** : acquis.

## Défis
- **Défi 1 :** *Array* de cutters (un cylindre + Array 6 × 4) dans la collection CUTTERS : une
  grille de 24 trous avec deux objets seulement.
- **Défi 2 :** Union : soudez un bossage cylindrique sur la platine, puis Bevel : le congé se crée
  à la jonction.

## Mini-projet — La grille d'aération ⏱ 1 h 30
Un panneau 50 × 30 × 2 cm avec 30 fentes (cutter + Array), 4 trous de fixation, un logo en creux
(texte converti en maillage comme cutter). Boolean puis Bevel + Harden Normals. Collection `PROPS`.
