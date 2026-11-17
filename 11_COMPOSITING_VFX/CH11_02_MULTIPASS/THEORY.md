# CH11.02 — Cours théorique : Compositing multipasse

## 1. La lumière est additive
Une image éclairée par deux lampes est la somme des images éclairées par chacune. Les light groups font ces images séparées.

## 2. Les prises
Un light group `key` ajoute la prise `Combined_key` au nœud Render Layers (avec `Combined_fill` pour `fill`).

## 3. Doser un groupe
Exposure multiplie par 2^EV : +1 = ×2, −1 = ×0,5.

## 4. Additionner
Nœud Mix (le nœud MixRGB du compositeur a disparu en 5.3) : data_type RGBA, blend_type ADD, Factor 1.

## 5. L'exercice
Départ : prise Image : rapport 1,17 (lampes identiques, asymétrie de distance). Solution : +1 / −1 : 4,28.

## 6. Mesurer
Luminance linéaire d'un flanc gauche et d'un flanc droit : (sRGB → linéaire) puis rapport.

## 7. Pièges
- Utiliser la prise Image : light groups ignorés.
- Oublier un groupe.
- Mesurer sur l'image affichée (compression des rapports).
- Relighter trop fort.

## 8. Limites
Pas d'ombres portées déplacées ; réflexions et lumière indirecte restent celles du rendu ; Diffuse/Glossy séparés non mesurés.
