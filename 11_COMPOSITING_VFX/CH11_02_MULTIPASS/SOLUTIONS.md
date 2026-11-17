# CH11.02 — Solutions

<!-- QUIZ_ANSWERS_START -->
## Réponses du quiz

| Q | Réponse | Explication |
|---|---|---|
| Q1 | **a** — La lumière est additive : la somme des contributions donne l'image complète | Image ≈ Combined_key + Combined_fill (rendu Cycles, sans passes post). |
| Q2 | **a** — Combined_key et Combined_fill | Constaté sur Render Layers : Image, Alpha, Noisy Image, Combined_key, Combined_fill. |
| Q3 | **a** — Mix (ShaderNodeMix, data_type RGBA, blend_type ADD) | Le nœud MixRGB du compositeur n'existe plus : constaté par l'API. |
| Q4 | — | Le but du relighting est de changer l'éclairage sans refaire le rendu : le correcteur vérifie que les lampes sont intactes. |
| Q5 | — | Si on passe par la prise Image, les light groups sont ignorés : rapport 1,17 comme au départ. |
| Q6 | **a** — Multiplie la lumière par 2 | +1 sur KEY et −1 sur FILL : rapport 2 / 0,5 = 4. |
| Q7 | **a** — Un rapport de lumière se lit sur des valeurs linéaires ; l'image affichée est en sRGB | En sRGB la solution donne 1,94 ; en linéaire 4,28. |
| Q8 | — | L'éteindre (missing_fill : 0,003) rend l'ombre noire et plate ; le correcteur exige ≥ 0,01. |
| Q9 | — | Deux (2^2 = 4) : +1 sur la KEY et −1 sur la FILL. |
| Q10 | — | Une sphère, deux lampes ponctuelles, deux flancs ; le relighting additif ne change ni les ombres portées ni les réflexions d'objets absents des groupes. |
<!-- QUIZ_ANSWERS_END -->

## Exercices
`COMPLETED_EXAMPLES/ch11_02_multipass_solution.blend` (+ `_reference.png`)

**Fabrication.** Générées par script (`build_ch11_02_files.py`) : sphère, deux lampes ponctuelles, light groups, arbre de compositing ; mesures par rendu. Score 38/38 ; starter 20/38. Rendus regardés.

## Contre-épreuve du correcteur (`COMPLETED_EXAMPLES/COUNTER_EXAMPLES/`)
| Fichier faux | Défaut | Tests qui le refusent |
|---|---|---|
| `…_no_relight` | exposures à 0 : rapport 1,17 | rapport key/fill |
| `…_too_strong` | +3 / −3 diaphragmes : rapport 27,8 | rapport key/fill |
| `…_reversed` | −1 / +1 : rapport 0,32 | rapport key/fill |
| `…_missing_fill` | KEY seule : FILL éteinte (0,003) | prises de light groups ; FILL éteinte |
| `…_image_only` | Image + Exposure : light groups ignorés | prises de light groups |
Aussi refusé : le starter.

## Limites
- Une sphère, deux lampes.
- Passes Diffuse/Glossy non évaluées.
- Création des nœuds par l'interface non vérifiée.
