# CH02.01 — Solutions

<!-- QUIZ_ANSWERS_START -->
## Réponses du quiz

| Q | Réponse | Explication |
|---|---|---|
| Q1 | — | La forme est la position des sommets ; la topologie est la façon dont ils sont reliés (arêtes, faces). |
| Q2 | **b** — Ils forment des boucles d'arêtes et se subdivisent/déforment proprement | Boucles, Loop Cut, subdivision et déformation reposent sur les quads. |
| Q3 | — | Sur une surface plane qui ne sera ni subdivisée ni déformée (couvercle plat, objet statique). |
| Q4 | **b** — Alt+clic | Alt+clic : boucle ; Ctrl+Alt+clic : anneau. |
| Q5 | — | Un sommet relié à 3 arêtes (N-pole) ou à 5 et plus (E-pole), au lieu de 4 dans une grille de quads. |
| Q6 | — | Sur des zones plates qui ne se déforment pas ; jamais sur une articulation ni sur une courbure visible. |
| Q7 | — | 8, aux coins (sommets reliés à 3 arêtes). |
| Q8 | **a** — Select All by Trait → Faces by Sides, 4, Greater Than | Faces by Sides avec Number of Vertices 4 et Type Greater Than. |
| Q9 | — | Edit Mode, tout sélectionner (A), M → By Distance (Merge by Distance). |
| Q10 | — | Les arêtes qui ne sont pas partagées par exactement deux faces (bords ouverts, trous…) ; on bouche avec Alt+F (Fill), F ou Grid Fill. |
<!-- QUIZ_ANSWERS_END -->

## Exercice 1
Le **Cube** et le **Torus** sont 100 % quads. La **UV Sphere** a des triangles aux deux pôles ;
l'**Ico Sphere** n'a que des triangles ; le **Cylinder** a deux couvercles n-gons ; **Monkey**
mélange quads et triangles. Vérifiez vos comptes avec Statistics (sélection de toutes les faces en
Edit Mode).

## Exercice 2
Mesuré (grille 7 × 7, inset puis extrusion de la face centrale) : **8 pôles** — les 4 coins
extérieurs de l'inset sont reliés à **5** arêtes (E-poles), les 4 coins de la face intérieure à
**3** arêtes (N-poles) ; l'extrusion ne change pas ce compte. Sous subdivision, un pôle placé sur
une zone courbe produit un léger pincement ; sur une zone plate, il est invisible.

## Exercice 3
Référence : `COMPLETED_EXAMPLES/ch02_01_topology_solution.blend` et `ch02_01_topology_reference.png`
(le fil de fer n'est ajouté qu'à l'image) :
- GEO_Ngon : *Only Faces* puis *Grid Fill* → 4 quads, contour inchangé ;
- GEO_Tris : *Triangles to Quads* → 83 % de quads (les 48 triangles des pôles restent) ;
- GEO_Doubles : *Merge by Distance* → 26 sommets, surface fermée ;
- GEO_Hole : bord sélectionné puis rempli → 0 arête non-manifold ;
- GEO_Poles : **8 pôles** (les 8 coins du cube subdivisé, reliés chacun à 3 arêtes).
