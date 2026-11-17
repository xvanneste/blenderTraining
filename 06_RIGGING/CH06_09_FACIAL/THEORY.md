# CH06.09 — Cours théorique : rig facial

## 1. Bones ou shape keys
- **Bones** : grands mouvements de rotation (mâchoire, yeux, paupières larges).
- **Shape keys** : formes fines et non rigides (sourire, plis, lèvres).
- Rigs de production : les deux, plus des contrôleurs placés sur ou autour du visage.

## 2. La tête de l'exercice
Sphère de 12 cm de rayon (32 × 16) : un support de mesure, pas un visage. Visage vers −Y. Zones : coins de la bouche à (±0,045 ; −0,1056 ; −0,04), paupières à (±0,04 ; −0,1086 ; 0,03).

## 3. La mâchoire
Bone jaw (charnière en (0 ; 0,06 ; −0,02), vers l'avant) enfant de head. Poids de jaw = smoothstep((0,04 − z)/0,14) : 0 au-dessus de z = 0,04, 1 sous z = −0,10. Rotation X de −15° : le menton descend de 3,4 cm, le haut du crâne ne bouge pas, l'étirement d'arête maximal est de 1,45 fois. Poids binaires (coupure à z = −0,03) : 2,92 fois. Le sens de rotation a été calibré par le script (le menton descend avec −15° autour de X).

## 4. Les shape keys par zone
smile : coins de la bouche vers le haut (12 mm au sommet le plus proche du centre, décroissance linéaire sur 35 mm) ; blink : paupières vers le bas (12 mm, rayon 25 mm). Chaque key est limité par un groupe (smile_zone, blink_zone), poids normalisés pour que le maximum soit exactement 1.

## 5. Contrôleurs et drivers
Glissières ctl_smile et ctl_blink : bones verticaux mobiles en X de 0 à 0,05 m (Limit Location, Local Space, Y et Z bloqués). Driver : valeur = x / 0,05 (Transform Channel, Location X, Local Space). Mesures : 0,025 m → 0,50 ; 0,05 m → 1,00 ; demandé 0,20 m → déplacement effectif 50 mm.

## 6. Pièges
- Poids de mâchoire trop durs.
- Shape key sans groupe (diaphonie).
- Contrôleur non borné.
- Driver mal normalisé.
- Contrôleurs au milieu du visage : préférer des contrôleurs en bordure ou un panneau dédié (CH06.10).

## 7. Limites
Tête sphérique sans bouche ni yeux modélisés ; deux expressions seulement ; la mesure porte sur les déplacements de sommets, pas sur le réalisme. Un vrai rig facial compte des dizaines de shape keys et de contrôleurs.
