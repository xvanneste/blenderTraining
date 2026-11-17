# CH11.10 — Solutions

<!-- QUIZ_ANSWERS_START -->
## Réponses du quiz

| Q | Réponse | Explication |
|---|---|---|
| Q1 | **a** — Le dessus du cube est presque deux fois plus lumineux que le sol de la plaque (en luminance affichée) | Avec Exposure −2 : 1,01. |
| Q2 | **a** — La luminance affichée est comprimée par l'encodage sRGB : −1 donne encore 1,37 | Mesuré : −1 → 1,37 ; −2 → 1,01 (rapport sur les valeurs affichées). |
| Q3 | **a** — L'écart de (rouge − bleu) entre le cube et le sol de la plaque | Départ −0,20 : cube plus bleu que la plaque ; solution +0,007. |
| Q4 | — | La plaque est déjà juste : corriger l'image entière la fausserait ; on raccorde l'élément 3D à la plaque. |
| Q5 | — | Un cube à la bonne luminosité mais neutre : écart de dominante −0,169 : un seul critère juste ne suffit pas. |
| Q6 | **a** — Deux rendus à graines différentes : écart-type de la différence / √2 | Bruit du cube 0,012 (2 échantillons) contre 0,011 pour la plaque. |
| Q7 | **a** — Il n'y a pas de nœud de grain dédié trouvé en 5.3 : on s'appuie sur le bruit naturel de Cycles non débruité | Solution : 2 échantillons sans débruitage. |
| Q8 | — | Le bruit varie avec la graine et le patch ; la plaque mesure 0,011 : on accepte un facteur de l'ordre de 2 autour de cette valeur. |
| Q9 | — | Noirs, flou de mouvement, distorsion, reflets du sol sur l'objet, netteté : le chapitre n'en mesure que trois critères. |
| Q10 | — | Un patch sur le dessus d'un cube gris : pas de matériaux complexes ni de texture ; l'exposition est comparée en valeurs affichées, pas en lumière. |
<!-- QUIZ_ANSWERS_END -->

## Exercices
`COMPLETED_EXAMPLES/ch11_10_consistency_solution.blend` (+ `_reference.png`)

**Fabrication.** Générées par script (`build_ch11_10_files.py`) : plaque granuleuse, cube, arbre Alpha Over ; mesures à deux graines. Score 39/39 ; starter 15/39. Rendus regardés.

## Contre-épreuve du correcteur (`COMPLETED_EXAMPLES/COUNTER_EXAMPLES/`)
| Fichier faux | Défaut | Tests qui le refusent |
|---|---|---|
| `…_exposure_only` | exposition juste mais cube neutre (−0,169) | dominante |
| `…_warm_only` | chaud mais trop clair (rapport 1,89) | exposition |
| `…_clean_cube` | exposition et couleur justes mais 128 échantillons (bruit 0,0016) | grain |
Aussi refusé : le starter.

## Limites
- Trois critères.
- Cube gris, patch unique.
- Pas de grain de film.
