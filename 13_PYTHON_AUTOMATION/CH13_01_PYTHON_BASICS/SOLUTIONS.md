# CH13.01 — Solutions

<!-- QUIZ_ANSWERS_START -->
## Réponses du quiz

| Q | Réponse | Explication |
|---|---|---|
| Q1 | **a** — None | Sans return, Python renvoie None : c'est l'état du starter. |
| Q2 | **a** — range(1, 4) | range(début, fin) exclut la fin : range(1, count + 1) pour count éléments à partir de 1. |
| Q3 | **a** — 007 | 03d : entier sur 3 chiffres complété par des zéros. |
| Q4 | — | Parce que sum([]) / len([]) divise par zéro (ZeroDivisionError) ; on teste « if not valeurs » et on renvoie 0.0. |
| Q5 | — | x : il varie d'abord (ligne par ligne) ; y est la boucle extérieure, qui varie le plus lentement. |
| Q6 | **a** — bpy.context.object | Le nouvel objet devient l'objet actif ; on le renomme avec ob.name. |
| Q7 | **a** — location=position dans l'opérateur | primitive_cube_add(size=1.0, location=p). |
| Q8 | — | Les cubes sont créés mais tous à l'origine : il manque location=p ; seul le contrôle de position échoue (les noms et le nombre sont justes). |
| Q9 | — | Les erreurs se cachent dans les cas limites : division par zéro, boucle qui ne tourne jamais ; un test qui ne couvre que le cas normal les rate. |
| Q10 | — | La dernière ligne donne le type et le message (ZeroDivisionError : division by zero) ; les lignes au-dessus donnent l'endroit (fichier, ligne). |
<!-- QUIZ_ANSWERS_END -->

## Exercices
`COMPLETED_EXAMPLES/ch13_01_python_solution.blend` (+ `_reference.png`)

**Fabrication.** Générées par script (`build_ch13_01_files.py`) : un Texte exercise.py (cinq fonctions) dans chaque fichier ; solution exécutée pour créer la grille de la référence. Score 56/56 ; starter 6/56. Rendu regardé.

## Contre-épreuve du correcteur (`COMPLETED_EXAMPLES/COUNTER_EXAMPLES/`)
| Fichier faux | Défaut | Tests qui le refusent |
|---|---|---|
| `…_clamp_swapped` | bornes inversées dans clamp | clamp (seul) |
| `…_average_crash` | division par zéro sur la liste vide | average (seul) |
| `…_grid_swapped` | x et y échangés dans la grille | grid_positions (seul) |
| `…_names_nopad` | numéros sans zéros (Rock_1) | numbered_names (seul) |
| `…_cubes_origin` | cubes tous à l'origine | position des cubes (seul) |
Aussi refusé : le starter.

## Limites
- Les fonctions pures ont un délai de 5 s ; make_cubes n'en a pas (exécutée dans le fil principal).
- Le correcteur teste des comportements, pas la qualité ni le style du code.
- Seules les bases de Python sont couvertes (classes, modules, exceptions : CH13.02 et suivants).
