# CH01.14 — Exercices

## Exercice 1 — Facile : EEVEE contre Cycles ⏱ 10 min
Rendez la nature morte en EEVEE puis en Cycles (même résolution). Notez les deux temps et
trois différences visibles (ombres, reflets, lumière indirecte…).

## Exercice 2 — Moyen : la courbe qualité/temps ⏱ 20 min
En Cycles, à 50 %, sans débruitage : *Max Samples* 16, 64, 256, 1024 (seuil 0). Puis 64 avec
débruitage. Tableau temps/qualité ; quel réglage choisiriez-vous pour une animation de
2 880 images ?

## Exercice 3 — Difficile : le premier rendu final (SANS procédure) ⏱ 10 min (hors temps de calcul)
Les consignes du `README_EXERCICE`, validez (`--exercise final`).
Barème (14 pts + bonus) : Cycles sur CPU ou GPU 2 · échantillonnage 2 · débruitage 1 · résolution 1 ·
format 1 · chemin 1 · couleurs 2 · image présente 3 · exposition 1 · bonus EEVEE 1.

## Défis
- **Défi 1 :** rendu à fond transparent (*Render → Film → Transparent*, PNG RGBA) et
  incrustation sur une couleur dans un logiciel d'image.
- **Défi 2 :** rendez les images 1 à 24 d'une rotation de caméra simple (*Ctrl+F12*), puis
  regardez la séquence (*Render → View Animation*).

## Mini-projet — PROJET DE PHASE P1 « Nature morte »
Voir [../PROJECT_P1/README.md](../PROJECT_P1/README.md) : il réunit tous les chapitres de la phase 1.

## Tests chronométrés
| Test | Cible |
|---|---|
| Réglage complet d'un rendu final Cycles | 1 min 30 |
| Enregistrer le rendu au bon endroit | 15 s |
| Passer de EEVEE à Cycles et comparer deux slots | 30 s |
