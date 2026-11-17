# CH01.02 — Tutoriels pas à pas

## Tutoriel 1 — Les trois gestes (10 min, starter du musée)
1. Ouvrez `STARTER_FILES/ch01_02_museum_starter.blend`.
2. `MMB` glissé : orbitez autour du musée. Lisez le nom de la vue en haut à gauche.
3. `Shift+MMB` : décalez la vue vers la statue.
4. Molette : approchez-vous. `Ctrl+MMB` glissé : zoom progressif.
5. Cliquez la statue, `Numpad Decimal`. ✅ La statue occupe le centre de la vue.
6. `Home`. ✅ Tout le musée est visible.

## Tutoriel 2 — Vues et projections
1. `Numpad 1`, `Numpad 3`, `Numpad 7` : face, droite, dessus. Nom de la vue : *… Orthographic*
   (Auto Perspective).
2. Orbitez légèrement : retour en *User Perspective*.
3. `Numpad 5` plusieurs fois : comparez les lignes du sol.
4. `` ` `` (accent grave, en haut à gauche du clavier QWERTY ; sur AZERTY la touche ²
   peut correspondre — sinon, utilisez le gizmo) : menu circulaire des vues.

## Tutoriel 3 — Trouver la pièce et l'objet caché
1. Outliner → `ART` → `GEO_Coin` (clic) → souris dans la vue 3D → `Numpad Decimal`.
   ✅ Une pièce dorée de 2 cm remplit la vue.
2. `GEO_Hidden` : sélectionnez-le dans l'Outliner, `Numpad Divide` (vue locale) : seul l'objet
   reste visible. `Numpad Divide` à nouveau pour revenir.
3. Variante : vue de dessus `Numpad 7`, `Alt+B`, tracez un rectangle autour de la zone du mur :
   seule cette région est affichée ; orbitez pour voir la sphère rouge. `Alt+B` pour annuler.

## Tutoriel 4 — Walk navigation
1. Depuis une vue libre, ouvrez *View → Navigation → Walk Navigation* dans la vue 3D.
   Déplacez la souris pour regarder et utilisez `W`, `A`, `S`, `D` pour avancer ou vous
   déplacer de côté. Avec la gravité désactivée, `E` monte et `Q` descend. La molette
   règle la vitesse. Adaptez les touches en lisant la barre d’état de Blender.
2. Placez-vous devant la statue à hauteur de regard. Un clic gauche confirme le point de vue.
   Relancez la marche, déplacez-vous et pressez `Échap` pour retrouver la vue précédente.

## Tutoriel 5 — Régler les trois caméras (exercice 3 guidé)
1. Sélectionnez `CAM_Front` dans l’Outliner. Replacez le pointeur dans la vue 3D et
   pressez `Ctrl+Numpad 0` pour la définir comme caméra active.
2. Sélectionnez la statue, placez le pointeur dans la vue 3D, puis utilisez `Numpad 1`
   et `Numpad Decimal` pour cadrer la statue de face.
3. `Ctrl+Alt+Numpad 0` aligne la caméra active sur la vue. Vérifiez le cadre de caméra.
   Si vous voyez toujours la vue libre, utilisez `Numpad 0` pour passer en vue caméra.
4. Resélectionnez `CAM_Front` dans l’Outliner. Dans *Properties → Object Data* (icône verte),
   réglez *Lens → Type* sur **Orthographic** et *Orthographic Scale* autour de 3,2. Cherchez
   un cadre où la statue reste entièrement visible et occupe 40 à 80 % de la hauteur.
5. Recommencez avec `CAM_Right` (`Numpad 3`) et `CAM_Top` (`Numpad 7`).
6. Enregistrez `ch01_02_museum_<prenom>_v001.blend` et validez :
```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch01_02_museum_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch01_02.py" -- --exercise cameras
```
✅ `RÉSULTAT : VALIDÉ` (15 points).

[Manuel Blender 5.3 des caméras](https://docs.blender.org/manual/en/5.3/editors/3dview/navigate/camera_view.html)

## Contrôle de transfert

Cadrez GEO_Coin par l’Outliner et **View → Frame Selected** au-dessus de la vue 3D. Affichez **View → Viewpoint → Top**, puis réaffichez tout avec **View → Frame All**. Comparez à la navigation du [chapitre des périphériques](../../00_SETUP/CH00_04_INPUT_DEVICES/TUTORIAL.md). **Réussite** La pièce est visible en deux cadrages et aucune transformation d’objet ou caméra n’a changé.
