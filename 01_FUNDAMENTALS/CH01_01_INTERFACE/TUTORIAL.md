# CH01.01 — Tutoriels pas à pas

## Tutoriel 1 — Visite guidée (10 min)
1. Ouvrez `STARTER_FILES/ch01_01_interface_starter.blend`.
2. **Topbar** : survolez *File*, *Edit*, *Render*, *Window*, *Help* sans cliquer.
3. **Onglets de workspaces** : cliquez *Modeling*, *Shading*, *Animation*, puis revenez à
   *Layout*. ✅ La disposition change, la scène reste la même.
4. **Outliner** (en haut à droite) : dépliez `HUNT` (triangle) : `GEO_Clue_A`, `GEO_Clue_B`.
   Cliquez `GEO_Clue_A` : il est sélectionné dans la vue 3D aussi.
5. **Properties** (en dessous) : la colonne d'icônes à gauche = onglets (Tool, Render,
   Output, View Layer, Scene, World, Object, Modifiers, …). Cliquez l'onglet **Object**
   (carré orange) : nom, transformations de l'objet actif.
6. **Status bar** (tout en bas) : lisez les indications de la souris.

## Tutoriel 2 — Régions de la vue 3D
1. Souris au-dessus de la vue 3D. `T` : la barre d'outils disparaît / réapparaît.
2. `N` : la sidebar apparaît ; onglet *Item* : *Location*, *Rotation*, *Scale*,
   *Dimensions* de l'objet actif.
3. *Add → Mesh → Cube* (`Shift+A`) : un panneau **Add Cube** apparaît en bas à gauche.
   Dépliez-le, mettez *Size* = 0.5. Fermez-le, `F9` le rouvre. ✅ Vous pouvez modifier une
   action **après** l'avoir faite.
4. `Ctrl+Z` pour annuler l'ajout.

## Tutoriel 3 — Zones : diviser, fusionner, changer d'éditeur, maximiser
1. Souris sur la **Timeline** (bas). `Ctrl+Space` : elle occupe toute la fenêtre.
   `Ctrl+Space` à nouveau : retour.
2. Bouton **Editor Type** (icône tout à gauche de l'en-tête de la Timeline) → **Text
   Editor**. Dans l'en-tête, menu déroulant des textes → `README_EXERCICE` : les consignes
   du chapitre s'affichent. ✅ Gardez-les sous les yeux.
3. **Diviser** : `RMB` sur la frontière entre la vue 3D et l'éditeur de texte → *Vertical
   Split* → déplacez la ligne qui apparaît, cliquez. ✅ Deux zones côte à côte.
4. **Fusionner** : `RMB` sur la nouvelle frontière → *Join Areas* → cliquez la zone à
   conserver.
5. Remettez la Timeline (Editor Type → *Timeline*).

## Tutoriel 4 — Trouver une commande avec F3
1. Souris dans la vue 3D, `F3`.
2. Tapez `cube` : *Add → Mesh → Cube* apparaît, avec le chemin du menu. `Entrée`.
3. `F3` → `shade smooth` → *Object → Shade Smooth*. ✅ Le cube est lissé.
4. `Ctrl+Z` deux fois.

## Tutoriel 5 — Créer votre workspace (exercice 3 guidé)
1. `RMB` sur l'onglet *Layout* → **Duplicate** : un onglet *Layout.001* apparaît, actif.
2. Double-clic sur l'onglet → renommez **BCMA_Study** → `Entrée`.
3. Transformez la Timeline en **Text Editor** (tutoriel 3, étape 2).
4. Vérifiez que *Outliner*, *Properties* et *3D Viewport* sont toujours là.
5. `Shift+Ctrl+S` → `ch01_01_interface_<prenom>_v001.blend`.
6. Validez :
```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch01_01_interface_<prenom>_v001.blend" `
  --python "SCRIPTS\validate_ch01_01.py" --python-exit-code 1 -- --exercise workspace
```
✅ `RÉSULTAT : VALIDÉ`.
> Les workspaces sont enregistrés **dans le `.blend`** (le *Load UI* de CH00.02 les
> recharge à l'ouverture). Pour les avoir dans tous vos nouveaux fichiers :
> *File → Defaults → Save Startup File*.
