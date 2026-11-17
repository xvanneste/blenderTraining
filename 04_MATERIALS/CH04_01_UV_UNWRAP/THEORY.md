# CH04.01 — Cours théorique : les UV

## 1. Ce que sont les UV
Chaque sommet de chaque face reçoit des coordonnées 2D (U, V) : sa position dans une image. Déplier = aplatir la surface 3D dans le plan de l'image.
Une surface fermée ne s'aplatit pas sans coupure : on la découpe le long de **seams** (coutures), comme un patron de vêtement.

## 2. Seams et îlots
- On coupe sur les **arêtes vives** et dans les endroits peu visibles.
- Chaque morceau déplié est un **îlot** (island). Peu d'îlots = peu de coutures visibles ; trop peu = distorsion.
- Dans ce chapitre : seams sur les arêtes d'angle > 50° → 22 îlots (corps, couvercle, sangles).
- Une surface courbe « développable » (comme le couvercle en demi-cylindre) se déplie sans distorsion sans couper davantage.

## 3. La distorsion
Déplier peut étirer ou comprimer. On la lit avec un **damier** (UV Grid) : des carrés réguliers = bon ; des bandes = étirement.
Mesure : pour chaque triangle, le rapport s₁/s₂ des valeurs singulières du jacobien 3D→UV (1 = parfait).
| | Étirement moyen | 95ᵉ centile |
|---|---|---|
| Starter (projection plane) | 1,59 | 2,76 |
| Solution | 1,00 | 1,00 |
Méthodes (menu UV > Unwrap, libellés 5.3) : **Unwrap Angle Based**, **Unwrap Conformal**, **Unwrap Minimum Stretch** ; aussi *Smart UV Project…*, *Follow Active Quads…*, *Cube Projection*.

## 4. La densité de texels
Texel = pixel de texture. Densité = nombre de texels par mètre. Si un îlot est 3× plus grand que son voisin pour la même surface 3D, il reçoit 3× plus de détails.
**UV > Average Islands Scale** égalise les échelles. Mesure : écart-type du log de la densité (pondéré par l'aire) ≤ 0,20 ; solution 0,00 ; « densité inégale » 0,47.
Exception volontaire : donner plus de densité au visage d'un personnage qu'à ses semelles.

## 5. Packing
Disposer les îlots dans le carré [0, 1] × [0, 1] : **UV > Pack Islands** (options : *Rotate*, *Margin Method*, *Margin*…).
- Aucun chevauchement (union rastérisée / somme des aires ≥ 98 %) ;
- tout dans [0, 1] (sinon la texture se répète ou tombe dans une autre tuile : CH04.02) ;
- occupation ≥ 50 % (solution 68 %) ;
- marge : environ 2 % pour éviter qu'un îlot « bave » sur l'autre au mip-mapping et au baking.

## 6. Mesures de la solution
22 îlots ; 124 arêtes marquées comme seams ; étirement 1,00 ; densité 0,00 ; chevauchement 0 % ; occupation 68 % ; UV de 0,01 à 0,99.

## 7. Limites
Le correcteur juge la mesure géométrique des UV, pas le choix esthétique des coutures ni l'orientation des îlots (important pour les textures directionnelles : bois, brossé).
