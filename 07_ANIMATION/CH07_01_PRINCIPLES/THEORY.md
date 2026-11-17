# CH07.01 — Cours théorique : les 12 principes

## 1. Les douze principes
Formulés par des animateurs des studios Disney et popularisés par l'ouvrage *The Illusion of Life* de Frank Thomas et Ollie Johnston (1981), ils valent pour le dessin, le 3D et le stop-motion.
1. **Squash & stretch** : écrasement et étirement ; volume constant.
2. **Anticipation** : préparation du mouvement (en sens inverse).
3. **Staging** : mise en scène ; une seule idée lisible à la fois.
4. **Straight ahead et pose to pose** : deux manières de construire (image après image ; poses clés puis intervalles).
5. **Follow through et overlapping action** : les parties souples continuent et se décalent (CH07.06).
6. **Slow in et slow out** : on accélère et on ralentit autour des poses (CH07.04).
7. **Arcs** : la plupart des mouvements naturels suivent des courbes.
8. **Secondary action** : action secondaire qui soutient l'action principale.
9. **Timing** : le nombre d'images donne poids, vitesse et émotion (CH07.05).
10. **Exaggeration** : accentuer sans trahir.
11. **Solid drawing** : volume, poids, équilibre (le « solid posing » en 3D, CH07.07).
12. **Appeal** : un personnage qui plaît et se lit.

## 2. Écraser et étirer à volume constant
Un objet dont le volume est constant : scale X × Y × Z = 1. Une balle écrasée sur Z (sz) s'élargit : sx = sy = 1/√sz. À sz = 0,6, sx = sy = 1,29. À sz = 1,35, sx = sy = 0,86. Entre clés, Blender interpole chaque courbe séparément : le volume s'écarte légèrement de 1 (mesuré : 0,088 au maximum, tolérance du correcteur 0,12).

## 3. Anticipation et pivot
Le saut de l'exercice : clés de position aux images 1 (sol), 8 (décollage), 18 (sommet, 2,0 m), 28 (atterrissage), 40 (repos). L'anticipation (image 5, sz = 0,72) précède le départ ; l'étirement est maximal juste après (image 8, sz = 1,35) ; le contact (image 28, sz = 0,6) écrase la balle. L'ORIGINE de la balle est à sa base : l'échelle part de là, la balle reste posée sur le sol.

## 4. Mesures de la solution
Contact au sol : 0,0 mm aux images 1, 8, 28. Anticipation : Scale Z min 0,72, X max 1,18. Étirement maximal : 1,35. Contact : 0,60. Sommet : (1, 1, 1). Repos final : (1, 1, 1).
Contre-exemple « floating » : origine au centre : point le plus bas à −17,5 cm (image 8) et +20 cm (image 28).

## 5. Pièges
- Écraser sans élargir (volume perdu).
- Pivot au centre (la balle flotte ou s'enfonce dans le sol).
- Oublier le repos final.
- Anticiper trop peu : le mouvement paraît soudain.
- Étirer pendant l'immobilité (au sommet).

## 6. Limites
Un seul objet, un seul saut ; la balle est lisse (pas de déformation interne) ; l'interpolation Bezier par défaut ; la qualité du timing (CH07.05) n'est pas jugée.
