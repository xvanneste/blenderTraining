# CH12.01 — Solutions

<!-- QUIZ_ANSWERS_START -->
## Réponses du quiz

| Q | Réponse | Explication |
|---|---|---|
| Q1 | **a** — Une bande de la ligne de temps : image, vidéo, son, couleur, effet | Ici quatre strips COLOR (Add > Color). |
| Q2 | **a** — Des strips qui se suivent ; des canaux superposés se recouvrent à l'image | Le canal le plus haut recouvre les autres. |
| Q3 | **a** — Le nombre d'images visibles du strip | 24, 30, 18 et 24 dans la solution. |
| Q4 | — | La fin d'un strip est exclusive : un strip de 24 images qui commence à 1 finit avant l'image 25 ; le suivant commence à 25. |
| Q5 | — | La plage de la scène (Frame End) borne ce qui est rendu ; les strips au-delà ne sont pas exportés : starter 1–139, solution 1–96. |
| Q6 | **a** — Déplacer le strip suivant pour qu'il commence à la fin du précédent | Contre-exemple gap : débuts [1, 30, 60, 78]. |
| Q7 | **a** — Les données peuvent être justes et l'image fausse (canal, ordre) | Le correcteur lit la couleur du pixel central aux images 12, 40, 63, 85. |
| Q8 | — | C_blue sur le canal 2 : le rendu est correct à l'image 63 (il recouvre le canal 1) mais le montage n'est pas sur une seule piste : le correcteur le refuse. |
| Q9 | — | Ce sont des copies légères de vidéos lourdes pour monter fluidement ; non mesurés ici (strips de couleur). |
| Q10 | — | Des strips de couleur : pas de vidéo, de son, de transition ni d'effet ; le montage narratif (rythme) est traité en CH12.02. |
<!-- QUIZ_ANSWERS_END -->

## Exercices
`COMPLETED_EXAMPLES/ch12_01_vse_solution.blend` (+ `_reference.png`)

**Fabrication.** Générées par script (`build_ch12_01_files.py`) : quatre strips COLOR ; mesures par données et par rendu du séquenceur. Score 45/45 ; starter 15/45. Rendus regardés.

## Contre-épreuve du correcteur (`COMPLETED_EXAMPLES/COUNTER_EXAMPLES/`)
| Fichier faux | Défaut | Tests qui le refusent |
|---|---|---|
| `…_gap` | trou de 5 images avant B_green | débuts |
| `…_wrong_durations` | B_green reste à 41 images | durées ; rendu |
| `…_wrong_order` | vert avant rouge | ordre ; débuts ; rendu |
| `…_wrong_channel` | C_blue sur le canal 2 | canal |
| `…_frame_end` | plage de la scène non réduite (1–139) | plage de la scène |
Aussi refusé : le starter.

## Limites
- Strips de couleur seulement.
- Libellés des panneaux non relus.
- Proxies et ripple non mesurés.
