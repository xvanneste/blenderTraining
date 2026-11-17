# CH12.05 — Solutions

<!-- QUIZ_ANSWERS_START -->
## Réponses du quiz

| Q | Réponse | Explication |
|---|---|---|
| Q1 | **a** — Un strip (type TEXT) qui affiche un texte pendant une durée | Add > Text ; API : `strips.new_effect(type='TEXT')`. |
| Q2 | **a** — (0,5 ; 0,5) | Coordonnées relatives à l'image ; (0,5 ; 0,1) pour un sous-titre en bas. |
| Q3 | **a** — Dans le tiers inférieur de l'image | Rendu : centre vertical à 0,90 de la hauteur (depuis le haut). |
| Q4 | — | Un titre de taille 12 ne fait que 310 pixels clairs au lieu de 5 686 : illisible ; le correcteur exige ≥ 1 500. |
| Q5 | — | Le titre est assez grand mais en bas à gauche (centre 0,28 / 0,76) : un titre se centre. |
| Q6 | **a** — Un fichier texte : numéro, temps début --> fin, texte | Exemple : 00:00:02,000 --> 00:00:03,500. |
| Q7 | **a** — Sequencer > Export Subtitles (bpy.ops.sequencer.export_subtitles) : tous les strips de texte | Constaté : il exporte aussi le titre ; le correcteur l'ignore. |
| Q8 | — | 2 images à 24 i/s, soit 0,0833 s : late_sub (+0,5 s) est refusé. |
| Q9 | — | La référence est « Bonjour. » : une faute de frappe ou de ponctuation est une erreur de sous-titre : typo est refusé. |
| Q10 | — | La police par défaut ; pas de style (boîte, ombre, contour), ni de retour à la ligne, ni de langues multiples ; le SRT n'est pas importé dans Blender (non trouvé en 5.3). |
<!-- QUIZ_ANSWERS_END -->

## Exercices
`COMPLETED_EXAMPLES/ch12_05_titles_solution.blend` (+ `_reference.png`)

**Fabrication.** Générées par script (`build_ch12_05_files.py`) : fond noir, strips TITLE/SUB1/SUB2, texte SUBTITLES.srt ; mesures par export SRT et rendu. Score 45/45 ; starter 3/45. Rendus regardés.

## Contre-épreuve du correcteur (`COMPLETED_EXAMPLES/COUNTER_EXAMPLES/`)
| Fichier faux | Défaut | Tests qui le refusent |
|---|---|---|
| `…_typo` | « Bonjour » sans le point | SRT exporté |
| `…_late_sub` | premier sous-titre en retard de 12 images (2,500 s) | SRT exporté |
| `…_top_sub` | sous-titres en haut de l'image | sous-titres lisibles ; rendu |
| `…_tiny_title` | titre de taille 12 (310 pixels) | titre ; titre rendu |
| `…_title_off_center` | titre en bas à gauche | titre rendu |
Aussi refusé : le starter.

## Limites
- Police par défaut.
- Pas d'import SRT.
- Menus non regardés.
