# CH08.03 — Solutions

<!-- QUIZ_ANSWERS_START -->
## Réponses du quiz

| Q | Réponse | Explication |
|---|---|---|
| Q1 | **a** — Un tissu : arêtes élastiques, flexion, collisions | Chaque arête résiste à l'étirement et à la flexion. |
| Q2 | **a** — Le déclarer comme obstacle pour les tissus et particules | COL_Ball et COL_Floor portent un modificateur Collision. |
| Q3 | **a** — Le drap tombe au sol à travers elle | Sommet central à z = −0,475 m au lieu de 0,525 m. |
| Q4 | — | Un tissu a besoin de sommets pour former des plis ; une grille grossière donne un drap raide et anguleux. |
| Q5 | — | Elle coûte cher et fait vibrer ; le drap ne se replie pas sur lui-même dans cet exercice. |
| Q6 | **a** — L'écart entre le tissu et l'obstacle | 5 mm : le drap épouse la sphère ; 50 mm avec Quality 1 : instable. |
| Q7 | **a** — Nombre de pas de calcul par image : plus haut = plus stable et plus lent | Quality 1 : drap non stabilisé (42 mm de mouvement entre les images 110 et 120). |
| Q8 | — | Le drap tombe de part et d'autre de la sphère et doit reposer sur le sol : sans collision, il le traverse (−0,84 m). |
| Q9 | — | Un tissu qui vibre encore à l'image 120 serait inutilisable dans un plan : 10 mm de mouvement entre les images 110 et 120 dans la solution. |
| Q10 | — | Cloth : il gère la flexion, les plis et les collisions de façon bien meilleure ; Soft Body pour des volumes mous. |
<!-- QUIZ_ANSWERS_END -->

## Exercices
`COMPLETED_EXAMPLES/ch08_03_cloth_solution.blend` (+ `_reference.png`)

**Fabrication.** Générées par script (`build_ch08_03_files.py`) : grille bmesh, sphère, plan, modificateurs CLOTH et COLLISION. Score 40/40 ; starter 2/6 (arrêt anticipé). Profil regardé.

## Contre-épreuve du correcteur (`COMPLETED_EXAMPLES/COUNTER_EXAMPLES/`)
| Fichier faux | Défaut | Tests qui le refusent |
|---|---|---|
| `…_no_ball_collision` | la sphère n'a pas de Collision : le drap passe à travers | obstacles ; drapé ; pénétration |
| `…_no_floor_collision` | le sol n'a pas de Collision : le drap le traverse | obstacles ; sol |
| `…_low_quality` | Quality 1, Distance 50 mm : drap instable | quality ; collisions ; repos |
| `…_no_gravity` | gravité à 0 : le drap flotte | drapé (seul) |
Aussi refusé : le starter.

## Limites
- Un drap et des obstacles fixes ; pas de pin ni de vent.
- Calcul de 10 s environ par fichier.
- Les contre-exemples « no_ball_collision » et « low_quality » échouent aussi sur la configuration.
