# CH02.10 — Cours théorique : optimisation

## 1. Pourquoi optimiser ?
Chaque triangle coûte : mémoire, temps d'affichage, temps de rendu, taille des fichiers, durée des
simulations. Un décor de film contient des milliers d'objets : un rocher à 60 000 triangles là où
2 000 suffisent multiplie les coûts par 30. Optimiser = **retirer ce qui ne se voit pas**.

## 2. Mesurer d'abord
- **Statistics** (Viewport Overlays) : objets, sommets, arêtes, faces, **triangles**.
- Les moteurs de rendu et le modificateur **Decimate** travaillent en **triangles** : un quad = 2
  triangles. Mesure faite pour ce chapitre : la statue de 31 488 quads compte **62 976 triangles** ;
  Decimate *Ratio* 0,2 la ramène à **12 595 triangles** (20 % exactement) mais 10 220 faces
  (32 % des faces) — ne pas confondre les deux unités.

## 3. Le modificateur Decimate
*Generate → Decimate*, trois modes :
| Mode | Principe | Usage |
|---|---|---|
| **Collapse** | fusionne des arêtes jusqu'au *Ratio* (ou *Face Count*) visé ; option *Symmetry* | sculptures, scans, objets organiques |
| **Un-Subdivide** | défait des niveaux de subdivision (*Iterations*) | maillages issus d'une subdivision régulière |
| **Planar** | dissout les faces coplanaires (*Angle Limit*) | objets architecturaux, hard surface plat |
Collapse produit des **triangles** : parfait pour un objet de fond ou un LOD, pas pour une cage à
animer (retopologie, CH02.09). En Edit Mode, *Mesh → Clean Up → Decimate Geometry* fait la même
chose sur une sélection (destructif).

## 4. Les LOD (Levels Of Detail)
Plusieurs versions d'un même objet, de plus en plus légères, utilisées selon la **distance à la
caméra** : LOD0 (gros plan), LOD1 (plan moyen), LOD2 (fond). Dans Blender, la méthode propre :
**copies liées** (`Alt+D`) — elles **partagent le maillage** (une correction de la statue se propage
à tous les LOD) — et un **Decimate par objet** avec un ratio différent (les modificateurs sont par
objet). Sur la statue du chapitre : 12 595 / 5 037 / 943 triangles, écart moyen du LOD0 à
l'original **0,01 %** de la taille.

## 5. Nettoyage (Mesh → Clean Up)
Blender 5.3 propose : *Delete Loose* (sommets/arêtes sans face), *Decimate Geometry*, *Degenerate
Dissolve* (faces et arêtes de taille nulle), *Limited Dissolve*, *Make Planar Faces*, *Split
Non-Planar Faces*, *Split Concave Faces*, *Merge by Distance*, *Fill Holes*. Un modèle importé (OBJ,
FBX, scan) passe systématiquement par : *Merge by Distance* → *Delete Loose* → *Degenerate Dissolve*
→ vérification des normales (CH02.04).

## 6. Autres leviers
- **Subdivision** : Levels viewport bas, Render juste suffisant (CH02.06) ; *Simplify*.
- **Instances** (`Alt+D`, collections instanciées, Geometry Nodes en phase 5) : 1 000 arbres
  identiques ne coûtent presque rien en mémoire.
- **Textures** à la bonne résolution (phase 4) : une texture 8K sur un objet de fond est un gâchis.
- Supprimer les **données orphelines** (*File → Clean Up → Purge Unused Data…*, CH01.04).
