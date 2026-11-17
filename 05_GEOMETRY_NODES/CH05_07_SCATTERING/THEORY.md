# CH05.07 — Cours théorique : décors et végétation

## 1. Principe d'un scattering contrôlé
1. Un **support** (terrain) ; 2. une **distribution** (Poisson pour éviter les chevauchements) ; 3. des **contraintes** (pente, altitude, masques) ; 4. des **variantes** et de la **variation** (échelle, rotation) ; 5. des **paramètres** exposés (graine, densité, pente).

## 2. La contrainte de pente
La normale d'un point d'un terrain unitaire : Normal Z = cos(pente). Masque : `Normal Z > cos(Max Slope)`. Nœuds : `GeometryNodeInputNormal` → `ShaderNodeSeparateXYZ` [Z] ; `ShaderNodeMath` RADIANS (Max Slope en degrés) → COSINE ; `ShaderNodeMath` GREATER_THAN. Le résultat (0 ou 1) alimente **Density Factor** du Distribute (Poisson). Le Distribute doit recevoir le terrain **déplacé** : la normale y est évaluée.

## 3. Variantes avec Pick Instance
`GeometryNodeGeometryToInstance` reçoit plusieurs géométries (ici trois cônes) et en fait des instances numérotées 0, 1, 2. Dans **Instance on Points** : *Pick Instance* activé, *Instance Index* ← Random Value (Integer, 0–2). Rotation ← Distribute [Rotation] ; Scale ← Random Value (Float, 0,8–1,2).
Le nœud **Cone** a sa **base à z = 0** (mesuré, z de 0 à Depth) : aucun Transform n'est nécessaire pour poser l'arbre, à la différence du Cylinder (centré).

## 4. L'outil de la solution
Terrain : Grid 20 × 20 m (120 × 120) ; Set Position (bruit Scale 0,08, amplitude 4) ; Set Material (MAT_Ground).
Arbres : cônes (rayon 0,2/0,3/0,4 ; hauteur 0,8/1,2/1,8) ; Set Material (MAT_Tree).
Interface : Seed (Integer, 0–1000, 0), Density (Float, 0,05–2, 0,5), Max Slope (Float, 0–90, 30 degrés).
Sortie : Join Geometry (terrain + arbres + géométrie d'entrée).

## 5. Mesures de la solution
Défaut : 187 arbres, écart vertical max 0,003 m, 100 % sur ≤ 33°, variantes 0,8/1,2/1,8 m, variation d'échelle 0,115. Seed 7 : 200 arbres, 1 % identiques. Density 0,25 : 108 arbres (58 %). Max Slope 10 : 123 arbres. Sans masque de pente (contre-exemple) : 187 arbres sur ≤ 20,2° (le terrain n'est jamais plus raide) — c'est le test Max Slope 10 qui le détecte.

## 6. Pièges
- Distribuer sur le plan d'entrée au lieu du terrain déplacé.
- Translater un Cone comme un Cylinder : arbres flottants.
- Seed non branché : changer la graine ne change rien.
- Variantes identiques : forêt de clones.
- Densité sans borne : instances par millions.

## 7. Limites
Les arbres sont des cônes : l'exercice porte sur la distribution, pas sur la modélisation végétale. Les mesures dépendent de la graine du bruit (fixe) et du seuil de pente.
