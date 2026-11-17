# CH18.20 — Tutoriels pas à pas

## Tutoriel 1 — Préparer un board dans une caméra (à refaire sur vos plans)
1. *Add > Camera*, cadrez le plan ; Timeline : marqueur, *Marker > Bind Camera to Markers* (Ctrl+B).
2. *Add > Grease Pencil > Blank* ; renommez `BOARD_SH0010`.
3. Dans *Object Properties → Relations → Parent*, choisissez la caméra. Sélectionnez seulement
   le board et utilisez `Alt+P → Clear Parent Inverse` s’il a un décalage de parentage. Remettez
   sa position et sa rotation locales à zéro, puis réglez *Location Z* à −0,5. Cela le place devant l’objectif.
4. Vue caméra (Num 0), mode Draw, *Drawing Plane* : *View* ; dessinez le plan (personnages, flèches).

## Tutoriel 2 — Lire les boards du starter
1. Ouvrez `STARTER_FILES/ch18_20_layout_starter.blend`, Num 0.
2. Dans la Timeline, saisissez successivement les images 1, 73 et 121 dans le champ de l’image
   courante. La caméra active change aux marqueurs associés. Chaque board indique la place du personnage.
3. Masquez (H) les boards des autres plans pour ne voir que celui du plan courant.

## Tutoriel 3 — Le blocking
1. À l’image 1 (SH0010), sélectionnez `CHR_A`. En orientation *Global*, faites `G`, `Shift+Z`
   pour déplacer le personnage dans le plan du sol, puis `R`, `Z` pour l’orienter. Rapprochez sa
   silhouette de celle du board dans la vue caméra et contrôlez en profil que ses pieds restent au sol.
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
  --python-exit-code 1 --python "SCRIPTS\validate_ch18_20.py" -- --exercise layout --render
```
Référence : `COMPLETED_EXAMPLES/ch18_20_layout_contact.png` (les 3 plans, board superposé).

## Variante de contrôle

Dans le layout, superposez un cadre de storyboard et les volumes de la scène. Faites coïncider regard, action et limites de cadre avant l’animation. **Preuve** Deux images de contrôle expliquent les écarts acceptés entre board et 3D.
