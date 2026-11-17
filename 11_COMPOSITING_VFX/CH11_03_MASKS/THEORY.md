# CH11.03 — Cours théorique : Masques et Cryptomatte

## 1. Pourquoi un masque
Pour traiter une partie de l'image : étalonner un objet, le flouter, le désaturer.

## 2. L'index d'objet
Object Properties > Relations > Pass Index (entier) ; View Layer Properties > Passes > Data > Object Index (Cycles). Render Layers : prise Object Index.

## 3. ID Mask
Nœud ID Mask : ID value ← Object Index, Index = 2, Anti-Alias : sortie Alpha (le masque).

## 4. Mix avec masque
Nœud Mix (RGBA, mode Mix) : Factor = masque, A = fond désaturé (Hue/Saturation, Saturation 0), B = image d'origine.

## 5. Cryptomatte
Passe Cryptomatte Object ; nœud Cryptomatte V2 : source Render, matte_id « Sphere_B » ; prise Matte. Les noms remplacent les indices.

## 6. Mesurer
Saturation HSV moyenne d'un patch au centre de chaque sphère, après compositing.

## 7. Pièges
- Index modifiés ou mal choisis.
- Masque inversé.
- Mauvais moteur (EEVEE : pas de prise Object Index).
- Oublier le Factor du Mix.

## 8. Limites
Bords nets ; transparence et flou de mouvement non mesurés ; création des nœuds par l'interface non vérifiée.
