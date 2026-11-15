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
**Comment elle a été produite (important)** : en arrière-plan, les opérateurs de sculpture de Blender
5.3 font planter le logiciel ; la solution n'a donc PAS été sculptée à la brosse. Elle a été générée par
script : déplacements le long de la normale (bosses gaussiennes équivalentes à Draw / Clay Strips, et
négatives pour creuser), masque et Face Sets écrits directement dans les attributs `.sculpt_mask` et
`.sculpt_face_set` que le Sculpt Mode utilise. Le résultat est un repère de forme et de mesure, pas un
exemple de geste de sculpteur.
Mesures du correcteur : 24 578 sommets conservés, nez +13,5 cm, orbites −4,6 cm, symétrie 100 %,
arrière masqué (1,00) et intact (0 mm), 3 Face Sets, Mirror X activé.
Contre-épreuve : masque supprimé, côté droit du visage et arrière modifiés → refusé (12/22 : orbite,
symétrie, masque, zone protégée).
