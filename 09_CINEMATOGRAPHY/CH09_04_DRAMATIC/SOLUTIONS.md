# CH09.04 — Solutions

<!-- QUIZ_ANSWERS_START -->
## Réponses du quiz

| Q | Réponse | Explication |
|---|---|---|
| Q1 | **a** — Image sombre à fort contraste | Solution : ratio 8,8 ; moyenne 0,057. |
| Q2 | **a** — Image claire, ombres ouvertes | Solution : ratio 0,9 ; moyenne 0,60. |
| Q3 | **a** — Fill très faible | Fill de 0,5 W. |
| Q4 | — | Il faut aussi une image globalement sombre : « low_not_dark » a ratio 9 mais une moyenne de 0,20 (Key 250 W) : contraste sans ambiance. |
| Q5 | — | Ratio 0,83 (contraste doux) mais moyenne 0,15 : trop sombre pour du high-key : l'ambiance dépend de la quantité de lumière, pas seulement du ratio. |
| Q6 | **a** — Orange et bleu-vert | Teintes 28° et 203° : écart 175°. |
| Q7 | **a** — Elle sépare le sujet du fond par la couleur | Contraste de température : chaud/froid. |
| Q8 | — | Il convertit la couleur de chaque lampe en HSV et compare les teintes (écart ≥ 120°) ; il vérifie aussi une saturation d'au moins 0,3. |
| Q9 | — | Le même objet Subject est lié à la collection des deux scènes ; seules les lampes diffèrent (LOW_*, HIGH_*). |
| Q10 | — | Une sphère unie sans fond ni décor : on mesure l'ambiance du modelé, pas celle d'un plan complet (couleur du fond, composition). |
<!-- QUIZ_ANSWERS_END -->

## Exercices
`COMPLETED_EXAMPLES/ch09_04_dramatic_solution.blend` (+ `_reference.png`)

**Fabrication.** Générées par script (`build_ch09_04_files.py`) : deux scènes, sujet partagé, six lampes, variantes ; calibration par rendu. Score 42/42 ; starter 2/42. Rendus de contrôle regardés.

## Contre-épreuve du correcteur (`COMPLETED_EXAMPLES/COUNTER_EXAMPLES/`)
| Fichier faux | Défaut | Tests qui le refusent |
|---|---|---|
| `…_low_not_dark` | LOWKEY : Key 250 W : le contraste y est mais l'image n'est pas sombre (moyenne 0,20) | image sombre |
| `…_low_low_ratio` | LOWKEY : Fill 25 W : ratio 1,0 | contraste |
| `…_mono_color` | LOWKEY : lampes blanches : pas de couleurs complémentaires | couleurs |
| `…_high_too_contrasty` | HIGHKEY : Fill 8 W : ratio 6,5 (et moyenne 0,30) | contraste doux ; image claire |
| `…_high_dark` | HIGHKEY : 60/40/30 W : ratio juste mais image sombre (0,15) | image claire |
Aussi refusé : le starter.

## Limites
- Sujet sphérique, sans fond.
- Teintes limitées.
- Pas de jugement esthétique.
