# CH02.08 — Cours théorique : modélisation organique

## 1. Organique : penser en volumes, pas en faces
Une forme organique (arbre, rocher, créature, personnage, vêtement) n'a ni arête vive ni surface
plane. On la construit **du gros au fin** :
1. **Blocking** : des volumes simples (sphères, cylindres, cubes) qui donnent proportions et
   silhouette — en 10 minutes, pas plus. On juge la silhouette (CH18.03) avant tout détail.
2. **Raffinage** : on remplace les volumes par une cage propre (box modeling, Skin, ou
   retopologie d'une sculpture, CH02.09).
3. **Détails** : sculpture (phase 3), textures (phase 4).

## 2. Box modeling
On part d'un cube (souvent avec **Subdivision** active dès le début, `Ctrl+2`) et on **extrude,
déplace, découpe** en gardant des quads :
- *Mirror* (modificateur, axe X, **Clipping**) pour ne modéliser qu'une moitié ;
- **édition proportionnelle** (`O`, CH01.05) pour déplacer des zones douces ;
- **Loop Cut** pour ajouter de la résolution là où la forme change ;
- formes rondes : *Cast* (modificateur) ou *To Sphere* (`Shift+Alt+S`) sur une sélection.

## 3. Le modificateur Skin : un squelette qui prend chair
Le **Skin** génère un volume autour d'un **squelette d'arêtes** (sommets reliés, sans faces) :
- chaque sommet a un **rayon** (deux valeurs X/Y) : `Ctrl+A` en Edit Mode (*Skin Resize*) ;
- **Branch Smoothing** adoucit les embranchements ; *Smooth Shading* ; symétrie X ;
- les autres commandes sont des **boutons du panneau du modificateur Skin** (Edit Mode) :
  marquer la **racine** (*Skin Root Mark*, sert à la création d'armature), marquer / libérer des
  sommets « loose » (*Skin Mark/Clear Loose*), égaliser les rayons (*Skin Radii Equalize*) et
  créer une **armature** suivant le squelette (*Skin Armature Create*, rig rapide, phase 6).
  Les noms entre parenthèses sont ceux des opérateurs (recherche `F3`).
Toujours suivi d'une **Subdivision Surface** (Skin → Subdivision dans la pile) : le Skin produit
une cage grossière en quads, la subdivision la lisse. Idéal pour : arbres, racines, tentacules,
créatures, blocking de personnage, câbles épais.

## 4. Repères d'une forme organique crédible
- **Rythme** : alternance de zones épaisses et fines (un tronc s'affine, une branche s'effile).
- **Asymétrie maîtrisée** : la nature n'est jamais parfaitement symétrique.
- **Lignes d'action** (CH18.03) : une branche suit une courbe, pas une droite.
- **Échelle** : un arbre de 3 m n'a pas le même rapport tronc/branches qu'un arbuste.

## 5. Après le Skin
On peut **appliquer** Skin et Subdivision pour **sculpter** (phase 3), puis retopologiser (CH02.09)
si l'objet doit se déformer. Gardez une copie du squelette : c'est la version modifiable.
