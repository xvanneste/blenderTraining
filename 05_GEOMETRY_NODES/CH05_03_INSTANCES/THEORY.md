# CH05.03 — Cours théorique : instances

## 1. Instance et géométrie réalisée
Une **instance** est une référence à une géométrie partagée, avec sa transformation (position, rotation, échelle). 441 piquets de 32 sommets ne coûtent que les sommets d'UN piquet plus 441 matrices. **Realize Instances** (`GeometryNodeRealizeInstances`) convertit les instances en vraie géométrie : à n'utiliser que si la suite de l'arbre doit modifier chaque copie.

## 2. Instance on Points
`GeometryNodeInstanceOnPoints` — entrées confirmées : **Points**, Selection, **Instance**, Pick Instance, Instance Index, **Rotation**, **Scale** ; sortie **Instances**. Une instance est créée par sommet de la géométrie reçue. L'origine de la géométrie instanciée est le point de pose.

## 3. Variation : Random Value
`FunctionNodeRandomValue` : type de données *Float*, *Vector*, *Boolean*, *Integer*…; entrées Min, Max, ID, Seed (les entrées ne sont actives que pour le type choisi). La valeur est tirée **par élément** (un champ) : chaque point obtient la sienne.
- Rotation : type Vector, Min (0, 0, 0), Max (0, 0, 6,283) → un angle aléatoire autour de Z.
- Scale : type Float, Min 0,6, Max 1,4 → échelle uniforme aléatoire (un flottant se convertit en vecteur).

## 4. L'arbre de la solution
```
Cylinder (R 0,05 ; D 1) ─▶ Transform (z 0,5) ─▶ Set Material (MAT_Post) ─┐
Grid (8 × 8 m ; 21 × 21) ───────────────────────────────────────────────▶ Instance on Points ─▶ Group Output
Random Value (Vector, Max z 2π) ─▶ Rotation        Random Value (Float 0,6–1,4) ─▶ Scale
```

## 5. Mesures de la solution
441 instances ; emprise 8,0 × 8,0 m ; échelles 0,60–1,40 (variation relative 0,22) ; orientations réparties (vecteur moyen 0,06) ; bases à z = 0 (écart 0,000 m) ; matériau MAT_Post. Énumération par `depsgraph.object_instances` (instances dont le parent est l'objet).

## 6. Pièges
- Cylinder non relevé : piquets à moitié enfoncés.
- Realize Instances par réflexe : géométrie × 441.
- Pas de Random : un champ de clones identiques et alignés.
- Set Material APRÈS l'instanciation : l'instance porte quand même le matériau de sa géométrie ; ici on l'applique au piquet avant.

## 7. Limites
Le correcteur énumère les instances et lit le graphe ; il ne juge pas la composition. Une seule géométrie instanciée ici ; la sélection parmi plusieurs géométries (Pick Instance) est vue en CH05.04 et 05.07.
