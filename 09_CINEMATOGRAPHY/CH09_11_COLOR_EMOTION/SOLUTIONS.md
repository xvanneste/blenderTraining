# CH09.11 — Solutions

<!-- QUIZ_ANSWERS_START -->
## Réponses du quiz

| Q | Réponse | Explication |
|---|---|---|
| Q1 | **a** — La couleur elle-même, en degrés sur le cercle | Rouge 0°, jaune 60°, vert 120°, cyan 180°, bleu 240°. |
| Q2 | **a** — L'intensité de la couleur (grisé ou vif) | S = 0 : gris ; S = 1 : couleur pure. |
| Q3 | **a** — La clarté (de noir à lumineux) | V = 0 : noir. |
| Q4 | — | Convention culturelle courante (bleu-gris, saturation faible, valeur basse) : une convention, pas une loi ; la mesure vérifie la convention choisie. |
| Q5 | — | Le noir cache l'espace (inquiétude), l'accent vif attire l'œil sur ce qui menace : contraste de valeur. |
| Q6 | **a** — Une suite de cartes de couleur qui planifie l'émotion du film | Ici cinq cartes : joie, tristesse, colère, calme, peur. |
| Q7 | **a** — Par la valeur ou par une teinte éloignée d'au moins 120° | JOY : fond jaune (45°), accent bleu ciel (200°) : 155° d'écart malgré des valeurs voisines. |
| Q8 | — | Les couleurs d'objet sont linéaires : un gris de 0,5 s'affiche à 0,73. Le correcteur rend l'image et mesure ce que voit le spectateur. |
| Q9 | — | Deux émotions de teintes trop proches (21°) se confondent : le color script perd sa lisibilité. |
| Q10 | — | Elle valide des plages de H, S, V pour une convention occidentale ; elle ne juge ni l'harmonie réelle, ni les contextes culturels, ni la lumière d'une vraie scène. |
<!-- QUIZ_ANSWERS_END -->

## Exercices
`COMPLETED_EXAMPLES/ch09_11_color_solution.blend` (+ `_reference.png`)

**Fabrication.** Générées par script (`build_ch09_11_files.py`) : dix plans colorés, caméra orthographique ; calibrations par rendu. Score 46/46 ; starter 5/46. Rendus regardés.

## Contre-épreuve du correcteur (`COMPLETED_EXAMPLES/COUNTER_EXAMPLES/`)
| Fichier faux | Défaut | Tests qui le refusent |
|---|---|---|
| `…_wrong_hue_sadness` | tristesse verdâtre (H 101°) | teinte de la tristesse |
| `…_saturated_calm` | calme très saturé (S 0,90) | saturation du calme |
| `…_dim_joy` | joie sombre (V 0,50) | valeur de la joie |
| `…_same_hues` | calme et tristesse presque de même teinte (21°) | teintes distinctes |
| `…_low_contrast` | colère : accent de la couleur du fond | accent contre fond |
| `…_bright_fear` | peur sur fond clair (V 0,50) | fond sombre de la peur |
Aussi refusé : le starter.

## Limites
- Conventions occidentales.
- Cartes planes sans lumière.
- Libellés non regardés à l'écran.
