# CH05.03 — Solutions

<!-- QUIZ_ANSWERS_START -->
## Réponses du quiz

| Q | Réponse | Explication |
|---|---|---|
| Q1 | **b** — Une référence à une géométrie partagée, placée par une matrice | Les instances partagent la même géométrie : seule leur transformation diffère, d'où un coût mémoire très faible. |
| Q2 | **b** — Un maillage ou un nuage de points : une instance par sommet | Chaque sommet de la géométrie reçue devient la position d'une instance. |
| Q3 | **b** — Le Cylinder est centré : son origine doit être à sa base pour qu'il se pose sur le point | Le point d'instance est l'origine de la géométrie : elle doit se trouver au pied du piquet. |
| Q4 | — | 441 (21 × 21), une par sommet. |
| Q5 | — | Rotation, Scale (et Pick Instance / Instance Index pour choisir parmi plusieurs géométries). |
| Q6 | **a** — Random Value (Vector, Max z = 6,283) → Rotation | 2π radians = un tour complet ; chaque instance reçoit un angle différent. |
| Q7 | **b** — Il transforme chaque instance en géométrie propre : 441 fois les sommets, plus de partage | Le correcteur exige de garder des instances ; réaliser ne se justifie que si l'on doit modifier la géométrie par la suite. |
| Q8 | — | Trop peu : pas un champ ; trop (3 600 ici) : coût inutile dans l'exercice. Dans un vrai décor on règle la densité selon la caméra. |
| Q9 | — | Il calcule la longueur du vecteur moyen des angles de lacet : proche de 0 pour des angles uniformément répartis (0,06 mesuré), proche de 1 si tous identiques. |
| Q10 | — | Quand on doit déformer ou fusionner chaque copie (Set Position sur la géométrie réalisée, export, booléens) ; sinon on garde les instances. |
<!-- QUIZ_ANSWERS_END -->

## Exercice 2
`COMPLETED_EXAMPLES/ch05_03_instances_solution.blend` (+ `_reference.png`).

**Fabrication.** Générée par script (`build_ch05_03_files.py`). Score du correcteur 38/38 ; starter 10/38.
Mesures : 441 instances ; emprise 8,0 × 8,0 m ; échelles 0,60–1,40 ; vecteur moyen des angles 0,056 ; écart de base 0,000 m ; MAT_Post.
Rendu regardé : un champ de piquets de hauteurs et d'orientations variées ; la première version était cadrée trop serré.

## Contre-épreuve du correcteur (`COMPLETED_EXAMPLES/COUNTER_EXAMPLES/`)
| Fichier faux | Défaut | Tests qui le refusent |
|---|---|---|
| `…_realized` | Realize Instances ajouté | Pas de Realize Instances ; plus d'instance évaluée (donc nombre, emprise, échelles, orientations, bases, matériau : conséquences du même défaut) |
| `…_no_random` | Rotation et Scale non alimentés | Rotation ; Scale ; échelles ; orientations (même défaut) |
| `…_sunk` | piquet non relevé (enfoncé) | Bases à z = 0 (seul) |
| `…_sparse` | Grid 4 × 4 (16 instances) | Nombre d'instances (seul) |
| `…_too_dense` | Grid 60 × 60 (3 600 instances) | Nombre d'instances (seul) |
| `…_no_material` | sans Set Material | Set Material ; matériau des instances (même défaut) |
Aussi refusé : le starter.

## Limites
- Contrôle du graphe et énumération des instances ; aucune appréciation de la composition.
- Les bornes 100–1 600 sont celles de l'exercice, pas des règles générales.
