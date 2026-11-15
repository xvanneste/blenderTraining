# CH02.10 — Solutions

<!-- QUIZ_ANSWERS_START -->
## Réponses du quiz

| Q | Réponse | Explication |
|---|---|---|
| Q1 | **b** — Triangles | Ratio 0,2 = 20 % des triangles (un quad = 2 triangles). |
| Q2 | — | Planar (dissout les faces coplanaires selon l'Angle Limit). |
| Q3 | — | Un-Subdivide (Iterations = nombre de niveaux à défaire). |
| Q4 | **b** — des triangles | Bien pour fonds et LOD, pas pour une cage à animer. |
| Q5 | — | Un niveau de détail : version plus ou moins légère d'un objet, choisie selon la distance à la caméra. |
| Q6 | **b** — Alt+D | Alt+D : copie liée. |
| Q7 | — | Les modificateurs appartiennent à l'objet, pas au maillage partagé. |
| Q8 | — | Merge by Distance, Delete Loose, Degenerate Dissolve, puis vérification des normales (Shift+N). |
| Q9 | **a** — Mesh → Clean Up | Mesh → Clean Up → Delete Loose. |
| Q10 | — | Instances/copies liées, niveaux de subdivision bas au viewport, Simplify, textures à la bonne résolution, purge des données inutilisées (un parmi ceux-ci). |
<!-- QUIZ_ANSWERS_END -->

## Exercice 1
(a) sphère subdivisée → *Collapse* ; (b) cube subdivisé → *Un-Subdivide* (Iterations = niveaux
appliqués) retrouve presque la cage ; (c) mur plat → *Planar* réduit à quelques faces.

## Exercice 2
Les valeurs dépendent de la focale et de la résolution : notez **vos** mesures. Tendance attendue :
plus la caméra est loin, plus le ratio acceptable baisse (de l'ordre de 0,3 de près, 0,05 de loin).

## Exercice 3
Référence : `COMPLETED_EXAMPLES/ch02_10_optim_solution.blend` et `ch02_10_optim_reference.png`
(de gauche à droite : statue, LOD1, LOD2, import nettoyé). Mesures du correcteur : statue
**12 595 / 62 976 triangles** (20 %), écart moyen **0,010 %** ; LOD1 **5 037**, LOD2 **943**
triangles ; trois objets partageant le maillage `ME_Statue` ; import sans doublon ni élément isolé.
