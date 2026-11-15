# CH02.10 — Exercices

## Exercice 1 — Facile : les trois modes ⏱ 15 min
Sur (a) une UV Sphere subdivisée niveau 3, (b) un cube subdivisé niveau 3 appliqué, (c) un mur
plat découpé en 20 × 20 : appliquez le mode de Decimate le plus adapté (Collapse, Un-Subdivide,
Planar). Notez triangles avant/après.

## Exercice 2 — Moyen : la règle de distance ⏱ 15 min
Placez la caméra à 2 m, 8 m, 25 m de la statue. Pour chaque distance, trouvez le Ratio le plus bas
dont le rendu `F12` reste indiscernable de l'original (comparaison A/B dans l'Image Editor). Tracez
un tableau distance → ratio.

## Exercice 3 — Difficile : alléger sans abîmer (SANS procédure) ⏱ 20 min
Statue ≤ 25 % des triangles avec écart < 0,4 %, deux LOD liés (≤ 10 %, ≤ 2 %), import nettoyé.
Validation : `--exercise optim --render`.

### Grille d'auto-évaluation (sur 20)
| Critère | 0 | 1 | 2 |
|---|---|---|---|
| Mesures avant/après notées (triangles) | non | partiel | oui |
| Decimate non destructif | non | — | oui |
| Silhouette conservée | non | — | oui |
| LOD dégressifs | non | un seul | deux |
| LOD en copies liées | non | — | oui |
| Collection LOD | non | — | oui |
| Doublons fusionnés | non | — | oui |
| Éléments isolés supprimés | non | — | oui |
| Référence intacte | non | — | oui |
| Temps < 20 min | > 35 | 20–35 | < 20 |
**≥ 14/20** : acquis.

## Défis
- **Défi 1 :** *Symmetry* du Decimate (axe X) sur la statue : comparez les deux moitiés avec et sans.
- **Défi 2 :** mur de briques importé : *Planar* (Angle Limit 1°) puis comptez les triangles gagnés.

## Mini-projet — Budget de scène ⏱ 1 h
Placez 30 copies liées de la statue en profondeur dans une scène (instances) : LOD0 pour les 3
premières, LOD1 au milieu, LOD2 au fond. Statistics avant/après, temps de rendu comparé (mesuré).
