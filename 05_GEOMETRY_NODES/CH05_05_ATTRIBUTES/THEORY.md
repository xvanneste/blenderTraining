# CH05.05 — Cours théorique : attributs

## 1. Domaines et types
Un **attribut** est une table de valeurs portée par un **domaine** de la géométrie : **Point** (sommets), **Edge**, **Face**, **Face Corner**, Spline, Instance… Chaque attribut a un **type** : Float, Integer, Vector, Color, Boolean, Rotation… Les attributs intégrés (position, normal, material_index…) et les attributs **nommés** (les vôtres) se lisent et s'écrivent de la même façon.
En script : `mesh.attributes["height"]` ; `.domain` (`POINT`, `FACE`…), `.data_type` (`FLOAT`…), `.data[i].value`.

## 2. Stocker : Store Named Attribute
`GeometryNodeStoreNamedAttribute` : entrées **Geometry**, **Selection**, **Name**, **Value** ; propriétés **data_type** et **domain**. Le champ branché sur Value est évalué sur le domaine choisi.
Dans l'arbre : Set Position → Store Named Attribute (Float, Point, « height », Value = Position → Separate XYZ [Z]).

## 3. Lire dans un shader
Nœud **Attribute** (`ShaderNodeAttribute`) : `attribute_type` = GEOMETRY, `attribute_name` = « height » ; sorties Color, Vector, Fac, Alpha. Ici : Fac → Map Range (From −0,5…0,5 → 0…1) → Color Ramp (bleu 0,25 ; vert 0,5 ; blanc 0,85) → Base Color.
Les attributs d'une géométrie générée par Geometry Nodes sont visibles du shader tant que le nom est identique.

## 4. Mesures de la solution (évaluée)
Attribut « height » : Point, Float ; écart-type 0,139 ; écart moyen à z 0,000 mm ; 10 000 sommets. Shader : Attribute « height » → Map Range → Color Ramp → Base Color.

## 5. Pièges
- Nom différent entre arbre et shader (« altitude »/« height ») : couleur uniforme.
- Mauvais domaine : l'attribut de face n'est pas lisse (facettes).
- Valeur constante : aucune variation.
- Stocker avant le déplacement : hauteur nulle.
- Oublier Set Material : la géométrie générée n'a pas le matériau.

## 6. Limites
Le correcteur contrôle l'attribut évalué et le graphe du shader ; il ne rend pas le matériau. Le rendu de référence a été regardé : bleu dans les creux, vert à mi-hauteur, blanc sur les crêtes.
