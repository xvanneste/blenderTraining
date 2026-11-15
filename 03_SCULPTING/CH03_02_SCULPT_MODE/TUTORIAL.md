# CH03.02 — Tutoriels pas à pas

Ouvrez `STARTER_FILES/ch03_02_face_starter.blend` et enregistrez-le sous
`ch03_02_face_<prenom>_v001.blend`. Sélectionnez `SCULPT_Head` ; **Ctrl+Tab** > *Sculpt Mode*.
Le visage regarde vers −Y : vue de face = **Num 1**.

## Tutoriel 1 — Prise en main
1. Brosse **Draw** (V). F : rayon ≈ un quart de la sphère ; Shift+F : force 0,5.
2. Cliquez-glissez sur une zone d'essai… puis Ctrl+Z : on teste, on annule.
3. Ctrl maintenu : la brosse creuse. Shift maintenu : elle lisse.

## Tutoriel 2 — Symétrie et masque
1. En-tête : activez **Mirror X**.
2. Brosse **Mask** (M) : peignez tout l'arrière du crâne (tournez la vue, Num 3 puis Ctrl+Num 1),
   ou **B** et tracez un rectangle en vue de dos. La zone devient sombre.
3. Ne l'effacez pas à la fin : le correcteur vérifie que l'arrière est masqué et intact.

## Tutoriel 3 — Le visage
1. **Nez** : Clay Strips (C) puis Draw, au centre, sous le milieu de la face ; Inflate (I) pour le bout.
2. **Orbites** : Ctrl + Draw, de part et d'autre du haut du nez (Mirror X fait le deuxième œil).
3. **Arcades** : Clay Strips au-dessus des orbites.
4. **Pommettes** : Inflate léger sous les orbites.
5. **Bouche** : Crease Polish (Shift+C) pour un sillon horizontal ; **menton** : Draw léger dessous.
6. Lissage général (Shift) ; tournez autour pour vérifier la silhouette de profil.

## Tutoriel 4 — Face Sets
Menu *Face Sets > Initialize Face Sets > By Normals* (ou brosse **Face Set Paint**) : au moins deux
zones colorées. Essayez **Shift+H** sur le visage (isolé), puis **H** sur un côté (caché), puis **Alt+H** (tout réafficher).

## Tutoriel 5 — Vérifier
```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch03_02_face_<prenom>_v001.blend" `
  --python "SCRIPTS\validate_ch03_02.py" --python-exit-code 1 -- --exercise face --render
```
Référence : `COMPLETED_EXAMPLES/ch03_02_face_reference.png`.
