# CH02.03 — Tutoriels pas à pas : l'atelier de découpe

Ouvrez `STARTER_FILES/ch02_03_cutting_starter.blend`. Six postes, de gauche à droite. Statistics
activées. Chaque tutoriel se fait en Edit Mode (`Tab`) sur l'objet indiqué, sauf le ressort.

## Tutoriel 1 — GEO_Bar : Bisect
1. `A`. *Mesh → Bisect* ; tracez à la souris une ligne horizontale à peu près aux 2/3 de la hauteur.
2. Panneau de l'opération : *Plane Point* **Z = 0.8** (X, Y = 0), *Plane Normal* **(0, 0, 1)**,
   cochez **Fill** et **Clear Outer**. Le haut disparaît, la coupe est bouchée à 80 cm.

## Tutoriel 2 — GEO_Messy : Limited Dissolve
1. Vue fil de fer : chaque face est découpée en 5 × 5 sans raison.
2. `A`, `X` → **Limited Dissolve** (*Max Angle* 5°). Statistics : 6 faces. La forme n'a pas bougé.
3. Comparez : `Ctrl+Z`, puis `X` → *Faces* : l'objet est troué. *Dissolve* ≠ *Delete*.

## Tutoriel 3 — GEO_Profile : Spin
1. `Shift+C` (curseur 3D au centre du monde, la vue se recadre). Sélectionnez `GEO_Profile`, `Tab`, `A`.
2. `Alt+E` → **Spin**. Panneau : *Steps* 24, *Angle* 360°, *Axis* (0, 0, 1), *Auto Merge* coché.
3. **`A`** puis **`M` → By Distance** : environ 23 sommets supprimés (les points du fond, sur l'axe).
4. `Tab`, clic droit → *Shade Smooth*.

## Tutoriel 4 — GEO_Pyramid : Merge
1. Mode sommet (`1`), vue de face, sélectionnez les 4 sommets du haut (boîte `B` en X-ray `Alt+Z`).
2. `M` → **At Center**. Une pyramide à 5 sommets.

## Tutoriel 5 — GEO_Spring : modificateur Screw
1. Object Mode, sélectionnez `GEO_Spring`. Properties → Modifiers → *Add Modifier → Generate →
   Screw*.
2. *Screw* 0.08, *Iterations* 5, *Steps* 24 (viewport et rendu). Un ressort de 5 spires.
3. Augmentez *Screw* : le ressort s'étire ; mettez 0 : un anneau (tore).

## Tutoriel 6 — GEO_Tile : Knife
1. Vue de dessus (`Num 7`), `Tab`, `K`.
2. Clic gauche sur un coin (le point s'aimante au sommet), clic gauche sur le coin opposé, `Entrée`.
3. Essayez de nouveau avec `Shift` maintenu : la coupe s'aimante au milieu des arêtes.

## Tutoriel 7 — Vérifier
Enregistrez `ch02_03_cutting_<prenom>_v001.blend` puis :
```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch02_03_cutting_<prenom>_v001.blend" `
  --python "SCRIPTS\validate_ch02_03.py" --python-exit-code 1 -- --exercise atelier --render
```
