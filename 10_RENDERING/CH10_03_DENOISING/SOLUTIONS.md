# CH10.03 — Solutions

<!-- QUIZ_ANSWERS_START -->
## Réponses du quiz

| Q | Réponse | Explication |
|---|---|---|
| Q1 | **a** — Du grain dû à un nombre d'échantillons insuffisant | 4 échantillons : EQM 0,073 contre la référence. |
| Q2 | **a** — Il estime l'image propre à partir de l'image bruitée | Sur CPU, sans carte NVIDIA. |
| Q3 | **a** — Render Properties > Sampling > Render > Denoise (case d'en-tête) | Panneau relu dans addons_core/cycles/ui.py. |
| Q4 | — | Le débruitage est très peu coûteux : 4 échantillons débruités donnent EQM 0,056 ; 64 échantillons coûtent 16 fois plus de calcul (EQM 0,0085). |
| Q5 | — | Non : EQM 0,110 et contraste 1,29 : trop peu d'information ; le débruiteur devine mal. |
| Q6 | **a** — Un préfiltre None n'apporte presque rien (EQM 0,071 contre 0,073) | Les passes d'aide bruitées guident mal le débruiteur. |
| Q7 | **a** — Si le damier garde son contraste (écart-type / référence) | Entre 0,85 et 1,15 ; le bruit l'augmente, un flou le baisse. |
| Q8 | — | Elle sert de vérité de terrain : à 256 échantillons le bruit résiduel est faible ; c'est ce que mesure l'EQM. |
| Q9 | — | OptiX demande une carte NVIDIA et l'énumération des débruiteurs est dynamique (vide en arrière-plan) : je n'ai pas pu le tester dans le correcteur. |
| Q10 | — | Une scène, un damier, une zone, une graine : elle ne juge pas le débruitage d'animations (scintillement entre images) ni les passes (CH10.04). |
<!-- QUIZ_ANSWERS_END -->

## Exercices
`COMPLETED_EXAMPLES/ch10_03_denoising_solution.blend` (+ `_reference.png`)

**Fabrication.** Générées par script (`build_ch10_03_files.py`) : plan et sphère à damier fin, lampe de zone ; mesures contre une référence de 256 échantillons. Score 33/33 ; starter 17/33. Rendus regardés.

## Contre-épreuve du correcteur (`COMPLETED_EXAMPLES/COUNTER_EXAMPLES/`)
| Fichier faux | Défaut | Tests qui le refusent |
|---|---|---|
| `…_no_denoise` | débruitage désactivé | débruitage ; EQM |
| `…_no_prefilter` | préfiltre None : EQM 0,071 | préfiltre ; EQM |
| `…_one_sample` | 1 échantillon : EQM 0,110, contraste 1,29 | EQM ; contraste |
| `…_too_many_samples` | 64 échantillons : hors budget | budget |
Aussi refusé : le starter.

## Limites
- OpenImageDenoise seulement.
- Une scène, une graine.
- Animations non traitées.
