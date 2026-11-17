# CH09.07 — Solutions

<!-- QUIZ_ANSWERS_START -->
## Réponses du quiz

| Q | Réponse | Explication |
|---|---|---|
| Q1 | **a** — L'image en 9 par 2 lignes horizontales et 2 verticales | Les intersections sont des points forts. |
| Q2 | **a** — Sur un tiers horizontal | Le milieu coupe l'image en deux moitiés égales : statique. |
| Q3 | **a** — Pour éviter un cadrage qui coupe le sujet par accident | Marge ≥ 3 % dans le correcteur. |
| Q4 | — | À 67 % de la hauteur le cadre descend de 0,17 : les pieds, déjà à 85 %, sortent du cadre : l'horizon haut convient mieux avec une caméra à 1,6 m. |
| Q5 | — | Sujet à 50 % et horizon à 51 % : tout est symétrique : le plan est stable mais statique. |
| Q6 | **a** — Décale le cadre horizontalement sans tourner la caméra | Positif : le sujet se déplace vers la gauche dans l'image (mesuré : +0,167 → 33 %). |
| Q7 | **a** — Négatif | Mesuré : −0,1 → horizon à 33 % depuis le haut ; +0,1 → 69 %. |
| Q8 | — | Le décalage garde les verticales parallèles (pas de perspective ascendante) : le cylindre reste vertical dans l'image. |
| Q9 | — | Il segmente le ciel (bleu), prend pour chaque colonne sans sujet la dernière ligne de ciel et en fait la moyenne. |
| Q10 | — | Elle suppose un sujet unique et simple ; elle ne juge ni l'équilibre des masses ni la direction du regard (lead room). |
<!-- QUIZ_ANSWERS_END -->

## Exercices
`COMPLETED_EXAMPLES/ch09_07_composition_solution.blend` (+ `_reference.png`)

**Fabrication.** Générées par script (`build_ch09_07_files.py`) : sol, sujet, caméra avec Shift ; calibrations par rendu. Score 37/37 ; starter 21/37. Rendus regardés.

## Contre-épreuve du correcteur (`COMPLETED_EXAMPLES/COUNTER_EXAMPLES/`)
| Fichier faux | Défaut | Tests qui le refusent |
|---|---|---|
| `…_subject_right` | sujet au tiers droit (67 %) | sujet au tiers gauche |
| `…_horizon_middle` | horizon au milieu (51 %) | horizon au tiers haut |
| `…_cropped` | caméra avancée de 6 m : sujet coupé en bas et en haut | cadre (marges) |
| `…_tiny_subject` | caméra reculée de 12 m : sujet de 14 % de la hauteur | taille du sujet |
| `…_centered` | composition de départ : tout au centre | tiers ; horizon |
Aussi refusé : le starter.

## Limites
- Sujet unique et fond uni.
- Couleurs de segmentation fixes.
- Affichage des guides non regardé dans l'interface.
