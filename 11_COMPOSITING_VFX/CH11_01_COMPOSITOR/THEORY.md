# CH11.01 — Cours théorique : Compositor

## 1. Le principe
Le rendu produit des images et des passes ; le compositeur les combine et les corrige sans recalculer la scène.

## 2. L'arbre en 5.3
`scene.compositing_node_group` : un groupe de nœuds de type compositeur. Entrées : Render Layers (Image, Alpha, passes). Sortie : Group Output avec une prise « Image ». Le nœud Composite n'apparaît plus dans la liste des types.

## 3. Les prises
Les réglages sont des prises : Exposure (Image, Exposure), Blur (Image, Size en pixels X et Y, Type, Extend Bounds, Separable).

## 4. Le compositing de rendu
Output Properties > Post Processing > Pipeline : Compositing (`render.use_compositing`). Sans lui, l'arbre est ignoré.

## 5. L'exposition
+1,5 EV multiplie par 2,8. Appliquée après le rendu, elle remonte aussi le bruit : mesuré 0,029 avec l'exposition seule.

## 6. Le flou
Blur (3, 3) pixels ramène le bruit à 0,0063 ; 60 pixels efface la sphère.

## 7. Pièges
- Un nœud non relié.
- Compositing désactivé.
- Exposition avant ou après le flou (ici l'ordre change peu).
- Confondre flou et débruitage.

## 8. Limites
Création de l'arbre depuis l'interface 5.3 non vérifiée (le fichier de départ fournit l'arbre) ; Viewer et Backdrop non mesurés ; scène simple.
