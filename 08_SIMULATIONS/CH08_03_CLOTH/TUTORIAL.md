# CH08.03 — Tutoriels pas à pas

Ouvrez `STARTER_FILES/ch08_03_cloth_starter.blend`. Sauvegardez sous `ch08_03_cloth_starter_<prenom>_v001.blend`.

## Tutoriel 1 — Les obstacles (10 min)
COL_Ball puis COL_Floor : Physics > Collision.

## Tutoriel 2 — Le tissu (15 min)
CLOTH_Sheet : Physics > Cloth ; Quality 12 ; Bending Stiffness 0,4 ; Air Damping 5.

## Tutoriel 3 — Les collisions du tissu (10 min)
Cloth > Collisions : cochées ; Quality 5 ; Distance 0,005 ; Self Collisions décochées.

## Tutoriel 4 — Lire (10 min)
Lisez depuis l’image 1 sans sauter directement à l’image finale. Comparez un arrêt juste avant le premier contact et un second après stabilisation. Après un changement de géométrie ou de réglage, effacez l’ancien cache avant de relancer. Conservez une copie distincte pour comparer des paramètres de collision. Lancez ensuite le correcteur sur votre version.

## Vérifier
```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch08_03_cloth_starter_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch08_03.py" -- --exercise cloth --debug
```

Remarque d'honnêteté : la solution est générée par script (modificateurs `CLOTH` et `COLLISION`, propriétés `settings` et `collision_settings`) et simulée par le correcteur en arrière-plan ; les noms de panneaux (Physics > Cloth, Collisions, Collision) n'ont pas été relus dans l'interface 5.3. Le profil (numpy) a été regardé : drap plat à l'image 1, drapé à l'image 30, posé à l'image 120.

## Variante de contrôle

Vérifiez un panneau de tissu dans une pose simple avant de doubler la résolution. Contrôlez groupe d’épinglage, épaisseur de collision et contact avec l’obstacle. **Preuve** Deux images, avant et après contact, démontrent d’où vient une traversée éventuelle.
