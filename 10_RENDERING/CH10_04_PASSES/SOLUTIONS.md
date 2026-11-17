# CH10.04 — Solutions

<!-- QUIZ_ANSWERS_START -->
## Réponses du quiz

| Q | Réponse | Explication |
|---|---|---|
| Q1 | **a** — Une image d'une propriété de la scène (profondeur, normales, couleur…) | Le départ n'écrit que Combined ; la solution écrit 39 canaux. |
| Q2 | **a** — Donner la distance à la caméra de chaque pixel | Canal FG.Depth.Z. |
| Q3 | **a** — Une couche qui ne contient que la lumière de certaines lampes | Canaux FG.Combined_key et FG.Combined_fill. |
| Q4 | — | On peut ensuite doser chaque lampe en compositing sans refaire le rendu. |
| Q5 | — | Une sortie personnalisée d'un matériau (ici « tint » via un nœud Shader AOV Output) écrite comme un canal supplémentaire. |
| Q6 | **a** — Un rendu séparé du même décor avec ses propres collections et passes | FG exclut Backdrop ; BG exclut Hero. |
| Q7 | **a** — Il lit les noms de canaux dans l'en-tête du fichier rendu | Le format multi-parties répète un en-tête par calque. |
| Q8 | — | 16 bits flottants suffisent pour la couleur et divisent la taille par deux ; la profondeur Z demande souvent 32 bits (voir CH10.06). |
| Q9 | — | C'est la propriété Object Properties > Relations > Pass Index : un entier par objet, écrit dans la passe Object Index pour fabriquer des masques. |
| Q10 | — | Le correcteur vérifie la présence des canaux et des réglages, pas leur contenu de pixels ; les canaux Z et Normal d'un rendu à 1 échantillon ne prouvent pas leur justesse. |
<!-- QUIZ_ANSWERS_END -->

## Exercices
`COMPLETED_EXAMPLES/ch10_04_passes_solution.blend` (+ `_reference.png`)

**Fabrication.** Générées par script (`build_ch10_04_files.py`) : deux collections, deux lampes, matériau, deux calques de vue ; mesures par rendu réel en EXR multicouche et lecture de l'en-tête. Score 69/69 ; starter 2/64. Rendu des calques regardé.

## Contre-épreuve du correcteur (`COMPLETED_EXAMPLES/COUNTER_EXAMPLES/`)
| Fichier faux | Défaut | Tests qui le refusent |
|---|---|---|
| `…_no_normal` | passe Normal absente | canal Normal |
| `…_no_lightgroups` | aucun light group | light groups |
| `…_no_aov` | aucun AOV tint | AOV |
| `…_wrong_index` | Hero avec Pass Index 0 | Pass Index |
| `…_no_bg_layer` | pas de calque BG | calques de vue ; canal BG |
| `…_png_output` | sortie PNG au lieu d'EXR multicouche | sortie |
Aussi refusé : le starter.

## Limites
- Contenu des pixels non vérifié.
- Cycles seulement.
- Libellé de la sortie multicouche non regardé à l'écran.
