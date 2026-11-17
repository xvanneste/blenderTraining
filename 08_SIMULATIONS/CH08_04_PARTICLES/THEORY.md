# CH08.04 — Cours théorique : Particules et distribution

## 1. Principe
Un système de particules naît sur un objet émetteur : nombre, intervalle d'émission (Frame Start/End), durée de vie, source (faces, sommets, volume), vitesse initiale (normale, aléatoire), physique (Newtonien, sans physique, Boids...), forces (gravité, vent, turbulence), obstacles (Collision).

## 2. L'exercice
EMITTER : grille de 0,5 m à z = 1 m (normales vers le haut). COL_Floor : plan de 6 × 6 m à z = 0. Réglages : 200 particules, images 1 à 30, vie 60, faces, vitesse normale 3, Newtonien, gravité 1, rendu None ; Collision du sol avec amortissement 0,5.

## 3. Rendu None
Pendant la mise au point on ne rend pas les particules : on lit leurs positions. Le rendu (objet instancié, halo, Geometry Nodes) vient après.

## 4. Mesures
Solution : 40/40 ; 97 particules nées à l'image 15 (49 %), 200 à l'image 30 ; sommet 1,46 m ; plus bas 0,00 m ; 0 vivante à l'image 95. Contre-exemples : sans collision du sol (−20,05 m) ; gravité 0 (sommet 8,2 m) ; vitesse normale 0 (sommet 1,0 m) ; rafale (200 nées à l'image 15) ; 40 particules ; vie 20.

## 5. Lire une simulation par script
Avancer de l'image 1 à N, puis lire `ob.evaluated_get(depsgraph).particle_systems[0].particles` : `alive_state` (UNBORN, ALIVE, DEAD) et `location` (espace monde).

## 6. Pièges
- Oublier Collision sur le sol.
- Frame End trop court (rafale).
- Vie plus courte que la durée utile.
- Gravité oubliée.
- Trop de particules pour un test.

## 7. Limites
Particules Newtoniennes sans rendu, un émetteur et un obstacle ; ni Boids, ni cheveux (CH08.08), ni forces autres que la gravité (CH08.09) ; le hasard de l'émission est reproductible (même graine) mais non figé par le correcteur : seuils larges.
