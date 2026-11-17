# CH09.03 — Solutions

<!-- QUIZ_ANSWERS_START -->
## Réponses du quiz

| Q | Réponse | Explication |
|---|---|---|
| Q1 | **a** — Image à grande plage dynamique | High Dynamic Range Image : valeurs bien au-delà de 1. |
| Q2 | **a** — Sa valeur est écrêtée à 1 | Dans l'exercice le soleil vaut 1 500 en flottant, 1 en 8 bits (contre-exemple ldr_image). |
| Q3 | **a** — Environment Texture | Branché sur Background > Color. |
| Q4 | — | Elle n'est plus éclairée par le soleil (chaud) mais seulement par le ciel (bleu) : bleu / rouge = 1,68 mesuré. |
| Q5 | — | Une source très lumineuse et petite dans l'image (le disque de soleil de 2,5°) ; un soleil flou donnerait une ombre douce. |
| Q6 | **a** — Rotation Z du nœud Mapping | 180° amène le soleil à gauche : l'ombre part vers +X. |
| Q7 | **a** — Background > Strength | Strength 1 : sol à 0,59 ; 0,3 : 0,18 ; 3 : 1,77 (proportionnel). |
| Q8 | — | Avec 90° l'ombre part vers +Y (angle 90° mesuré) : l'orientation est visible dans l'image, pas dans la valeur Strength. |
| Q9 | — | Sans perspective, la direction de l'ombre se lit comme un angle dans l'image (0° = vers +X) et sa longueur comme une distance. |
| Q10 | — | 1 m / tan(20°) = 2,75 m ; mesuré 2,56 m (pointe floue). Le correcteur ne mesure que la direction (au moins 30 pixels). |
<!-- QUIZ_ANSWERS_END -->

## Exercices
`COMPLETED_EXAMPLES/ch09_03_natural_hdri_solution.blend` (+ `_reference.png`)

**Fabrication.** Générées par script (`build_ch09_03_files.py`) : HDRI EXR générée, monde à nœuds, scène, variantes ; calibration par rendu. Score 32/32 ; starter 18/32. Vue du dessus regardée.

## Contre-épreuve du correcteur (`COMPLETED_EXAMPLES/COUNTER_EXAMPLES/`)
| Fichier faux | Défaut | Tests qui le refusent |
|---|---|---|
| `…_wrong_rotation` | rotation 90° : l'ombre part vers +Y | direction de l'ombre |
| `…_too_dark` | Strength 0,3 : sol à 0,18 | exposition |
| `…_too_bright` | Strength 3 : sol à 1,77 | exposition |
| `…_no_hdri` | fond gris uni, sans HDRI | HDRI (et tout ce qui en dépend) |
| `…_ldr_image` | même image écrêtée en 8 bits : soleil à 1, plus d'ombre nette | image flottante ; ombre |
Aussi refusé : le starter.

## Limites
- HDRI synthétique, un seul instant.
- Direction de l'ombre seulement.
- Pas de Sky Texture.
