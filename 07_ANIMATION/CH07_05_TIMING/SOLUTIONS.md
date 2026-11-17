# CH07.05 — Solutions

<!-- QUIZ_ANSWERS_START -->
## Réponses du quiz

| Q | Réponse | Explication |
|---|---|---|
| Q1 | **a** — Le nombre d'images entre deux événements | Contacts aux images 19, 44, 62 : c'est le timing de la balle. |
| Q2 | **a** — La distance parcourue entre deux images | Il augmente quand l'objet accélère (chute), diminue quand il ralentit (montée). |
| Q3 | **a** — 0,01703 | 9,81 / 24² = 0,01703. |
| Q4 | — | h = g·T²/8 avec T = 25/24 s : 9,81 × 1,085 / 8 = 1,33 m. |
| Q5 | — | La vitesse de rebond est multipliée par le coefficient de restitution (≈ 0,7) : le vol dure 0,7 fois moins longtemps (25 puis 18 images) et monte 0,5 fois moins haut. |
| Q6 | **a** — Vector ou raide | Auto Clamped aplatit la courbe au contact : la balle flotte (espacement −0,006 au lieu de −0,017). |
| Q7 | **a** — Horizontale (Auto Clamped) | Au sommet la vitesse verticale est nulle : tangente horizontale. |
| Q8 | — | Un point par image montre le spacing : points serrés au sommet, écartés près du sol ; une balle linéaire montre des points équidistants. |
| Q9 | — | Les contacts à −12 cm : la balle s'enfonce dans le sol ; le correcteur exige Z ≥ −0,02 m. |
| Q10 | — | Pour travailler avec des poses clés lisibles et laisser la courbe faire les intervalles ; une animation bakée image par image est difficile à corriger. |
<!-- QUIZ_ANSWERS_END -->

## Exercices
`COMPLETED_EXAMPLES/ch07_05_bounce_solution.blend` (+ `_reference.png`)

**Fabrication.** Générées par script (`build_ch07_05_files.py`) : sept clés de position, poignées exactes (`FREE`), variantes (linéaire, Auto Clamped, Vector). Score 39/39 ; starter 8/13 (arrêt anticipé : un seul contact). Croquis regardé : trois arches décroissantes, points serrés aux sommets.

## Contre-épreuve du correcteur (`COMPLETED_EXAMPLES/COUNTER_EXAMPLES/`)
| Fichier faux | Défaut | Tests qui le refusent |
|---|---|---|
| `…_linear` | interpolation linéaire | espacement (seul) |
| `…_floaty` | poignées Auto Clamped aux contacts : balle flottante | espacement (seul) |
| `…_no_decay` | hauteurs et durées sans décroissance | décroissance ; gravité ; espacement ; repos |
| `…_same_time` | durées de vol égales | durées ; gravité ; espacement ; repos |
| `…_no_rest` | la balle ne s'arrête pas (Z = 0,5 m à la fin) | repos (seul) |
| `…_below_floor` | contacts à −12 cm | sol (seul) |
Aussi refusé : le starter.

## Limites
- Balle sans déformation ni déplacement horizontal.
- Trois contacts puis arrêt net (stylisé).
- Les contre-exemples « sans décroissance » et « durées égales » échouent aussi sur la gravité et l'espacement (la physique est liée).
