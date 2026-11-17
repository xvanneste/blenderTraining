# CH11.08 — Solutions

<!-- QUIZ_ANSWERS_START -->
## Réponses du quiz

| Q | Réponse | Explication |
|---|---|---|
| Q1 | **a** — La position d'un même point de l'image suivie d'image en image | Chaque piste contient un marqueur par image suivie. |
| Q2 | **a** — Le solveur en a besoin pour relier points 2D et rayons 3D | Focale 35 mm, capteur 36 mm dans l'exercice. |
| Q3 | **a** — Detect Features (clip.detect_features) | À l'image 1 : 8 à 28 pistes selon les réglages. |
| Q4 | — | Le solveur compare des points visibles sur plusieurs images : les pistes courtes ne donnent pas de mouvement (suivi de 8 images : aucune piste de 30 marqueurs, résolution impossible). |
| Q5 | — | L'opérateur suit les pistes sélectionnées ; sans sélection rien n'est suivi. |
| Q6 | **a** — Sans mouvement de translation, le solveur ne sait pas séparer profondeur et mouvement | La caméra avance de −1 à +1 m : les points proches bougent plus. |
| Q7 | **a** — L'écart en pixels entre un point suivi et le point 3D reconstruit reprojeté | 0,75 pixel pour la solution ; le correcteur exige ≤ 1,0. |
| Q8 | — | La résolution a réussi (0,75 px) avec 100 mm : le solveur s'adapte ; mais la caméra reconstruite aurait une mauvaise perspective : c'est pourquoi la focale est contrôlée par le correcteur. |
| Q9 | — | Des pistes valides mais aucune reconstruction enregistrée : le correcteur la détecte et refait la résolution pour montrer qu'elle est possible. |
| Q10 | — | Un plan synthétique sans flou, sans bruit ni occlusion, avec des points parfaits : un vrai plan demande du nettoyage de pistes et de la calibration d'objectif ; l'alignement de la scène 3D (setup tracking scene) n'est pas évalué. |
<!-- QUIZ_ANSWERS_END -->

## Exercices
`COMPLETED_EXAMPLES/ch11_08_tracking_solution.blend` (+ `_reference.png`)

**Fabrication.** Générées par script (`build_ch11_08_files.py`) : séquence de 40 images rendue (Workbench), clip, pistes et solution par opérateurs ; mesures sur les données enregistrées et sur une nouvelle résolution. Score 36/36 ; starter 6/36. Image regardée.

## Contre-épreuve du correcteur (`COMPLETED_EXAMPLES/COUNTER_EXAMPLES/`)
| Fichier faux | Défaut | Tests qui le refusent |
|---|---|---|
| `…_short_tracks` | suivi sur 8 images seulement : aucune piste de 30 marqueurs | pistes ; reconstruction |
| `…_wrong_focal` | focale 100 mm : le solveur réussit quand même (0,75 px) | focale du clip |
| `…_not_solved` | pistes sans Solve Camera Motion | reconstruction enregistrée |
| `…_few_tracks` | 4 pistes seulement : le solveur échoue | pistes ; reconstruction |
Aussi refusé : le starter.

## Limites
- Plan synthétique parfait.
- Opérateurs de clip appelés par un éditeur temporaire.
- Alignement de scène non évalué.
