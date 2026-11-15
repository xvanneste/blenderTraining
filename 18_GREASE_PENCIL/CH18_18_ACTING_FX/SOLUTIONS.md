# CH18.18 — Solutions

<!-- QUIZ_ANSWERS_START -->
## Réponses du quiz

| Q | Réponse | Explication |
|---|---|---|
| Q1 | — | Attente, déclencheur, anticipation, réaction écrasé/étiré, pose extrême tenue, retour. |
| Q2 | **c** — 1 à 6 images après | Juste après : il perçoit puis réagit. |
| Q3 | — | Pour que le spectateur ait le temps de la lire. |
| Q4 | **b** — Les sourcils | Sourcils = émotion ; yeux = attention ; bouche = intensité. |
| Q5 | — | Une tenue maintenue vivante par un très léger mouvement (dessins alternés, clignement). |
| Q6 | — | Pour le minuter, le modifier ou le remplacer sans toucher au personnage, et régler l'ordre d'affichage. |
| Q7 | **b** — Une clé vide (Insert Blank Keyframe) | Sinon le dernier dessin reste affiché. |
| Q8 | — | Positions alternées, amplitude décroissante sur ~8–12 images, début sur l'impact, retour exact au repos. |
| Q9 | **a** — en un, 1 à 3 dessins | Bref et violent. |
| Q10 | — | L'interpolation des clés (Linear ou Constant au lieu de Bézier) et/ou raccourcir les intervalles. |
<!-- QUIZ_ANSWERS_END -->

## Exercice 1 (indications)
Surprise : sourcils hauts, intérieur relevé, yeux ronds, bouche en O. Peur : sourcils hauts et
serrés, yeux ouverts, bouche tendue vers le bas. Méfiance : yeux plissés, un sourcil bas. Joie :
paupières inférieures relevées, sourire large. Soulagement : paupières mi-closes, petit sourire.

## Exercice 2
`COMPLETED_EXAMPLES/ch18_18_shot_solution.blend` (+ `_contact.png`) :
- USER_Char : clés 1, 24 (clignement), 26, 36 (regard), 40, 44 (anticipation), 49 (écrasé),
  51 (étiré), 53, 55, 79, 81, 85, 89, 91 ; tenues 1–23, 26–35, 55–78, 91–120.
- USER_FX : éclair 48, 49, 50 (en un) ; fumée 52 à 70 (en deux) ; clé vide 72.
- PROP_Bulb : clé vide 48. Caméra : Location aux images 47, 48, 49, 50, 52, 54, 56, 58 ; repos en 47 et 58.
Mesures du correcteur : 15 dessins, 4 tenues, 6 enchaînements rapides, proportions ×1,23, réaction
1 image après l'effet, effet ×15,8 en taille, 6 changements de sens de la caméra.
Contre-épreuve : sans les dessins 49/51, sans la clé vide 72 et sans animation de caméra → refusé (12/21).
