# CH07.07 — Solutions

<!-- QUIZ_ANSWERS_START -->
## Réponses du quiz

| Q | Réponse | Explication |
|---|---|---|
| Q1 | **a** — Épaules et hanches inclinées en sens opposés | Mesuré : épaules +10°, hanches −8° dans la solution. |
| Q2 | **a** — Celle dont le genou est tendu, sous les hanches | L'appui : cheville au sol à moins de 15 cm sous le centre des hanches. |
| Q3 | **a** — La courbe principale de la pose, souvent en C ou en S | Solution : colonne et haut du corps forment 18°. |
| Q4 | — | Sinon les jambes basculent avec les hanches et les pieds quittent le sol : le poids n'est plus posé. |
| Q5 | — | Elle porte le poids : l'autre hanche, libérée, tombe ; les épaules compensent en sens inverse. |
| Q6 | **a** — Lisible en aplat noir, sans détail | Test : tout remplir en blanc sur noir et voir si la pose se lit. |
| Q7 | **a** — Aire de la silhouette / aire de son enveloppe convexe | Bras collés : 0,64 ; pose ouverte : 0,37 ; limite du correcteur 0,50. |
| Q8 | — | Ils se fondent dans le torse : on ne lit plus ni les bras, ni les mains, ni l'attitude ; l'enveloppe est pleine. |
| Q9 | — | Deux genoux pliés (28°) : aucune jambe ne soutient, les deux pieds sont au-dessus du sol : pose flottante. |
| Q10 | — | Une pose lisible de face peut s'écraser de profil ; le correcteur du chapitre mesure la face ; en production on contrôle deux vues. |
<!-- QUIZ_ANSWERS_END -->

## Exercices
`COMPLETED_EXAMPLES/ch07_07_posing_solution.blend` (+ `_reference.png`)

**Fabrication.** Générées par script (`build_ch07_07_files.py`) : mannequin de capsules, armature de 13 bones, rotations monde, silhouette réelle rendue en Workbench. Score 35/35 ; starter 15/35. Silhouettes regardées : T-pose et pose.

## Contre-épreuve du correcteur (`COMPLETED_EXAMPLES/COUNTER_EXAMPLES/`)
| Fichier faux | Défaut | Tests qui le refusent |
|---|---|---|
| `…_no_tilt` | épaules et hanches de niveau | contrapposto ; ligne d'action |
| `…_twin_tilt` | épaules et hanches inclinées dans le même sens | contrapposto ; ligne d'action |
| `…_both_bent` | les deux genoux fléchis (pas de jambe d'appui) | appui ; équilibre |
| `…_unbalanced` | jambe d'appui écartée de 48 cm des hanches | équilibre (seul) |
| `…_no_curve` | colonne rectiligne | ligne d'action (seul) |
| `…_arms_at_sides` | bras collés au corps | silhouette (seul) |
Aussi refusé : le starter.

## Limites
- Mannequin FK de capsules, mesures de face seulement.
- Les contre-exemples « sans bascule » et « bascule parallèle » échouent aussi sur la ligne d'action (la colonne y est droite) ; « deux genoux pliés » échoue aussi sur l'équilibre.
- Les seuils mesurent des inclinaisons, des genoux, une courbe et une solidité, pas la qualité artistique.
