# CH10.05 — Solutions

<!-- QUIZ_ANSWERS_START -->
## Réponses du quiz

| Q | Réponse | Explication |
|---|---|---|
| Q1 | **a** — 200 | Un par rocher : ME_Rock_000 … ME_Rock_199. |
| Q2 | **a** — Un empty qui affiche une collection sans la dupliquer | L'objet source n'est évalué qu'une fois. |
| Q3 | **a** — Plusieurs objets partagent le même maillage en mémoire | Object > Link/Transfer Data > Link Object Data (Ctrl+L). |
| Q4 | — | Non : chaque objet applique son modificateur : 200 objets à Subdivision Surface niveau 2 = 384 000 triangles (contre-exemple high_poly). |
| Q5 | — | Pour qu'elle ne s'affiche pas en plus des instances : elle n'est évaluée que par les instances. |
| Q6 | **a** — 64 Mo (4 096 × 4 096 × 4 octets) | Avec Texture Limit 1024 : 4 Mo. |
| Q7 | **a** — Render Properties > Simplify > Render > Texture Limit | Réglage `Scene.cycles.texture_limit_render` : « OFF », 128, 256, 512, 1024… ; actif avec Simplify. |
| Q8 | — | Il parcourt les instances du graphe de dépendances, évalue chaque objet source une seule fois (modificateurs inclus) et additionne les triangles. |
| Q9 | — | Les contraintes sont des budgets (≤ 5 maillages, ≤ 100 000 triangles, ≤ 16 Mo) : instances ou maillage partagé au niveau 0 tiennent le budget ; c'est le résultat qui compte. |
| Q10 | — | Elle compte des proxys (triangles, Mo de textures) : elle ne mesure pas la mémoire réelle du processus, ni la mémoire GPU, ni le temps de rendu ; pas de LOD ni de simplification des particules. |
<!-- QUIZ_ANSWERS_END -->

## Exercices
`COMPLETED_EXAMPLES/ch10_05_memory_solution.blend` (+ `_reference.png`)

**Fabrication.** Générées par script (`build_ch10_05_files.py`) : 200 rochers, matériau à texture 4 096², variantes ; mesures par graphe de dépendances. Score 34/34 ; starter 10/34. Rendu regardé.

## Contre-épreuve du correcteur (`COMPLETED_EXAMPLES/COUNTER_EXAMPLES/`)
| Fichier faux | Défaut | Tests qui le refusent |
|---|---|---|
| `…_unique_meshes` | 200 maillages différents (niveau 0, texture limitée) | nombre de maillages |
| `…_high_poly` | un maillage partagé mais niveau 2 : 384 000 triangles | triangles évalués |
| `…_big_texture` | instances mais texture 4 096 sans limite | textures |
| `…_few_rocks` | 50 rochers seulement | rochers conservés |
Aussi refusé : le starter.

## Limites
- Proxys, pas la mémoire réelle.
- Pas de LOD.
- Panneaux non regardés à l'écran.
