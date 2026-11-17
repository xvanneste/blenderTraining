# CH05.01 — Cours théorique : principes de Geometry Nodes

## 1. Un modificateur à nœuds
Geometry Nodes est un modificateur de type **Nodes** (API : `modifier.type == 'NODES'`, `modifier.node_group`). Son **arbre** (`GeometryNodeTree`) reçoit une géométrie (Group Input), la transforme et la rend (Group Output). Un arbre peut aussi **générer** sa géométrie (Grid, Cube, Cylinder, UV Sphere…) et ignorer l'entrée : c'est le cas ici, l'objet hôte est un maillage vide.
Une opération « Nouveau » du bouton du modificateur crée un arbre prêt à l'emploi (opérateur `node.new_geometry_nodes_modifier`, libellé « New Geometry Node Modifier »).

## 2. La géométrie circule
Les liens de géométrie vont de gauche à droite jusqu'au **Group Output**. Chaque nœud de géométrie reçoit une géométrie, la modifie et la renvoie. Un nœud dont aucune sortie n'est utilisée est inutile (orphelin).

## 3. Les champs
Un **champ** est une fonction évaluée en chaque point/face/arête de la géométrie que le nœud consommateur traite. Exemples d'entrées de champ : **Position**, **Normal**, **Index**, les textures (Noise…), les attributs nommés. Le **Noise Texture** a pour vecteur par défaut la position du point : branché sur Offset de **Set Position**, il donne un déplacement différent à chaque sommet. À l'inverse, un nombre saisi dans une case est la même valeur partout.

## 4. L'arbre de la solution
```
Grid (10 × 10 m, 100 × 100 sommets) ─▶ Set Position ─▶ Set Shade Smooth ─▶ Set Material (MAT_Terrain) ─▶ Group Output
Noise Texture [Fac] ─▶ Math (Subtract 0,5) ─▶ Math (Multiply 2) ─▶ Combine XYZ [Z] ─▶ Set Position [Offset]
```
Valeurs : Noise Scale 0,35, Detail 5. Le bruit varie entre ≈ 0,2 et 0,8 : (Fac − 0,5) × 2 donne ± 0,6 m environ.
**Set Material** est nécessaire : l'arbre remplace la géométrie, qui n'a plus les matériaux du maillage d'origine (le premier rendu de ce chapitre sortait blanc pour cette raison).

## 5. Mesures de la solution (géométrie évaluée)
10 000 sommets ; emprise 10,0 × 10,0 m ; écart-type de Z 0,139 m ; étendue de Z 0,84 m ; 100 % de faces lisses ; matériau MAT_Terrain présent.

## 6. Inspecter
Le **Spreadsheet** affiche les valeurs de chaque élément (position, attributs) de la géométrie évaluée ; le nœud **Viewer** (`GeometryNodeViewer`) montre un champ dans la vue 3D. À utiliser avant de chercher une erreur à l'aveugle.

## 7. Pièges
- Offset constant (0, 0, 0) : terrain plat.
- Grille trop grossière : relief anguleux et peu de sommets.
- Oublier Set Material : surface blanche.
- Amplitude excessive : échelle absurde.
- Évaluer la géométrie sous le sol du studio : le terrain disparaît (ici l'objet est surélevé de 0,8 m).

## 8. Limites
Le correcteur ne juge pas l'esthétique du terrain ; il contrôle des mesures et le graphe. L'arbre est évalué dans la scène telle qu'enregistrée (graine du bruit fixe).
