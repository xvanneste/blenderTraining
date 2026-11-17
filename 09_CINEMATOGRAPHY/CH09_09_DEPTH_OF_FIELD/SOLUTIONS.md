# CH09.09 — Solutions

<!-- QUIZ_ANSWERS_START -->
## Réponses du quiz

| Q | Réponse | Explication |
|---|---|---|
| Q1 | **a** — Le plus petit (grande ouverture) | f/1,0 : solution (pic lointain 0,31) ; f/16 : tout net (0,97). |
| Q2 | **a** — La distance du plan net | 5 m dans l'exercice (distance de Near). |
| Q3 | **a** — Camera > Depth of Field | Propriété `Camera.dof.use_dof` (API ; libellé non relu à l'écran). |
| Q4 | — | Rien : tout est net (contre-exemple no_dof_bad_fstop, pics 1,00 et 1,00). |
| Q5 | — | Le cercle de confusion croît avec l'écart à la distance nette : la barre à 30 m est bien plus floue que celle à 12 m quand on vise 5 m. |
| Q6 | **a** — 1,0 | Maximum moins le fond, sur une barre émissive de luminance 1. |
| Q7 | **a** — Un objet large reste net en son centre même flou | Essai mesuré : barre de 20 cm de large, pic 0,91 floue ; barre de 6 cm, pic 0,31. |
| Q8 | — | Le flou dépend aussi de la focale et des distances : les changer fausserait la comparaison ; le correcteur les vérifie. |
| Q9 | — | La mise au point sur le fond rend le sujet proche flou (0,70) : le flou existe aussi AVANT le plan net. |
| Q10 | — | Rendu Cycles à 32 échantillons, deux barres émissives, pas de bokeh à lames ni de profondeur de champ en post ; Workbench n'a pas montré de flou lors de l'essai. |
<!-- QUIZ_ANSWERS_END -->

## Exercices
`COMPLETED_EXAMPLES/ch09_09_dof_solution.blend` (+ `_reference.png`)

**Fabrication.** Générées par script (`build_ch09_09_files.py`) : deux barres émissives, caméra 200 mm ; calibrations par rendu. Score 29/29 ; starter 16/29. Rendus regardés.

## Contre-épreuve du correcteur (`COMPLETED_EXAMPLES/COUNTER_EXAMPLES/`)
| Fichier faux | Défaut | Tests qui le refusent |
|---|---|---|
| `…_dof_off` | profondeur de champ désactivée | activation ; flou |
| `…_focus_far` | mise au point sur 30 m : barre proche floue (0,70) | netteté du sujet ; flou |
| `…_small_aperture` | F-Stop 16 : tout reste net (0,97) | flou |
| `…_focus_between` | mise au point sur 12 m : tout flou (0,82 et 0,55) | netteté du sujet ; flou |
| `…_no_dof_bad_fstop` | F-Stop 1,0 mais DOF désactivée : aucun effet | activation ; flou |
Aussi refusé : le starter.

## Limites
- Deux barres émissives.
- Cycles 32 échantillons.
- Libellés non relus à l'écran.
