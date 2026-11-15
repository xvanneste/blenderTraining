# CH18.06 — Tutoriels pas à pas

Ouvrez `STARTER_FILES/ch18_06_gp_scene_starter.blend` : un petit décor 3D (sol, maison, arbre),
une caméra `CAM_Shot`, un soleil. Aucun objet Grease Pencil.

## Tutoriel 1 — Découvrir les modèles 2D (5 min, sans enregistrer)
1. **File → New → 2D Animation** : observez les onglets de workspace en haut (« 2D Animation »,
   « 2D Full Canvas »), l'objet *Stroke* et la caméra. Dessinez quelques traits.
2. **File → New → Storyboarding** : trois caméras, trois objets GP, workspace « Video Editing ».
3. Revenez à votre fichier : **File → Open Recent** → le starter (sans enregistrer les essais).

## Tutoriel 2 — Créer et ranger le premier objet
1. Outliner : clic droit sur *Scene Collection* → **New Collection** ; double-clic → `DRAWINGS`.
   Cliquez sur DRAWINGS pour la rendre active (les nouveaux objets y seront créés).
2. Curseur 3D au centre (`Shift+C` recentre aussi la vue), puis **Add → Grease Pencil → Blank**.
3. `F2` → `GP_Character`.
4. Déplacez-le devant la maison : `G` `Y` `1.5` `Entrée` (la maison est à Y = 4, la caméra à Y = −9).

## Tutoriel 3 — Calques et groupe
1. **Properties → Object Data** (icône du trait GP) → panneau **Layers**.
2. Bouton **+** trois fois ; double-clic pour renommer : `LINE`, `COLOR`, `SKETCH`.
3. Icône **dossier** (infobulle *Add New Layer Group*) → renommez le groupe `CHAR`.
4. Glissez-déposez `LINE` puis `COLOR` sur le groupe `CHAR`.
5. Cadenas sur `SKETCH` (après y avoir esquissé, voir tutoriel 4) ; baissez son **Opacity** à 0,3.

## Tutoriel 4 — Dessiner dans la scène
1. `Num 0` (vue caméra). `Ctrl+Tab` → **Draw Mode**.
2. En-tête : vérifiez **Stroke Placement : Origin** et **Drawing Plane : View**.
3. Calque `SKETCH` : grande ellipse de gestuelle. Puis calque `LINE` : le personnage (mannequin
   CH18.03), au moins 6 traits. Calque `COLOR` : quelques hachures ou aplats.
4. Orbitez (molette) : le dessin est un plan dans l'espace, devant la maison.

## Tutoriel 5 — Le fond derrière la maison
1. `Ctrl+Tab` → Object Mode. **Add → Grease Pencil → Blank**, `F2` → `GP_Background`.
2. `G` `Y` `9` `Entrée` (derrière la maison). Vérifiez qu'il est dans DRAWINGS (sinon `M`).
3. `Num 0`, Draw Mode : dessinez des collines et des nuages larges (ils sont loin : dessinez grand).
4. Orbitez pour vérifier : personnage devant, maison, collines derrière.
5. `F12` : au rendu, les collines passent **devant** la maison ! Fermez la fenêtre de rendu.
6. **Properties → View Layer** → panneau **Passes → Data** → cochez **Z**. `F12` à nouveau : la
   maison cache désormais les collines (voir THEORY §5).

## Tutoriel 6 — Vérifier
Enregistrez `ch18_06_gp_scene_<prenom>_v001.blend`, puis :
```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch18_06_gp_scene_<prenom>_v001.blend" `
  --python "SCRIPTS\validate_ch18_06.py" --python-exit-code 1 -- --exercise organize --render
```
