# CH08.02 — Solutions

<!-- QUIZ_ANSWERS_START -->
## Réponses du quiz

| Q | Réponse | Explication |
|---|---|---|
| Q1 | **a** — Un maillage de masses reliées par des ressorts | Chaque sommet est une masse, chaque arête un ressort. |
| Q2 | **a** — Il ramène les sommets vers leur position d'origine selon leur poids | Poids 1 : le sommet reste accroché ; poids 0 : il est libre. |
| Q3 | **a** — Un groupe de sommets (poids) | Groupe « pin » : poids 1 sur le bord x = −1. |
| Q4 | — | Avec Goal Default à 1, un sommet absent du groupe reste fixe ; les poids 0 explicites le libèrent (mesure : la plaque ne pend pas sans eux). |
| Q5 | — | Sans goal, toute la plaque tombe : z minimal de −39 m après 100 images. |
| Q6 | **a** — La raideur des arêtes (étirement et compression) | À 0,02 la plaque s'étire de 2,8 fois ; à 0,9 de 1,01 fois. |
| Q7 | **a** — Une masse forte étire les arêtes | 30 kg : arêtes étirées à 1,20 fois, plaque à 1,10 m de haut. |
| Q8 | — | L'état d'une image dépend de la précédente : on avance de l'image 1 à 100 avant de mesurer. |
| Q9 | — | Sans arêtes-ressorts les sommets se dispersent : étirement de 213 fois. |
| Q10 | — | Soft Body pour des volumes mous et des plaques simples ; Cloth (CH08.03) pour les tissus (plis, collisions, couture). |
<!-- QUIZ_ANSWERS_END -->

## Exercices
`COMPLETED_EXAMPLES/ch08_02_softbody_solution.blend` (+ `_reference.png`)

**Fabrication.** Générées par script (`build_ch08_02_files.py`) : grille bmesh, groupe de sommets, modificateur Soft Body, variantes. Score 39/39 ; starter 2/6 (arrêt anticipé). Profil regardé.

## Contre-épreuve du correcteur (`COMPLETED_EXAMPLES/COUNTER_EXAMPLES/`)
| Fichier faux | Défaut | Tests qui le refusent |
|---|---|---|
| `…_no_goal` | Goal décoché : la plaque tombe | goal ; accrochage ; bord libre ; arêtes |
| `…_no_group` | Goal sans groupe : tout reste fixe | goal (groupe) ; bord libre |
| `…_soft_edges` | Pull et Push à 0,02 : la plaque s'étire | edges ; bord libre ; arêtes |
| `…_heavy_mass` | masse de 30 kg | masse ; bord libre ; arêtes |
| `…_no_edges` | Edges décoché : les sommets se dispersent | edges ; bord libre ; arêtes |
Aussi refusé : le starter.

## Limites
- Une plaque, un accrochage, pas de collisions.
- Mesure à l'image 100 (balancement encore en cours).
- Comportement du goal (Default) non expliqué.
