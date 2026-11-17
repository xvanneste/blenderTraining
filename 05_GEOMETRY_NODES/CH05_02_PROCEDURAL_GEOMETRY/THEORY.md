# CH05.02 — Cours théorique : géométrie procédurale

## 1. Primitives
Les nœuds de maillage primitif génèrent de la géométrie : **Cube**, **Cylinder**, **UV Sphere**, **Grid**, **Cone**… (noms d'API confirmés : `GeometryNodeMeshCube`, `GeometryNodeMeshCylinder`, `GeometryNodeMeshUVSphere`, `GeometryNodeMeshGrid`). Entrées du Cylinder : Vertices, Side Segments, Fill Segments, Radius, Depth ; du Cube : Size, Vertices X/Y/Z. Les primitives sont **centrées sur l'origine**.

## 2. Transform et Join
**Transform** (`GeometryNodeTransform`) : Translation, Rotation, Scale. **Join Geometry** (`GeometryNodeJoinGeometry`) : accepte plusieurs liens sur son entrée Geometry et fusionne ; les pièces restent des composantes connexes distinctes (pas de soudure).

## 3. Des courbes aux maillages
**Curve Circle** (`GeometryNodeCurvePrimitiveCircle`) : Resolution, Radius ; sortie Curve. **Curve to Mesh** (`GeometryNodeCurveToMesh`) : Curve (chemin), Profile Curve (section), Scale, Fill Caps… Un cercle de 5 cm de rayon le long d'un cercle de 33 cm donne un anneau fermé (tore).

## 4. La colonne (dimensions réelles, Z haut)
| Pièce | Nœuds | Placement |
|---|---|---|
| Fût | Cylinder (Radius 0,3 ; Depth 2,6 ; 32 sommets) → Transform | z = 1,5 → de 0,2 à 2,8 |
| Base | Cube (0,9 × 0,9 × 0,2) → Transform | z = 0,1 → de 0 à 0,2 |
| Chapiteau | Cube (0,9 × 0,9 × 0,2) → Transform | z = 2,9 → de 2,8 à 3,0 |
| Anneau | Curve Circle (0,33 ; 48) + Curve Circle (0,05 ; 8) → Curve to Mesh → Transform | z = 2,6 |
Puis Join Geometry → Set Shade Smooth → Set Material → Group Output.

## 5. Mesures de la solution (évaluée)
4 pièces ; hauteur 3,00 m ; z min 0,000 ; emprise 0,90 × 0,90 m ; centre (0 ; 0) ; fût de 2,6 m ; 0 arête non manifold ; MAT_Column ; 100 % de faces lisses.

## 6. Pièges
- Oublier que les primitives sont centrées : le fût de 2,6 m sort à moitié sous le sol sans Transform.
- Join Geometry ne soude pas : pour fusionner, voir Merge by Distance.
- Un cercle en profil trop défini alourdit : 8 points suffisent pour un anneau fin.
- Translation en X/Y involontaire : pièce décentrée.

## 7. Limites
Contrôles de dimensions et de graphe ; pas d'évaluation esthétique. Les pièces se chevauchent légèrement (l'anneau entoure le fût) : volontaire, la colonne n'est pas un volume unique soudé.
