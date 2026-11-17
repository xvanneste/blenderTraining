# CH11.07 — Cours théorique : Keying

## 1. La clé
Choisir la couleur du fond (Key Color) pour fabriquer un matte.

## 2. Le nœud Keying
Entrées : Image, Key Color, Blur Size, Balance, Black/White Level, Size, Tolerance, Garbage/Core Matte, Dilate, Feather… ; sorties : Image, Matte, Edges. Il fait aussi une correction de contamination.

## 3. Le Chroma Matte
Autre matte, plus simple, sans correction de contamination.

## 4. La contamination
Le vert du fond se reflète sur le sujet et se voit sur le nouveau fond : on le retire avec Color Spill (canal G) ou avec le Keying.

## 5. La composition
Alpha Over : Background = nouveau fond (nœud RGB, image, rendu 3D), Foreground = sujet détouré.

## 6. L'exercice
Image → Keying → (Color Spill) → Alpha Over (fond bleu) → Group Output.

## 7. Pièges
- Mauvaise Key Color (bleu au lieu de vert).
- Oublier le nouveau fond (fond noir).
- Comparer des couleurs linéaires à des couleurs affichées.
- Un matte trop dur.

## 8. Limites
Pas de cheveux, de transparence ni de flou ; un sujet simple ; un fond généré.
