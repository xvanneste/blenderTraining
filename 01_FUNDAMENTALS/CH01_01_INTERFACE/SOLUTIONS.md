# CH01.01 — Solutions

<!-- QUIZ_ANSWERS_START -->
## Réponses du quiz

| Q | Réponse | Explication |
|---|---|---|
| Q1 | **b** — Une disposition de zones et d'éditeurs prête à l'emploi | Onglets en haut : Layout, Modeling, Shading… |
| Q2 | **b** — Outliner | Outliner. |
| Q3 | — | Dans l'éditeur Properties (onglets Render, Material, Modifiers…). |
| Q4 | — | Non, dans le .blend ; pour les retrouver dans chaque nouveau fichier : File > Defaults > Save Startup File. |
| Q5 | **b** — N | N (T = toolbar). |
| Q6 | — | Panneau Adjust Last Operation (en bas à gauche, ou F9) : Size. |
| Q7 | — | Les transformations numériques de l'objet actif : Location, Rotation, Scale, Dimensions. |
| Q8 | **a** — Ctrl+Space | Ctrl+Space (Ctrl+Alt+Space : plein écran sans interface). |
| Q9 | — | Bouton Editor Type, à gauche de l'en-tête de la zone. |
| Q10 | — | Clic droit sur la frontière > Join Areas (ou glisser depuis un coin vers la zone voisine). |
| Q11 | **b** — F3 | F3 : Menu Search. |
| Q12 | — | La souris était au-dessus d'un autre éditeur (Outliner, Properties) : les raccourcis s'appliquent à l'éditeur survolé. |
<!-- QUIZ_ANSWERS_END -->

## Exercice 1 — chasse au trésor
1. *Layout* ; autres : Modeling, Sculpting, UV Editing, Texture Paint, Shading, Animation,
   Rendering, Compositing, Geometry Nodes, Scripting.
2. Layout : 4 zones — 3D Viewport, Outliner, Properties, Timeline.
3. `T` / `N` avec la souris au-dessus de la vue 3D.
4. `GEO_Clue_A` est dans la collection `HUNT`.
5. `F3` → « cube » → *Add → Mesh → Cube*.
6. `Ctrl+Space` (même raccourci pour revenir).
7. Editor Type de la Timeline → *Text Editor* → puis *Timeline*.
8. `secret` = **42** (Object → Custom Properties).

## Exercice 2
Diviser la vue 3D verticalement (coin ou `RMB` frontière → *Vertical Split*), passer la
nouvelle zone de droite en Outliner ; diviser celle-ci horizontalement, passer la partie basse
en *Shader Editor* ; ajuster les frontières ; la Timeline est déjà en bas. Retour : *Join Areas*.

## Exercice 3
Méthode : `RMB` sur l'onglet *Layout* → *Duplicate* → renommer *BCMA_Study* → Timeline →
*Text Editor*. Le fichier de référence (`COMPLETED_EXAMPLES/ch01_01_interface_solution.blend`)
utilise un raccourci technique : il renomme le workspace *Scripting*, qui contient déjà ces
éditeurs (les scripts en arrière-plan ne peuvent pas diviser des zones).

## Leçon 2 moyen
`Shift+A` → *Mesh → Cylinder* → panneau *Add Cylinder* : *Vertices* = 6, *Depth* = 2.
