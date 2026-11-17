# CH09.10 — Solutions

<!-- QUIZ_ANSWERS_START -->
## Réponses du quiz

| Q | Réponse | Explication |
|---|---|---|
| Q1 | **a** — La droite qui relie les deux personnages | Ici l'axe X, de A (x = −1) à B (x = +1). |
| Q2 | **a** — Les personnages changent de côté à l'écran | Mesuré : gros plan de l'autre côté → rouge à 74 % de la largeur (au lieu de 26 %). |
| Q3 | **a** — Large, moyen, gros plan | C'est une convention, pas une loi. |
| Q4 | — | Le spectateur se repère par la direction à l'écran : si A et B échangent leurs côtés, le dialogue semble s'inverser. |
| Q5 | — | Hauteur de A : large ≤ 35 % (mesuré 27 %), moyen 40–65 % (58 %), gros plan 70–95 % (82 %). |
| Q6 | **a** — Marker > Bind Camera to Markers (marker.camera_bind) | Libellé relu par l'API : « Bind Camera to Markers » ; menu relu dans bl_ui/space_time.py ; M ajoute un repère (keymap). |
| Q7 | **a** — Grandir les personnages dans le cadre | Mesuré : 58 % → 78 % de la hauteur de l'image. |
| Q8 | — | Un travelling à vitesse constante : une interpolation par défaut (Bézier) accélère et ralentit aux extrémités. |
| Q9 | — | Pour comparer la taille de A au début et à la fin du travelling : la valeur à 48 doit dépasser 1,15 fois celle de 25. |
| Q10 | — | Deux cylindres de couleur et trois caméras ; elle ne juge ni le rythme du montage, ni le regard, ni le raccord de mouvement. |
<!-- QUIZ_ANSWERS_END -->

## Exercices
`COMPLETED_EXAMPLES/ch09_10_movements_solution.blend` (+ `_reference.png`)

**Fabrication.** Générées par script (`build_ch09_10_files.py`) : deux cylindres, trois caméras, repères et clés ; calibrations par rendu. Score 55/55 ; starter 25/55. Planches regardées.

## Contre-épreuve du correcteur (`COMPLETED_EXAMPLES/COUNTER_EXAMPLES/`)
| Fichier faux | Défaut | Tests qui le refusent |
|---|---|---|
| `…_cross_line` | gros plan de l'autre côté de la ligne : A à droite de B | ligne d'action |
| `…_no_markers` | aucun repère de timeline | repères |
| `…_wrong_order` | repères dans l'ordre inverse (serré, moyen, large) | ordre des repères ; échelles |
| `…_static_med` | plan moyen fixe | travelling |
| `…_dolly_out` | recul au lieu d'une avancée | travelling |
| `…_no_progression` | plan moyen aussi large que le plan large | échelle du moyen ; travelling |
Aussi refusé : le starter.

## Limites
- Deux personnages-cylindres.
- Un seul mouvement mesuré.
- Menus non regardés à l'écran.
