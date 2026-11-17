# CH08.06 — Solutions

<!-- QUIZ_ANSWERS_START -->
## Réponses du quiz

| Q | Réponse | Explication |
|---|---|---|
| Q1 | **a** — Gas | Domain Type Gas ; Liquid pour l'eau (CH08.05). |
| Q2 | **a** — Flow Type Fire (ou Fire + Smoke) | Fire + Smoke (BOTH) : flammes et fumée. |
| Q3 | **a** — Alimente le domaine en continu | Le foyer produit du gaz à chaque image. |
| Q4 | — | La température crée de la flottabilité : le gaz chaud monte (paramètres Buoyancy du domaine). |
| Q5 | — | Un foyer de fumée sans flammes : le cache grossit (111 Ko) mais moins qu'avec le feu (165 Ko) ; la configuration exige du feu. |
| Q6 | **a** — Principled Volume relié à la sortie Volume | Material Output > Volume. |
| Q7 | **a** — Par un nœud Attribute « density » | Attribute « density » vers Density ; « flame » vers Emission Strength. |
| Q8 | — | Elle croît avec la quantité de gaz : 62 Ko à l'image 1, 165 Ko à l'image 30 ; sans foyer, 17 Ko constants : la simulation n'a rien produit. |
| Q9 | — | À la résolution 8 le cache reste à 54 Ko (croissance de 1 %) : la grille est trop grossière pour représenter la colonne. |
| Q10 | — | Le mode Modular cuit chaque image dans un fichier ; un cache de 1 à 10 ne donne que 10 fichiers. |
<!-- QUIZ_ANSWERS_END -->

## Exercices
`COMPLETED_EXAMPLES/ch08_06_smoke_solution.blend` (+ `_reference.png`)

**Fabrication.** Générées par script (`build_ch08_06_files.py`) : domaine gaz, foyer, matériau de volume, variantes. Score 38/38 ; starter 2/6 (arrêt anticipé). Courbe de tailles regardée.

## Contre-épreuve du correcteur (`COMPLETED_EXAMPLES/COUNTER_EXAMPLES/`)
| Fichier faux | Défaut | Tests qui le refusent |
|---|---|---|
| `…_no_flow` | le foyer n'est pas un fluide : le cache reste vide (17 Ko constants) | foyer ; taille du cache |
| `…_smoke_only` | foyer de fumée seule : pas de flammes | foyer (type) seul |
| `…_low_res` | résolution 8 | domaine ; taille du cache (croissance nulle) |
| `…_short_cache` | cache de 1 à 10 | domaine ; bake ; taille à l'image 30 |
| `…_no_shader` | pas de shader de volume | shader (seul) |
Aussi refusé : le starter.

## Limites
- Mesure par la taille des fichiers du cache, pas par le contenu de la grille.
- Rendu du volume non testé.
- « smoke_only » n'est refusé que par la configuration.
