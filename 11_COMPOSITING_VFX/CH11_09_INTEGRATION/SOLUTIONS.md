# CH11.09 — Solutions

<!-- QUIZ_ANSWERS_START -->
## Réponses du quiz

| Q | Réponse | Explication |
|---|---|---|
| Q1 | **a** — Par la direction des ombres des objets réels | Le poteau de la plaque projette son ombre vers la droite : le soleil est à gauche. |
| Q2 | **a** — Il ne rend que les ombres reçues et devient transparent ailleurs | Propriété `is_shadow_catcher` de l'objet (Cycles). |
| Q3 | **a** — Pour que le fond du rendu ait un alpha 0 et laisse voir la plaque | `render.film_transparent` ; sans lui l'alpha vaut 1 partout (+0,279 sur le sol lointain). |
| Q4 | — | Deux directions d'ombre dans la même image trahissent l'incrustation : contre-exemple wrong_side : ombre à gauche (−0,062). |
| Q5 | — | Le sol 3D opaque recouvre la plaque : l'image est le sol 3D, plus de plaque (+0,328). |
| Q6 | **a** — Alpha Over : Background = plaque, Foreground = Render Layers Image | Sortie : Group Output. |
| Q7 | **a** — X 50°, Z −50° (mesuré) | Avec Z +50° l'ombre tombe à gauche (wrong_side). |
| Q8 | — | Le sol lointain doit rester identique à la plaque (± 0,03) : toute différence est du sol 3D visible ; la différence à droite du cube mesure l'ombre. |
| Q9 | — | La plaque est générée et plate : pas de perspective du sol réel, pas de grain, pas d'éclairage HDRI capturé ; la caméra est calée à la main, pas issue d'un matchmoving (CH11.08). |
| Q10 | — | Un cube, un sol plan, un seul soleil : pas de réflexions ni de lumière indirecte colorée du sol sur l'objet. |
<!-- QUIZ_ANSWERS_END -->

## Exercices
`COMPLETED_EXAMPLES/ch11_09_integration_solution.blend` (+ `_reference.png`)

**Fabrication.** Générées par script (`build_ch11_09_files.py`) : plaque empaquetée, cube, sol, soleil, arbre Alpha Over ; mesures par rendu composé. Score 49/49 ; starter 23/49. Rendus regardés.

## Contre-épreuve du correcteur (`COMPLETED_EXAMPLES/COUNTER_EXAMPLES/`)
| Fichier faux | Défaut | Tests qui le refusent |
|---|---|---|
| `…_no_catcher` | sol non shadow catcher : sol 3D visible (+0,328) | sol lointain ; ombre |
| `…_no_transparent` | film non transparent : alpha 1 partout (+0,279) | sol lointain ; ombre |
| `…_wrong_side` | soleil à droite : ombre à gauche (−0,062) | ombre à droite ; côté gauche |
| `…_no_composite` | rendu seul, plaque absente (−0,537) | sol lointain ; orphelin |
Aussi refusé : le starter.

## Limites
- Plaque synthétique.
- Pas de HDRI capturé ni de grain.
- Caméra calée à la main.
