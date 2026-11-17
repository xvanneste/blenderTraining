# CH07.02 — Solutions

<!-- QUIZ_ANSWERS_START -->
## Réponses du quiz

| Q | Réponse | Explication |
|---|---|---|
| Q1 | **a** — Une valeur de propriété à une image donnée | Entre deux clés, Blender interpole la valeur. |
| Q2 | **a** — I | I insère une clé (anim.keyframe_insert) ; K ouvre le menu de Keying Set. |
| Q3 | **a** — 24 i/s | Le chapitre fixe 24 images par seconde ; d'autres cadences existent selon la diffusion. |
| Q4 | — | Les images de début et de fin de l'animation (ici 1 à 72) : ce que Blender lit et rend. |
| Q5 | — | Pour contrôler indépendamment le timing de chaque canal : ici la rotation se fait pendant que la position est maintenue. |
| Q6 | **a** — Deux clés consécutives de même valeur | Avec des poignées Auto Clamped, deux clés égales donnent une valeur constante entre elles (X = 4 de l'image 24 à 48). |
| Q7 | **b** — Linear | Linear : 22,5° à l'image 30 ; Bezier par défaut : 14,1° (mesuré). |
| Q8 | — | Dope Sheet ou Graph Editor : T (interpolation_type), puis Linear. |
| Q9 | — | Elles évitent les dépassements : X reste entre 0 et 4 ; avec d'autres poignées la courbe peut sortir de l'intervalle des clés. |
| Q10 | — | À repérer des moments clés (arrive, turn_end) ; M les ajoute en timeline, F2 ouvre le nom du marqueur (keymap par défaut). |
<!-- QUIZ_ANSWERS_END -->

## Exercices
`COMPLETED_EXAMPLES/ch07_02_keyframes_solution.blend` (+ `_reference.png`)

**Fabrication.** Générée par script (`build_ch07_02_files.py`) : clés de position (1, 24, 48, 72), de rotation (24, 48, 72, interpolation LINEAR), plage 1–72, marqueurs. Score 34/34 ; starter 8/34. Croquis regardé : maintien de X, rotation en ligne droite, clés blanches.

## Contre-épreuve du correcteur (`COMPLETED_EXAMPLES/COUNTER_EXAMPLES/`)
| Fichier faux | Défaut | Tests qui le refusent |
|---|---|---|
| `…_wrong_range` | fin de plage à 60 | timeline (seul) |
| `…_no_hold` | X = 3,5 à l'image 48 | clés de X ; repos |
| `…_bezier_rot` | rotation en Bezier | rotation linéaire (seul) |
| `…_no_markers` | aucun marqueur | marqueurs (seul) |
| `…_off_frames` | clés de position à 25 et 49 | images des clés de X (seul) |
| `…_no_rot` | pas de rotation | clés de rotation ; repos ; rotation linéaire |
Aussi refusé : le starter.

## Limites
- Une caisse, deux canaux ; l'auto-key et les Keying Sets personnalisés ne sont pas testés.
- Le correcteur ne juge pas l'esthétique du mouvement.
