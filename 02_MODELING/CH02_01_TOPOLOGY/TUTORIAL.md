# CH02.01 — Tutoriels pas à pas

Ouvrez `STARTER_FILES/ch02_01_topology_starter.blend`. Cinq « patients » sont alignés de gauche à
droite. Activez **Viewport Overlays → Statistics** et passez en vue fil de fer quand c'est utile
(`Z` → *Wireframe*).

## Tutoriel 1 — Diagnostiquer avant d'opérer
1. Sélectionnez un objet, `Tab` (Edit Mode), `A` (tout sélectionner).
2. *Select → Select All by Trait → Faces by Sides* : réglez *Number of Vertices* = 4 et
   *Type* = *Greater Than* dans le panneau de l'opération (en bas à gauche) : les n-gons
   s'allument. Répétez avec 3 / *Equal To* pour les triangles.
3. *Select → Select All by Trait → Non Manifold* : les bords ouverts s'allument.
4. Notez pour chaque patient son défaut avant de réparer.

## Tutoriel 2 — GEO_Ngon : remplacer un n-gon par des quads
1. Edit Mode, mode face (`3`), cliquez la face. `X` → **Only Faces** : la face disparaît, le
   contour reste.
2. Mode arête (`2`), `Alt+clic` sur le contour (toute la boucle).
3. *Face → Grid Fill* : le contour se remplit de quads. Vérifiez qu'aucune face n'a plus de 4 côtés.

## Tutoriel 3 — GEO_Tris : regrouper les triangles
1. Edit Mode, `A`, **`Alt+J`** (*Face → Triangles to Quads*).
2. Observez : le corps redevient en quads, les deux « calottes » restent en triangles (pôles d'une
   sphère UV) — ce n'est pas une erreur.

## Tutoriel 4 — GEO_Doubles : fusionner les doublons
1. Edit Mode, `A`. Notez le nombre de sommets dans Statistics.
2. **`M` → By Distance**. Le message en bas indique le nombre de sommets supprimés ; Statistics
   chute. Le cube est de nouveau une surface fermée.

## Tutoriel 5 — GEO_Hole : boucher le trou
1. Edit Mode, *Select → Select All by Trait → Non Manifold* : le bord du haut s'allume.
2. **`Alt+F`** (*Fill*, triangles) ou **`F`** (une face unique, n-gon plan — acceptable sur un
   couvercle plat qui ne se déforme pas).

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
  --python "SCRIPTS\validate_ch02_01.py" --python-exit-code 1 -- --exercise clinic --render
```
