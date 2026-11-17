# CH04.08 — Solutions

<!-- QUIZ_ANSWERS_START -->
## Réponses du quiz

| Q | Réponse | Explication |
|---|---|---|
| Q1 | **c** — Displacement | Seul le displacement déplace la géométrie ; bump et normal map ne changent que l'ombrage. |
| Q2 | **b** — Normal map ou bump | Elles ne demandent pas de polygones supplémentaires. |
| Q3 | **b** — Une hauteur en normale perturbée | Bump dérive une normale d'un champ de hauteur (CH04.05). |
| Q4 | — | Elle ne déplace pas les sommets : la silhouette reste celle du maillage, le relief disparaît de profil. |
| Q5 | — | Pas d'image ni de bake : il se dérive directement d'une texture procédurale ou d'une image de hauteur ; réglage immédiat. |
| Q6 | **a** — 0,5 : la surface reste en moyenne à sa place | Le déplacement vaut (Height − Midlevel) × Scale : au niveau moyen il est nul. |
| Q7 | **a** — Displacement : Displacement Only ou Displacement and Bump | Material Properties > Settings > Displacement (propriété displacement_method) ; par défaut c'est Bump Only. |
| Q8 | — | Le déplacement agit sur les sommets : il faut des sommets en nombre suffisant, donc une subdivision (adaptive ou niveaux de rendu élevés). |
| Q9 | — | Le relief dépasse la moitié de la largeur : le sol devient montagneux et l'échelle est absurde ; le correcteur exige 0,02–0,3 m. |
| Q10 | — | Le vrai displacement (Displacement Only) y est pris en charge ; dans les sources de l'interface 5.3, ce mode est signalé « Unsupported displacement method » pour EEVEE. Nous utilisons donc Cycles pour la solution. |
<!-- QUIZ_ANSWERS_END -->

## Exercice 2
`COMPLETED_EXAMPLES/ch04_08_relief_solution.blend` (+ `_reference.png`).

**Fabrication.** Générée par script (`build_ch04_08_files.py`). Cycles CPU, 24 échantillons, sans débruitage ; soleil rasant (14° d'élévation) ; Noise (Scale 0,9 ; Detail 4 ; Roughness 0,55) → Displacement (Midlevel 0,5 ; Scale 0,25 m) ; `displacement_method = DISPLACEMENT` ; Subdivision Surface Simple, adaptatif. Score du correcteur 20/20 ; starter 2/20.
Rendu regardé : la ligne d'horizon du sol ondule (vrai déplacement des sommets) et le relief est lisible en lumière rasante. Une première version (Scale 0,15 ; bruit trop fin) donnait un relief à peine visible : amplitude et échelle du bruit augmentées.

## Contre-épreuve du correcteur (`COMPLETED_EXAMPLES/COUNTER_EXAMPLES/`)
| Fichier faux | Défaut | Test qui le refuse (et lui seul) |
|---|---|---|
| `…_method_bump` | méthode Bump Only | Material > Settings > Displacement |
| `…_no_subdiv` | pas de modificateur Subdivision Surface | Maillage subdivisé |
| `…_huge_scale` | Scale 3 m | Displacement Scale |
| `…_const_height` | Height non reliée | Height alimentée par une texture |
| `…_unlinked` | Displacement non relié à la sortie | Displacement relié à Material Output |
| `…_eevee` | moteur EEVEE | Moteur de rendu |
Aussi refusé : le starter.

## Limites
- Le correcteur ne rend pas la scène : il lit le graphe et les réglages ; la subdivision adaptative n'est pas visible dans le maillage évalué en arrière-plan (d'où l'acceptation de `use_adaptive_subdivision`).
- Il n'évalue pas la quantité de relief réellement produite ni la qualité du bruit.
- Le contre-exemple « eevee » refuse le moteur : choix pédagogique (voir THEORY.md §5), pas une affirmation que EEVEE ne sait rien déplacer.
