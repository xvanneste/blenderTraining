# CH08.04 — Solutions

<!-- QUIZ_ANSWERS_START -->
## Réponses du quiz

| Q | Réponse | Explication |
|---|---|---|
| Q1 | **a** — Des points émis selon des règles (naissance, vitesse, vie, forces) | Ici 200 particules, émises de l'image 1 à 30. |
| Q2 | **a** — La durée de vie en images | Vie 60 : la dernière née (image 30) meurt à l'image 90. |
| Q3 | **a** — Les particules naissent sur les faces de l'émetteur | Faces de la grille de 0,5 m. |
| Q4 | — | Une émission continue donne un jet ; tout émettre en une fois (5 images) donne une rafale (200 nées à l'image 15 au lieu de 97). |
| Q5 | — | Elle lance les particules dans la direction de la normale des faces : 3 donne un sommet de 1,46 m ; 0 les laisse tomber de l'émetteur. |
| Q6 | **a** — Elle tire les particules vers le bas | À 0 les particules montent jusqu'à 8,2 m. |
| Q7 | **a** — Modificateur Collision sur le sol | Sans Collision elles tombent à −20 m. |
| Q8 | — | Pendant le test on ne veut que la simulation ; l'apparence (objet, halo) se règle ensuite. |
| Q9 | — | Sur l'objet évalué : `ev.particle_systems[0].particles`, avec `alive_state` et `location`, en avançant image par image. |
| Q10 | — | Particules pour la simulation (forces, collisions, vie) ; Geometry Nodes pour la distribution paramétrique (CH05.04) sans simulation. |
<!-- QUIZ_ANSWERS_END -->

## Exercices
`COMPLETED_EXAMPLES/ch08_04_particles_solution.blend` (+ `_reference.png`)

**Fabrication.** Générées par script (`build_ch08_04_files.py`) : grille bmesh, système de particules, collision. Score 40/40 ; starter 2/6 (arrêt anticipé). Nuage regardé.

## Contre-épreuve du correcteur (`COMPLETED_EXAMPLES/COUNTER_EXAMPLES/`)
| Fichier faux | Défaut | Tests qui le refusent |
|---|---|---|
| `…_no_floor` | le sol n'a pas de Collision : les particules tombent à −20 m | sol (collision) ; sous le sol |
| `…_short_life` | durée de vie 20 images | configuration (vie) |
| `…_no_gravity` | gravité à 0 : les particules montent à 8 m | configuration (gravité) ; sommet |
| `…_too_few` | 40 particules | configuration (nombre) |
| `…_burst` | émission sur 5 images (tout d'un coup) | configuration (fin) ; émission étalée |
| `…_static` | vitesse normale 0 : pas de fontaine | configuration (vitesse) ; sommet |
Aussi refusé : le starter.

## Limites
- Particules simulées sans rendu ; un émetteur ; seuils larges.
- Les contre-exemples « short_life », « too_few », « no_gravity », « static » et « burst » échouent surtout sur la configuration (une ligne de configuration regroupe plusieurs réglages).
