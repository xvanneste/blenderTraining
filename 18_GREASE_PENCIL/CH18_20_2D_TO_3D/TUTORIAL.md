# CH18.20 — Tutoriels pas à pas

## Tutoriel 1 — Préparer un board dans une caméra (à refaire sur vos plans)
1. *Add > Camera*, cadrez le plan ; Timeline : marqueur, *Marker > Bind Camera to Markers* (Ctrl+B).
2. *Add > Grease Pencil > Blank* ; renommez `BOARD_SH0010`.
3. Object Properties > *Relations* > *Parent* : la caméra. Puis Alt+G et Alt+R (effacer position et
   rotation) : le GP est au centre de la caméra ; *Location* Z local = −0,5 (devant l'objectif).
4. Vue caméra (Num 0), mode Draw, *Drawing Plane* : *View* ; dessinez le plan (personnages, flèches).

## Tutoriel 2 — Lire les boards du starter
1. Ouvrez `STARTER_FILES/ch18_20_layout_starter.blend`, Num 0.
2. Timeline : flèches haut/bas pour sauter de marqueur en marqueur (images 1, 73, 121) : la caméra
   active change, chaque board montre où doit être le personnage.
3. Masquez (H) les boards des autres plans pour ne voir que celui du plan courant.

## Tutoriel 3 — Le blocking
1. Image 1 (SH0010), vue caméra : sélectionnez `CHR_A`, G pour déplacer (G puis Z bloque l'axe
   vertical — restez au sol : Z = 0), R Z pour l'orienter ; superposez-le à la silhouette rouge.
2. K > *Location & Rotation*.
3. Image 73 (SH0020) puis 121 (SH0030) : même chose.
4. Dope Sheet : sélectionnez toutes les clés de CHR_A, T > *Constant*.
5. Lecture : le personnage change de place exactement aux coupes.

## Tutoriel 4 — Nettoyer pour le rendu
1. Outliner : filtre (entonnoir) > cochez l'icône appareil photo ; désactivez le rendu des `BOARD_*`.
2. F12 sur chaque plan : seuls le décor et le mannequin apparaissent.

## Tutoriel 5 — Vérifier
```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch18_20_layout_<prenom>_v001.blend" `
  --python "SCRIPTS\validate_ch18_20.py" --python-exit-code 1 -- --exercise layout --render
```
Référence : `COMPLETED_EXAMPLES/ch18_20_layout_contact.png` (les 3 plans, board superposé).
