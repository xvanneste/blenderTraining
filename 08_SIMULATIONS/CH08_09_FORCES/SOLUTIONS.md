# CH08.09 — Solutions

<!-- QUIZ_ANSWERS_START -->
## Réponses du quiz

| Q | Réponse | Explication |
|---|---|---|
| Q1 | **a** — L'axe Z local de l'objet | Rotation de 90° autour de Y : vers +X ; −90° : vers −X (mesuré). |
| Q2 | **a** — Field Weights | Poids par type de champ (wind, turbulence, gravity…). |
| Q3 | **a** — Turbulence | Turbulence : bruit de force (Strength, Size). |
| Q4 | — | Le système ignore le vent : le nuage ne dérive pas (contre-exemple ignore_wind : x moyen 0,15 m). |
| Q5 | — | La direction vient de la rotation (axe local Z) ; la position ne compte que pour les champs à falloff. |
| Q6 | **a** — Le brassage latéral | Sans turbulence 0,15 m ; avec 0,30 m ; turbulence seule 0,48 m. |
| Q7 | **a** — Environ 4 m | x moyen 4,06 m (vent seul) ; 3,9 m avec turbulence. |
| Q8 | — | Elle disperse les particules : la moyenne en x passe de 4,06 à 3,9 m. |
| Q9 | — | Un vent de force 0,3 : x moyen 0,14 m : la gravité à 20 % et l'impulsion initiale dominent. |
| Q10 | — | Les particules sont une simulation : positions calculées image par image depuis l'image 1. |
<!-- QUIZ_ANSWERS_END -->

## Exercices
`COMPLETED_EXAMPLES/ch08_09_forces_solution.blend` (+ `_reference.png`)

**Fabrication.** Générées par script (`build_ch08_09_files.py`) : émetteur, champs de force, variantes. Score 47/47 ; starter 10/34. Vue de dessus regardée.

## Contre-épreuve du correcteur (`COMPLETED_EXAMPLES/COUNTER_EXAMPLES/`)
| Fichier faux | Défaut | Tests qui le refusent |
|---|---|---|
| `…_no_wind` | pas de vent : le nuage ne dérive pas (x moyen 0,15 m) | vent ; dérive |
| `…_wrong_direction` | vent tourné de −90° : le nuage part vers −X | direction ; dérive |
| `…_weak_wind` | vent de force 0,3 : dérive de 0,14 m | force ; dérive |
| `…_no_turbulence` | sans turbulence : le nuage reste étroit (écart-type en y 0,15 m) | turbulence ; brassage |
| `…_ignore_wind` | Field Weights : wind 0 : le système ignore le vent | poids ; dérive |
Aussi refusé : le starter.

## Limites
- Falloff et champs locaux non traités.
- Effets sur tissu et corps rigides non testés.
- Liste complète des champs non relue.
