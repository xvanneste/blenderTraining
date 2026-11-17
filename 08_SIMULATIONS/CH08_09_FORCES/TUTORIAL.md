# CH08.09 — Tutoriels pas à pas

Ouvrez `STARTER_FILES/ch08_09_forces_starter.blend`. Sauvegardez sous `ch08_09_forces_starter_<prenom>_v001.blend`.

## Tutoriel 1 — Le vent (10 min)
Add > Force Field > Wind ; nommez FORCE_Wind ; Physics > Strength 5 ; Rotation Y 90°.

## Tutoriel 2 — La turbulence (10 min)
Add > Force Field > Turbulence ; nommez FORCE_Turb ; Strength 5 ; Size 0,5.

## Tutoriel 3 — Les poids (5 min)
EMITTER > Physics > Particles > Field Weights : vérifiez Wind et Turbulence à 1.

## Tutoriel 4 — Observer (10 min)
Lisez de l’image 1 à 60. Testez d’abord le vent seul, puis réactivez la turbulence à graine identique. Comparez la direction moyenne du nuage et la dispersion à une même image. Relancez la lecture depuis la première image après chaque modification.

## Vérifier
```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch08_09_forces_starter_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch08_09.py" -- --exercise forces --debug
```

Remarque d'honnêteté : la solution est générée par script (`bpy.ops.object.effector_add(type='WIND' / 'TURBULENCE')`, `rotation`, `field.strength`, `field.size`, `effector_weights`) ; la liste des types de champs du THEORY vient de mon souvenir de l'interface et n'a pas été relue ; les noms de panneaux n'ont pas été relus dans l'interface 5.3 ; pas d'effet sur tissu ni corps rigides testé. Vue de dessus (numpy) regardée : nuage immobile, bande dérivée, bande brassée.

## Variante de contrôle

Faites un contrôle avec un seul champ, puis activez le second. Conservez la graine, les conditions initiales et le cache de chaque version. **Preuve** Une direction ou une irrégularité apparaît seulement dans le résultat qui contient le champ correspondant.
