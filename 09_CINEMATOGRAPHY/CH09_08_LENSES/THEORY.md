# CH09.08 — Cours théorique : Objectifs et focales

## 1. Focale et champ de vision
Champ horizontal = 2 × atan(largeur du capteur / (2 × focale)). Capteur de 36 mm : 35 mm → 54,4° ; 70 mm → 28,8° ; 144 mm → 14,3° (valeurs lues sur `Camera.angle_x`).

## 2. Le capteur
Camera > Sensor > Size (largeur) et Sensor Fit (Auto : la dimension la plus grande de l'image suit la largeur). En 16:9, la hauteur utile est 20,25 mm.

## 3. Grand angle et téléobjectif
Grand angle : caméra proche, perspective accentuée, fond minuscule. Téléobjectif : caméra loin, fond comprimé. Le sujet peut avoir la même taille dans les deux cas : c'est la distance qui change l'effet, pas la focale seule.

## 4. Hauteur apparente
Hauteur dans l'image (fraction) = hauteur réelle × focale / (distance × hauteur du capteur utile).

## 5. L'exercice
Sujet à 8 m, fond à 16 m, 1,8 m chacun. Rapport = (8 + c) / (16 + c) où c est le recul. Sujet à 40 % : f = 0,4 × (8 + c) × 20,25 / 1,8. Solution c = 24, f = 144 mm.

## 6. Mesure
Rendu Workbench plat 160 × 90 : segmentation rouge (sujet) et vert (fond) ; hauteurs = étendue verticale. Mesuré : départ 0,46, solution 0,78.

## 7. Pièges
- Zoomer sans reculer : le sujet grossit, le rapport ne change pas.
- Reculer sans zoomer : tout devient minuscule.
- Déplacer les objets au lieu de la caméra.
- Oublier que Sensor Fit change l'angle.

## 8. Limites
Pas de distorsion des bords, pas de profondeur de champ (CH09.09), pas de mouvement de caméra (CH09.10).
