# CH05.08 — Solutions

<!-- QUIZ_ANSWERS_START -->
## Réponses du quiz

| Q | Réponse | Explication |
|---|---|---|
| Q1 | **b** — 23,8 m | 7 × 3,4 = 23,8 m ; le correcteur mesure 23,80 m. |
| Q2 | **b** — Le Cube est centré : il faut le monter de la moitié de sa hauteur pour poser sa base sur z = 0 | Le Cube du nœud est centré sur l'origine. |
| Q3 | **a** — Grid de Vertices X = Bays et Size X = (Bays − 1) × Bay Width : les sommets tombent aux centres | Aux bords, les sommets d'une Grid sont aux extrémités : n sommets, espacement Size ÷ (n − 1) = Bay Width. |
| Q4 | — | (5 − 1) × 2,5 = 10 m ; les sommets sont à −5, −2,5, 0, 2,5, 5 : espacés de 2,5 m, symétriques autour de l'axe. |
| Q5 | — | La Grid est dans le plan XY ; la façade est dans le plan XZ : une rotation de 90° autour de X amène Y vers Z. |
| Q6 | **a** — L'outil marche en défaut mais pas pour d'autres réglages : le nombre de fenêtres ne suit pas Bays et Floors | Il passe le réglage A (5 × 4) et échoue au réglage B (7 × 3) : d'où deux réglages dans le correcteur. |
| Q7 | **b** — À 0,55 × Floor Height | 0,55 × hauteur d'étage : une allège sous la fenêtre, comme sur un vrai étage. |
| Q8 | — | Un outil peut être correct pour ses valeurs par défaut et faux dès qu'on change un paramètre (valeur codée en dur, mauvais lien) : deux réglages différents l'exposent. |
| Q9 | — | Leur y doit valoir −Depth ÷ 2 (± 5 cm) : à y = 0 elles sont au centre du volume, invisibles (contre-exemple « off_facade »). |
| Q10 | — | Instancier une porte sur la travée centrale du premier étage et supprimer la fenêtre correspondante (Selection de Instance on Points ou Delete Geometry sur un Index). |
<!-- QUIZ_ANSWERS_END -->

## Exercice 2
`COMPLETED_EXAMPLES/ch05_08_architecture_solution.blend` (+ `_reference.png`).

**Fabrication.** Générée par script (`build_ch05_08_files.py`) ; les valeurs du modificateur sont posées par `modifier.properties.inputs[identifiant]["value"]`. Score du correcteur 43/43 ; starter 3/7 (interface absente : arrêt anticipé).
Mesures : voir THEORY.md §5.
Rendu regardé : deux immeubles (4 × 5 et 7 × 3), façades régulières, fenêtres sombres ; le cadrage a été élargi deux fois (les immeubles de 24 m dépassaient du cadre).

## Contre-épreuve du correcteur (`COMPLETED_EXAMPLES/COUNTER_EXAMPLES/`)
| Fichier faux | Défaut | Tests qui le refusent |
|---|---|---|
| `…_fixed_count` | nombre de fenêtres fixe (Grid 5 × 4) | Réglage B : nombre de fenêtres et régularité (passe le réglage A) |
| `…_body_height_fixed` | hauteur du corps fixe (3 m par étage) | Réglage B : hauteur du corps (seul ; passe le réglage A) |
| `…_bad_spacing` | espacement vertical des fenêtres moitié trop petit | Régularité de la façade, réglages A et B |
| `…_off_facade` | fenêtres posées à y = 0 (dans le volume) | Fenêtres sur la façade, réglages A et B |
Aussi refusé : le starter.
Le contre-exemple « body_height_fixed » passe entièrement le réglage A (3 m = valeur par défaut) : sans le réglage B il serait accepté.

## Limites
- Quatre murs, une seule façade ; pas de portes, balcons, toit.
- Les tolérances (2 cm, 5 cm) conviennent à des dimensions de l'ordre du mètre.
