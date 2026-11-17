# CH04.09 — Solutions

<!-- QUIZ_ANSWERS_START -->
## Réponses du quiz

| Q | Réponse | Explication |
|---|---|---|
| Q1 | **b** — Une Wave Texture en bandes étirée, passée dans une Color Ramp brune | Des bandes distordues (Wave) donnent les veines ; l'étirement selon un axe (Mapping) les allonge. |
| Q2 | **b** — Pour casser l'aspect lisse : micro-relief qui accroche la lumière | Un bump alimenté par un Noise fin ajoute du grain sans polygone. |
| Q3 | **b** — Anisotropic | L'anisotropie étire le reflet dans une direction, comme les rayures d'un brossage. |
| Q4 | — | Le plastique coloré est souvent recouvert d'une couche brillante (vernis) : Coat Weight ajoute ce second reflet sans changer la couleur de base. |
| Q5 | — | Des rayures de rugosité alignées imitent un brossage ; une valeur constante donne un métal trop parfait. |
| Q6 | **a** — Mark as Asset | Le libellé de l'opérateur `asset.mark` est « Mark as Asset » (confirmé par l'API). |
| Q7 | **b** — Pour retrouver et comprendre le matériau dans l'Asset Browser | Une bibliothèque sans métadonnées est inutilisable à plusieurs. |
| Q8 | — | Base Color pilotée par une texture (Voronoi ou Noise), un Bump alimenté par une texture relié à Normal, Roughness ≥ 0,6. |
| Q9 | — | Transmission Weight 1, Roughness 0,02, IOR 1,5 (comme en CH04.03). |
| Q10 | — | Il devient mat comme du caoutchouc : plus de reflet net, donc plus du tout l'aspect plastique brillant attendu. |
<!-- QUIZ_ANSWERS_END -->

## Exercice 2
`COMPLETED_EXAMPLES/ch04_09_materials_solution.blend` (+ `_reference.png`).

**Fabrication.** Générée par script (`build_ch04_09_files.py`) : valeurs du tableau de THEORY.md §1, matériaux marqués par `asset_mark()` avec description et tag « BCMA » (les métadonnées survivent à l'enregistrement et à la réouverture, vérifié par le correcteur). Score 36/36 ; starter 11/36.
Rendu regardé : les cinq sphères se distinguent nettement ; plastique légèrement rosé, acier brossé discret.

## Contre-épreuve du correcteur (`COMPLETED_EXAMPLES/COUNTER_EXAMPLES/`)
| Fichier faux | Défaut | Test qui le refuse (et lui seul) |
|---|---|---|
| `…_wood_flat` | bois sans texture (couleur unie) | Wood : Base Color pilotée par Wave + Color Ramp |
| `…_stone_no_bump` | pierre sans Bump | Stone : Normal alimentée par Bump et une texture |
| `…_steel_isotropic` | acier avec Anisotropic 0 | Steel : Anisotropic |
| `…_not_marked` | matériau de la pierre non marqué asset | Matériaux marqués asset avec description |
| `…_plastic_matte` | plastique à Roughness 0,9 | Plastic : Roughness |
Aussi refusé : le starter.

## Limites
- Valeurs et liens, pas la qualité visuelle ; l'asset n'est pas vérifié dans une bibliothèque déclarée.
- Les seuils (Roughness, Anisotropic…) sont des choix pédagogiques raisonnables, pas des mesures physiques.
