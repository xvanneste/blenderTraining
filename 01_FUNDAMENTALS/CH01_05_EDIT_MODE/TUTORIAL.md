# CH01.05 — Tutoriels pas à pas

## Tutoriel 1 — Entrer, sélectionner, sortir
1. Ouvrez `STARTER_FILES/ch01_05_house_starter.blend`, cliquez `GEO_Practice` (la grille verte).
2. `Tab` : Edit Mode (les sommets apparaissent).
3. `1`, `2`, `3` : modes sommets / arêtes / faces. Cliquez chaque fois un élément.
4. Mode arêtes, `Alt+LMB` sur une arête : une **boucle** entière. `Ctrl+Alt+LMB` : un **anneau**.
5. `A`, puis `Alt+A`. `Tab` pour sortir.

## Tutoriel 2 — La maison (exercice 3 guidé)
1. Cliquez `GEO_House`, `Tab`.
2. Mode faces (`3`), vue de face `Num 1`, puis orbitez un peu pour voir le dessus ;
   cliquez la **face du haut**.
3. `E` puis tapez `1` puis `Entrée` : une nouvelle face 1 m plus haut (extrusion le long
   de la normale).
4. `S X 0 Entrée` : la face s'écrase en arête.
   ✅ Un toit à deux pans, faîtage parallèle à Y, à 3 m de haut.
5. `Tab` (Object Mode).

## Tutoriel 3 — La colline (édition proportionnelle)
1. `GEO_Practice`, `Tab`, mode sommets, `Alt+A`, cliquez le sommet **central** de la grille.
2. `O` (l'icône d'édition proportionnelle s'allume dans l'en-tête).
3. `G Z` puis bougez la souris vers le haut ; **molette** pour agrandir le cercle
   d'influence (≈ 1,5 m) ; tapez `1`, `Entrée`.
   ✅ Une colline douce.
4. `O` pour désactiver (sinon toutes vos éditions suivantes seront proportionnelles !). `Tab`.

## Tutoriel 4 — X-Ray et sélection à travers
1. `GEO_House`, `Tab`, mode sommets, vue de face `Num 1`.
2. `B` + rectangle autour des sommets du bas : seuls les sommets **visibles** sont pris.
3. `Alt+Z` (X-Ray), recommencez : ceux de derrière aussi. `Alt+Z` pour revenir.

## Tutoriel 5 — Vérifier
Enregistrez (en Object Mode !) `ch01_05_house_<prenom>_v001.blend` puis :
```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch01_05_house_<prenom>_v001.blend" `
  --python "SCRIPTS\validate_ch01_05.py" --python-exit-code 1 -- --exercise house
```
