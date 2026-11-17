# CH07.12 — Cours théorique : Animation de caméra

## 1. Les mouvements de base
- **Travelling** : la caméra se déplace (avant, arrière, latéral).
- **Panoramique** : la caméra pivote sur place.
- **Suivi** : la caméra garde le sujet au même endroit de l'image.
- **Zoom** : l'objectif change de focale (non traité ici).
Un mouvement doit être **motivé** par l'histoire.

## 2. Le travelling de l'exercice
CAM_Main, hauteur 1,6 m, focale 35 mm. Position Y de −8 m (image 1) à −4 m (image 72), interpolation Bezier. Vitesse maximale de 84 mm/image (2,0 m/s) ; vitesse aux extrémités 9 mm/image (11 % du maximum).

## 3. Le suivi
Contrainte Track To vers EMP_Subject : Track Axis −Z (l'axe de visée de la caméra), Up Axis Y. Écart de visée maximal mesuré : 0,03°. Le sujet traverse le champ de X = −1 à +1 en interpolation linéaire.

## 4. La caméra à l'épaule
Modificateur Noise sur les courbes X et Z de la position : Strength 0,1 ; Scale 8 images ; phases différentes. Écart-type du tremblé : 6,1 mm ; maximum 12 mm. Pas de bruit sur Y.

## 5. L'horizon
Le roulis est l'inclinaison de l'axe X de la caméra par rapport à l'horizontale : 0,0° dans la solution (Track To, Up Y). Un Damped Track conserve le roulis de départ (contre-exemple : 8,24°).

## 6. Mesures
Solution : 37/37 ; trajet −7,99 → −4,01 m ; hauteur 1,60 m ; vitesses 9 / 84 mm/image ; recul 0 mm ; visée 0,03° ; tremblé 6,1 mm ; roulis 0,0°. Contre-exemples : visée 16,4° (sans contrainte) ; vitesse aux extrémités 38 mm/image pour 56 (linéaire) ; tremblé 32 mm (Strength 0,5) ; tremblé 0 mm ; roulis 8,24° ; trajet −8 → −6 m.

## 7. Pièges
- Caméra sans suivi : le sujet quitte le cadre (16° d'écart).
- Travelling linéaire : départ et arrêt brusques.
- Bruit trop fort ou sur tous les axes.
- Horizon penché par accident.
- Même phase de bruit sur plusieurs axes.

## 8. Limites
Un seul plan, une seule caméra ; pas de zoom ni de profondeur de champ ; pas de rig de caméra complet (grue, rail) ; mesures de trajectoire, de visée et de tremblé seulement.
