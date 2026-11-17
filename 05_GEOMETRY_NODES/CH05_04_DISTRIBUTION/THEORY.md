# CH05.04 — Cours théorique : distribution

## 1. Distribute Points on Faces
`GeometryNodeDistributePointsOnFaces` : entrées **Mesh**, Selection, puis des réglages qui **dépendent de la méthode** (propriété `distribute_method`) ; sorties **Points**, **Normal**, **Rotation**.
| Méthode | Entrées | Comportement |
|---|---|---|
| **RANDOM** | Density, Seed | points tirés au hasard, densité par m² ; des paquets et des points très proches apparaissent |
| **POISSON** | Distance Min, Density Max, Density Factor, Seed | points écartés d'au moins Distance Min ; Density Factor (0–1) module la densité |
Les points sont répartis proportionnellement à l'aire des faces : un maillage régulier convient. Le nombre dépend de la méthode, de la densité et de la surface.

## 2. Masques
Un **masque** est un champ de 0 à 1. En Poisson, il va dans **Density Factor** ; en Random, une **Selection** booléenne convient. Ici : Position → Separate XYZ [X] → Math (Greater Than 0) : 1 pour x > 0, 0 sinon. D'autres masques : bruit (zones de forêt), distance à un point (clairière), pente (normal.z), attribut peint (CH05.05).

## 3. L'arbre de la solution
```
Grid (10 × 10 m ; 11 × 11) ─▶ Distribute (Poisson ; Dist. Min 0,5 ; Dens. Max 3 ; Seed 0) ─▶ Instance on Points ─▶ Join Geometry (+ sol) ─▶ Set Shade Smooth ─▶ Group Output
Position ─▶ Separate XYZ [X] ─▶ Math (Greater Than 0) ─▶ Density Factor        Cone (R 0,2 ; D 0,8) ─▶ Transform (z 0,4) ─▶ Set Material ─▶ Instance
Distribute [Rotation] ─▶ Instance on Points [Rotation]
```

## 4. Mesures de la solution
73 arbres ; 100 % sur x > 0 ; distance minimale 0,503 m ; tous dans le sol ; MAT_Tree. Sans masque : 154 arbres (50 % du bon côté). En méthode Random (même densité) : distance minimale 0,02 m.

## 5. Pièges
- Poisson sans masque connecté : arbres partout.
- Random avec une grande densité : arbres qui se touchent.
- Maillage de sol avec un très petit nombre de faces très grandes : répartition grossière.
- Densité trop faible : un « semis » plutôt qu'un bois.

## 6. Limites
Le correcteur mesure nombre, côté et distance minimale ; il ne juge pas l'esthétique de la répartition. La graine (Seed 0) est fixée pour des mesures reproductibles.
