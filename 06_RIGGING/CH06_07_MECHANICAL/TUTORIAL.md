# CH06.07 — Tutoriels pas à pas

Ouvrez `STARTER_FILES/ch06_07_truck_starter.blend` (camion et armature, rien d'autre). Sauvegardez sous `ch06_07_truck_starter_<prenom>_v001.blend`.

## Tutoriel 1 — Un driver de roue (30 min)
Sélectionnez RIG_Truck, passez en Pose Mode, sélectionnez le bone wheel_FL. Dans Bone properties, Transform : Rotation Mode = XYZ Euler. Clic droit sur la valeur Y de la rotation > Add Driver. Dans l'éditeur de driver : type Scripted Expression `-d / 0.3` ; ajoutez la variable d : type Transform Channel, objet RIG_Truck, bone root, type Y Location, espace Local Space. Déplacez root dans Y : la roue tourne. Répétez pour les trois autres roues.

## Tutoriel 2 — Parenter les roues (5 min)
Les bones wheel_* doivent avoir root pour parent (Bone properties > Relations > Parent).

## Tutoriel 3 — Le vérin (20 min)
Bone cyl > Bone Constraints > Add Bone Constraint > Damped Track : Target RIG_Truck, Bone bed_pt. Bone rod : Damped Track, Target RIG_Truck, Bone anchor. Tournez `bed` autour de X. Vérifiez de profil que les axes des deux tubes restent alignés et que le vérin rejoint ses points d’ancrage. Le suivi oriente les os. La longueur visible se contrôle séparément.

## Tutoriel 4 — La benne (10 min)
Bone bed > Bone Constraints > Limit Rotation : cochez Limit X (min 0°, max 45°), Limit Y et Limit Z (0 et 0), Owner Space Local Space.

## Tutoriel 5 — Vérifier
```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch06_07_truck_starter_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch06_07.py" -- --exercise truck --debug
```

Remarque d'honnêteté : les fichiers sont construits par script avec les mêmes propriétés que celles de l'interface (driver, Damped Track, Limit Rotation) et testés en arrière-plan ; le croquis de profil a été regardé (roues tournées, vérin aligné, benne à 35°). Les noms de menus et de panneaux de ce tutoriel n'ont pas été relus dans l'interface 5.3.

## Variante de contrôle

Faites avancer le véhicule de deux distances connues. Comparez les rotations avec la circonférence de la roue et observez le sens sur les deux côtés. **Preuve** Un tableau établit la relation entre longueur et angle, puis situe le problème si le driver roule à l’envers.
