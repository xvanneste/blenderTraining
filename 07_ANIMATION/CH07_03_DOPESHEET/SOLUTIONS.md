# CH07.03 — Solutions

<!-- QUIZ_ANSWERS_START -->
## Réponses du quiz

| Q | Réponse | Explication |
|---|---|---|
| Q1 | **a** — Les clés sur une grille d'images | Chaque clé est un losange ; on déplace ou met à l'échelle le temps. |
| Q2 | **a** — S | S met à l'échelle autour de l'image courante ; G déplace ; T change l'interpolation (keymap par défaut). |
| Q3 | **a** — Autour de la première clé (image 1) | Le pivot reste fixe : un pivot à 0 décale toutes les clés (2, 26, 50, mesuré). |
| Q4 | — | Curseur à l'image 1, sélectionner toutes les clés, S ×2 : les clés passent de 1, 13, 25 à 1, 25, 49. |
| Q5 | — | Le temps est multiplié par 2 depuis l'image 1 : 1 + (13 − 1) × 2 = 25 et 1 + (25 − 1) × 2 = 49. |
| Q6 | **a** — Un bloc de données qui contient des courbes d'animation | Une action (bloc de données) peut être assignée à des objets et dupliquée. |
| Q7 | **a** — Le lien entre une action et l'objet qu'elle anime | Un slot associe un groupe de courbes de l'action à un objet ; animation_data.action_slot. |
| Q8 | — | Sinon A et B partagent la même action : décaler l'une décale l'autre (contre-exemple « shared_action »). |
| Q9 | — | Son nombre d'utilisateurs est supérieur à 1 (users = 2 dans le contre-exemple). |
| Q10 | — | Pour que la dernière clé de B (image 73) soit lue et rendue. |
<!-- QUIZ_ANSWERS_END -->

## Exercices
`COMPLETED_EXAMPLES/ch07_03_dopesheet_solution.blend` (+ `_reference.png`)

**Fabrication.** Générées par script (`build_ch07_03_files.py`) : clés de position (images 1, 25, 49 et 25, 49, 73), actions nommées, slots. Score 33/33 ; starter 6/33. Croquis regardé : lignes grises, vertes et orange, losanges aux images attendues.

## Contre-épreuve du correcteur (`COMPLETED_EXAMPLES/COUNTER_EXAMPLES/`)
| Fichier faux | Défaut | Tests qui le refusent |
|---|---|---|
| `…_not_retimed` | A non retimée (1, 13, 25) | clés de Slide ; A évaluée |
| `…_wrong_pivot` | mise à l'échelle autour de l'image 0 : clés à 2, 26, 50 | clés de Slide ; A évaluée |
| `…_shared_action` | B partage l'action Slide | action distincte ; Slide_Late ; utilisateurs ; B évaluée |
| `…_late_not_shifted` | Slide_Late non décalée (1, 25, 49) | clés de Slide_Late ; B évaluée |
| `…_no_range` | fin de plage à 49 | plage (seul) |
| `…_wrong_values` | valeurs inversées (4, 2, 0) | clés de Slide ; A évaluée |
Aussi refusé : le starter.

## Limites
- Deux objets, un canal ; les slots multiples par action ne sont pas testés.
- Le correcteur lit les clés, pas l'esthétique du timing.
