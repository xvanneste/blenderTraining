# CH07.04 — Cours théorique : Graph Editor

## 1. Les courbes
Le Graph Editor trace une courbe par propriété animée : l'axe horizontal est le temps, le vertical la valeur ; la pente est la vitesse. Les clés sont des points ; les **poignées** règlent la tangente à chaque clé. Touches de la keymap par défaut : **T** (interpolation), **V** (type de poignée).

## 2. Interpolation et poignées
- **Linear** : vitesse constante ; mécanique.
- **Constant** : marche d'escalier (blocking).
- **Bezier** avec poignées **Auto Clamped** : ralentis aux extrema, pas de dépassement.
Le pendule : clés −30°, +30°, −30° aux images 1, 13, 25. En linéaire : 5 °/image partout. En Bezier Auto Clamped : 0,31 °/image à l'extrémité (image 13) et 7,5 °/image au milieu.

## 3. Modificateurs de courbe
Chaque courbe peut recevoir des modificateurs (onglet Modifiers de la barre latérale du Graph Editor). **Cycles** répète la courbe à l'infini avant et après ses clés. **Noise** ajoute une variation pseudo-aléatoire lisse (Strength : amplitude, Scale : durée en images).

## 4. L'exercice
GEO_Pendulum (tige de 1 m pendue à son origine). Rotation Y : −30°, +30°, −30° aux images 1, 13, 25 ; Cycles ; Position Z plate avec Noise (Strength 0,06, Scale 6) ; plage 1–48.

## 5. Mesures
Solution : 33/33. Vitesse à l'extrémité 0,31 °/image ; maximale 7,5 °/image ; rotation de −30,0° à 30,0° sans dépassement ; répétition : 30,0°, −30,0°, 30,0° aux images 37, 49, 61 ; bruit : écart-type 5,9 mm, amplitude 24 mm. Contre-exemples : linéaire (5,0 °/image partout) ; constante (0 °/image) ; sans Cycles (−30° partout après l'image 25) ; sans Noise ; Strength 0,5 (amplitude 201 mm) ; amplitude 45°.

## 6. Pièges
- Poignées libres qui font dépasser la courbe.
- Cycles sans plage assez longue pour le voir.
- Noise trop fort : le mouvement saute.
- Modifier les clés au lieu des courbes (le correcteur vérifie les clés).
- Interpolation constante laissée du blocking.

## 7. Limites
Un seul objet, deux courbes ; pas de modificateurs Generator, Envelope ou Limits testés ; pas d'éditions de poignées à la main (les poignées Auto Clamped sont automatiques) ; l'esthétique du pendule n'est pas jugée.
