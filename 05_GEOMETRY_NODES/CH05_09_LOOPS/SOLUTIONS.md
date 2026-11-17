# CH05.09 — Solutions

<!-- QUIZ_ANSWERS_START -->
## Réponses du quiz

| Q | Réponse | Explication |
|---|---|---|
| Q1 | **a** — Un groupe de nœuds exécuté plusieurs fois, avec un état transmis d'une itération à la suivante | Repeat Input → nœuds → Repeat Output : l'état (ici la géométrie) bouclé n fois. |
| Q2 | **b** — Le numéro de l'itération en cours (0, 1, 2…) | On s'en sert pour placer chaque élément : rotation = Iteration × Angle. |
| Q3 | **a** — Join Geometry reçoit l'état précédent ET la nouvelle marche | Sans l'état précédent dans le Join, chaque itération remplace la précédente (1 seule marche). |
| Q4 | — | Pour que l'escalier ne contienne que les marches : le plan d'entrée ne s'y ajoute pas ; la zone part d'une géométrie vide. |
| Q5 | — | 0,05 + 9 × 0,18 = 1,67 m (centre de la marche). |
| Q6 | **b** — Une rotation tourne autour de l'origine : la translation préalable place la marche à distance de l'axe, puis la rotation la fait tourner autour | D'où deux Transform : (1) Translation x = Radius ; (2) Rotation z puis Translation z. |
| Q7 | **a** — Par composantes connexes de la géométrie évaluée | Chaque marche est une pièce séparée : le nombre de composantes vaut Steps. |
| Q8 | — | Un Join sans l'état précédent : une seule marche (la dernière) au lieu de Steps ; on voit que la zone existe et tourne mais ne conserve rien. |
| Q9 | — | Repeat boucle un nombre fixe de fois dans une même image ; Simulation fait évoluer l'état image après image (cache, bake) : on y programme particules, croissance… Elle n'est pas évaluée ici. |
| Q10 | — | À exécuter des nœuds pour chaque élément d'un domaine (point, face, instance…) avec accès à ses valeurs : un traitement par élément plutôt que par champ. |
<!-- QUIZ_ANSWERS_END -->

## Exercice 2
`COMPLETED_EXAMPLES/ch05_09_loops_solution.blend` (+ `_reference.png`).

**Fabrication.** Générée par script (`build_ch05_09_files.py`) : zone créée par `GeometryNodeRepeatInput`/`Output` appariés (`pair_with_output`). Score du correcteur 43/43 ; starter 3/11 (zone et interface absentes : arrêt anticipé).
Mesures : voir THEORY.md §3. Rendu regardé : un escalier en spirale ; deux réglages (16 marches, puis 30 marches plus larges) ; cadrage élargi une fois.

## Contre-épreuve du correcteur (`COMPLETED_EXAMPLES/COUNTER_EXAMPLES/`)
| Fichier faux | Défaut | Tests qui le refusent |
|---|---|---|
| `…_fixed_steps` | Iterations codé en dur à 16 | Iterations alimenté ; réglage B : nombre de marches (16 au lieu de 30) |
| `…_no_rotation` | pas de rotation (colonne droite) | Écart angulaire, réglages A et B |
| `…_no_rise` | pas de montée (marches à plat) | Contremarche et écart angulaire (les marches sont toutes à la même hauteur : l'ordre par z devient arbitraire), réglages A et B |
| `…_no_accumulate` | Join sans l'état précédent (1 seule marche) | Nombre de marches (1) ; mesures impossibles |
| `…_radius_ignored` | rayon codé en dur à 1,2 m | Réglage B : rayon (1,20 au lieu de 2,00 ; passe le réglage A) |
Aussi refusé : le starter.

## Limites
- Seule la Repeat Zone est évaluée.
- Le tri par altitude suppose des marches à des hauteurs distinctes (Rise > 0).
