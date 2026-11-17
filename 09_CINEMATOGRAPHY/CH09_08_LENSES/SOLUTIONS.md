# CH09.08 — Solutions

<!-- QUIZ_ANSWERS_START -->
## Réponses du quiz

| Q | Réponse | Explication |
|---|---|---|
| Q1 | **a** — Elle agrandit les objets et réduit le champ de vision | Hauteur apparente ∝ focale / distance. |
| Q2 | **a** — Environ 14° | 2 × atan(18 / 144) = 14,25° (mesuré : 14,3°). |
| Q3 | **a** — Une focale courte (champ large) | 35 mm : champ de 54° sur 36 mm de capteur. |
| Q4 | — | Les rayons convergent vers le centre optique : un objet deux fois plus loin couvre un angle deux fois plus petit (pour de petits angles). |
| Q5 | — | Largeur 36 mm, Sensor Fit Auto : en 16:9 la hauteur du capteur utile est 36 × 9 / 16 = 20,25 mm. |
| Q6 | **a** — 24 m (rapport 32/40) | (8 + c) / (16 + c) = 0,8 → c = 16 minimum pour 0,75. |
| Q7 | **a** — Non : le rapport des distances ne change pas | Mesuré : focale 70 sans reculer → rapport 48 %, comme au départ. |
| Q8 | — | Pour comparer deux focales à cadrage égal : seule la perspective change, pas la taille du sujet. Hauteur = 1,8 × f / ((8 + c) × 20,25). |
| Q9 | — | Il segmente le rouge et le vert, prend l'étendue verticale de chacun et divise ; la quantification à 90 lignes donne 0,46 pour une valeur théorique de 0,5. |
| Q10 | — | Deux cylindres, un fond uni, un rendu Workbench : elle ne juge ni la distorsion des bords (grand angle) ni le rendu des visages ; elle vérifie le calcul de la compression. |
<!-- QUIZ_ANSWERS_END -->

## Exercices
`COMPLETED_EXAMPLES/ch09_08_lenses_solution.blend` (+ `_reference.png`)

**Fabrication.** Générées par script (`build_ch09_08_files.py`) : sol, deux cylindres, caméra reculée ; calibrations par rendu. Score 32/32 ; starter 19/32. Rendus regardés.

## Contre-épreuve du correcteur (`COMPLETED_EXAMPLES/COUNTER_EXAMPLES/`)
| Fichier faux | Défaut | Tests qui le refusent |
|---|---|---|
| `…_wide` | départ : grand angle, rapport 46 % | compression ; téléobjectif |
| `…_moved_only` | caméra reculée de 24 m mais focale 35 : sujet de 9 % | hauteur du sujet ; focale |
| `…_zoomed_only` | focale 70 sans reculer : sujet de 79 %, rapport 48 % | hauteur du sujet ; compression |
| `…_short_lens` | reculé de 24 m, focale 75 : sujet de 20 % | hauteur du sujet |
| `…_subject_moved` | sujet reculé à 16 m pour tricher | cylindres immobiles ; hauteur |
Aussi refusé : le starter.

## Limites
- Deux cylindres et un fond uni.
- Rendu 160 × 90 : quantification.
- Libellés d'interface non relus à l'écran.
