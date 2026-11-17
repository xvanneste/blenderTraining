# CH07.12 — Solutions

<!-- QUIZ_ANSWERS_START -->
## Réponses du quiz

| Q | Réponse | Explication |
|---|---|---|
| Q1 | **a** — Un déplacement de la caméra dans l'espace | Ici, la caméra avance de 4 m sur l'axe Y. |
| Q2 | **a** — Une rotation de la caméra sur place | La Track To fait pivoter la caméra pour suivre le sujet, sans la déplacer. |
| Q3 | **a** — Track To | Track To : axe de visée −Z, haut Y : écart de visée maximal 0,03° dans la solution. |
| Q4 | — | Un mouvement de caméra qui démarre à pleine vitesse paraît mécanique ; en Bezier la vitesse aux extrémités est de 11 % du maximum (9 mm/image pour 84). |
| Q5 | — | Un mouvement qui a une raison dans l'histoire : suivre le sujet, révéler un détail, accentuer une émotion ; pas un mouvement gratuit. |
| Q6 | **a** — Un modificateur Noise sur la position | Noise sur X et Z Location : écart-type 6 mm, maximum 12 mm dans la solution. |
| Q7 | **a** — Pour garder le travelling propre | Le bruit sur Y bousculerait la vitesse du travelling. |
| Q8 | — | Un horizon penché se lit comme un effet voulu (angle hollandais) : s'il est accidentel, il gêne ; le contre-exemple « rolled » penche de 8°. |
| Q9 | — | Avec Strength 0,5, l'écart-type du tremblé atteint 32 mm : la caméra paraît secouée, plus à l'épaule. |
| Q10 | — | Avec la même phase, X et Z tremblent à l'identique (mouvement diagonal artificiel) ; la solution met 1 et 5. |
<!-- QUIZ_ANSWERS_END -->

## Exercices
`COMPLETED_EXAMPLES/ch07_12_camera_solution.blend` (+ `_reference.png`)

**Fabrication.** Générées par script (`build_ch07_12_files.py`) : sujet animé, caméra à clés de position, contrainte Track To, Noise sur X et Z (phases 1 et 5). Score 37/37 ; starter 7/37. Croquis regardé.

## Contre-épreuve du correcteur (`COMPLETED_EXAMPLES/COUNTER_EXAMPLES/`)
| Fichier faux | Défaut | Tests qui le refusent |
|---|---|---|
| `…_no_tracking` | pas de contrainte de visée (écart de visée 16°) | suivi (seul) |
| `…_linear_dolly` | travelling en interpolation linéaire | départ et arrivée doux (seul) |
| `…_too_shaky` | Noise Strength 0,5 | tremblé (valeur) ; tremblé mesuré |
| `…_no_handheld` | aucun modificateur Noise | tremblé ; tremblé mesuré |
| `…_rolled` | horizon penché de 8° | horizon (seul) |
| `…_short_dolly` | travelling de 2 m seulement (−8 → −6) | travelling (seul) |
Aussi refusé : le starter.

## Limites
- Un plan, une caméra, pas de zoom ni de profondeur de champ.
- Le contre-exemple « too_shaky » échoue deux fois (valeur et amplitude mesurée) ; « no_handheld » aussi.
- Le contenu du plan est un point : on valide la caméra, pas la mise en scène.
