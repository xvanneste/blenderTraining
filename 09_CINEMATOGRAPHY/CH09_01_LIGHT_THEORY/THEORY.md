# CH09.01 — Cours théorique : Théorie de la lumière

## 1. Quantité de lumière
Une lampe ponctuelle émet une puissance (Power, en watts dans Blender) : l'éclairement reçu à la distance d varie comme P / d². Mesure : lampe blanche de 10 W à 1 m, luminance au centre du plan 0,119 ; 3 fois plus loin : 0,0119 à 10 W, retrouvée avec 100 W (0,119).

## 2. Exposition
Une image est « bien exposée » quand ses valeurs sont dans la plage utile. Pour comparer des éclairages, on mesure sur un rendu linéaire (EXR en virgule flottante), pas sur un PNG encodé en sRGB.

## 3. Direction
Une lampe au-dessus du centre éclaire de façon symétrique ; une lampe décalée donne des ombres obliques. Ici : directement au-dessus (x = y = 0).

## 4. Dureté
Une source ponctuelle (Radius 0) donne une ombre nette ; une source étendue (Radius 0,5 m) donne un bord progressif : la pénombre. Mesuré : 3 pixels (nette), 8 pixels (étendue) sur 128 pixels de large.

## 5. Couleur
Color de la lampe multiplie la couleur de la surface : rouge 1, vert 0,85, bleu 0,65 → rouge / bleu = 1,54 sur un plan gris (chaud). Les lampes ont aussi une température (Temperature) : non testée ici.

## 6. L'exercice
Scène : Plate gris 50 % (6 × 6 m), Occluder (cube plat à z = 1 m), CAM à z = 6 m, monde noir. Le correcteur rend deux images Cycles (64 échantillons) : plan seul (exposition, couleur), puis avec l'ombre (pénombre).

## 7. Pièges
- Monde non noir : lumière ambiante parasite (mesuré : fond 0,05).
- Lampe visible à la caméra : disque lumineux parasite ; la mettre invisible.
- Oublier de compenser la couleur chaude (elle retire du vert et du bleu).
- Mesurer sur un PNG sRGB.

## 8. Limites
Une seule lampe ; surface mate ; pas de lumières de zone, spots ni soleil ; la température de couleur n'est pas testée ; mesure en un point.
