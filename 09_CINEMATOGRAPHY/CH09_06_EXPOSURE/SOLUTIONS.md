# CH09.06 — Solutions

<!-- QUIZ_ANSWERS_START -->
## Réponses du quiz

| Q | Réponse | Explication |
|---|---|---|
| Q1 | **a** — Un pixel écrêté à la valeur maximale | Luminance ≥ 0,99 : le détail est perdu. |
| Q2 | **a** — Standard | Standard : 4,4 % de pixels brûlés dans la scène. |
| Q3 | **a** — Double la lumière (un diaphragme) | L'échelle est logarithmique : +1 = ×2. |
| Q4 | — | Il comprime les valeurs au-delà de 1 vers une courbe douce au lieu de les couper : la sphère reste lisible (0 % brûlés). |
| Q5 | — | Exposure +3 avec AgX : moyenne 0,66 et 3,4 % de pixels brûlés : même une vue filmique sature si on sur-expose. |
| Q6 | **a** — L'étendue des tons (contraste) | Solution 0,64 ; image écrasée 0,41. |
| Q7 | **a** — Un réglage de contraste et de couleur après la vue | Exemples : AgX - Punchy, AgX - High Contrast. |
| Q8 | — | Le look Punchy assombrit et contraste : moyenne 0,279 (< 0,3) : il faut compenser par l'exposition. |
| Q9 | — | Le PNG est l'image affichée, après la vue et l'exposition ; l'EXR est linéaire, avant ces réglages. |
| Q10 | — | Une seule scène : les seuils sont calibrés sur elle ; une autre scène demanderait d'autres valeurs ; la mesure ne juge pas l'esthétique. |
<!-- QUIZ_ANSWERS_END -->

## Exercices
`COMPLETED_EXAMPLES/ch09_06_exposure_solution.blend` (+ `_reference.png`)

**Fabrication.** Générées par script (`build_ch09_06_files.py`) : scène, vue et exposition par variante ; calibration par rendu. Score 28/28 ; starter 20/28. Rendus et histogrammes regardés.

## Contre-épreuve du correcteur (`COMPLETED_EXAMPLES/COUNTER_EXAMPLES/`)
| Fichier faux | Défaut | Tests qui le refusent |
|---|---|---|
| `…_standard_clipped` | Standard : 4,4 % de pixels brûlés | hautes lumières |
| `…_too_dark` | AgX −2,5 : moyenne 0,16, image écrasée | exposition ; contraste |
| `…_too_bright` | AgX +3 : moyenne 0,66, 3,4 % brûlés | hautes lumières ; exposition ; contraste |
| `…_punchy_dark` | Look AgX - Punchy : moyenne 0,28 | exposition |
Aussi refusé : le starter.

## Limites
- Une seule scène.
- Looks non énumérables en -b.
- Pas de test EEVEE.
