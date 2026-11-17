# CH06.07 — Solutions

<!-- QUIZ_ANSWERS_START -->
## Réponses du quiz

| Q | Réponse | Explication |
|---|---|---|
| Q1 | **b** — d / r radians | Arc = rayon × angle, donc angle = d / r (en radians). |
| Q2 | **b** — Son axe Y (l'axe du bone, qui coïncide avec l'axe de la roue) | Le bone wheel_* est dirigé le long de l'essieu : tourner autour de l'axe du bone fait tourner la roue sur elle-même. |
| Q3 | **b** — Transform Channel | Transform Channel (Location Y, Local Space) lit le déplacement de root. |
| Q4 | — | Le camion avance vers +Y ; pour que le dessus de la roue avance, la roue tourne dans le sens négatif autour de +X (règle de la main droite). |
| Q5 | — | Avec 0,15 au lieu de 0,30, la roue tourne deux fois trop : elle glisse. Le correcteur mesure la rotation des sommets (−1,67 rad attendus pour 0,5 m). |
| Q6 | **a** — Damped Track | Damped Track oriente l'axe Y du bone vers la cible. |
| Q7 | — | Le corps (cyl) part de l'ancrage et vise le point de la benne ; la tige (rod), enfant de ce point, vise l'ancrage : les deux restent alignés et emboîtés. |
| Q8 | **b** — Local Space | La limite se rapporte à la rotation propre du bone par rapport à son parent. |
| Q9 | — | La benne dépasse 45° (le bout monte à 1,79 m au lieu de 1,48 m) et traverse l'objet qui la porte. |
| Q10 | — | Les bones peuvent être justes alors que le maillage ne suit pas (poids, parenté) : c'est le résultat visible qui compte. |
<!-- QUIZ_ANSWERS_END -->

## Exercice 2
`COMPLETED_EXAMPLES/ch06_07_truck_solution.blend` (+ `_reference.png`).

**Fabrication.** Générée par script (`build_ch06_07_files.py`) : armature, drivers (`driver_add` sur `rotation_euler[1]`), Damped Track, Limit Rotation. Score du correcteur 59/59 ; starter 28/59.
Croquis regardé : roues tournées de 95° quand le camion avance de 0,5 m ; vérin aligné quand la benne est levée de 35°.

## Contre-épreuve du correcteur (`COMPLETED_EXAMPLES/COUNTER_EXAMPLES/`)
| Fichier faux | Défaut | Tests qui le refusent |
|---|---|---|
| `…_no_drivers` | roues sans driver | drivers (config) ; rotation à 0,5 m et 0,2 m ; proportionnalité |
| `…_wrong_radius` | rayon 0,15 au lieu de 0,30 (roue qui glisse) | rotation à 0,5 m et 0,2 m ; proportionnalité (seuls) |
| `…_wrong_axis` | driver sur la rotation X (vrille) | rotation ; plan de la roue ; proportionnalité |
| `…_unparented_wheels` | roues non enfants de root | parenté ; avance des roues à 0,5 m et 0,2 m |
| `…_no_track` | vérin sans Damped Track | Damped Track ; alignement cyl et rod ; recouvrement |
| `…_no_limit` | benne sans Limit Rotation | Limit Rotation (config) ; benne à 80° |
Aussi refusé : le starter.

## Limites
- Camion simple, un seul vérin, pas de direction ni de suspension.
- Le correcteur teste le roulement sans glissement par les angles de sommets, pas par un contact au sol.
