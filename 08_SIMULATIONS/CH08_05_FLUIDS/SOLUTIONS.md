# CH08.05 — Solutions

<!-- QUIZ_ANSWERS_START -->
## Réponses du quiz

| Q | Réponse | Explication |
|---|---|---|
| Q1 | **a** — La boîte qui contient la simulation | FLUID_Domain : cube de 2 m ; tout ce qui sort est perdu. |
| Q2 | **a** — À alimenter le domaine en liquide ou en gaz | FLUID_Source : Flow Type Liquid, Behavior Geometry. |
| Q3 | **a** — Remplit le volume de l'objet avec du liquide | Le cube de 0,6 m devient du liquide à l'image 1. |
| Q4 | — | Elle fixe la finesse de la grille : à 8 le liquide est un maillage grossier (380 sommets à l'image 20) ; à 32, 18 594 sommets. |
| Q5 | — | Aucun liquide n'est créé : le domaine reste vide (contre-exemple « gas_flow »). |
| Q6 | **a** — Les données puis le maillage | bake_data puis bake_mesh : 20 fichiers de maillage. |
| Q7 | **a** — Dans un dossier de cache du domaine | Cache modulaire : data/ (.vdb), mesh/ (.bobj.gz), config/. |
| Q8 | — | Le z minimal de la surface à l'image 20 : −0,475 m (le fond du domaine en repère local) ; à l'image 1 : −0,056 m. |
| Q9 | — | Le liquide n'a pas le temps de tomber (z minimal −0,15 m) ni de s'étaler (0,34 m). |
| Q10 | — | Pour ne pas modifier le fichier de l'apprenant ni dépendre d'un cache déjà cuit. |
<!-- QUIZ_ANSWERS_END -->

## Exercices
`COMPLETED_EXAMPLES/ch08_05_fluid_solution.blend` (+ `_reference.png`)

**Fabrication.** Générées par script (`build_ch08_05_files.py`) : cubes bmesh, modificateurs FLUID (domaine et Flow). Score 43/43 ; starter 2/6 (arrêt anticipé). Surface du liquide lue dans le cache, profil regardé.

## Contre-épreuve du correcteur (`COMPLETED_EXAMPLES/COUNTER_EXAMPLES/`)
| Fichier faux | Défaut | Tests qui le refusent |
|---|---|---|
| `…_no_flow` | la source n'est pas un fluide : le domaine est vide | source ; bake (aucun liquide) |
| `…_gas_flow` | la source est de la fumée : pas de liquide | source ; bake (aucun liquide) |
| `…_low_res` | résolution 8 : maillage grossier | domaine ; chute ; sommets |
| `…_short_cache` | cache de 1 à 5 : trop court | domaine ; bake ; chute ; étalement ; sommets |
Aussi refusé : le starter.

## Limites
- Un liquide qui tombe ; pas d'obstacle ni de viscosité.
- Le correcteur cuit à chaque exécution (moins d'une seconde à la résolution 32).
- Pas de contre-exemple « sans gravité » (propriété sans effet mesuré).
