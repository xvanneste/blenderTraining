# CH02.07 — Tutoriels pas à pas : la platine percée

Ouvrez `STARTER_FILES/ch02_07_plate_starter.blend`. `GEO_Plate` : 60 × 40 × 3 cm, posée au sol.

## Tutoriel 1 — La collection de cutters
1. Outliner : clic droit sur *Scene Collection* → *New Collection* → `CUTTERS`. Cliquez-la (active).
2. `Shift+A` → *Mesh → Cylinder* ; panneau : *Vertices* 32, *Radius* 0.025, *Depth* 0.1,
   *Location* (0.24, −0.14, 0.015). `F2` → `CUT_Hole_FR`.
3. `Shift+D` puis déplacements chiffrés pour les 3 autres coins : (−0.24, −0.14), (0.24, 0.14),
   (−0.24, 0.14). Nommez-les.
4. `Shift+A` → *Cube* ; *Size* 1 ; *Location* (0, 0, 0.015) ; `S` puis échelle (0.2, 0.04, 0.1)
   via `N` → *Dimensions* 0,2 × 0,04 × 0,1 ; `Ctrl+A` → *Scale*. Nom : `CUT_Slot`.

## Tutoriel 2 — Rendre les cutters discrets
1. Sélectionnez les 5 cutters. Object Properties → *Viewport Display* → **Display As : Wire**
   (`Alt+clic` sur la valeur pour l'appliquer à toute la sélection, ou *Copy to Selected*).
2. *Visibility* → *Show In* : décochez **Renders** (ou l'icône caméra dans l'Outliner, filtre activé).

## Tutoriel 3 — Le Boolean en mode Collection
1. Sélectionnez `GEO_Plate`. *Add Modifier → Generate → Boolean*.
2. **Difference**, **Operand Type : Collection**, **Collection : CUTTERS**, **Solver : Exact**.
   Les 5 trous apparaissent.
3. Déplacez `CUT_Slot` (`G` `X`) : la lumière suit. `Ctrl+Z`.

## Tutoriel 4 — Le Bevel après le Boolean
1. *Add Modifier → Generate → Bevel* : *Limit Method* Angle, *Width* 0.0015, *Segments* 2,
   *Shading → Harden Normals*. `Object → Shade Smooth`.
2. Le Bevel est **sous** le Boolean dans la pile : les bords des trous sont biseautés. Glissez-le
   au-dessus (poignée ⋮⋮) pour voir la différence, puis remettez-le dessous.

## Tutoriel 5 — Vérifier
```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch02_07_plate_<prenom>_v001.blend" `
  --python "SCRIPTS\validate_ch02_07.py" --python-exit-code 1 -- --exercise plate --render
```
Le correcteur compte les trous **traversants** par la formule d'Euler (V − E + F = 2 − 2 × trous).
