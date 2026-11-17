# CH07.10 — Solutions

<!-- QUIZ_ANSWERS_START -->
## Réponses du quiz

| Q | Réponse | Explication |
|---|---|---|
| Q1 | **a** — Ce qu'il veut ou ressent, et que le mouvement doit montrer | On anime une intention, pas des bones. |
| Q2 | **a** — Dans l'immobilité d'un maintien | La tête reste à 55° de l'image 27 à 45 : variation 0,0° dans la solution. |
| Q3 | **a** — Les yeux et la tête, puis le corps | Retard mesuré : buste 6 images après la tête, hanches 6 images après le buste. |
| Q4 | — | Un événement soudain provoque une réaction rapide (5 images pour 90 % du tour de tête) ; une réaction lente se lit comme de l'indifférence. |
| Q5 | — | Un moment d'intention dans la scène : remarquer, hésiter, décider, agir ; chaque beat a son timing. |
| Q6 | **a** — Préparer et annoncer l'action | Recul de 8° avant l'avance de 14°. |
| Q7 | **a** — Établit le calme avant la réaction (immobile ≤ 2°) | Sans idle (la tête part à l'image 5) la remarque n'est pas lisible. |
| Q8 | — | Chaque segment lourd réagit avec un retard : la chaîne tête, buste, hanches donne l'impression d'un corps réel (overlap). |
| Q9 | — | Si la tête continue de bouger pendant la réflexion (14,9° de variation), le spectateur n'a pas le temps de lire la pensée. |
| Q10 | — | Un tour de tête trop petit ne se lit pas comme un regard vers un objet ; 40° à 70° le rend lisible. |
<!-- QUIZ_ANSWERS_END -->

## Exercices
`COMPLETED_EXAMPLES/ch07_10_acting_solution.blend` (+ `_reference.png`)

**Fabrication.** Générées par script (`build_ch07_10_files.py`, qui importe le mannequin de `build_ch07_08_files.py`) : lacet monde de la tête, du buste et des hanches, inclinaison de la colonne, une clé par image sur 72 images. Score 39/39 ; starter : arrêt anticipé (pas d'animation). Courbes regardées.

## Contre-épreuve du correcteur (`COMPLETED_EXAMPLES/COUNTER_EXAMPLES/`)
| Fichier faux | Défaut | Tests qui le refusent |
|---|---|---|
| `…_no_hold` | la tête dérive pendant la réflexion | vitesse de remarque ; temps de pensée |
| `…_no_lag` | tête, buste et hanches partent ensemble | retard du corps (seul) |
| `…_no_anticipation` | la colonne part en avant sans recul | anticipation (seul) |
| `…_no_idle` | la tête part dès l'image 5 | idle ; retard du corps |
| `…_too_slow` | remarque en 20 images | vitesse de remarque ; temps de pensée |
| `…_small_turn` | tête tournée de 20° seulement | amplitude de la remarque (seul) |
Aussi refusé : le starter.

## Limites
- Mannequin sans visage ni mains ; mesures de lacet et d'inclinaison seulement.
- Les contre-exemples « no_hold » et « too_slow » échouent aussi sur la vitesse de remarque (la tête qui dérive ne s'arrête pas) ; « no_idle » échoue aussi sur le retard du corps.
- Le correcteur ne juge pas l'intention artistique, seulement des seuils de lisibilité.
