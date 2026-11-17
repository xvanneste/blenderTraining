# CH09.12 — Solutions

<!-- QUIZ_ANSWERS_START -->
## Réponses du quiz

| Q | Réponse | Explication |
|---|---|---|
| Q1 | **a** — Il crée de la profondeur et des lignes de regard variées | Mesuré : triangle de 7 m² et angle minimal 39° contre une aire de 0,3 m² au départ. |
| Q2 | **a** — Placer les sujets à des distances différentes de la caméra | Solution : 7,5 m, 9,5 m et 12 m de la caméra. |
| Q3 | **a** — Un personnage peut être caché par un autre depuis la caméra | Contre-exemple occluded : C vaut 0 pixel. |
| Q4 | — | La caméra regarde vers +Y : la distance utile le long de l'axe de visée est y − (−9) ; le correcteur utilise cette différence. |
| Q5 | — | Le dernier instant du plan 1 (image 36) où le blocking doit être lisible. |
| Q6 | **a** — Un objet ou un acteur qui change de place entre deux plans | Départ : A saute de 2,55 m, la tasse de 60 cm. |
| Q7 | **a** — 0,15 m par image (≈ 3,6 m/s à 24 i/s) | Solution : 0,09 m par image au plus (B). |
| Q8 | — | Les cylindres ont un rayon de 0,25 m : moins de 0,5 m ils se traversent ; 0,6 m laisse une marge. |
| Q9 | — | Un défaut peut n'exister qu'à une image (le saut du raccord) : frame_set sur 72 images détecte ce que l'image 36 seule ne montre pas. |
| Q10 | — | Des cylindres sans regard, sans acting ni lumière ; elle valide la géométrie du blocking et la continuité de position, pas la qualité dramatique. |
<!-- QUIZ_ANSWERS_END -->

## Exercices
`COMPLETED_EXAMPLES/ch09_12_staging_solution.blend` (+ `_reference.png`)

**Fabrication.** Générées par script (`build_ch09_12_files.py`) : sol, table, tasse, trois personnages, clés linéaires ; mesures par frame_set et rendu. Score 62/62 ; starter 23/62. Vue de dessus regardée.

## Contre-épreuve du correcteur (`COMPLETED_EXAMPLES/COUNTER_EXAMPLES/`)
| Fichier faux | Défaut | Tests qui le refusent |
|---|---|---|
| `…_line_up` | personnages alignés à y = 1 | triangle ; étagement |
| `…_flat_depth` | triangle mais profondeur étalée sur 2 m seulement | étagement |
| `…_teleport` | A saute de 2 m au raccord | continuité des personnages ; vitesse |
| `…_cup_moved` | la tasse change de place au raccord | continuité de la tasse |
| `…_too_fast` | A traverse 2 m en 4 images | vitesse |
| `…_occluded` | C caché derrière A | visibilité |
| `…_collision` | B finit à 0,36 m de A | distance entre personnages |
Aussi refusé : le starter.

## Limites
- Cylindres sans regard ni jeu.
- Géométrie seulement.
- Raccourcis non regardés à l'écran.
