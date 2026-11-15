# CH02.07 — Cours théorique : booléens et non destructif

## 1. Le modificateur Boolean
Il combine un objet avec d'autres volumes (*Generate → Boolean*) :
- **Operation** : **Difference** (percer, découper), **Union** (fusionner), **Intersect** (garder la
  partie commune).
- **Operand Type** : **Object** (un cutter) ou **Collection** (tous les objets d'une collection :
  un seul modificateur pour 20 trous).
- **Solver** (Blender 5.3) : **Float** (rapide, sensible aux faces coplanaires), **Exact** (robuste,
  gère les cas limites ; options *Self Intersection*, *Hole Tolerant*), **Manifold** (rapide et
  robuste, exige des maillages fermés « manifold »).
Règle d'or : le cutter doit **traverser franchement** la pièce (jamais affleurer exactement une
face : les faces coplanaires sont la première cause d'échec).

## 2. Travailler en non destructif
Non destructif = **rien n'est appliqué** : on peut déplacer, tourner, redimensionner un cutter à tout
moment, le trou suit (rendus `ch02_07_plate_reference.png` → `_moved.png`). Organisation :
1. Une collection **CUTTERS** (ou par objet : `CUT_Plate_*`).
2. Cutters affichés en **Wire** ou **Bounds** (*Object Properties → Viewport Display → Display As*) ;
   invisibles au rendu (*Visibility → Show In → Renders* décoché, ou icône caméra de l'Outliner).
3. Nommage `CUT_*`, et cutters éventuellement **parentés** à la pièce pour qu'ils la suivent.

## 3. L'ordre de la pile compte
Les modificateurs s'exécutent **de haut en bas**. Pour une pièce percée et biseautée :
```
Boolean   → les trous sont découpés
Bevel     → TOUTES les arêtes, y compris le bord des trous, sont biseautées (Angle, Harden Normals)
(Weighted Normal éventuel, toujours en dernier)
```
Inverser Boolean et Bevel = trous aux arêtes vives (le bevel est calculé avant que les trous
n'existent). Autres ordres classiques : *Mirror* avant *Boolean* (symétrie de la pièce), *Array*
avant *Boolean* si chaque copie doit être percée, *Subdivision* après les booléens est **déconseillé**
(topologie booléenne en triangles → bosses).

## 4. Topologie booléenne : propre ou pas ?
Le résultat d'un booléen est fait de **n-gons et de triangles**. C'est acceptable sur :
- des pièces **rigides** rendues avec Bevel + Harden Normals / Weighted Normal (hard surface) ;
- des surfaces **planes** autour des trous.
Ce n'est pas acceptable pour : subdivision, déformation (personnages), UV complexes. Dans ce cas, on
applique (en gardant une copie) puis on **retopologise** (CH02.09) ou on modélise les trous à la main.

## 5. Quand appliquer ?
Seulement à la fin, sur une **copie** (`Shift+D` puis masquer l'original), et pour une raison
précise : export vers un moteur, sculpture, impression 3D. *Object → Apply → Visual Geometry to Mesh*
ou *Apply* (`Ctrl+A` dans la pile) un par un, de haut en bas.

## 6. Outils complémentaires
L'extension *Bool Tool* (raccourcis de booléens rapides) existe sur extensions.blender.org ; elle
n'est **pas** installée ni nécessaire ici (règle de l'académie : aucune installation sans votre
accord). Tout ce chapitre utilise le modificateur natif.
