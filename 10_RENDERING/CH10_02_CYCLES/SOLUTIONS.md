# CH10.02 — Solutions

<!-- QUIZ_ANSWERS_START -->
## Réponses du quiz

| Q | Réponse | Explication |
|---|---|---|
| Q1 | **a** — Le nombre de rebonds de la lumière sur les surfaces mates | Départ : 0 → plafond à 0,01 ; solution : 4 → 0,33. |
| Q2 | **a** — La lampe éclaire vers le bas : le plafond n'est atteint que par la lumière indirecte | Sans rebond diffus, il ne reçoit que du bruit résiduel. |
| Q3 | **a** — Render Properties > Light Paths > Max Bounces > Diffuse | Panneau relu dans addons_core/cycles/ui.py. |
| Q4 | — | Dans une pièce fermée la lumière du jour ou d'une lampe n'arrive que par rebonds : trop peu de rebonds laisse des zones noires. |
| Q5 | — | Un plafond à 0,013 au lieu de 0,33 : la lumière indirecte disparaît sans rien changer d'autre. |
| Q6 | **a** — Il arrête les pixels déjà propres et continue sur les pixels bruités | Case dans l'en-tête de Sampling > Render ; seuil : Noise Threshold. |
| Q7 | **a** — Moins de bruit et plus de temps | Seuil 0,5 : bruit 0,0138 ; seuil 0,02 : 0,0097 (64 échantillons maximum). |
| Q8 | — | Il rend deux fois avec deux graines (Seed) et prend l'écart-type de la différence sur le mur, divisé par √2. |
| Q9 | — | C'est un plafond de coût, pas un gain de qualité : le correcteur limite Max Samples à 256 ; les contre-exemples montrent que 64 suffisent ici (bruit 0,0097). |
| Q10 | — | Une pièce simple, un patch de mur, CPU et sans débruitage ; Light Tree, caustiques et rebonds glossy ne sont pas mesurés ; le temps de rendu n'est pas évalué. |
<!-- QUIZ_ANSWERS_END -->

## Exercices
`COMPLETED_EXAMPLES/ch10_02_cycles_solution.blend` (+ `_reference.png`)

**Fabrication.** Générées par script (`build_ch10_02_files.py`) : pièce ouverte, lampe de zone orientée vers le bas, deux rendus par mesure. Score 36/36 ; starter 18/36. Rendus regardés.

## Contre-épreuve du correcteur (`COMPLETED_EXAMPLES/COUNTER_EXAMPLES/`)
| Fichier faux | Défaut | Tests qui le refusent |
|---|---|---|
| `…_no_indirect` | Diffuse 0 : plafond noir (0,013) | lumière indirecte |
| `…_few_samples` | 4 échantillons : bruit 0,049 | échantillons ; bruit |
| `…_no_adaptive` | échantillonnage adaptatif désactivé | adaptatif |
| `…_loose_threshold` | seuil 0,5 | Noise Threshold |
| `…_too_many_samples` | 4 096 échantillons maximum | Max Samples |
Aussi refusé : le starter.

## Limites
- Une pièce simple.
- Light Tree et caustiques non mesurés.
- CPU, sans débruitage.
