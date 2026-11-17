# CH18.19 — Tutoriels pas à pas

Ouvrez `STARTER_FILES/ch18_19_hybrid_starter.blend` ; Num 0 (vue caméra `CAM_Shot`).

## Tutoriel 1 — Les contours Line Art
1. Outliner : cliquez la collection `SET` (collection active).
2. Object Mode : *Add > Grease Pencil > Collection Line Art*. Un objet GP apparaît ; ses traits suivent
   les arêtes du décor vues de la caméra.
3. Modifier Properties : vérifiez *Source Type* Collection = SET ; *Radius* ≈ 0,02 m.
4. Rendu (F12) : les contours apparaissent sur le décor.

## Tutoriel 2 — Placer le personnage dans la pièce
1. Shift+clic droit au sol, derrière la caisse avant, pour poser le curseur 3D (≈ x 0,9, y 1,0, z 0) ;
   vérifiez dans Sidebar (N) > View > 3D Cursor (mettez Z à 0).
2. Sélectionnez `GP_Character`, mode **Draw**, calque `USER_Char`.
3. En-tête : *Stroke Placement* : **3D Cursor** ; *Drawing Plane* : **Front (X-Z)**.
4. Dessinez le personnage debout, pieds sur la ligne du sol, ~1,75 m (comparez avec la caisse de 0,9 m).
5. Orbitez la vue (molette) : le personnage est un plan dans la pièce, derrière la caisse.

## Tutoriel 3 — Dessiner sur le mur
1. Sélectionnez `GP_Decal`, mode Draw, calque `USER_Decal`.
2. *Stroke Placement* : **Surface** (Offset faible, ex. 0,005).
3. Dessinez une affiche, une fenêtre peinte… sur le mur du fond : les traits épousent le mur.

## Tutoriel 4 — L'occlusion au rendu
1. F12 : si le personnage passe DEVANT la caisse au rendu, c'est normal tant que la passe Z est coupée.
2. *View Layer Properties > Passes > Data* : cochez **Z**. F12 : la caisse cache maintenant le bas du
   personnage, comme dans la vue 3D.

## Tutoriel 5 — Vérifier
```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch18_19_hybrid_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch18_19.py" -- --exercise hybrid --render
```
Référence : `COMPLETED_EXAMPLES/ch18_19_hybrid_reference.png`.

## Variante de contrôle

Comparez une vue caméra, une vue de côté et un export de test. Recherchez un croisement entre le trait et un objet 3D. **Preuve** Vous résolvez un défaut de visibilité par placement ou réglage en gardant le cadre voulu.
