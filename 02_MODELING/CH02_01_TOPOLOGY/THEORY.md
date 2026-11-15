# CH02.01 — Cours théorique : la topologie

## 1. Topologie : la façon dont les points sont reliés
La **forme** d'un objet, c'est la position de ses sommets ; sa **topologie**, c'est la façon dont
ces sommets sont **reliés** (arêtes, faces). Deux objets de forme identique peuvent avoir des
topologies très différentes — et se comporter très différemment quand on les subdivise, les
déforme (animation), les déplie (UV) ou les ombre.

## 2. Triangles, quads, n-gons
| Type | Côtés | Usage |
|---|---|---|
| **Triangle** (*tri*) | 3 | toujours plan ; format final des moteurs de jeu ; à limiter pendant la modélisation |
| **Quad** | 4 | **standard** de la modélisation : boucles d'arêtes, subdivision propre, déformation prévisible |
| **N-gon** | 5 et plus | pratique sur une surface **plane** qui ne bouge pas ; problèmes en subdivision et en déformation |
Pourquoi les quads ? Ils forment des **boucles d'arêtes** (*edge loops*, sélection `Alt+clic`) et
des **anneaux** (*edge rings*, `Ctrl+Alt+clic`) ; les outils Loop Cut, Slide, Bevel et la subdivision
reposent sur elles. Un triangle ou un n-gon **interrompt** la boucle.

## 3. Le flux des arêtes (*edge flow*)
Les boucles d'arêtes doivent **suivre la forme** : autour des yeux et de la bouche d'un visage, le
long d'un bras, autour d'une articulation. Un bon flux permet d'ajouter du détail là où il faut et de
déformer proprement (phase 6–7). Règle pratique : si une boucle d'arêtes « tourne » sans raison ou
s'arrête au milieu d'une surface courbe, le flux est à revoir.

## 4. Les pôles
Dans une grille de quads, chaque sommet est relié à **4 arêtes**. Un **pôle** est un sommet relié à
**3** arêtes (*N-pole*) ou à **5 ou plus** (*E-pole*). Les pôles sont **inévitables** dès qu'on
ferme une forme (un cube subdivisé en a toujours 8, aux coins) ; on les **place** là où la surface
est plate et ne se déforme pas, jamais sur une articulation ni au sommet d'une courbure visible
(pincement après subdivision).

## 5. Densité
La densité de maillage doit être **suffisante pour la forme et la déformation**, pas plus :
- répartition **homogène** (quads de taille comparable) ;
- plus dense là où la courbure ou la déformation l'exigent ;
- au cinéma, on modélise une cage légère et on laisse la **subdivision** (CH02.06) lisser au rendu.
Overlay **Statistics** (Viewport Overlays) : nombre d'objets, sommets, arêtes, faces, triangles.

## 6. Les défauts à diagnostiquer
| Défaut | Comment le trouver (Blender 5.3) | Réparation courante |
|---|---|---|
| N-gons | *Select → Select All by Trait → Faces by Sides* (Number of Vertices 4, Type *Greater Than*) | découpe au Knife, *Grid Fill*, *Vertex Connect Path* (`J`) |
| Triangles en trop | *Faces by Sides* (3, *Equal To*) | *Face → Triangles to Quads* (`Alt+J`) |
| Sommets en double | Statistics anormales, ombrage cassé | *Merge* (`M`) → *By Distance* ; ou *Mesh → Clean Up → Merge by Distance* |
| Trous, bords ouverts | *Select All by Trait → Non Manifold* | *Fill* (`Alt+F`), *F*, *Grid Fill* |
| Géométrie isolée | *Select All by Trait → Loose Geometry* | supprimer |
| Faces internes | *Select All by Trait → Interior Faces* | supprimer |
L'overlay **Mesh Analysis** (Edit Mode) colore les surplombs (*Overhang*), l'épaisseur, les
intersections, la distorsion des faces (*Distortion*) et les angles vifs (*Sharp*).

## 7. Au cinéma
Les assets de film passent une **validation de topologie** avant le rigging : quads, flux autour
des articulations, aucun sommet en double, aucune face non-manifold, échelle réelle. Une erreur de
topologie découverte à l'animation coûte un retour en modélisation, puis un nouveau rig et de
nouveaux UV : c'est l'une des erreurs les plus chères d'un pipeline.
