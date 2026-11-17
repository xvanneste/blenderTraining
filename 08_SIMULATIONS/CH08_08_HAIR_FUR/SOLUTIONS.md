# CH08.08 — Solutions

<!-- QUIZ_ANSWERS_START -->
## Réponses du quiz

| Q | Réponse | Explication |
|---|---|---|
| Q1 | **a** — Hair | Type Hair : brins attachés à une racine. |
| Q2 | **a** — Groupe de sommets en densité | Vertex Groups > Density. |
| Q3 | **a** — Multiplier les brins sans les simuler tous | Interpolated : suivent les parents voisins. |
| Q4 | — | Il rassemble les enfants autour de leur parent : des mèches. Mesuré : distance moyenne extrémité enfant–parent 73 mm à 0, 39 mm à 0,5, 0 à 1. |
| Q5 | — | On ne simule que les parents ; les enfants sont déduits : plus rapide, même densité visuelle. |
| Q6 | **a** — Hair Dynamics du système de particules | Panneau Hair Dynamics (`ps.use_hair_dynamics`). |
| Q7 | **a** — `co_hair(particle_no=nb_parents + j)` | Les enfants n'ont pas de hair_keys : `co_hair` donne le point d'une étape (0 à 4 ici). |
| Q8 | — | Hauteur moyenne des pointes : 0,96 m à l'image 1, 0,28 m à l'image 30 : les cheveux retombent ; sans dynamique : 0 m de chute. |
| Q9 | — | Sans densité par groupe, les racines sont réparties sur toute la sphère : z minimal −0,98 m au lieu de 0,23 m. |
| Q10 | — | La dynamique de cheveux est une simulation : il faut avancer image par image depuis l'image 1. |
<!-- QUIZ_ANSWERS_END -->

## Exercices
`COMPLETED_EXAMPLES/ch08_08_hair_solution.blend` (+ `_reference.png`)

**Fabrication.** Générées par script (`build_ch08_08_files.py`) : tête, groupe de sommets, système Hair, variantes. Score 56/56 ; starter 2/7. Vue de face regardée.

## Contre-épreuve du correcteur (`COMPLETED_EXAMPLES/COUNTER_EXAMPLES/`)
| Fichier faux | Défaut | Tests qui le refusent |
|---|---|---|
| `…_no_group` | pas de groupe de densité : des cheveux poussent sous la tête | racines sur la calotte |
| `…_no_children` | pas d'enfants : 300 brins seulement | enfants ; mèches |
| `…_no_clump` | Clumping 0 : pas de mèches | Clumping ; mèches |
| `…_no_dynamics` | pas de Hair Dynamics : les cheveux restent dressés | dynamique |
| `…_short` | cheveux de 0,15 m | longueur ; dynamique |
| `…_too_few` | 50 cheveux | nombre ; enfants ; mèches |
Aussi refusé : le starter.

## Limites
- Rendu des cheveux et collision avec la tête non traités.
- Curves et nœuds de cheveux non testés.
- Lecture des enfants par `co_hair` (étapes 0–4).
