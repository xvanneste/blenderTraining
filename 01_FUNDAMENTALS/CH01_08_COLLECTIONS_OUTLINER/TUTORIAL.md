# CH01.08 — Tutoriels pas à pas

## Tutoriel 1 — Afficher tous les interrupteurs de l'Outliner
1. Ouvrez `STARTER_FILES/ch01_08_living_room_starter.blend`.
2. Outliner → icône **entonnoir** (Filter) → *Restriction Toggles* : activez la flèche, l'écran
   et l'appareil photo.
   ✅ Chaque ligne affiche maintenant ses icônes de visibilité.

## Tutoriel 2 — Créer les collections et ranger
1. Sélectionnez `GEO_Floor`, `GEO_Wall_Back`, `GEO_Wall_Left` (`Ctrl`+clic dans l'Outliner).
2. Souris dans la vue 3D, `M` → **+ New Collection** → nom `SET` → *OK*.
3. Sélectionnez les 7 objets de mobilier (`GEO_Sofa` … `GEO_Shelf`), `M` → *+ New Collection* → `PROPS`.
4. Idem : `LGT_Key`, `LGT_Window` → `LIGHTS` ; `CAM_Main`, `EMP_CamTarget` → `CAMERAS` ;
   `EMP_Guide_1..3`, `GEO_Debug_Box` → `HELPERS`.
   (Astuce : *Select → Select All by Type → Light* sélectionne toutes les lumières.)
   ✅ La Scene Collection ne contient plus que 5 collections.

## Tutoriel 3 — HELPERS hors du rendu
1. Dans l'Outliner, cliquez l'icône **appareil photo** de `HELPERS` (elle se grise).
2. `F12` : les repères et la boîte de debug n'apparaissent pas. Ils restent visibles dans la vue.

## Tutoriel 4 — Parenter l'abat-jour
1. Cliquez `GEO_LampShade`, puis `Ctrl`+clic (ou `Shift`+clic dans la vue) sur `GEO_LampBase` :
   le pied est **actif** (dernier sélectionné).
2. `Ctrl+P` → **Object**.
   ✅ Dans l'Outliner, l'abat-jour apparaît sous le pied ; une ligne pointillée les relie dans la vue.
3. Test : sélectionnez le pied seul, `G X 1` : l'abat-jour suit. `Échap`.

## Tutoriel 5 — Vérifier
Enregistrez `ch01_08_living_room_<prenom>_v001.blend` puis :
```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch01_08_living_room_<prenom>_v001.blend" `
  --python "SCRIPTS\validate_ch01_08.py" --python-exit-code 1 -- --exercise organize --render
```
