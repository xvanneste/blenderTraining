# CH01.06 — Tutoriels pas à pas

## Tutoriel 1 — Appliquer l'échelle de la caisse
1. Ouvrez `STARTER_FILES/ch01_06_moving_starter.blend`, cliquez `GEO_Crate`, `N`.
2. Lisez *Scale* (2, 1, 0,5) et *Dimensions* (2 × 1 × 0,5 m).
3. `Ctrl+A` → **Scale**.
   ✅ *Scale* = (1, 1, 1), *Dimensions* inchangées.
4. Expérience : avant d'appliquer (refaites `Ctrl+Z`), ajoutez un modificateur *Bevel*
   (*Properties → Modifiers → Add Modifier → Generate → Bevel*) : biseaux inégaux. Appliquez
   l'échelle : biseaux réguliers. Supprimez le modificateur.

## Tutoriel 2 — Poser le livre sur la table (snapping)
1. En mode Objet, sélectionnez `GEO_Book`. Vérifiez que l’orientation de transformation
   est *Global* et placez-vous en vue oblique pour voir la surface du plateau.
2. Icône **aimant** de l'en-tête → menu à côté : *Snap Target* = **Face** ;
   *Snap Base* = **Closest**. Activez l'aimant (`Shift+Tab`).
3. `G`, `Z`, puis survolez une zone dégagée du dessus du plateau. Confirmez d’un clic
   lorsque le dessous du livre rejoint la table.
4. Vérifiez de côté. Pour le livre fourni, *Item → Location Z* doit être à environ
   0,82 m, soit les 0,80 m du plateau et la demi-épaisseur du livre. Une autre valeur
   peut indiquer que le pointeur visait le bord ou une autre surface.
5. Désactivez l’aimant (`Shift+Tab`). Si le contact reste difficile à obtenir, saisissez
   `0.8 + 0.02` dans *N → Item → Location Z* et inspectez le résultat de côté.

## Tutoriel 3 — Plaquer l'étagère au mur
1. `GEO_Shelf`, aimant : *Snap Target* = **Face**, *Snap Base* = **Closest**.
2. `G Y`, `Ctrl` maintenu, survolez la face du mur : le dos de l'étagère touche le mur.
   ✅ Le dos est à y = 2 ; X et Z n'ont pas bougé (contrainte Y).

## Tutoriel 4 — Avancer la planche dans sa propre direction
1. `GEO_Plank` (tournée de 30°).
2. `G X 1 Entrée` : elle part le long du X **global** — `Ctrl+Z`.
3. `G X X 1 Entrée` : elle avance le long de **son** axe X (l'en-tête affiche *along local X*).
4. Variante : menu `,` → *Local*, puis `G X 1`.
   Remettez ensuite l’orientation sur *Global* pour les exercices suivants.

[Manuel Blender 5.3 de l’accrochage](https://docs.blender.org/manual/en/5.3/editors/3dview/controls/snapping.html)

## Tutoriel 5 — Vérifier
Enregistrez `ch01_06_moving_<prenom>_v001.blend` puis :
```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch01_06_moving_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch01_06.py" -- --exercise moving
```

## Contrôle de transfert

Avant Ctrl+A → Scale, notez Scale et Dimensions. Après application, comparez la boîte englobante et les reflets du Bevel. Si le snapping de la table n’atteint pas Z = 0,82 m, revenez à la vue de côté et contrôlez le jeu entre le dessous du livre et le plateau. Le test direct de position sert à séparer un problème de snapping d’une taille inattendue. **Réussite** La caisse garde son volume, le livre est posé sans interpénétration et vous expliquez le rôle de chaque contrôle.
