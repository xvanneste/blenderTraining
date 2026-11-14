# CH01.02 — Tutoriels pas à pas

## Tutoriel 1 — Les trois gestes (10 min, starter du musée)
1. Ouvrez `STARTER_FILES/ch01_02_museum_starter.blend`.
2. `MMB` glissé : orbitez autour du musée. Lisez le nom de la vue en haut à gauche.
3. `Shift+MMB` : décalez la vue vers la statue.
4. Molette : approchez-vous. `Ctrl+MMB` glissé : zoom progressif.
5. Cliquez la statue, `Num .`. ✅ La statue occupe le centre de la vue.
6. `Home`. ✅ Tout le musée est visible.

## Tutoriel 2 — Vues et projections
1. `Num 1`, `Num 3`, `Num 7` : face, droite, dessus. Nom de la vue : *… Orthographic*
   (Auto Perspective).
2. Orbitez légèrement : retour en *User Perspective*.
3. `Num 5` plusieurs fois : comparez les lignes du sol.
4. `` ` `` (accent grave, en haut à gauche du clavier QWERTY ; sur AZERTY la touche ²
   peut correspondre — sinon, utilisez le gizmo) : menu circulaire des vues.

## Tutoriel 3 — Trouver la pièce et l'objet caché
1. Outliner → `ART` → `GEO_Coin` (clic) → souris dans la vue 3D → `Num .`.
   ✅ Une pièce dorée de 2 cm remplit la vue.
2. `GEO_Hidden` : sélectionnez-le dans l'Outliner, `Num /` (vue locale) : seul l'objet
   reste visible. `Num /` à nouveau pour revenir.
3. Variante : vue de dessus `Num 7`, `Alt+B`, tracez un rectangle autour de la zone du mur :
   seule cette région est affichée ; orbitez pour voir la sphère rouge. `Alt+B` pour annuler.

## Tutoriel 4 — Walk navigation
1. `Shift+`` → déplacez la souris pour regarder, `W/S/A/D` pour marcher, `E/Q` pour
   monter/descendre, molette pour la vitesse. `LMB` pour valider.
2. Placez-vous devant la statue, à 1,60 m de hauteur.

## Tutoriel 5 — Régler les trois caméras (exercice 3 guidé)
1. Outliner → `CAM_Front` → `Ctrl+Num 0` (caméra active).
2. `Num 1` (vue de face), `Num .` sur la statue, ajustez le zoom.
3. `Ctrl+Alt+Num 0` : la caméra se place sur la vue. `Num 0` pour vérifier.
4. *Properties → Object Data* (icône caméra verte) → *Lens → Type* = **Orthographic** ;
   *Orthographic Scale* ≈ 3,2 (la statue doit remplir ~40–80 % de l'image).
5. Recommencez avec `CAM_Right` (`Num 3`) et `CAM_Top` (`Num 7`).
6. Enregistrez `ch01_02_museum_<prenom>_v001.blend` et validez :
```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch01_02_museum_<prenom>_v001.blend" `
  --python "SCRIPTS\validate_ch01_02.py" --python-exit-code 1 -- --exercise cameras
```
✅ `RÉSULTAT : VALIDÉ` (15 points).
