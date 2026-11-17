# CH09.02 — Solutions

<!-- QUIZ_ANSWERS_START -->
## Réponses du quiz

| Q | Réponse | Explication |
|---|---|---|
| Q1 | **a** — Modeler le volume (lumière principale) | Elle définit la direction et le caractère. |
| Q2 | **a** — Déboucher l'ombre sans l'effacer | Plus faible que la Key, de l'autre côté. |
| Q3 | **a** — Derrière et au-dessus du sujet | Elle dessine le bord. |
| Q4 | — | À (0, 3, 3) elle éclairait seulement la toute dernière frange du bord visible (angle rasant, contribution 1 %) ; remontée à (0, 1,5, 4,5) elle apporte 29 % du bord haut. |
| Q5 | — | Fill de 150 W pour une Key de 250 W : ratio 0,9, pas de modelé : l'image est plate. |
| Q6 | **a** — Environ 2 : 1 à 5 : 1 | Solution : 2,9 : 1. |
| Q7 | **a** — Rendre avec et sans cette lampe et comparer | Par exemple Rim : bande du haut avec 0,747 contre 0,527 sans. |
| Q8 | — | La Key éclaire aussi un peu l'ombre (0,05 sans Fill) : le ratio sans Fill est 10,4 et non l'infini. |
| Q9 | — | Key à droite et Fill à gauche : ratio 0,35 (le flanc de gauche est dans l'ombre) : positions refusées. |
| Q10 | — | Elle suppose un sujet sphérique centré : un visage a des plans multiples ; elle ne juge ni l'esthétique ni la couleur. |
<!-- QUIZ_ANSWERS_END -->

## Exercices
`COMPLETED_EXAMPLES/ch09_02_three_point_solution.blend` (+ `_reference.png`)

**Fabrication.** Générées par script (`build_ch09_02_files.py`) : sphère, caméra, trois lampes de zone, puissances par variante ; calibration par rendu. Score 37/37 ; starter 16/37. Rendus de contrôle regardés.

## Contre-épreuve du correcteur (`COMPLETED_EXAMPLES/COUNTER_EXAMPLES/`)
| Fichier faux | Défaut | Tests qui le refusent |
|---|---|---|
| `…_flat` | Fill 150 W : ratio 0,9, éclairage plat (aussi : Key moins de 2 fois la Fill) | ratio ; puissances |
| `…_no_fill` | Fill 0 W : ratio 10,4, ombre noire | ratio ; Fill |
| `…_no_rim` | Rim 0 W : bord haut non détaché | Rim |
| `…_key_on_right` | Key et Fill échangées : ratio 0,35 | positions ; ratio ; Fill |
Aussi refusé : le starter.

## Limites
- Sujet sphérique.
- Lampes fixes.
- Pas de couleur ni de fond.
