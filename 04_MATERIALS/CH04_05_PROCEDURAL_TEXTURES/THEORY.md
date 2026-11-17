# CH04.05 — Cours théorique : textures procédurales

## 1. Procédural ou image
| | Procédural | Image |
|---|---|---|
| Résolution | illimitée | fixe |
| UV | inutiles (Object, Generated) | nécessaires |
| Répétition | aucune (ou contrôlée) | visible sans soin |
| Contrôle artistique | paramètres | pixel par pixel |
| Idéal pour | pierre, bois, brique, métal usé, nuages | logos, visages, usure placée |
En production on combine les deux (CH04.08).

## 2. Les textures procédurales du Shader Editor
Noise, Voronoi, Musgrave (selon version), Wave, Brick, Checker, Gradient, Magic, White Noise… Nous utilisons **Brick Texture** (type API `TEX_BRICK`).

## 3. La Brick Texture : réglages
Les entrées règlent les coordonnées, les couleurs, la taille des briques et le joint. Les propriétés *Offset* et *Offset Frequency* déterminent le décalage des rangées. La sortie **Color** fournit la couleur finale. **Fac** vaut 1 sur le mortier et 0 sur la brique, avec une transition si *Mortar Smooth* est activé.
Réglages de la solution : Scale 3, Mortar Size 0,03, Mortar Smooth 0,1, Offset 0,5 ; Color1 (0,35 ; 0,10 ; 0,06), Color2 (0,22 ; 0,07 ; 0,05), Mortar (0,55 ; 0,52 ; 0,47).

## 4. Le relief par Bump
Reliez Brick [Fac] à Bump [Height] et activez *Invert* pour que le joint paraisse plus bas que la brique. La sortie de Bump alimente *Normal* du Principled. *Strength* 0,8 et *Distance* 0,02 constituent le réglage de départ. Bump modifie l’ombrage. Pour modifier la silhouette, voir le [déplacement géométrique](../CH04_08_RELIEF/TUTORIAL.md).

[Manuel Blender 5.3 de Brick Texture](https://docs.blender.org/manual/en/5.3/render/shader_nodes/textures/brick.html)

## 5. Le mur
`PROP_Wall` : boîte de 3 × 2 × 0,2 m dont les dimensions sont dans la géométrie (échelle objet 1), tournée de 90° autour de X pour se tenir debout ; le motif lit les coordonnées Object (x, y locaux).

## 6. Pièges
- Échelle objet non uniforme : briques étirées.
- Offset = 0 : joints verticaux alignés (maçonnerie impossible).
- Bump non alimenté : rendu plat.
- Scale excessif : moirage.

## 7. Limites
Le correcteur contrôle réglages et liens ; il ne juge pas l'esthétique. Sur les côtés du mur (épaisseur), le motif se projette en traînées : acceptable pour ce chapitre.
