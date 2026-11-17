# CH04.07 — Cours théorique : baking

## 1. Principe
Le **baking** calcule une information (normales, ombrage, occlusion ambiante, couleur…) et l'écrit dans une **image** selon les UV d'un objet. Avantage : on remplace un calcul coûteux ou un détail géométrique par une lecture d'image.

## 2. Normal map
Une normal map stocke une normale (x, y, z) par pixel, encodée en RVB : valeur = (n + 1) / 2. Un plat vaut **(0,5 ; 0,5 ; 1)**. En espace **Tangent**, la normale est relative à la surface : l'image reste valable si l'objet se déforme ou tourne.
Branchement : *Image Texture* (Non-Color) → nœud **Normal Map** (Space : Tangent) → entrée **Normal** du Principled.

## 3. Réglages du bake (Cycles, onglet Render, panneau Bake ; libellés confirmés dans `cycles/ui.py`)
- **Bake Type** : Normal ; **Space** : Tangent.
- Sous-panneau **Selected to Active** : coché ; **Extrusion** (distance du « cage » en mètres, 0,25 ici) ; la case **Cage** est une alternative avec un objet cage.
- Sous-panneau **Margin** (Type et Size) : bande de pixels étendue autour des îlots (16 px ici).
Le haute définition est sélectionné, le basse définition est actif et son matériau a l'Image Texture cible **active**.

## 4. L'exercice
HIGH_Rock : icosphère 20 480 faces avec relief fractal (± 16 %). LOW_Rock : icosphère 320 faces, UV Smart Project (angle 66°, marge 0,02). Image `T_Rock_N` 512 × 512, Non-Color. Bake `object.bake(type='NORMAL')` (CPU, 1 échantillon, Extrusion 0,25 m, Margin 16 px).

## 5. Mesures du correcteur
Dans les îlots UV : 99,4 % des pixels portent du relief (écart ≥ 0,02 du plat), longueur moyenne des normales décodées 1,00, z moyen 0,87. Maillages intacts (HIGH ≥ 10 000, LOW ≤ 1 000 faces), HIGH caché au rendu.

## 6. Pièges
- Image en **sRGB** : relief faux.
- Image directement sur Normal, sans nœud Normal Map.
- Image non empaquetée : bake perdu.
- Cage trop courte : trous et coutures (extruder davantage).
- Changer l'espace colorimétrique d'une image générée réinitialise son tampon : à régler AVANT de remplir ou de baker.

## 7. Limites
Le correcteur mesure l'image et le graphe, pas la fidélité du relief par rapport au haute définition ; il n'évalue ni AO ni couleur bakées.
