# CH18.19 — Cours théorique : dessiner dans et sur la 3D

## 1. Un trait GP est un objet 3D
Chaque point d'un trait Grease Pencil a une position **3D**. Ce qui décide où tombe le trait quand
on dessine, ce sont deux réglages de l'en-tête de la vue 3D (mode Draw) :
- **Stroke Placement** : *Origin* (plan passant par l'origine de l'objet), *3D Cursor* (plan passant
  par le curseur), *Surface* (projeté sur la surface des objets visibles, avec un *Offset*),
  *Stroke* (sur les traits existants) ;
- **Drawing Plane** : l'orientation du plan de dessin — *View* (face à la vue), *Front (X-Z)*,
  *Side (Y-Z)*, *Top (X-Y)*, *Cursor* (orienté comme le curseur 3D).
Pour dessiner un personnage debout dans une pièce : *Drawing Plane* Front, *Stroke Placement*
3D Cursor, curseur posé au sol à l'endroit où il se tient (CH18.09).

## 2. Dessiner sur des surfaces
*Stroke Placement : Surface* projette chaque point sur la surface sous la souris : affiches, fissures,
graffitis, ombres dessinées, marquages au sol. *Offset* écarte légèrement le trait de la surface pour
éviter qu'il ne la traverse (scintillement). Option *Project Onto Selected* : ne projeter que sur les objets
sélectionnés.

## 3. La perspective 3D comme référence
Un décor 3D simple (blocs) donne une perspective exacte : on dessine par-dessus, depuis la caméra du
plan. Les points de fuite sont « gratuits » ; on peut changer d'angle de caméra sans redessiner le
décor, seulement les éléments 2D.

## 4. Line Art : des contours dessinés calculés
Le modificateur **Line Art** génère des traits GP à partir des arêtes visibles de maillages, vus depuis
la caméra active : contours, plis (*crease*), intersections, matériaux, arêtes marquées. Ajout :
*Add > Grease Pencil > Scene / Collection / Object Line Art*. Réglages clés : *Source Type* et source,
*Target Layer* et *Target Material*, épaisseur (*Radius*, en mètres : 0,02 m est lisible à 8 m, 4 mm
devient invisible). Il se recalcule quand la caméra ou le décor bougent (coûteux : on peut le cuire,
*Bake Line Art*).

## 5. Occlusion : le 2D derrière le 3D
Un personnage GP placé en profondeur doit être **caché** par les objets 3D devant lui. Dans la vue 3D
c'est automatique. Au **rendu final** de Blender 5.3 (EEVEE, Workbench, Cycles), c'est vrai seulement
si la **passe Z** est activée : *View Layer Properties > Passes > Data > Z*. Sans elle, le GP est
composé PAR-DESSUS tous les maillages (constaté dans cette formation en 5.2 et 5.3, CH18.06).

## 6. Personnages 2D dans un décor 3D
Règles de réussite : échelle humaine cohérente avec le décor ; pieds **au sol** (sinon le personnage
flotte) ; éclairage cohérent (aplats compatibles avec la lumière du décor, ou calque `use_lights`) ;
une ombre dessinée au sol si nécessaire ; contours du décor (Line Art) d'épaisseur proche de ceux du
personnage pour unifier le style.
