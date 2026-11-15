# CH02.03 — Solutions

<!-- QUIZ_ANSWERS_START -->
## Réponses du quiz

| Q | Réponse | Explication |
|---|---|---|
| Q1 | **b** — aimante au milieu des arêtes | Shift = milieux ; Ctrl = sans aimantation ; C = à travers ; Entrée = valider. |
| Q2 | — | Mesh → Bisect, puis dans le panneau : Plane Point (Z voulu), Plane Normal (0,0,1), Clear Outer, et Fill pour boucher. |
| Q3 | — | C (cut through) pendant la coupe ; ou Shift+K sur une sélection. |
| Q4 | **b** — Le curseur 3D (Center) | Center = curseur 3D par défaut ; Shift+C le remet au centre. |
| Q5 | — | Tout sélectionner (A) puis M → By Distance : les sommets superposés sur l'axe ne sont pas fusionnés par Auto Merge. |
| Q6 | — | Screw (montée par tour) > 0, Iterations = 5, axe Z, section décalée de l'origine (rayon de l'hélice). |
| Q7 | **b** — une pyramide | Les 4 sommets fusionnent en un point centré. |
| Q8 | — | Delete retire des éléments et laisse un trou ; Dissolve les retire en réunissant les faces voisines, sans trou. |
| Q9 | — | À retirer les arêtes inutiles des zones planes (Max Angle) ; il crée des n-gons, donc à réserver aux surfaces planes qui ne se déforment pas, avec un angle faible. |
| Q10 | **c** — By Distance | By Distance (Merge by Distance). |
<!-- QUIZ_ANSWERS_END -->

## Exercice 2
Profil type (en m, x = rayon, z = hauteur) : (0 ; 0), (0,035 ; 0), (0,035 ; 0,008), (0,005 ; 0,012),
(0,005 ; 0,09), (0,03 ; 0,11), (0,04 ; 0,16), (0,038 ; 0,2). Spin 360°, 32 pas, puis `A`, `M` →
*By Distance* (les 32 sommets de l'axe fusionnent), *Shade Smooth*, *Solidify* 2 mm.

## Exercice 3
Référence : `COMPLETED_EXAMPLES/ch02_03_cutting_solution.blend` et `ch02_03_cutting_reference.png`.
- GEO_Bar : z max = 0,80, coupe bouchée (0 arête ouverte).
- GEO_Messy : 6 faces après Limited Dissolve, cube de 70 cm intact.
- GEO_Profile : généré avec les **opérateurs de l'interface** (Spin 24 pas, Auto Merge, puis `A`,
  `M` → By Distance) : 193 sommets, 192 faces, seul le col est ouvert (24 arêtes de bord).
  Sans le *By Distance* final, on mesure 216 sommets dont 23 superposés au fond.
- GEO_Pyramid : 5 sommets, pointe centrée.
- GEO_Spring : modificateur Screw (Screw 0,08, Iterations 5, Steps 24) → ressort de 47 cm.
- GEO_Tile : arête diagonale d'un coin à l'autre.
