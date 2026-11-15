# CH18.20 — Solutions

<!-- QUIZ_ANSWERS_START -->
## Réponses du quiz

| Q | Réponse | Explication |
|---|---|---|
| Q1 | — | Perspective, focale et échelle justes d'emblée ; les cadrages sont réutilisés au layout sans traduction. |
| Q2 | **b** — Parent = la caméra | Object Properties > Relations > Parent. |
| Q3 | — | Ce sont des guides de travail, pas des éléments de l'image finale. |
| Q4 | **b** — View | Plan parallèle à la vue. |
| Q5 | — | Placer personnages et accessoires 3D dans leurs poses clés, plan par plan, sans animation fine. |
| Q6 | **c** — Constant | Il garde sa position jusqu'à la clé suivante. |
| Q7 | **b** — K | I insère directement les canaux par défaut des préférences. |
| Q8 | — | Trancher : corriger le board si le décor est juste, ou le décor si l'intention du board prime. |
| Q9 | — | 3D sous un rendu dessiné (Line Art, toon) ; 2D dans un décor 3D ; 3D avec effets ou annotations 2D. |
| Q10 | — | Désactiver sa sélection (Outliner) ou la verrouiller ; travailler en vue caméra sans la sélectionner. |
<!-- QUIZ_ANSWERS_END -->

## Exercice 2
`COMPLETED_EXAMPLES/ch18_20_layout_solution.blend` (+ `_contact.png`) :
- CHR_A : image 1 en (−1,8 ; 2,2 ; 0) tourné de −60°, images 73 et 121 en (0,3 ; 1,0 ; 0) tourné de −20° ;
  18 clés (Location + Rotation × 3 plans) en Constant.
- Recouvrements mesurés board / mannequin : SH0010 0,70, SH0020 0,76, SH0030 0,80 ; pieds alignés à
  moins de 0,03 de hauteur d'image.
- Caméras identiques au starter ; boards *Disable in Renders*.
Contre-épreuve : CHR_A décalé de 0,8 m au plan 2, focale et hauteur de CAM_SH0030 modifiées → refusé
(caméra modifiée ; blocking 1/3).

## Exercice 3 (indications)
Contradictions fréquentes : personnage dessiné plus grand que la porte du décor ; deux plans qui
supposent deux positions différentes de la table ; un contrechamp qui franchit l'axe. On tranche en
modifiant le board (si le décor est juste) ou le décor (si l'intention du board prime).
