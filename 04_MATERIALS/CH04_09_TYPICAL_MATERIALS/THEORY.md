# CH04.09 — Cours théorique : matériaux types

## 1. Recettes
| Matériau | Idée | Entrées clés |
|---|---|---|
| Bois | veines = bandes distordues, étirées | Wave (Bands, Distortion 4, Detail 3), Mapping Scale (1 ; 1 ; 0,15), Color Ramp brune → Base Color ; Roughness 0,45 |
| Pierre | cellules irrégulières + micro-relief | Voronoi [Distance] → Color Ramp grise → Base Color ; Noise (Scale 18) → Bump → Normal ; Roughness 0,85 |
| Plastique | diélectrique saturé et verni | Base Color (0,80 ; 0,05 ; 0,04), Roughness 0,3, Coat Weight 0,5 |
| Verre | transmission pure | Transmission Weight 1, Roughness 0,02, IOR 1,5 |
| Acier brossé | métal + rayures | Metallic 1, Base Color (0,75 ; 0,76 ; 0,78), Anisotropic 0,6, Noise étiré (Mapping Scale (1 ; 60 ; 1)) → Map Range (0,2–0,45) → Roughness |

## 2. Principes communs
- Toujours **une variation** : une texture (couleur, rugosité ou relief) casse l'aspect de « plastique uniforme ».
- Les valeurs PBR de CH04.03 restent la base (diélectriques non métalliques, métaux clairs).
- Des matériaux **paramétrables** (échelle, couleur) se réutilisent ; des groupes de nœuds les rendent propres (CH04.04).

## 3. Publier dans l'Asset Browser
Opérateur **Mark as Asset** (`asset.mark`, libellé vérifié) sur le matériau (Outliner en mode Blender File, ou clic droit sur le matériau). Un asset porte : une description (`asset_data.description`), des tags (`asset_data.tags`), un catalogue. Ici : description non vide et tag « BCMA ».
Les assets d'un .blend apparaissent dans l'Asset Browser lorsqu'il est dans un dossier déclaré comme bibliothèque (Preferences > File Paths) ; le projet P4 de la phase assemble 25 matériaux ainsi.

## 4. Mesures du correcteur
Voir la docstring de `validate_ch04_09.py` : plages par matériau (Wood Roughness 0,3–0,7 ; Stone ≥ 0,6 ; Plastic 0,15–0,5 et Coat ≥ 0,3 ; Glass Transmission ≥ 0,9, IOR 1,4–1,6 ; Steel Metallic ≥ 0,9, Anisotropic ≥ 0,4), liens de graphe, assets marqués avec description.

## 5. Pièges
- Bois uni : pas de veines → plastique brun.
- Pierre sans bump : trop lisse.
- Acier sans anisotropie ni rayures : métal « parfait ».
- Plastique mat : caoutchouc.
- Matériau non marqué : absent de la bibliothèque.

## 6. Limites
Le correcteur contrôle graphes et valeurs, pas le « réalisme » ; vous devez regarder le rendu. Il ne vérifie pas que les assets sont dans une bibliothèque déclarée.
