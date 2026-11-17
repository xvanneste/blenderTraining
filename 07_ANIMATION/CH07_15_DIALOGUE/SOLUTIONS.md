# CH07.15 — Solutions

<!-- QUIZ_ANSWERS_START -->
## Réponses du quiz

| Q | Réponse | Explication |
|---|---|---|
| Q1 | **a** — Les poses clés principales, souvent en Constant | Sept poses aux images 1, 13, 25, 37, 49, 61, 73. |
| Q2 | **a** — On juge les poses sans les mouvements entre elles | Le regard saute de pose en pose : on lit l'histoire. |
| Q3 | **a** — Baliser les moments clés de la scène | beat_1 à beat_7 aux images des poses (touche M). |
| Q4 | — | Pour comparer, corriger les poses sans perdre le splining, et revenir au blocking si le polish dérive. |
| Q5 | — | Neutre, regarde A, écoute A, regarde B, écoute B, regarde la caméra, maintien final : chaque maintien est une écoute. |
| Q6 | **a** — Une clé entre deux poses qui précise le trajet | Images 7 (+22°), 31 (+5°), 55 (−12°) : ils décident du trajet entre les poses. |
| Q7 | **a** — Rester plats | Deux clés égales en Auto Clamped donnent une valeur plate : 0,0° d'écart mesuré. |
| Q8 | — | Un breakdown (25°) dans le maintien : la tête dérive de 15° pendant l'écoute ; le personnage ne tient plus son regard. |
| Q9 | — | Le blocking a été validé : le splining règle le mouvement, pas l'histoire ; contre-exemple « drift » : +55° au lieu de +40°. |
| Q10 | — | L'overlap et le follow-through, les détails (clignements, respirations), le timing fin : CH07.06, CH07.10, CH07.11. |
<!-- QUIZ_ANSWERS_END -->

## Exercices
`COMPLETED_EXAMPLES/ch07_15_dialogue_solution.blend` (+ `_reference.png`)

**Fabrication.** Générées par script (`build_ch07_15_files.py`) : tête et nez, actions BLOCK (Constant) et FINAL (Bezier, Auto Clamped, breakdowns), marqueurs. Score 36/36 ; starter : arrêt anticipé (pas de FINAL). Courbe regardée.

## Contre-épreuve du correcteur (`COMPLETED_EXAMPLES/COUNTER_EXAMPLES/`)
| Fichier faux | Défaut | Tests qui le refusent |
|---|---|---|
| `…_still_stepped` | FINAL encore en Constant | breakdowns ; Bezier ; mouvement lisse |
| `…_no_breakdowns` | aucun breakdown | breakdowns (seul) |
| `…_drift` | pose modifiée (+55° au lieu de +40°) | poses conservées ; mouvement lisse ; maintiens |
| `…_hold_lost` | un breakdown dans un maintien | maintiens plats ; mouvement lisse (seuls) |
| `…_no_markers` | aucun marqueur | marqueurs (seul) |
| `…_block_active` | BLOCK reste l'action active | FINAL active ; mouvement lisse |
Aussi refusé : le starter.

## Limites
- Un objet et un canal (le lacet) ; pas de dialogue audio, pas de polish mesuré.
- Les contre-exemples « still_stepped » et « block_active » échouent aussi sur le mouvement lisse (le saut de 70° vient de l'interpolation Constant) ; « drift » aussi sur le maintien et le mouvement.
- Le correcteur lit des clés et des valeurs, pas la justesse du jeu.
