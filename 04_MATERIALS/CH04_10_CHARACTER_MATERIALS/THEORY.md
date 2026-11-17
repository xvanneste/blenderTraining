# CH04.10 — Cours théorique : matériaux de personnages

## 1. Peau
Base Color chair (0,65 ; 0,42 ; 0,34), Roughness 0,45. **Subsurface** : Weight 1 ; Radius (1 ; 0,2 ; 0,1) — le rouge diffuse plus loin que le vert puis le bleu ; Scale 0,05 (échelle en mètres du rayon, à adapter à la taille du modèle). Pores : Noise (Scale 250 ; Detail 3) → Bump (Strength 0,15 ; Distance 0,005) → Normal.
En production : cartes de couleur, de rugosité et de relief peintes ou photographiées (UV, CH04.01–02), plusieurs couches de sous-surface.

## 2. Œil
Sclère (0,85 ; 0,82 ; 0,78) et iris (0,22 ; 0,10 ; 0,04) séparés par une Color Ramp à interpolation constante pilotée par une Gradient Texture (linéaire, via Mapping tourné de 90° autour de Z). Cornée : **Coat Weight 1, Coat Roughness 0,02**, Roughness 0,2. En production : une vraie géométrie d'œil (cornée en dôme, iris en retrait), une texture d'iris détaillée et une pupille.

## 3. Cheveux
Nœud **Principled Hair BSDF** relié à Surface : modèle Chiang, paramétrage par couleur (Color 0,12 ; 0,06 ; 0,03), Roughness 0,3. Il est pensé pour des fibres (courbes) ; sur une sphère l'aspect est celui de points sombres, ce n'est qu'un banc d'essai du matériau.

## 4. Tissu
Base Color (0,15 ; 0,25 ; 0,55), Roughness 0,8, **Sheen Weight 0,5** (Sheen Roughness 0,5), Metallic 0. Trame : Wave (Bands, Scale 120) → Bump (Strength 0,4) → Normal.

## 5. Règles du correcteur
Skin : Base Color R > V > B, luminance 0,3–0,8 ; Subsurface Weight ≥ 0,5 ; Radius R > V > B et R ≥ 3 × B ; Scale 0,01–0,2 ; Roughness 0,3–0,65 ; bump + texture sur Normal.
Eye : Gradient + Color Ramp (écart de luminance ≥ 0,3) ; Roughness ≤ 0,4 ; Coat Weight ≥ 0,8, Coat Roughness ≤ 0,1.
Hair : Principled Hair BSDF → Surface ; luminance ≤ 0,4 ; Roughness 0,2–0,5.
Cloth : Metallic ≤ 0,05 ; Roughness ≥ 0,6 ; Sheen ≥ 0,3 ; bump + texture sur Normal.
Moteur Cycles.

## 6. Pièges
- Peau sans sous-surface : plastique ; rayon uniforme : peau grise.
- Œil sans vernis : œil mort.
- Cheveux en Principled BSDF : plastique.
- Tissu sans Sheen : papier.
- Sous-surface en EEVEE : approximée ; Cycles pour juger.

## 7. Limites
Les sphères ne sont pas des visages ; le correcteur contrôle les valeurs et les graphes, pas la ressemblance. Le rendu a été regardé (peau rosée et douce, œil crédible, cheveux en points, tissu bleu).
