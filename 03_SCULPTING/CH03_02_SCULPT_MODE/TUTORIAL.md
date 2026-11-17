# CH03.02 — Tutoriels pas à pas

Ouvrez `STARTER_FILES/ch03_02_face_starter.blend` et enregistrez-le sous
`ch03_02_face_<prenom>_v001.blend`. Sélectionnez `SCULPT_Head` ; **Ctrl+Tab** > *Sculpt Mode*.
Le visage regarde vers −Y : vue de face = **Num 1**.

## Tutoriel 1 — Prise en main
1. Choisissez **Draw** dans l’étagère de brosses. `Shift+Espace` ouvre aussi le sélecteur
   de brosses. Réglez la taille avec `F` et la force autour de 0,5 avec `Shift+F`.
2. Cliquez-glissez sur une zone d'essai… puis Ctrl+Z : on teste, on annule.
3. Ctrl maintenu : la brosse creuse. Shift maintenu : elle lisse.

## Tutoriel 2 — Symétrie et masque
1. En-tête : activez **Mirror X**.
2. Sélectionnez la brosse **Mask** et tournez le modèle jusqu’à voir l’arrière. Peignez cette
   zone, puis contrôlez de profil où le masque s’arrête. La zone protégée apparaît sombre.
3. Ne l'effacez pas à la fin : le correcteur vérifie que l'arrière est masqué et intact.

## Tutoriel 3 — Le visage
1. **Nez**. Prenez *Clay Strips* puis *Draw* au centre, sous le milieu du visage. Terminez le
   bout du nez avec un trait léger d’*Inflate/Deflate*.
2. **Orbites** : Ctrl + Draw, de part et d'autre du haut du nez (Mirror X fait le deuxième œil).
3. **Arcades** : Clay Strips au-dessus des orbites.
4. **Pommettes** : Inflate léger sous les orbites.
5. **Bouche et menton**. Tracez le sillon avec *Crease Sharp*. Avec *Draw*, ajoutez du volume
   au menton. Vérifiez en profil que la bouche garde du relief.
6. Lissage général (Shift) ; tournez autour pour vérifier la silhouette de profil.

## Tutoriel 4 — Face Sets
Menu *Face Sets > Initialize Face Sets > By Normals* (ou brosse **Face Set Paint**) : au moins deux
zones colorées. Essayez **Shift+H** sur le visage (isolé), puis **H** sur un côté (caché), puis **Alt+H** (tout réafficher).

## Tutoriel 5 — Vérifier
```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch03_02_face_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch03_02.py" -- --exercise face --render
```
[Rendu de référence](COMPLETED_EXAMPLES/ch03_02_face_reference.png) · [Manuel Blender 5.3 des brosses](https://docs.blender.org/manual/en/5.3/sculpt_paint/brush/introduction.html)

## Variante de contrôle

Comparez une seule passe de sculpt à petit rayon et une passe à grand rayon sur une copie. Surveillez la silhouette et le niveau de résolution. **Preuve** Vous pouvez retrouver quel réglage a produit la différence et annuler une correction locale sans effacer le blocage.
