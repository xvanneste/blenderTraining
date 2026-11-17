# CH10.01 — Solutions

<!-- QUIZ_ANSWERS_START -->
## Réponses du quiz

| Q | Réponse | Explication |
|---|---|---|
| Q1 | **a** — Le moteur de rendu temps réel de Blender | Il rend la scène de test en moins d'une seconde dans nos mesures. |
| Q2 | **a** — Active les ombres portées | Rapport ombre / lumière : 0,96 sans, 0,70 avec. |
| Q3 | **a** — La sphère chromée reflète le sol, le mur et la boule | Écart-type de la luminance de la sphère : 0,008 sans, 0,081 avec. |
| Q4 | — | Un métal parfait n'a pas de couleur propre : il ne montre que ce qu'il reflète ; sans ray tracing il reflète seulement le monde (image plate). |
| Q5 | — | Non : approximation en espace écran : ce qui n'est pas visible à l'image ne peut pas être reflété ; le reflet n'est pas celui de Cycles. |
| Q6 | **a** — Render Properties > Sampling > Render > Samples | Panneau relu dans bl_ui/properties_render.py (taa_render_samples). |
| Q7 | **a** — 16 à 128 | Contre-exemples : 8 et 512. |
| Q8 | — | Mesuré : avec Raytracing et 1 échantillon l'écart-type n'est que de 0,022 (bruit non lissé) contre 0,081 à 64 : le ray tracing a besoin de plusieurs échantillons pour converger. |
| Q9 | — | Je n'ai pas réussi à mesurer son effet sur cette scène : l'activer ne changeait aucune zone mesurée ; le chapitre le dit au lieu de l'inventer. |
| Q10 | — | Une scène, trois zones fixes de l'image ; la mesure vérifie la présence d'un effet, pas sa qualité ni son temps de rendu. |
<!-- QUIZ_ANSWERS_END -->

## Exercices
`COMPLETED_EXAMPLES/ch10_01_eevee_solution.blend` (+ `_reference.png`)

**Fabrication.** Générées par script (`build_ch10_01_files.py`) : sol, mur, boule, sphère chromée, soleil ; mesures par rendu EEVEE. Score 32/32 ; starter 11/32. Rendus regardés.

## Contre-épreuve du correcteur (`COMPLETED_EXAMPLES/COUNTER_EXAMPLES/`)
| Fichier faux | Défaut | Tests qui le refusent |
|---|---|---|
| `…_no_shadows` | Shadows désactivé : pas d'ombre (rapport 0,96) | ombres |
| `…_no_raytracing` | Raytracing désactivé : sphère chromée plate (0,008) | ray tracing |
| `…_samples_low` | 8 échantillons | nombre d'échantillons |
| `…_samples_high` | 512 échantillons | nombre d'échantillons |
| `…_cycles` | moteur Cycles au lieu d'EEVEE | moteur de rendu |
Aussi refusé : le starter.

## Limites
- Une seule scène de test.
- Fast GI non mesuré.
- Dépend du GPU.
