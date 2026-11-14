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
1. Cliquez `GEO_Book`.
2. Icône **aimant** de l'en-tête → menu à côté : *Snap Target* = **Face** ;
   *Snap Base* = **Closest**. Activez l'aimant (`Shift+Tab`).
3. `G Z`, survolez le plateau : le livre s'y colle. `LMB`.
4. Vérifiez : sidebar → *Location Z* ≈ 0,82 m (plateau à 0,8 + demi-épaisseur 0,02).
5. Désactivez l'aimant (`Shift+Tab`).
   Variante sans snapping : `N` → *Location Z* = `0.8 + 0.02`.

## Tutoriel 3 — Plaquer l'étagère au mur
1. `GEO_Shelf`, aimant : *Snap Target* = **Face**, *Snap Base* = **Closest**.
2. `G Y`, `Ctrl` maintenu, survolez la face du mur : le dos de l'étagère touche le mur.
   ✅ Le dos est à y = 2 ; X et Z n'ont pas bougé (contrainte Y).

## Tutoriel 4 — Avancer la planche dans sa propre direction
1. `GEO_Plank` (tournée de 30°).
2. `G X 1 Entrée` : elle part le long du X **global** — `Ctrl+Z`.
3. `G X X 1 Entrée` : elle avance le long de **son** axe X (l'en-tête affiche *along local X*).
4. Variante : menu `,` → *Local*, puis `G X 1`.

## Tutoriel 5 — Vérifier
Enregistrez `ch01_06_moving_<prenom>_v001.blend` puis :
```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch01_06_moving_<prenom>_v001.blend" `
  --python "SCRIPTS\validate_ch01_06.py" --python-exit-code 1 -- --exercise moving
```
