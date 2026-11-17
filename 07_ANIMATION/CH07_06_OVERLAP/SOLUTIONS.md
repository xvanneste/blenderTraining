# CH07.06 — Solutions

<!-- QUIZ_ANSWERS_START -->
## Réponses du quiz

| Q | Réponse | Explication |
|---|---|---|
| Q1 | **a** — Chaque partie atteint son extrême un peu après la précédente | Mesuré : maxima aux images 13, 15, 17, 19 (retards de 2 images). |
| Q2 | **a** — La queue continue quand le corps s'arrête | À l'image 26 la base est arrêtée, tail_3 est encore à 7,2°. |
| Q3 | **a** — Un arc | La pointe s'écarte de 51 cm de la droite entre ses positions : trajectoire courbe. |
| Q4 | — | 18°, 14°, 10° : une pointe plus légère et plus loin se déplace moins par rapport à son parent ; c'est un choix de style, pas une loi. |
| Q5 | — | Entre 1 et 4 images le retard se lit comme une cascade ; au-delà (6 images, contre-exemple) la queue paraît détachée du corps. |
| Q6 | **a** — La pointe passe au-delà du repos avant de s'y stabiliser | tail_3 descend à −6° (image 35) avant de revenir à 0 (image 44). |
| Q7 | **a** — Quand tout est au repos (≤ 1°) | Le contre-exemple « no_settle » finit à 5° : la queue ne s'arrête pas. |
| Q8 | — | La queue revient au repos en même temps que la base : à l'image 26, tail_3 est à −1,6° au lieu de 7,2° : l'antenne paraît rigide. |
| Q9 | — | Une copie donnerait les mêmes images clés (aucun retard) : l'overlap vient du décalage des extrêmes. |
| Q10 | — | Queues, oreilles, cheveux, vêtements, antennes, bras mous ; les simulations (CH08) les produisent automatiquement mais ils se contrôlent aussi à la main. |
<!-- QUIZ_ANSWERS_END -->

## Exercices
`COMPLETED_EXAMPLES/ch07_06_overlap_solution.blend` (+ `_reference.png`)

**Fabrication.** Générées par script (`build_ch07_06_files.py`) : armature de quatre bones, rotation X par clés, variantes. Score 28/28 ; starter 12/28. Croquis regardé : quatre courbes décalées, dépassement bleu de la pointe, arc à droite.

## Contre-épreuve du correcteur (`COMPLETED_EXAMPLES/COUNTER_EXAMPLES/`)
| Fichier faux | Défaut | Tests qui le refusent |
|---|---|---|
| `…_no_overlap` | tous les bones au maximum à l'image 13 | retards ; suite du mouvement |
| `…_too_late` | retards de 6 images par bone | retards ; dépassement |
| `…_no_followthrough` | la queue revient au repos avec la base (image 25) | suite du mouvement (seul) |
| `…_no_overshoot` | tail_3 revient à 0 sans dépasser | dépassement (seul) |
| `…_no_settle` | tail_3 finit à 5° | repos (seul) |
| `…_stiff` | queue immobile (antenne raide) | retards ; suite du mouvement ; dépassement |
Aussi refusé : le starter.

## Limites
- Quatre bones sur un seul axe ; pas de simulation physique.
- Les contre-exemples « sans overlap » et « retards trop longs » échouent aussi sur la suite du mouvement ou le dépassement (les mesures sont liées).
- Le rig est seul (pas de maillage).
