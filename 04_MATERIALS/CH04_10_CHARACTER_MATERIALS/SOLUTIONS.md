# CH04.10 — Solutions

<!-- QUIZ_ANSWERS_START -->
## Réponses du quiz

| Q | Réponse | Explication |
|---|---|---|
| Q1 | **b** — La lumière pénètre la peau, diffuse et ressort : sans cela elle paraît en plastique | La diffusion sous la surface adoucit les ombres et donne la teinte chaude. |
| Q2 | **b** — (1 ; 0,2 ; 0,1) | Le rouge diffuse beaucoup plus loin que le bleu : rayon R > V > B. |
| Q3 | **a** — La cornée humide brillante | Coat Weight 1 et Coat Roughness bas ajoutent le reflet net de la cornée. |
| Q4 | — | Une Gradient Texture linéaire (via Mapping) passe dans une Color Ramp à interpolation constante : sclère claire jusqu'à un seuil, puis iris brun (écart de luminance ≥ 0,3). |
| Q5 | — | Un Noise très fin (échelle 250) en Bump casse l'aspect lisse et accroche la lumière sans polygone. |
| Q6 | **b** — Principled Hair BSDF | Le Principled Hair BSDF modélise la diffusion de la lumière dans une fibre. |
| Q7 | **b** — Il ajoute un liseré clair en bordure, comme les fibres d'un tissu | Sheen Weight modélise la diffusion rétro-réfléchissante des fibres ; Sheen Roughness en règle l'étalement. |
| Q8 | — | Un tissu est mat : pas de reflet net ; la rugosité forte reste cohérente avec Sheen. |
| Q9 | — | Un Principled sur une surface donne un aspect de plastique ; le nœud dédié reproduit les reflets décalés (primaire, secondaire) d'une fibre. |
| Q10 | — | Le shader de cheveux est conçu pour des courbes (cheveux, fibres) ; sur une sphère il donne un aspect à points. La solution valide le matériau, pas la coiffure. |
<!-- QUIZ_ANSWERS_END -->

## Exercice 2
`COMPLETED_EXAMPLES/ch04_10_character_solution.blend` (+ `_reference.png`).

**Fabrication.** Générée par script (`build_ch04_10_files.py`) avec les valeurs de THEORY.md. Cycles CPU, 96 échantillons, débruitage. Score 38/38 ; starter 9/35.
Rendus regardés (trois versions) : la première avait du bruit (32 échantillons), une peau trop claire et un iris décentré (l'œil regardait sur le côté : la caméra voit l'œil par l'arrière-gauche) ; corrigés par plus d'échantillons, une peau plus foncée et une rotation de l'œil vers la caméra. Les cheveux sur une sphère donnent un aspect de points : c'est la limite de l'essai.

## Contre-épreuve du correcteur (`COMPLETED_EXAMPLES/COUNTER_EXAMPLES/`)
| Fichier faux | Défaut | Test qui le refuse (et lui seul) |
|---|---|---|
| `…_skin_opaque` | Subsurface Weight 0 | Skin : Subsurface Weight |
| `…_skin_uniform_radius` | rayon de sous-surface (1 ; 1 ; 1) | Skin : Subsurface Radius |
| `…_eye_dry` | Coat Weight 0 (cornée sèche) | Eye : Coat |
| `…_hair_principled` | cheveux en Principled BSDF (pas de Hair BSDF) | Hair : Principled Hair BSDF relié à Surface (les contrôles suivants disparaissent avec lui) |
| `…_cloth_no_sheen` | Sheen Weight 0 | Cloth : Sheen Weight |
Aussi refusé : le starter.

## Limites
- Les sphères ne sont ni un visage ni une chevelure ; le correcteur lit des valeurs.
- Le correcteur ne vérifie pas la ressemblance de la peau, ni une texture d'iris détaillée.
