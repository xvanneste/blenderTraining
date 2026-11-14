# CH01.03 — Tutoriels pas à pas

## Tutoriel 1 — Sélections (starter du puzzle, collection PEBBLES)
1. Ouvrez `STARTER_FILES/ch01_03_puzzle_starter.blend`, vue de dessus `Num 7`.
2. `LMB` sur un caillou ; `Shift+LMB` sur deux autres. Observez : le dernier est plus clair (actif).
3. `A` (tout), `Alt+A` (rien). `Ctrl+I` après avoir sélectionné 3 cailloux : tout sauf eux.
4. `B` + rectangle autour d'un groupe de cailloux.
5. `C` : peignez la sélection, molette pour le rayon, `RMB` pour sortir.
6. `Ctrl+RMB` glissé : lasso autour de quelques cailloux.
7. *Select → Select Pattern…* : `GEO_Pebble_1*` → tous les cailloux 10 à 19.
   ✅ La barre d'état indique le nombre d'objets sélectionnés.

## Tutoriel 2 — Transformations au clavier (pièce A)
1. Cliquez `GEO_Piece_A` (cube rouge).
2. `G` : bougez la souris, `Échap` pour annuler.
3. `Alt+G` : la pièce revient à l'origine du monde (0, 0, 0).
4. `G X 2 Entrée`, `G Y 2 Entrée`, `G Z 0.5 Entrée`.
   ✅ Sidebar `N` → *Item* → *Location* : (2, 2, 0,5). Le cube est dans sa silhouette.

## Tutoriel 3 — Rotation et échelle (pièces B, C, D)
1. Pièce B (cône) : `Alt+G`, puis `G X 4 Entrée`, `G Y 2`, `G Z 0.5`, puis `R X 90 Entrée`.
2. Pièce C (cylindre) : position (2, 4, 1) puis `S Z 2 Entrée`.
3. Pièce D (Suzanne) : position (4, 4, 0.3), `R Z 45 Entrée`, `S 0.5 Entrée`.
   ✅ Les 4 pièces remplissent leurs silhouettes.
4. Astuce : tapez directement les valeurs dans la sidebar (champ *Location X* = `4`…).

## Tutoriel 4 — Axes locaux et exclusion d'axe
1. Pièce B (couchée) : `G Z Z` → déplacement le long de l'axe **local** Z du cône (son axe
   de pointe), indiqué dans l'en-tête. `Échap`.
2. `G Shift+Z` : déplacement dans le plan X-Y uniquement (Z exclu). `Échap`.

## Tutoriel 5 — Vérifier
Enregistrez `ch01_03_puzzle_<prenom>_v001.blend` puis :
```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch01_03_puzzle_<prenom>_v001.blend" `
  --python "SCRIPTS\validate_ch01_03.py" --python-exit-code 1 -- --exercise puzzle
```
✅ 13/13.
