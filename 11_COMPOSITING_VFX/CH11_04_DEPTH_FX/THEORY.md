# CH11.04 — Cours théorique : Depth, defocus, motion blur

## 1. Les passes
Depth (distance) et Vector (déplacement par pixel) sont activées dans View Layer Properties > Passes > Data. Render Layers en fournit les prises.

## 2. Defocus
Nœud Defocus : Image, Z ← Depth, Use Z-Buffer, F-stop (Blur Max). La distance de mise au point vient de la caméra (Focus Distance). Mesuré : 5 m → Near 1,00 et Far 0,30 ; 30 m → Far 0,92.

## 3. Le flou en post
Il agit sur l'image : plus de souplesse, mais pas d'information masquée.

## 4. Vector Blur
Nœud Vector Blur : Image, Speed ← Vector, Depth ← Depth, Samples, Shutter.

## 5. Shutter
Durée d'obturation en fraction d'image : 0 = net ; 1 = flou d'une image entière de déplacement.

## 6. L'exercice
Défocus puis Vector Blur sur l'image 10 d'une barre qui bouge de −0,5 à 0,5 m.

## 7. Pièges
- Oublier la mise au point de la caméra.
- Oublier la passe Vector (aucun étalement).
- Compter le flou de mouvement deux fois (rendu + post).
- Pic de flou trop fort (blur_max).

## 8. Limites
Barres fines et fond noir ; pas de bokeh coloré ni de bords de profondeur ; un seul mouvement.
