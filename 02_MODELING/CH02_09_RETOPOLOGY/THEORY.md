# CH02.09 — Cours théorique : la retopologie

## 1. Pourquoi retopologiser ?
Une sculpture (phase 3), un scan ou un booléen produisent des maillages **denses et désordonnés**
(ici 20 480 triangles). Impossibles à animer, à déplier (UV) ou à subdiviser proprement. La
**retopologie** consiste à reconstruire **par-dessus** une nouvelle surface : peu de faces, des quads,
des boucles qui suivent la forme et la déformation. Les détails fins reviendront par les textures
(*normal map*, *baking*, phase 4) ou le *Multiresolution* (phase 3).

## 2. Densité selon l'usage
| Usage | Densité indicative de la cage |
|---|---|
| Rocher, prop de fond | 100 – 1 000 faces |
| Prop principal | 1 000 – 10 000 |
| Personnage pour l'animation (avant subdivision) | 5 000 – 30 000 |
Règle : assez de boucles **là où ça plie** (articulations, bouche, yeux), peu ailleurs. Boucles
d'articulation : CH02.12 et CH03.09.

## 3. Outils de Blender 5.3
- **Snapping sur la surface** : *Snap* (aimant, `Shift+Tab`) avec *Snap Target for Individual
  Elements* = **Face Project** (projette chaque sommet déplacé sur la surface vue) ou **Face
  Nearest** (point le plus proche). *Snap Base* (Closest / Center / Median / Active) règle quel
  point de la sélection est aimanté. Par défaut (vérifié en 5.3), l'aimant vise aussi l'objet en
  cours d'édition (panneau Snapping → *Target Selection* : *Include Active*, *Include Edited*
  cochés) : en retopologie, **décochez
  Include Active** pour que les sommets ne s'aimantent qu'à la sculpture.
- **Poly Build** (barre d'outils, Edit Mode) : **clic** = extruder une arête au curseur,
  **`Ctrl+clic`** = créer une face au curseur, **`Shift+clic`** = supprimer. Combiné à Face Project,
  on « dessine » la nouvelle topologie sur la sculpture.
- **Overlay Retopology** (Viewport Overlays, Edit Mode) : affiche la cage par-dessus la sculpture
  même si elle est légèrement dessous (*Retopology Offset*).
- **Shrinkwrap** (modificateur *Deform*) : colle un maillage sur une cible. *Wrap Method* :
  **Nearest Surface Point**, **Project**, *Nearest Vertex*, *Target Normal Project* ; *Offset* ;
  *Wrap Mode* (*On Surface*, *Outside*…). Rapide pour des formes **fermées simples** (rocher, galet,
  casque) : une sphère subdivisée qui **enveloppe** la forme est collée dessus.
- **Mirror** (axe X, Clip) pour ne retopologiser qu'une moitié d'une forme symétrique.

## 4. Le piège de la cage trop petite (mesuré)
Avec Shrinkwrap *Nearest Surface Point*, chaque sommet va au point **le plus proche**. Une sphère
plus petite que la forme se colle sur le « ventre » de l'objet et laisse les extrémités vides : sur le
rocher du chapitre, une sphère de 50 cm de rayon ne couvre que **63 %** de la surface ; la même
sphère mise à l'échelle pour **envelopper** le rocher en couvre **100 %**, à 0,5 cm d'écart moyen.

## 5. Méthode manuelle (formes complexes)
1. Nouvel objet maillage (`GEO_*_Retopo`), un plan ; *Mirror* si symétrie.
2. Snap activé, *Face Project* ; overlay Retopology.
3. Tracer d'abord les **boucles principales** (contour des yeux, de la bouche, des articulations),
   puis remplir entre elles avec Poly Build / extrusions.
4. Vérifier régulièrement : quads, pôles bien placés (CH02.01), densité régulière.
5. Ajouter un *Shrinkwrap* final (Project) pour recoller exactement, puis *Subdivision* pour juger.
