# CH03.02 — Solutions

<!-- QUIZ_ANSWERS_START -->
## Réponses du quiz

| Q | Réponse | Explication |
|---|---|---|
| Q1 | — | Les brosses déplacent les sommets existants : sans assez de sommets, pas de forme fine. |
| Q2 | **b** — F | Shift+F = force. |
| Q3 | **b** — Inverse : creuse | Shift maintenu = lissage. |
| Q4 | **c** — Crease Polish | Shift+C. |
| Q5 | — | Grab (G). |
| Q6 | — | Dans l'en-tête du Sculpt Mode (Mirror X/Y/Z) ; en espace local de l'objet. |
| Q7 | **a** — Alt+M | Ctrl+I inverse le masque, M = brosse Mask. |
| Q8 | — | Grouper des faces pour isoler, cacher, masquer ou travailler par parties. |
| Q9 | **b** — Shift+H | H le cache, Alt+H réaffiche tout. |
| Q10 | — | Grandes formes, formes secondaires, lissage, détails seulement quand les volumes sont justes. |
<!-- QUIZ_ANSWERS_END -->

## Exercice 2
`COMPLETED_EXAMPLES/ch03_02_face_solution.blend` (+ `_reference.png`).
**Comment elle a été produite (important)** : la solution est **réellement sculptée à la brosse**, dans Blender 5.2 LTS en interface, pilotée via le MCP
(les opérateurs de sculpt plantent en 5.3 en arrière-plan ; la 5.2 en interface les exécute). Gestes réalisés : Mirror X ; **masque** de l'arrière du crâne
(brosse *Mask*, vue arrière, 3 passes) ; **volumes** du front, des joues, du menton (*Inflate/Deflate*, gros rayon) ; **nez** (*Inflate* en colonne puis bout) ;
**arcades** (*Draw*) ; **orbites** (*Inflate/Deflate* inversé) ; pommettes ; sillon de bouche ; **lissage** (*Smooth*) ; **Face Sets** créés depuis le masque
(*Sculpt > Face Sets > Create Face Set > From Masked*, opérateur `sculpt.face_sets_create`). Le fichier est enregistré par la 5.2 ; le correcteur 5.3 le valide.
Le style est doux (« visage lunaire ») : c'est ce que donnent des brosses larges sans retouche fine.
Mesures du correcteur : 24 578 sommets conservés, nez +6,8 cm, orbites −2,5 cm, symétrie 100 %, 5,2 % des sommets déplacés de plus de 5 mm,
arrière masqué (0,90) et intact (0 mm), 2 Face Sets, Mirror X activé. Score 23/23.
**Ce que l'essai a appris** : (1) la position d'un trait (`sculpt.brush_stroke`) est en coordonnées LOCALES de l'objet ; (2) le rayon effectif d'une brosse est environ le tiers
du réglage (rayon 0,25 → ≈ 8 cm d'effet), il faut des rayons ~3× plus grands pour des volumes ; (3) des touches répétées au même point font des pointes, un trait long de
*Draw* fait des crêtes, un gribouillis fait des anneaux : *Inflate/Deflate* au gros rayon donne les volumes, *Draw* les arêtes, *Smooth* fond le tout ;
(4) un correcteur vert ne suffisait pas : deux premières versions le satisfaisaient avec des formes laides (barres, boudins), seul le rendu regardé les a refusées.
Contre-épreuve : masque supprimé, côté droit du visage et arrière modifiés → refusé (12/22 : orbite,
symétrie, masque, zone protégée).
