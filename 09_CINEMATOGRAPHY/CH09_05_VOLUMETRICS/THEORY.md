# CH09.05 — Cours théorique : Volumétrie

## 1. Diffusion
Un volume contient des particules qui absorbent et diffusent la lumière. Le faisceau d'un spot devient visible parce que les particules diffusent un peu de lumière vers la caméra.

## 2. Le matériau
Cube Fog (8 × 8 × 6 m) : matériau sans surface, avec un Principled Volume relié à Material Output > Volume. Réglages : Density, Anisotropy.

## 3. Densité
Mesures du centre de l'image : Density 0 : 0 ; 0,004 : 0,007 ; 0,08 : 0,088 ; 1,5 : 0,0007. Une densité moyenne maximise la visibilité ; trop dense, la lumière n'atteint pas le centre du faisceau.

## 4. Le spot
3 000 W, 40°, Blend 0,3, placé à 5,5 m, visant vers le bas. Un spot trop large (150°) éclaire tout le brouillard.

## 5. L'exercice
Régler Density (0,08) ; le correcteur rend 96 × 96 (Cycles, 64 échantillons) et lit le centre et les bords du tiers médian de l'image.

## 6. Bruit
Un volume est bruité ; sur un rendu final il faut plus d'échantillons ou un débruitage. La mesure moyenne sur 9 colonnes.

## 7. Pièges
- Cube dont le matériau a aussi une surface : un objet opaque.
- Caméra à l'intérieur du volume : comportement différent (non testé).
- Densité trop forte : image noire.

## 8. Limites
Rendu Cycles seulement (EEVEE non testé) ; un seul volume homogène ; pas de brouillard de hauteur ni de bruit de densité ; le faisceau est mesuré, pas jugé.
