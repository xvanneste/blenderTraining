# CH09.01 — Solutions

<!-- QUIZ_ANSWERS_START -->
## Réponses du quiz

| Q | Réponse | Explication |
|---|---|---|
| Q1 | **a** — 4 fois plus faible | Inverse du carré : 1/d². |
| Q2 | **a** — 9 fois plus | 10 W à 1 m ↔ 90 W à 3 m (100 W avec la couleur chaude de l'exercice). |
| Q3 | **a** — Les valeurs sont proportionnelles à la lumière | Un PNG est encodé en sRGB (courbe de contraste). |
| Q4 | — | 10 W à 3 m : luminance 0,012, soit 10 % de la référence 0,119 : 9 fois moins de lumière (inverse du carré), arrondi. |
| Q5 | — | Un monde de couleur éclaire aussi la scène : le défaut gris du fond (0,05) ajoutait une lumière ambiante et faussait la mesure. |
| Q6 | **a** — Une source plus grande (Radius) | Pénombre : 3 pixels (Radius 0) → 8 pixels (Radius 0,5). |
| Q7 | **a** — Rouge / bleu > 1 | Couleur (1 ; 0,85 ; 0,65) : rouge / bleu = 1,54 sur un plan gris. |
| Q8 | — | 44 W à 2 m donne la même exposition (0,113), mais la consigne est une lampe à 3 m : l'exposition seule ne fixe pas la position. |
| Q9 | — | La caméra est au-dessus : le cube cacherait son ombre. `visible_camera = False` le garde actif pour les ombres. |
| Q10 | — | Elle ne dit rien de l'ensemble de l'image (dégradé, bords) ; ici elle mesure l'éclairement, pas l'ambiance. |
<!-- QUIZ_ANSWERS_END -->

## Exercices
`COMPLETED_EXAMPLES/ch09_01_light_solution.blend` (+ `_reference.png`)

**Fabrication.** Générées par script (`build_ch09_01_files.py`) : plan, Occluder, caméra, monde noir, lampe réglée par variante ; calibration des mesures par rendu. Score 34/34 ; starter 13/34. Profils regardés.

## Contre-épreuve du correcteur (`COMPLETED_EXAMPLES/COUNTER_EXAMPLES/`)
| Fichier faux | Défaut | Tests qui le refusent |
|---|---|---|
| `…_under_exposed` | 10 W à 3 m : 10 % de la référence | exposition |
| `…_over_exposed` | 400 W à 3 m : 4 fois la référence | exposition |
| `…_too_close` | 44 W à 2 m : bonne exposition, mais pas à 3 m | position |
| `…_hard_shadow` | Radius 0 : ombre nette | Radius ; pénombre |
| `…_cold_light` | couleur bleue | lumière chaude |
Aussi refusé : le starter.

## Limites
- Un seul type de lampe testé.
- Mesure au centre du plan.
- Température de couleur non testée.
