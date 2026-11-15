# CH03.03 — Cours théorique : choisir sa résolution

## 1. Le problème
Les brosses ne créent pas de sommets (CH03.02) : il faut adapter la **densité** du maillage à l'étape
du sculpt. Trois outils, trois logiques :

| Méthode | Principe | Atouts | Limites | Quand |
|---|---|---|---|---|
| **Voxel Remesh** | reconstruit tout l'objet en quads réguliers à une taille de voxel donnée | fusionne des volumes qui se chevauchent, densité uniforme, rapide | détruit la topologie et les UV ; trous fins comblés si voxel trop gros | blocage, fusion de masses, « nettoyage » |
| **DynTopo** (*Dynamic Topology*) | ajoute/retire des triangles sous la brosse, à la volée | détail exactement là où l'on sculpte (cornes, pointes) | triangles, topologie chaotique, perd UV et attributs | exploration de formes, appendices |
| **Multiresolution** | modificateur : niveaux de subdivision au-dessus d'une base fixe | base légère conservée (rig, UV), détail fin, retour aux niveaux bas | base nécessaire en bonne topologie ; coûteux à haut niveau | détails finaux d'un personnage retopologisé |

## 2. Voxel Remesh
Object Data Properties > *Remesh* : *Mode* Voxel, **Voxel Size** (taille d'une arête en mètres),
bouton **Voxel Remesh** (en Sculpt Mode : **R** pour régler la taille à l'écran, **Ctrl+R** pour remesher).
Options : *Adaptivity* (moins de faces dans les zones plates, mais triangles), *Fix Poles*,
*Preserve Volume*, *Preserve Attributes* (garde masque/couleurs).
Règle d'or : **les masses doivent se chevaucher** pour être fusionnées. Deux masses qui se touchent à
peine ou sont séparées de 2 cm restent deux morceaux — le mannequin du CH03.01 (sans cou, sans taille,
bras écartés de la cage) donne 3 morceaux ; avec un cou, un abdomen et deux épaules, un seul volume.
Taille de voxel ≈ 1/100 à 1/200 de la hauteur du sujet pour un blocage (0,012 m pour 1,75 m :
18 278 faces).

## 3. DynTopo
En-tête du Sculpt Mode : case **Dyntopo**. Réglages : *Detail Size* (en pixels, mode *Relative*),
*Resolution* (mode *Constant*, en unités de scène), méthode de raffinement (*Subdivide*, *Collapse*,
ou les deux), *Detail Flood Fill* pour appliquer la densité à tout l'objet. Le maillage devient
triangulé et irrégulier : on termine en général par un Voxel Remesh puis une **retopologie** (CH03.09).
Il détruit les attributs (UV, Face Sets peuvent être perdus) : à réserver à l'exploration.

## 4. Multiresolution
*Add Modifier > Generate > Multiresolution*. Boutons : **Subdivide** (Catmull-Clark), *Simple*,
*Linear*, **Unsubdivide** (reconstruire des niveaux bas), **Delete Higher**, **Apply Base** (reporter la
forme sur la base). Niveaux : **Levels Viewport** (affichage), **Sculpt** (niveau sur lequel on
sculpte), **Render**. Bonne pratique : Viewport plus bas que Sculpt pour rester fluide ; ne pas
appliquer le modificateur — la base légère (quelques centaines à quelques milliers de faces) reste
celle que l'on rigge et anime ; le détail peut être cuit en *normal map* ou *displacement* (phase 4).

## 5. Le flux de travail type d'un personnage
1. **Blocage** : masses (CH03.01) qui se chevauchent → Voxel Remesh (grossier) → sculpt des grandes
   formes ; nouveaux remesh plus fins au besoin.
2. **Exploration** : DynTopo pour ajouter des éléments (cornes, oreilles) ; Voxel Remesh pour régulariser.
3. **Retopologie** (CH03.09) : base propre en quads, boucles autour des articulations.
4. **Détail** : Multiresolution sur la base retopologisée (reprojection du sculpt : *Shrinkwrap* ou
   *Multires Reshape*), rides et pores aux niveaux hauts.
5. **Cuisson** des détails en textures (phase 4) pour le rendu et l'animation.
