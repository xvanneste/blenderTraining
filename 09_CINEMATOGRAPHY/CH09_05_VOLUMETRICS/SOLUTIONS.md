# CH09.05 — Solutions

<!-- QUIZ_ANSWERS_START -->
## Réponses du quiz

| Q | Réponse | Explication |
|---|---|---|
| Q1 | **a** — Rien ne diffuse la lumière vers la caméra | Il faut des particules (brume, poussière). |
| Q2 | **a** — Principled Volume relié à Volume | Material Output > Volume. |
| Q3 | **a** — Density | Density 0,08 dans l'exercice. |
| Q4 | — | Density 0,004 : la luminance du centre tombe à 0,007 (contre 0,088) : le faisceau est presque invisible. |
| Q5 | — | Density 0 : aucune particule ne diffuse la lumière ; on ne voit que la tache sur le sol. |
| Q6 | **a** — La lumière est absorbée et l'image devient opaque | Density 1,5 : centre à 0,0007. |
| Q7 | **a** — La direction préférée de la diffusion | 0 = uniforme ; > 0 = vers l'avant. |
| Q8 | — | Avec 150° le brouillard est éclairé partout : le centre vaut 0,59 et le faisceau ne se distingue plus du reste. |
| Q9 | — | C'est un volume délimité : le maillage sert de frontière ; son affichage en filaire évite de le confondre avec un objet solide. |
| Q10 | — | Elle lit la luminance du centre et le contraste avec les bords : elle ne juge ni la forme du faisceau, ni le bruit, ni l'esthétique. |
<!-- QUIZ_ANSWERS_END -->

## Exercices
`COMPLETED_EXAMPLES/ch09_05_volumetrics_solution.blend` (+ `_reference.png`)

**Fabrication.** Générées par script (`build_ch09_05_files.py`) : brouillard, sol, spot, caméra, variantes ; calibration par rendu. Score 27/27 ; starter 13/27. Rendus regardés.

## Contre-épreuve du correcteur (`COMPLETED_EXAMPLES/COUNTER_EXAMPLES/`)
| Fichier faux | Défaut | Tests qui le refusent |
|---|---|---|
| `…_too_thin` | Density 0,004 : faisceau presque invisible (0,007) | faisceau (luminance) |
| `…_too_dense` | Density 1,5 : le brouillard éteint la lumière (0,0007) | faisceau (luminance) |
| `…_wide_spot` | spot de 150° : plus de faisceau, tout est éclairé (0,59) | spot ; faisceau |
| `…_no_light` | spot éteint (0 W) | spot ; faisceau ; contraste |
Aussi refusé : le starter.

## Limites
- Cycles seulement.
- Volume homogène.
- Pas de jugement de forme.
