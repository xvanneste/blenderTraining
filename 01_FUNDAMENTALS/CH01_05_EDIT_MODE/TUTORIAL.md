# CH01.05 — Tutoriels pas à pas

## Tutoriel 1 — Entrer, sélectionner, sortir
1. Ouvrez `STARTER_FILES/ch01_05_house_starter.blend`, cliquez `GEO_Practice` (la grille verte).
2. `Tab` : Edit Mode (les sommets apparaissent).
3. `1`, `2`, `3` : modes sommets / arêtes / faces. Cliquez chaque fois un élément.
4. Mode arêtes. Si le raccourci Alt+clic est utilisé par l’émulation de la souris, désactivez-la pour cet essai. Sinon, `Alt+LMB` sur une arête : une **boucle** entière. `Ctrl+Alt+LMB` : un **anneau**.
5. `A`, puis `Alt+A`. `Tab` pour sortir.

## Tutoriel 2 — La maison (exercice 3 guidé)
1. Cliquez `GEO_House`, `Tab`.
2. Mode faces (`3`), vue de face `Numpad 1`, puis orbitez un peu pour voir le dessus ;
   cliquez la **face du haut**.
3. `E` puis tapez `1` puis `Entrée` : une nouvelle face 1 m plus haut (extrusion le long
   de la normale).
4. `S X 0 Entrée` : la face s'écrase en arête.
   Le faîtage est parallèle à Y et à 3 m de hauteur. Les sommets coïncidents demandent une fusion.
5. Passez en mode sommets avec 1 ou le bouton de l’en-tête. Sur la sélection du faîtage, faites **M → By Distance**. La face devenue plate disparaît lorsque ses sommets fusionnent.
6. Sélectionnez toute la maison avec **A**, puis **Shift+N** pour recalculer les normales vers l’extérieur. Comparez les deux pans en Solid et Face Orientation.
7. Revenez en mode Objet avec **Tab** et enregistrez votre copie.


## Tutoriel 3 — La colline (édition proportionnelle)
1. `GEO_Practice`, `Tab`, mode sommets, `Alt+A`, cliquez le sommet **central** de la grille.
2. `O` (l'icône d'édition proportionnelle s'allume dans l'en-tête).
3. `G Z` puis bougez la souris vers le haut ; **molette** pour agrandir le cercle
   d'influence (≈ 1,5 m) ; tapez `1`, `Entrée`.
   ✅ Une colline douce.
4. `O` pour désactiver (sinon toutes vos éditions suivantes seront proportionnelles !). `Tab`.

## Tutoriel 4 — X-Ray et sélection à travers
1. `GEO_House`, `Tab`, mode sommets, vue de face `Numpad 1`.
2. `B` + rectangle autour des sommets du bas : seuls les sommets **visibles** sont pris.
3. `Alt+Z` (X-Ray), recommencez : ceux de derrière aussi. `Alt+Z` pour revenir.

## Tutoriel 5 — Vérifier
Enregistrez (en Object Mode !) `ch01_05_house_<prenom>_v001.blend` puis :
```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch01_05_house_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch01_05.py" -- --exercise house
```

## Contrôle de transfert

Sur une copie, refaites l’opération et arrêtez-vous avant la fusion. En filaire, comparez cette variante avec la maison terminée. Après la fusion, vérifiez à nouveau Face Orientation dans Overlays et comparez la hauteur. **Réussite** La hauteur reste de 3 m et les deux pans restent raccordés. [Aide aux modes de sélection sans pavé numérique](../../00_SETUP/CH00_04_INPUT_DEVICES/TUTORIAL.md).
