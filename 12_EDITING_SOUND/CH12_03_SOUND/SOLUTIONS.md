# CH12.03 — Solutions

<!-- QUIZ_ANSWERS_START -->
## Réponses du quiz

| Q | Réponse | Explication |
|---|---|---|
| Q1 | **a** — Un son continu qui installe le lieu | AMB : bruit grave de 4,2 s sous toute la séquence. |
| Q2 | **a** — Un son ponctuel lié à une action visible | HIT : le coup sur l'image 49. |
| Q3 | **a** — À l'image 49 (à ± 2 images) | Au-delà de 2 images l'écart se voit : HIT à 53 est refusé. |
| Q4 | — | Le cerveau lie un son et un geste s'ils sont presque simultanés ; un retard de 4 images (0,17 s) paraît faux. |
| Q5 | — | La réplique à l'image 50 chevauche le coup : le silence relatif entre 56 et 59 disparaît (0,153 pour 0,04 exigé). |
| Q6 | **a** — Il mixe en WAV et mesure l'énergie (RMS) sur des fenêtres d'images | Opérateur `bpy.ops.sound.mixdown` ; solution : coup 0,162, réplique 0,139, ambiance 0,0135. |
| Q7 | **a** — Un signal qui dépasse le maximum (crête ≥ 1,0) : distorsion | HIT à volume 6 : crête 1,00 ; la solution : 0,55. |
| Q8 | — | C'est une zone où rien d'autre ne sonne (avant le coup) : elle sert de référence de niveau. |
| Q9 | — | Un son muet n'existe pas dans le mixage : le coup muet donne un rapport de 1,0. |
| Q10 | — | Des sons synthétiques à attaque nette : un vrai son a une attaque plus floue ; la qualité du son et de la voix ne se mesure pas ici. |
<!-- QUIZ_ANSWERS_END -->

## Exercices
`COMPLETED_EXAMPLES/ch12_03_sound_solution.blend` (+ `_reference.png`)

**Fabrication.** Générées par script (`build_ch12_03_files.py`) : trois WAV synthétiques, trois strips, deux marqueurs ; mesures par mixdown. Score 61/61 ; starter 19/61. Enveloppes regardées.

## Contre-épreuve du correcteur (`COMPLETED_EXAMPLES/COUNTER_EXAMPLES/`)
| Fichier faux | Défaut | Tests qui le refusent |
|---|---|---|
| `…_late_hit` | HIT à 53 (4 images de retard) | HIT à IMPACT ; silence entre les sons |
| `…_early_voice` | VOICE à 50 (chevauche le coup) | VOICE à LINE ; silence entre les sons |
| `…_short_ambience` | AMB seulement 1–60 | ambiance qui dure |
| `…_clipping` | HIT à volume 6 : crête 1,00 | écrêtage |
| `…_muted_hit` | HIT muet | strips non muets ; coup audible |
Aussi refusé : le starter.

## Limites
- Sons synthétiques.
- Chemins relatifs aux ASSETS.
- Menus d'ajout de son non regardés.
