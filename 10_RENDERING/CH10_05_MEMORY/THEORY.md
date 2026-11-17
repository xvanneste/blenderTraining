# CH10.05 — Cours théorique : Mémoire et optimisation

## 1. Trois sources de poids
Maillages (un par objet si non partagés), géométrie évaluée (modificateurs), textures (taille × octets par pixel).

## 2. Partager un maillage
Object > Link/Transfer Data > Link Object Data (Ctrl+L) : plusieurs objets utilisent le même datablock Mesh. Mesuré : 200 maillages → 1.

## 3. Instancier une collection
Un empty avec Instance > Collection affiche la collection sans la dupliquer ; la source (collection exclue du calque) n'est évaluée qu'une fois : 1 920 triangles au lieu de 384 000.

## 4. Triangles évalués
Un maillage partagé reste évalué par objet : le modificateur Subdivision Surface se paie 200 fois (384 000 triangles à 1 920 par rocher). Baisser le niveau (0 : 16 000) ou instancier.

## 5. Textures
64 Mo pour 4 096² en 8 bits RGBA. Render Properties > Simplify (case de l'en-tête) > Render > Texture Limit : à 1 024, 4 Mo.

## 6. Simplify
Panneau Simplify : réglages globaux de rendu (subdivision maximale, enfants de particules, limite de texture…). Ici on n'utilise que la limite de texture.

## 7. LOD
Niveaux de détail (objets différents selon la distance) : non traité ici ; à envisager pour des scènes d'animation avec caméra mobile.

## 8. Limites
Triangles et Mo sont des proxys ; la mémoire réelle d'un rendu dépend aussi des BVH, des passes et des matériaux.
