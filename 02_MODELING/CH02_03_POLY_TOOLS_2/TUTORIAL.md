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
3. Pour comparer, annulez *Limited Dissolve* et essayez `X → Faces`. Observez la géométrie
   supprimée, annulez, puis refaites *Limited Dissolve* avant de quitter l’objet.

## Tutoriel 3 — GEO_Profile : Spin
1. `Shift+C` (curseur 3D au centre du monde, la vue se recadre). Sélectionnez `GEO_Profile`, `Tab`, `A`.
2. Passez en vue de dessus (`Numpad 7`). Lancez **Spin** avec `F3`. Dans le panneau de
   l’opération, réglez *Steps* à 24, *Angle* à 360° et *Axis* à (0, 0, 1). Activez *Auto Merge*.
3. **`A`** puis **`M` → By Distance** : environ 23 sommets supprimés (les points du fond, sur l'axe).
4. `Tab`, clic droit → *Shade Smooth*.

## Tutoriel 4 — GEO_Pyramid : Merge
1. Mode sommet (`1`), vue de face, sélectionnez les 4 sommets du haut (boîte `B` en X-ray `Alt+Z`).
2. `M` → **At Center**. Une pyramide à 5 sommets.

## Tutoriel 5 — GEO_Spring : modificateur Screw
1. Object Mode, sélectionnez `GEO_Spring`. Properties → Modifiers → *Add Modifier → Generate →
   Screw*.
2. *Screw* 0.08, *Iterations* 5, *Steps* 24 (viewport et rendu). Un ressort de 5 spires.
3. Augmentez *Screw* pour étirer le ressort. Pour voir une seule révolution sans avance,
   essayez *Screw* à 0 et *Iterations* à 1. Rétablissez 0,08 et 5 pour l’exercice.

## Tutoriel 6 — GEO_Tile : Knife
1. Vue de dessus (`Numpad 7`), `Tab`, `K`.
2. Clic gauche sur un coin (le point s'aimante au sommet), clic gauche sur le coin opposé, `Entrée`.
3. Sur une copie, essayez de nouveau en maintenant `Shift` près d’une arête pour viser
   son milieu. Gardez la diagonale sur la scène à valider.

## Tutoriel 7 — Vérifier
Enregistrez `ch02_03_cutting_<prenom>_v001.blend` puis :
```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch02_03_cutting_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch02_03.py" -- --exercise atelier --render
```

## Variante de contrôle

Dupliquez GEO_Messy. Testez Limited Dissolve à deux angles puis comparez le contour en vue orthographique et le nombre de faces. Gardez la plus forte réduction qui préserve le contour. Pour Spin, vérifiez l’emplacement du curseur et l’axe sur une copie avant de fermer le tour. **Preuve** Capture filaire des deux réglages et décision argumentée.

[Manuel Blender 5.3 de Spin](https://docs.blender.org/manual/en/5.3/modeling/meshes/tools/spin.html)
