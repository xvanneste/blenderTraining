# CH07.09 — Solutions

<!-- QUIZ_ANSWERS_START -->
## Réponses du quiz

| Q | Réponse | Explication |
|---|---|---|
| Q1 | **a** — Une phase aérienne où les deux pieds quittent le sol | En marche, un pied touche toujours le sol ; en course il y a un vol. |
| Q2 | **a** — Plus court que celui d'une marche | Un pas de course dure moins longtemps : le cycle est plus rapide (par exemple 16 à 18 images). |
| Q3 | **a** — Un mouvement sans appui soumis à la gravité | Pendant le vol, seule la gravité agit : parabole. |
| Q4 | — | Pour compenser la rotation du bassin et donner de l'élan ; ils s'opposent aux jambes comme en marche, avec plus d'amplitude. |
| Q5 | — | Corps incliné vers l'avant, pieds bas et écartés, mouvement lent, l'objet bouge après le contact de la main (overlap) ; tirer : poids vers l'arrière, bras tendus. |
| Q6 | **a** — Anticipation, impulsion, vol, réception | Flexion (hanches 0,65 m), impulsion (décollage), vol parabolique, amortissement (0,68 m). |
| Q7 | **a** — Une parabole | Accélération constante : −0,0170 m/image² (mesuré). |
| Q8 | — | h = g·T²/8 avec T = 14/24 s : 9,81 × 0,34 / 8 = 0,417 m au-dessus du décollage. |
| Q9 | — | Un corps qui retombe d'un saut absorbe l'énergie en fléchissant ; sans amortissement (0,95 m), le personnage paraît sans poids. |
| Q10 | — | Un vol de 21 images pour la même hauteur : la gravité effective tombe à 0,0069 m/image² : le personnage flotte comme sur la Lune. |
<!-- QUIZ_ANSWERS_END -->

## Exercices
`COMPLETED_EXAMPLES/ch07_09_jump_solution.blend` (+ `_reference.png`)

**Fabrication.** Générées par script (`build_ch07_09_files.py`, qui importe le mannequin et l'IK de `build_ch07_08_files.py`) : hanches (fonctions lissées et parabole), chevilles, IK analytique, balancement des bras, 40 clés par bone. Score 43/43 ; starter : arrêt anticipé (pas d'animation). Courbe de hauteur regardée.

## Contre-épreuve du correcteur (`COMPLETED_EXAMPLES/COUNTER_EXAMPLES/`)
| Fichier faux | Défaut | Tests qui le refusent |
|---|---|---|
| `…_no_anticipation` | pas de flexion avant le saut | anticipation (seul) |
| `…_no_landing` | pas d'amortissement à la réception | réception (seul) |
| `…_floaty` | vol de 21 images à gravité faible | durée du vol ; gravité ; retour debout |
| `…_too_low` | sommet à 0,12 m seulement | hauteur du vol ; gravité |
| `…_feet_slide` | pieds qui glissent au sol | pieds plantés (seul) |
| `…_no_return` | le mannequin reste fléchi à la fin | retour debout (seul) |
Aussi refusé : le starter.

## Limites
- Saut sur place, mannequin FK ; course et interactions non testées.
- Les contre-exemples « floaty » et « too_low » échouent aussi sur la gravité (la physique relie hauteur et durée) ; « floaty » aussi sur le retour debout.
- Le tutoriel décrit une version à clés espacées non validée par le correcteur.
