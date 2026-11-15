# CH02.07 — Solutions

<!-- QUIZ_ANSWERS_START -->
## Réponses du quiz

| Q | Réponse | Explication |
|---|---|---|
| Q1 | **c** — Difference | Difference retire le volume du cutter. |
| Q2 | — | Float (rapide), Exact (robuste) et Manifold (rapide et robuste sur maillages fermés). |
| Q3 | — | Des faces exactement coplanaires provoquent des faces parasites ou des trous ratés, surtout avec le solver Float. |
| Q4 | **a** — d'utiliser tous les objets d'une collection comme cutters avec un seul modificateur | Un seul Boolean pour tous les cutters de la collection. |
| Q5 | — | Object Properties → Viewport Display → Display As : Wire (ou Bounds) ; Visibility → Show In → Renders décoché. |
| Q6 | — | Pour qu'ils suivent ses transformations (animation, déplacement) et que les trous restent en place. |
| Q7 | **b** — sous le Boolean | La pile s'exécute de haut en bas : Boolean d'abord, puis Bevel. |
| Q8 | — | Sur des pièces rigides rendues avec Bevel + Harden Normals/Weighted Normal, et sur des surfaces planes ; pas pour la subdivision ni la déformation. |
| Q9 | — | Seulement à la fin et sur une copie, pour une raison précise (export, sculpture, impression) : Object → Apply → Visual Geometry to Mesh, ou Ctrl+A sur chaque modificateur de haut en bas. |
| Q10 | **b** — des bosses dues aux n-gons et triangles | La topologie booléenne n'est pas faite pour la subdivision. |
<!-- QUIZ_ANSWERS_END -->

## Exercice 1
Difference retire la sphère du cube, Union fusionne les deux volumes, Intersect garde la partie
commune. Avec des faces exactement coplanaires, le solver Float laisse des faces parasites ou
des trous ; Exact gère le cas. Règle : faire **dépasser** le cutter.

## Exercice 2
Une fois parentés, les cutters suivent toute transformation de la platine : sans parentage, une
pièce animée « sortirait » de ses trous (les cutters restant immobiles).

## Exercice 3
Référence : `COMPLETED_EXAMPLES/ch02_07_plate_solution.blend` ; rendus `ch02_07_plate_reference.png`
et `ch02_07_plate_moved.png` (lumière déplacée et tournée de 90° sans rien refaire).
Pile : *Boolean* (Difference, Collection CUTTERS, Exact) → *Bevel* (Angle 30°, 1,5 mm, 2 segments,
Harden Normals). Le correcteur mesure **5 trous traversants** (caractéristique d'Euler du résultat
évalué) et vérifie que le maillage d'origine a toujours 8 sommets (rien d'appliqué).
