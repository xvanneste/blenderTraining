# CH02.01 — Tutoriels pas à pas

Ouvrez `STARTER_FILES/ch02_01_topology_starter.blend`. Cinq « patients » sont alignés de gauche à
droite. Activez **Viewport Overlays → Statistics** et passez en vue fil de fer quand c'est utile
(`Z` → *Wireframe*).

## Tutoriel 1 — Diagnostiquer avant d'opérer
1. Sélectionnez un objet et entrez en mode Édition (`Tab`). Passez en sélection de faces
   (`3`) et désélectionnez avec `Alt+A` pour que le diagnostic soit lisible.
2. *Select → Select All by Trait → Faces by Sides* : réglez *Number of Vertices* = 4 et
   *Type* = *Greater Than* dans le panneau de l'opération (en bas à gauche) : les n-gons
   s'allument. Répétez avec 3 / *Equal To* pour les triangles.
3. Passez en sélection d’arêtes (`2`) et désélectionnez à nouveau. Lancez
   *Select → Select All by Trait → Non Manifold*. Les bords ouverts font partie
   des résultats. Une arête partagée par trois faces peut aussi être sélectionnée.
4. Notez pour chaque patient son défaut avant de réparer.

## Tutoriel 2 — GEO_Ngon : remplacer un n-gon par des quads
1. Edit Mode, mode face (`3`), cliquez la face. `X` → **Only Faces** : la face disparaît, le
   contour reste.
2. En mode arête (`2`), pressez `A`. Ce patient ne contient plus que les huit arêtes
   du contour. Vérifiez qu’elles sont sélectionnées ensemble.
3. Lancez *Face → Grid Fill*. Vérifiez que le contour reste à sa place et que la grille
   compte uniquement des faces à quatre côtés.

## Tutoriel 3 — GEO_Tris : regrouper les triangles
1. Edit Mode, `A`, **`Alt+J`** (*Face → Triangles to Quads*).
2. Observez : le corps redevient en quads, les deux « calottes » restent en triangles (pôles d'une
   sphère UV) — ce n'est pas une erreur.

## Tutoriel 4 — GEO_Doubles : fusionner les doublons
1. Edit Mode, `A`. Notez le nombre de sommets dans Statistics.
2. **`M` → By Distance**. Le message en bas indique le nombre de sommets supprimés ; Statistics
   chute. Le cube est de nouveau une surface fermée.

## Tutoriel 5 — GEO_Hole : boucher le trou
1. En mode Édition et sélection d’arêtes, faites `Alt+A`, puis
   *Select → Select All by Trait → Non Manifold*. Seul le bord du haut doit s’allumer.
2. **`Alt+F`** (*Fill*, triangles) ou **`F`** (une face unique, n-gon plan — acceptable sur un
   couvercle plat qui ne se déforme pas).
3. Désélectionnez tout et relancez *Non Manifold*. Si plus aucune arête ne s’allume,
   le cylindre est fermé. Inspectez aussi les normales depuis l’extérieur.

## Tutoriel 6 — GEO_Poles : compter les pôles
1. Vue fil de fer (`Z`), orbitez autour du cube.
2. Repérez les sommets d'où partent 3 arêtes (ou 5 et plus) : ce sont les pôles.
3. Ouvrez un **Text Editor** (changez le type d'une zone), choisissez le texte **DIAGNOSTIC**,
   remplacez `?` par votre nombre : `POLES = …`.

## Tutoriel 7 — Vérifier
Enregistrez `ch02_01_topology_<prenom>_v001.blend` puis :
```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch02_01_topology_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch02_01.py" -- --exercise clinic --render
```

## Variante de contrôle

Sur une copie de GEO_Ngon, notez le nombre de faces, puis rabattez un sommet du contour dans une direction différente de la normale. Une face non plane sera triangulée pour l’affichage. Comparez la diagonale apparente, puis refaites une division qui suit le relief. **Preuve** Une vue filaire et la même vue en Solid au même angle, avec le contour conservé.

[Manuel Blender 5.3 des sélections par propriété](https://docs.blender.org/manual/en/5.3/modeling/meshes/selecting/all_by_trait.html)
