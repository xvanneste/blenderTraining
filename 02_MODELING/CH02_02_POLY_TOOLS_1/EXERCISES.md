# CH02.02 — Exercices

## Exercice 1 — Facile : gammes d'outils ⏱ 15 min
Sur un cube : (a) 3 Loop Cuts verticales ; (b) Inset *Individual* sur les 4 faces latérales puis
`E` −5 cm (4 « fenêtres ») ; (c) Bevel 3 segments sur les 4 arêtes verticales. Notez les réglages
utilisés dans le panneau de l'opération.

## Exercice 2 — Moyen : l'étagère ⏱ 30 min
Une étagère murale 80 × 25 × 120 cm : un pavé, Loop Cuts horizontales pour 4 niveaux, Inset +
Extrude vers l'intérieur pour creuser les 4 casiers (profondeur 23 cm), Bevel de 5 mm sur les arêtes
de façade. Dimensions vérifiées dans `N` → Item.

## Exercice 3 — Difficile : le tabouret (SANS procédure) ⏱ 30 min
Reprenez le starter et modélisez le tabouret complet : 4 pieds au sol, au moins 2 traverses,
chanfrein de l'assise, dessus creusé, maillage fermé en quads.
Validation : `--exercise stool --render`.

### Grille d'auto-évaluation (sur 20)
| Critère | 0 | 1 | 2 |
|---|---|---|---|
| Dimensions réelles respectées | non | approx. | oui |
| Pieds réguliers, au sol | non | partiel | oui |
| Traverses droites (pas de vrille) | non | partiel | oui |
| Chanfrein régulier | non | irrégulier | oui |
| Creux du dessus propre | non | partiel | oui |
| Quads, pas de n-gon inutile | non | quelques | oui |
| Aucune arête non-manifold | non | — | oui |
| Méthode du gros au fin respectée | non | partiel | oui |
| Panneau de l'opération utilisé (valeurs chiffrées) | non | parfois | toujours |
| Temps < 30 min | > 50 | 30–50 | < 30 |
**≥ 14/20** : acquis.

## Défis
- **Défi 1 :** un tabouret de bar (pieds plus longs, repose-pieds circulaire) — même méthode.
- **Défi 2 :** traverses arrondies : Bridge Edge Loops avec *Number of Cuts* 4 et
  *Interpolation* *Blend Path* entre deux pieds non alignés.

## Mini-projet — Trois props de la pièce ⏱ 1 h 30
Modélisez une table basse, une caisse en bois et une lampe de bureau simple avec uniquement les
outils du chapitre, en dimensions réelles, nommés `GEO_*`, dans une collection `PROPS`. Ils
serviront au projet P2. Appliquez votre checklist de CH02.01.
