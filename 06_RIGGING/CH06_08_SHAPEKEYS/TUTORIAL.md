# CH06.08 — Tutoriels pas à pas

Ouvrez `STARTER_FILES/ch06_08_shapekeys_starter.blend` : le bras est lié. Sauvegardez sous `ch06_08_shapekeys_starter_<prenom>_v001.blend`.

## Tutoriel 1 — Constater (5 min)
Pose Mode, fore : Rotation Mode XYZ Euler, rotation Z de 90° : le coude s'écrase.

## Tutoriel 2 — Les shape keys (20 min)
Sélectionnez CHR_Arm > Object Data > Shape Keys : « + » deux fois (Basis, puis Key 1), renommez le second elbow_fix. Edit Mode avec elbow_fix actif : sélectionnez les anneaux du coude (|x − 0,30| < 12 cm), Scale en pivot sur l'axe (X) : environ 1,22 en Y et Z (Scale 1,22 ; contraindre à l'axe X via Shift+X). Retour en Object Mode.

## Tutoriel 3 — Le groupe (10 min)
Vertex Groups : « elbow », poids 1 au centre du coude décroissant jusqu'à 0 à 12 cm. Dans Shape Keys, Vertex Group = elbow. Réglez Value à 1 pour voir : seul le coude gonfle.

## Tutoriel 4 — Le driver (20 min)
Clic droit sur Value > Add Driver ; Scripted Expression `a / 1.5708` ; variable a : Transform Channel, objet RIG_Arm, bone fore, Z Rotation, Local Space. Vérifiez la valeur à 0°, 45° et 90°. Elle doit être proche de 0, 0,5 et 1. Comparez le profil du coude avec et sans correction à la même pose.

## Tutoriel 5 — Vérifier
```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch06_08_shapekeys_starter_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch06_08.py" -- --exercise shapekeys --debug
```

Remarque d'honnêteté : le shape key de la solution est écrit par script (gonflage de 22 % calibré par mesure) ; le gonflage au clavier du tutoriel 2 est une approximation à ajuster d'après la mesure du correcteur. Les menus et raccourcis cités n'ont pas été relus dans l'interface 5.3. Le croquis a été regardé : coude écrasé à gauche, volume restauré à droite.

## Variante de contrôle

Testez une forme à valeur 0, intermédiaire et 1 avec une vue fixe. Revenez ensuite sur la pose qui pilote la correction. **Preuve** Les trois images distinguent la forme de base, l’effet complet et la transition, et la correction disparaît au neutre quand elle le doit.
