# CH11.06 — Solutions

<!-- QUIZ_ANSWERS_START -->
## Réponses du quiz

| Q | Réponse | Explication |
|---|---|---|
| Q1 | **a** — Les ombres | Lift teinté bleu : ombres bleutées (+0,111 bleu−rouge). |
| Q2 | **a** — Les hautes lumières | Gain teinté orange : hautes lumières chaudes (+0,060 rouge−bleu). |
| Q3 | **a** — Les tons moyens (et la luminosité globale) | Gamma 2,0 neutre éclaircit trop : +0,125 de luminance. |
| Q4 | — | Le nœud 5.3 expose un facteur et une couleur par zone ; on règle la couleur (les prises 4, 6, 8) pour teinter. |
| Q5 | — | Une inversion : ombres chaudes et hautes lumières froides : l'étalonnage « orange et teal » à l'envers. |
| Q6 | **a** — Pour que la teinte seule change : on étalonne la couleur, pas la luminosité | Écart de luminance −0,001 : la solution ne change que la couleur. |
| Q7 | **a** — Pour vérifier séparément ombres et hautes lumières | Colonnes 4–31 (ombres) et 128–155 (hautes lumières). |
| Q8 | — | Le bout de la rampe vaut 1,0 : un Gain trop fort écrête tous les canaux au blanc et la teinte disparaît : mesuré, un Gain de 1,7/1,55/1,4 donnait 0 de chaleur. |
| Q9 | — | Un étalonnage subtil change la couleur sans rendre l'image artificielle ; ces écarts de 4 % suffisent à passer les seuils. |
| Q10 | — | Une rampe de gris : pas de peau, de ciel ni de saturation ; le goût de l'étalonnage n'est pas mesuré. |
<!-- QUIZ_ANSWERS_END -->

## Exercices
`COMPLETED_EXAMPLES/ch11_06_grading_solution.blend` (+ `_reference.png`)

**Fabrication.** Générées par script (`build_ch11_06_files.py`) : rampe de gris émissive, arbre Color Balance ; mesures par rendu avec et sans compositing. Score 36/36 ; starter 20/36. Rendus regardés.

## Contre-épreuve du correcteur (`COMPLETED_EXAMPLES/COUNTER_EXAMPLES/`)
| Fichier faux | Défaut | Tests qui le refusent |
|---|---|---|
| `…_all_warm` | Lift et Gain chauds : ombres chaudes (−0,164) | ombres froides |
| `…_all_cool` | Lift et Gain froids : hautes lumières froides (−0,068) | hautes lumières chaudes |
| `…_swapped` | ombres chaudes et hautes lumières froides | ombres ; hautes lumières |
| `…_too_bright` | solution + Gamma 2,0 : trop clair (+0,125) | exposition préservée |
| `…_no_grade` | Color Balance neutre | ombres ; hautes lumières |
Aussi refusé : le starter.

## Limites
- Rampe de gris seule.
- Lift/Gamma/Gain seulement.
- Goût non mesuré.
