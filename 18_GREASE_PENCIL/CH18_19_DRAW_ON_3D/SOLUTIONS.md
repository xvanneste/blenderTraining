# CH18.19 — Solutions

<!-- QUIZ_ANSWERS_START -->
## Réponses du quiz

| Q | Réponse | Explication |
|---|---|---|
| Q1 | **c** — Surface | Surface (avec un Offset). |
| Q2 | — | Curseur 3D au sol à cet endroit, Stroke Placement 3D Cursor, Drawing Plane Front (X-Z). |
| Q3 | — | À décoller légèrement le trait de la surface pour éviter qu'il la traverse ou scintille. |
| Q4 | **a** — au sol | Plan horizontal. |
| Q5 | — | Ses pieds ne sont pas sur le sol (curseur 3D au-dessus) ou il manque une ombre de contact. |
| Q6 | — | Des traits GP calculés à partir des arêtes visibles (contours, plis, intersections) des maillages vus de la caméra. |
| Q7 | **b** — Activer la passe Z du View Layer | View Layer Properties > Passes > Data > Z (Blender 5.3). |
| Q8 | — | Radius trop faible (en mètres) ; pas de caméra active / mauvaise source ou calque cible. |
| Q9 | — | Pour ne plus le recalculer à chaque changement : viewport fluide, résultat figé une fois le cadrage validé. |
| Q10 | — | Échelle cohérente et pieds au sol ; occlusion correcte ; style de trait unifié ; lumière/ombre cohérentes. |
<!-- QUIZ_ANSWERS_END -->

## Exercice 2
`COMPLETED_EXAMPLES/ch18_19_hybrid_solution.blend` (+ `_reference.png`) :
- `GP_LineArt` : modificateur Line Art, Source Type Collection = SET, Target Layer `Lines`,
  Radius 0,02 m → 25 traits générés.
- `GP_Character` : 10 traits dans le plan y = 1,0, pieds à z = 0, hauteur 1,75 m ; 18 % des points
  cachés par la caisse avant vus de la caméra.
- `GP_Decal` : affiche (aplat rouge) et fenêtre peinte à 5 mm devant le mur du fond (y = 3,995).
- Passe Z activée.
Contre-épreuve : personnage déplacé à y = −5 (devant la caméra), décor déplacé hors du mur et passe Z
coupée → refusé (11/20).

## Exercice 3 (réponse attendue)
Le Line Art se recalcule pour la nouvelle caméra (il dépend de la caméra active). Le personnage,
dessiné dans un plan, s'aplatit ou se déforme vu de biais : soit on l'oriente vers chaque caméra
(contrainte *Track To* / rotation), soit on redessine le personnage pour ce plan — c'est la pratique
courante en production hybride (CH18.20).
