# CH01.10 — Solutions

<!-- QUIZ_ANSWERS_START -->
## Réponses du quiz

| Q | Réponse | Explication |
|---|---|---|
| Q1 | — | Il modifie le résultat affiché/rendu sans changer le maillage d'origine : réglable et réversible tant qu'on ne l'applique pas. |
| Q2 | **b** — De haut en bas | Chaque modificateur reçoit le résultat du précédent (au-dessus). |
| Q3 | — | Icône appareil photo (Render) du modificateur. |
| Q4 | **b** — Array | Array. |
| Q5 | — | Par rapport à l'origine de l'objet (ou à un Mirror Object). |
| Q6 | **a** — Solidify | Solidify. |
| Q7 | — | Les arêtes réelles ne sont jamais parfaitement vives : le biseau accroche la lumière et crée un liseré qui lit les formes. |
| Q8 | — | Relative : en multiples de la taille de l'objet ; Constant : en distance fixe (mètres). |
| Q9 | **b** — Solidify puis Subdivision | Épaissir puis lisser. |
| Q10 | — | Retouche manuelle impossible autrement, ou export vers un logiciel qui ne gère pas les modificateurs. |
<!-- QUIZ_ANSWERS_END -->

## Exercice 1
Array : *Count* 12, *Relative Offset* (0, 1, 1) — chaque copie avance d'une profondeur de marche
et monte d'une hauteur de marche.

## Exercice 3
Fichier : `COMPLETED_EXAMPLES/ch01_10_bridge_solution.blend` ; rendu
`COMPLETED_EXAMPLES/ch01_10_bridge_reference.png`.
| Objet | Pile |
|---|---|
| GEO_Plank | Array (Count 10, Relative Offset X 1,05) |
| GEO_Railing | Mirror (X) |
| GEO_Pillar | Bevel (0,02 m, 3 segments) |
| GEO_Bucket | Solidify (0,02 m) → Subdivision (1 / 2) + Shade Smooth |

## Défi 1
Ajouter un Empty à l'origine de la marche, l'orienter de 20° sur Z et le monter de 0,18 m ;
Array : décocher *Relative Offset*, cocher *Object Offset* → l'Empty. Chaque copie applique la
transformation relative de l'Empty : la spirale se forme.
