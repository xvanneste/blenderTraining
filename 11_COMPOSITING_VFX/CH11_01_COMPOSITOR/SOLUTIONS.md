# CH11.01 — Solutions

<!-- QUIZ_ANSWERS_START -->
## Réponses du quiz

| Q | Réponse | Explication |
|---|---|---|
| Q1 | **a** — À fournir l'image rendue (et ses passes) à l'arbre | Prises : Image, Alpha, plus les passes activées. |
| Q2 | **a** — Dans un nœud Group Output (prise « Image ») | Le nœud Composite n'existe plus dans la liste des nœuds : constaté par l'API. |
| Q3 | **a** — Par sa prise « Exposure » (en diaphragmes) | Dans 5.3 les réglages des nœuds sont des prises. |
| Q4 | — | Un nœud qui ne mène pas à la sortie : il ne change pas l'image et encombre l'arbre. |
| Q5 | — | Le rendu ignore l'arbre : mesuré, l'image est identique au rendu brut (compositing_off). |
| Q6 | **a** — Multiplie la lumière par 2^1,5 ≈ 2,8 | Luminance moyenne 0,277 → 0,459 (après l'affichage Standard). |
| Q7 | **a** — Il moyenne les pixels voisins | Bruit 0,029 (exposition seule) → 0,0063 avec Blur (3, 3). |
| Q8 | — | Le sujet disparaît dans le fond : avec 60 pixels la lisibilité tombe de 0,81 à 0,47. |
| Q9 | — | Deux rendus avec deux graines : la différence ne contient que du bruit ; écart-type / √2. |
| Q10 | — | Un flou n'est pas un débruitage (voir le nœud Denoise) : il lisse aussi les détails ; scène simple ; la création de l'arbre depuis l'interface n'est pas vérifiée. |
<!-- QUIZ_ANSWERS_END -->

## Exercices
`COMPLETED_EXAMPLES/ch11_01_compositor_solution.blend` (+ `_reference.png`)

**Fabrication.** Générées par script (`build_ch11_01_files.py`) : sphère et sol, arbre de compositing ; mesures par rendu avec deux graines. Score 45/45 ; starter 29/45. Rendus regardés.

## Contre-épreuve du correcteur (`COMPLETED_EXAMPLES/COUNTER_EXAMPLES/`)
| Fichier faux | Défaut | Tests qui le refusent |
|---|---|---|
| `…_no_exposure` | sans nœud Exposure : image trop sombre (0,278) | luminance |
| `…_no_blur` | sans nœud Blur : bruit 0,029 | bruit |
| `…_over_blur` | Blur de 60 pixels : lisibilité 0,47 | lisibilité de la sphère |
| `…_orphan_node` | nœud Glare non relié | nœud orphelin |
| `…_compositing_off` | compositing de rendu désactivé | compositing activé |
Aussi refusé : le starter.

## Limites
- Création de l'arbre dans l'interface non vérifiée.
- Une scène simple.
- Flou ≠ débruitage.
