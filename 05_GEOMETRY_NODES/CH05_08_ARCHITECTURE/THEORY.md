# CH05.08 — Cours théorique : architecture procédurale

## 1. Penser en grille
Un immeuble courant est une **grille** : `Floors` étages × `Bays` travées. Chaque cellule reçoit un élément (fenêtre, balcon, porte). Les paramètres sont des dimensions réelles : Floor Height (≈ 3 m), Bay Width (≈ 2,5 m), Depth.

## 2. Le corps
Cube (`GeometryNodeMeshCube`, centré) dont Size = Combine XYZ (X = Bays × Bay Width ; Y = Depth ; Z = Floors × Floor Height), puis Transform (Translation z = hauteur ÷ 2) pour poser la base sur z = 0 ; Set Material (MAT_Wall).

## 3. La façade : une Grid centrée sur les travées
Une Grid de n × m sommets a des sommets aux extrémités de sa taille : pour obtenir un point au centre de chaque cellule, on prend **Vertices X = Bays**, **Vertices Y = Floors**, **Size X = (Bays − 1) × Bay Width**, **Size Y = (Floors − 1) × Floor Height** : l'espacement vaut exactement Bay Width et Floor Height, la grille est symétrique autour de l'axe.
Transform de la grille : Rotation X = 90° (Y → Z), Translation y = −Depth ÷ 2 (façade avant), z = Size Y ÷ 2 + 0,55 × Floor Height (première rangée à 0,55 × hauteur d'étage).
Instance on Points : fenêtre = Cube 1,2 × 0,12 × 1,4 + Set Material (MAT_Window).

## 4. Les mathématiques en nœuds
Multiply, Divide, Subtract, Add (nœud Math) ; Combine XYZ pour les vecteurs. Garder les noms et un nœud par opération ; Frames pour grouper (corps, façade).

## 5. Mesures de la solution
Réglage A (4 étages, 5 travées, 3 m, 2,5 m, 8 m) : 20 fenêtres, corps 12,5 × 8 × 12 m, colonnes espacées de 2,5 m, rangées de 3 m, première rangée à 1,65 m. Réglage B (7, 3, 3,4, 3,2, 10) : 21 fenêtres, corps 9,6 × 10 × 23,8 m.

## 6. Pièges
- Valeur codée en dur (nombre de fenêtres, hauteur) : correct pour un réglage seulement.
- Vertices X = Bays + 1 : une colonne de plus, espacement faux.
- Oublier la translation de hauteur ÷ 2 : bâtiment à moitié enterré.
- Fenêtres à y = 0 : invisibles, à l'intérieur du volume.

## 7. Limites
Façade avant seulement, fenêtres identiques, toit plat sans corniche, pas de porte : un point de départ, pas un bâtiment complet. Le correcteur ne juge pas l'architecture.
