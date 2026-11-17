# CH06.09 — Solutions

<!-- QUIZ_ANSWERS_START -->
## Réponses du quiz

| Q | Réponse | Explication |
|---|---|---|
| Q1 | **b** — Un bone (rotation autour d'une charnière) | Un grand mouvement de rotation se fait par bone ; les shape keys servent aux formes fines. |
| Q2 | **b** — Pour éviter une cassure : une coupure binaire étire les arêtes | Mesure : étirement d'arête max 1,45 fois (lisse) contre 2,92 (coupure binaire). |
| Q3 | **b** — Une commande qui agit sur une zone qui n'est pas la sienne | Contre-exemple : le sourire qui baisse aussi les paupières (12 mm mesurés). |
| Q4 | — | Par un groupe de sommets à poids dégradés (Vertex Group du shape key), nul en dehors de la zone. |
| Q5 | — | Pour que le déplacement maximal soit exactement celui voulu (12 mm) ; sans normalisation, le sommet le plus proche du centre ne pesait que 0,6 et le sourire montait de 7,6 mm seulement. |
| Q6 | **b** — À borner sa course (ici X de 0 à 0,05 m) | Sans limite, l'animateur peut tirer la glissière à 0,20 m ; la valeur du key est bornée par le curseur, mais la glissière part ailleurs. |
| Q7 | **b** — x / 0.05 | 0,05 m → 1 ; 0,025 m → 0,5. |
| Q8 | — | Avec x / 0.1, la valeur n'atteint que 0,5 à fond : le sourire ne monte que de 6 mm au lieu de 12. |
| Q9 | — | Pour vérifier que la glissière elle-même est bornée : la valeur du key reste à 1 dans les deux cas, seul le déplacement effectif (50 mm) distingue le rig avec limite. |
| Q10 | — | Bone : mâchoire, yeux (rotation). Shape key : plis du front, sourire, paupières, lèvres. |
<!-- QUIZ_ANSWERS_END -->

## Exercice 2
`COMPLETED_EXAMPLES/ch06_09_facial_solution.blend` (+ `_reference.png`).

**Fabrication.** Générée par script (`build_ch06_09_files.py`) : sphère, armature, poids smoothstep, shape keys à poids normalisés, drivers, Limit Location. Score 57/57 ; starter 6/19 (arrêt anticipé : pas de shape keys). Le sens de rotation de la mâchoire et le seuil d'étirement (1,8) ont été calibrés par mesure (lisse 1,45 ; binaire 2,92).
Croquis regardé : menton qui descend (profil), coins relevés et paupières baissées (face).

## Contre-épreuve du correcteur (`COMPLETED_EXAMPLES/COUNTER_EXAMPLES/`)
| Fichier faux | Défaut | Tests qui le refusent |
|---|---|---|
| `…_no_drivers` | keys sans driver (valeur fixée à 1) | drivers ; valeurs ; amplitudes |
| `…_crosstalk` | le sourire baisse aussi les paupières | zone du key ; paupières immobiles pendant le sourire (seuls) |
| `…_no_limit` | glissières non bornées | Limit Location (config) ; déplacement effectif à 0,20 m |
| `…_weak_driver` | driver x / 0.1 | valeurs à 0,025 et 0,05 m ; amplitudes |
| `…_no_jaw_weights` | aucun poids sur jaw | poids de jaw ; mouvement du menton |
| `…_jaw_rigid` | poids binaires (coupure à z = −0,03) | lissage de la mâchoire (étirement 2,92, seul) |
Aussi refusé : le starter.

## Limites
- Tête sphérique sans bouche ni yeux modélisés ; deux expressions.
- Le correcteur mesure des déplacements de sommets, pas l'esthétique.
