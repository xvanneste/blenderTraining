# CH11.05 — Solutions

<!-- QUIZ_ANSWERS_START -->
## Réponses du quiz

| Q | Réponse | Explication |
|---|---|---|
| Q1 | **a** — Ajoute un halo ou des traînées autour des zones très lumineuses | Types : Bloom, Ghosts, Streaks, Fog Glow, Simple Star. |
| Q2 | **a** — Fog Glow (anneau 0,0066) | Bloom et Ghosts noient l'image avec les réglages par défaut. |
| Q3 | **a** — La luminosité à partir de laquelle un pixel produit un halo | Défaut 1,0 : seules les valeurs supérieures à 1 débordent. |
| Q4 | — | Une valeur de 30 dans le rendu (HDR) dépasse le seuil : seules les sources réellement plus lumineuses que le blanc font un halo ; la barre (1,0) n'en fait pas. |
| Q5 | — | Des reflets multiples qui remplissent le champ lointain : 0,80 (≤ 0,1 exigé). |
| Q6 | **a** — Courbe les lignes droites vers les bords, comme un objectif réel | Distortion 0,3 : la barre se courbe de +7 pixels. |
| Q7 | **a** — Entre 0,15 et 0,4 environ (courbure +4 à +12 pixels) | 0,1 → +2 pixels ; 0,6 → la barre sort de l'image. |
| Q8 | — | Elle grossit le centre : la lampe passe de 11 à environ 16 pixels de rayon ; le correcteur place donc l'anneau de mesure plus loin (rayon 20–30). |
| Q9 | — | Je n'ai pas trouvé de nœud de grain dédié dans la liste des nœuds du compositeur 5.3 : le grain peut se faire avec du bruit procédural, non traité ici. |
| Q10 | — | Une lampe et une barre ; le halo est mesuré par l'énergie d'un anneau, pas par son aspect ; Streaks et Simple Star ne sont pas évalués individuellement. |
<!-- QUIZ_ANSWERS_END -->

## Exercices
`COMPLETED_EXAMPLES/ch11_05_glare_solution.blend` (+ `_reference.png`)

**Fabrication.** Générées par script (`build_ch11_05_files.py`) : disque émissif, barre émissive, arbre Glare / Lens Distortion ; mesures par rendu. Score 37/37 ; starter 21/37. Rendus regardés.

## Contre-épreuve du correcteur (`COMPLETED_EXAMPLES/COUNTER_EXAMPLES/`)
| Fichier faux | Défaut | Tests qui le refusent |
|---|---|---|
| `…_no_glare` | sans Glare : anneau 0,0003 | halo |
| `…_bloom_strong` | Bloom : anneau 0,88 | halo ; halo contenu ; courbure |
| `…_ghosts` | Ghosts : anneau 1,0, champ lointain 0,80 | halo ; halo contenu |
| `…_no_distortion` | sans Lens Distortion : courbure 0 | courbure de la barre |
| `…_over_distortion` | Distortion 0,6 : la barre sort de l'image | courbure de la barre |
Aussi refusé : le starter.

## Limites
- Fog Glow par défaut très discret.
- Pas de grain.
- Scène minimale.
