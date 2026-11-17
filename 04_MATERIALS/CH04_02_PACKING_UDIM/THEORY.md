# CH04.02 — Cours théorique : packing et UDIM

## 1. Packing : rappel et marges
Pack Islands place les îlots dans le carré [0, 1]². Réglages (libellés 5.3) : *Rotate*, *Rotation Method*, *Scale*, *Margin Method* (Scaled / Add / Fraction), *Margin*, *Pack to* (carré courant ou UDIM : voir §4).
Une marge de ≈ 2 % évite qu'un îlot « bave » sur son voisin au mip-mapping et au baking.

## 2. UDIM : pourquoi
Une texture unique est limitée en résolution et en mémoire. UDIM juxtapose des carrés UV ; chacun reçoit **sa propre image**. Un personnage : tête sur 1001, corps sur 1002, vêtements sur 1003…

## 3. Numérotation
Tuile = **1001 + ⌊u⌋ + 10·⌊v⌋**.
| u | v | Tuile |
|---|---|---|
| [0,1] | [0,1] | 1001 |
| [1,2] | [0,1] | 1002 |
| [0,1] | [1,2] | 1011 |
| [1,2] | [1,2] | 1012 |
Dix tuiles par rangée (1001–1010), puis 1011.

## 4. Workflow du chapitre
1. Les faces du couvercle ont l'index de matériau 1 (le groupe à part).
2. Chaque groupe est packé séparément : il remplit son carré.
3. Le couvercle est déplacé d'une unité en U : tuile 1002.
4. Une image UDIM (Image Texture > Source : UDIM Tiles) possède les tuiles 1001 et 1002.
Mesures de la solution : tuile 1001 (corps et sangles) occupation 76 %, tuile 1002 (couvercle) occupation 74 %, étirement 1,00, densité uniforme dans chaque tuile ;
densité du couvercle ≈ 1,5× celle du corps (longueur 3D par unité UV : 2,38 contre 1,57).

## 5. Pièges
- **Îlot à cheval** sur deux tuiles : coupure et perte de la peinture ; toujours déplacer un îlot d'un bloc.
- **Tuile manquante** dans l'image : magenta.
- **Chevauchement** dans une tuile : même défaut que dans CH04.01.
- Les tuiles ne s'affichent pas toutes en Solid : utiliser Material Preview.

## 6. Limites
Le correcteur vérifie les mesures par tuile et la présence des tuiles de l'image ; il ne juge pas le choix du découpage (quelles parties sur quelles tuiles) ni la résolution des images.
