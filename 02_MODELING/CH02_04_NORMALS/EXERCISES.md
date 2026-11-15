# CH02.04 — Exercices

## Exercice 1 — Facile : la pièce vue de l'intérieur ⏱ 10 min
Un cube de 4 × 4 × 2,5 m sert de pièce ; la caméra sera à l'intérieur. Activez Face Orientation :
vu de l'intérieur, tout est rouge. Utilisez *Recalculate Inside* (`Shift+Ctrl+N`) : les normales
pointent vers l'intérieur de la pièce. Pourquoi est-ce utile avec le *Backface Culling* ?

## Exercice 2 — Moyen : Mark Sharp ⏱ 15 min
Sur un cylindre en Shade Auto Smooth 60°, certaines arêtes restent molles. Sélectionnez les
boucles du haut et du bas, *Edge → Mark Sharp*. Dans le modificateur Smooth by Angle, vérifiez que
*Ignore Sharpness* est décoché : les arêtes marquées restent vives. Cochez-le pour voir la différence ; comparez aussi avec Angle 30°.

## Exercice 3 — Difficile : les ombrages ratés (SANS procédure) ⏱ 15 min
Corrigez les 3 objets du starter. Validation : `--exercise normals --render`.

### Grille d'auto-évaluation (sur 20)
| Critère | 0 | 1 | 2 |
|---|---|---|---|
| Face Orientation utilisée pour diagnostiquer | non | — | oui |
| Toutes les faces orientées vers l'extérieur | non | presque | oui |
| Couvercles plats, flanc lisse | non | un des deux | oui |
| Smooth by Angle laissé modifiable (non appliqué) | non | — | oui |
| Grandes faces planes sur le pavé | non | Weight 50 | Weight ≥ 75 |
| Keep Sharp coché | non | — | oui |
| Weighted Normal en fin de pile | non | — | oui |
| Explication : pourquoi le défaut d'orientation est invisible au rendu | non | floue | claire |
| Rendu comparé avant/après | non | — | oui |
| Temps < 15 min | > 30 | 15–30 | < 15 |
**≥ 14/20** : acquis.

## Défis
- **Défi 1 :** importez un modèle du mini-projet CH02.02 et passez-le à la checklist normales.
- **Défi 2 :** feuillage cartoon — sur une sphère de feuilles, *Mesh → Normals → Point to Target*
  vers le centre : ombrage doux et uniforme (technique « stylisée »).

## Mini-projet — Trois props propres ⏱ 45 min
Reprenez trois props de CH02.02/CH02.03 : orientation vérifiée, Shade Auto Smooth ou Weighted Normal
selon l'objet, rendu de contrôle. Notez dans `PROJECTS/checklist_asset.md` les réglages retenus.
