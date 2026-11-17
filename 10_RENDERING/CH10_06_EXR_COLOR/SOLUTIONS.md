# CH10.06 — Solutions

<!-- QUIZ_ANSWERS_START -->
## Réponses du quiz

| Q | Réponse | Explication |
|---|---|---|
| Q1 | **a** — C'est un format flottant linéaire sans limite à 1,0 | Le PNG écrête à 1,0 (blanc). |
| Q2 | **a** — 1000,5 (arrondi du demi-flottant) | Un demi-flottant a un pas de 0,5 près de 1000. |
| Q3 | **a** — Compression avec perte : valeurs modifiées (1001,5 mesuré) | DWAA/DWAB sont destinés à l'image finale, pas aux données ni aux masters. |
| Q4 | — | ZIP, ZIPS, PIZ, RLE (et NONE) : mesuré à 1000,700. PXR24 perd un peu en 32 bits (1000,703) : erreur de 0,003. |
| Q5 | — | Constaté à la construction : passer de multicouche à monocouche réinitialise la profondeur et le codec ; on les réapplique avant d'écrire. Le correcteur le fait. |
| Q6 | **a** — Il lit le type du canal Combined.R dans l'en-tête (FLOAT = 2, HALF = 1) | Avec 16 bits le canal Combined.R est HALF. |
| Q7 | **a** — Blender relit les pixels d'un monocouche ; un multicouche n'a pas de pixels lisibles ainsi | En 5.3 `images.load` d'un multicouche a renvoyé aucune donnée. |
| Q8 | — | Non : constaté, le canal Depth.Z est toujours FLOAT (32 bits), seule la couleur passe en HALF. |
| Q9 | — | Non : en relisant les pixels aucune différence n'apparaît entre Linear Rec.709 et ACEScg ; le chapitre ne l'évalue pas et recommande de garder l'espace par défaut (Linear Rec.709). |
| Q10 | — | Un pixel, une valeur, un rendu de 16 × 16 ; pas de lecture des couches de profondeur ni de Cryptomatte, pas de mesure de taille ni de vitesse d'écriture. |
<!-- QUIZ_ANSWERS_END -->

## Exercices
`COMPLETED_EXAMPLES/ch10_06_exr_solution.blend` (+ `_reference.png`)

**Fabrication.** Générées par script (`build_ch10_06_files.py`) : plan émissif de 1000,7, quatre variantes ; mesures par écriture et relecture. Score 32/32 ; starter 5/32. Tableau regardé.

## Contre-épreuve du correcteur (`COMPLETED_EXAMPLES/COUNTER_EXAMPLES/`)
| Fichier faux | Défaut | Tests qui le refusent |
|---|---|---|
| `…_half_float` | 16 bits : valeur relue 1000,5 | profondeur ; valeur |
| `…_lossy_codec` | codec DWAA : valeur relue 1001,5 | valeur relue |
| `…_single_layer` | EXR monocouche | type de média |
| `…_no_z_pass` | passe Z désactivée | canal Depth.Z |
Aussi refusé : le starter.

## Limites
- Un pixel, 16 × 16.
- Espace colorimétrique non évalué.
- Pas de taille de fichier.
