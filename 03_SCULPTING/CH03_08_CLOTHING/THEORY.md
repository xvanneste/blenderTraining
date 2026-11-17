# CH03.08 — Cours théorique : les vêtements

## 1. Deux familles de méthodes
| Méthode | Principe | Quand |
|---|---|---|
| **Sculpt des plis** | Brosses (Clay Strips, Draw Sharp, brosses « Cloth »…) sur un volume | plis stylisés, poses fixes, vêtements serrés |
| **Simulation de tissu** (ce chapitre) | Modificateur Cloth : le tissu tombe sur le corps | plis naturels, tissus lâches (poncho, cape, nappe) |
Les deux se combinent : simuler le gros des plis, puis retoucher au sculpt.
Brosses « Cloth » vérifiées dans les brosses essentielles 5.3 (noms) : Drag Cloth, Grab Cloth, Push Cloth, Inflate Cloth,
Pinch Folds Cloth, Pinch Point Cloth, Bend/Twist Cloth, Stretch/Move Cloth, Expand/Contract Cloth. Elles n'ont pas été essayées dans ce chapitre (la retouche réelle a utilisé Smooth et Crease Sharp en 5.2).

## 2. Le workflow de simulation
1. **Corps** : un collider simplifié (≈ 10 000 faces) avec le modificateur **Collision** ; il doit rester **évalué** (affichage
   Wire, pas masqué). Le sol aussi (Collision).
2. **Tissu** : une grille à maille régulière (ici 1,6 cm), trouée au col, posée au-dessus des épaules (aucune intersection au départ).
3. **Cloth** : Physics > Cloth.
4. **Simulation** : lecture de l'animation ; on observe, on ajuste, on rejoue.
5. **Application** : à l'image de repos, appliquer le modificateur → le tissu est un maillage figé.
6. **Contrôle** : pénétration, étirement, couverture, plis, sol.

## 3. Les réglages (libellés 5.3 vérifiés)
| Panneau | Réglage | Valeur de la solution |
|---|---|---|
| Cloth | Quality Steps | 12 |
| Physical Properties | Vertex Mass ; Air Viscosity | 0,3 ; 2 |
| Stiffness | Tension, Compression ; Shear ; Bending | 15, 15 ; 5 ; 0,4 |
| Damping | Tension, Compression, Shear ; Bending | 5 ; 0,5 |
| Collisions | Quality | 5 |
| Object Collisions | Distance | 0,005 m |
| Self Collisions | (case) | décochée |
Effets : **Bending** faible = plis nombreux ; **Vertex Mass** = chute plus ou moins rapide ; **Damping** = moins de vibrations ;
**Distance** = écart entre tissu et corps (trop faible : pénétration ; trop fort : tissu qui flotte).

## 4. Ce que les mesures disent d'un tissu simulé
| Mesure | Solution | Défaut simulé |
|---|---|---|
| Sommets dans le corps | 0 % | tissu repoussé de 1,5 cm vers l'intérieur : 80,4 % |
| Arête moyenne / repos (16,4 mm) | 16,4 mm | tissu mis à l'échelle ×1,6 : 23,9 mm |
| Couverture des épaules (≤ 1,2 cm) | 94 % | tissu trop petit : 60 % ; décalé : 0 % |
| Rugosité (90ᵉ centile) | 10,6 mm | tissu lissé : 0,93 mm |

## 5. Limites de ce que l'on obtient
Une grille simulée donne des plis plausibles mais pas « de production » : les coins du tissu se froissent légèrement (visible sur
`ch03_08_poncho_reference.png`). Pour un vêtement final : maillage dédié (retopologie, CH03.09), couture, épaisseur (Solidify).
