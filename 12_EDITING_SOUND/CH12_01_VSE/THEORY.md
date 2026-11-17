# CH12.01 — Cours théorique : Video Sequencer

## 1. Strips et canaux
Un strip : début (`frame_final_start`), durée (`frame_final_duration`), canal (`channel`). Add > Color crée un strip de couleur.

## 2. Bout à bout
Chaque strip commence là où finit le précédent (fin exclusive). Trou = image noire ; recouvrement = le canal supérieur gagne.

## 3. Raccourcir
Poignées d'extrémité ou propriété de durée : le contenu est coupé, pas déformé.

## 4. La plage de la scène
Frame Start / Frame End de la timeline : ce que le rendu exporte.

## 5. L'exercice
A_red 24, B_green 30, C_blue 18, D_yellow 24 : total 96.

## 6. Mesurer
Données (débuts, durées, canal) et rendu du séquenceur à quatre images (Workbench, vue Standard).

## 7. Pièges
- Plage de scène oubliée.
- Strip sur le mauvais canal.
- Fin exclusive prise pour inclusive.
- Strips muets.

## 8. Proxies et ripple
Proxies (copies légères de vidéos) et édition « ripple » (les strips suivants suivent un retrait) ne sont pas mesurés ici ; les libellés exacts des panneaux Strip > Time n'ont pas été relus.
