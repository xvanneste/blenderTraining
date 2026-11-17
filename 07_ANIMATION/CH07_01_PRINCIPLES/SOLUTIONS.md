# CH07.01 — Solutions

<!-- QUIZ_ANSWERS_START -->
## Réponses du quiz

| Q | Réponse | Explication |
|---|---|---|
| Q1 | **b** — Squash & stretch | Écrasement et étirement donnent poids et souplesse. |
| Q2 | **a** — Un mouvement préparatoire en sens inverse | Avant de sauter, on plie les genoux : le spectateur comprend l'action. |
| Q3 | **a** — Staging (mise en scène) | La mise en scène dirige le regard vers l'essentiel. |
| Q4 | **a** — Straight ahead | Straight ahead : image après image ; pose to pose : poses clés puis intervalles. |
| Q5 | — | Squash & stretch, anticipation, staging, straight ahead et pose to pose, follow through et overlapping action, slow in et slow out, arcs, secondary action, timing, exaggeration, solid drawing, appeal. |
| Q6 | **b** — Une balle écrasée s'élargit : elle ne perd pas de matière | Mesuré : Scale X = Scale Y = 1/√(Scale Z) donne un écart de volume maximal de 0,088 entre les clés. |
| Q7 | **b** — L'échelle part de l'origine : la balle se déforme depuis le sol sans flotter | Contre-exemple « floating » : origine au centre, le bas de la balle est à 20 cm du sol au contact. |
| Q8 | — | 1 (repos), 5 (anticipation, écrasée), 8 (décollage, étirée), 13 et 23 (en vol, étirée), 18 (sommet, neutre), 28 (contact, écrasée), 32 (rebond), 40 (repos). |
| Q9 | — | Au sommet, la vitesse est quasi nulle : plus d'étirement ; la forme neutre marque le temps suspendu avant la chute. |
| Q10 | — | On a écrasé seulement Z : la balle perd 40 % de volume à l'écrasement ; elle paraît aplatie comme un ballon qui se dégonfle. |
<!-- QUIZ_ANSWERS_END -->

## Exercice 2
`COMPLETED_EXAMPLES/ch07_01_principles_solution.blend` (+ `_reference.png`).

**Fabrication.** Générée par script (`build_ch07_01_files.py`) : position (images 1, 8, 18, 28, 40) puis échelle (images 1, 5, 8, 13, 18, 23, 28, 32, 40). Score 48/48 ; starter 26/48.
Croquis regardé : neuf silhouettes (écrasée en orange, étirée en vert, neutre en gris), la balle toujours posée sur le sol aux contacts.

## Contre-épreuve du correcteur (`COMPLETED_EXAMPLES/COUNTER_EXAMPLES/`)
| Fichier faux | Défaut | Tests qui le refusent |
|---|---|---|
| `…_no_squash` | aucune clé de déformation (échelle à 1) | anticipation ; étirement ; contact écrasé |
| `…_no_anticipation` | pas d'écrasement avant le départ | anticipation (seul) |
| `…_no_stretch` | pas d'étirement en vol | étirement (seul) |
| `…_volume_break` | seul Z est écrasé (volume perdu) | volume ; anticipation, étirement, contact (X non élargi) |
| `…_floating` | origine au centre : le bas flotte ou s'enfonce | contact au sol (seul) |
| `…_no_settle` | la balle ne revient pas à (1, 1, 1) | repos (seul) |
Aussi refusé : le starter (pas de courbes d'échelle).

## Limites
- Un seul objet et un seul saut ; le correcteur lit l'échelle et la position, pas la qualité artistique du timing.
- Interpolation Bezier par défaut : l'écart de volume entre clés atteint 0,088 (tolérance 0,12).
