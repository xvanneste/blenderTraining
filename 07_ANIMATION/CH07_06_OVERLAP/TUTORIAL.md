# CH07.06 — Tutoriels pas à pas

Ouvrez `STARTER_FILES/ch07_06_overlap_starter.blend`. Sauvegardez sous `ch07_06_overlap_starter_<prenom>_v001.blend`.

## Tutoriel 1 — Regarder (10 min)
Pose Mode : lisez l'animation de la base ; les bones tail_1 à tail_3 restent alignés sur elle.

## Tutoriel 2 — L'overlap (30 min)
Pour chaque bone de queue : rotation X (Rotation Mode XYZ Euler) ; clés : tail_1 : 1 (0°), 15 (+18°), 27 (0°), 48 (0°) ; tail_2 : 1, 17 (+14°), 29, 48 ; tail_3 : 1, 19 (+10°), 31, 48.

## Tutoriel 3 — Le follow-through (15 min)
tail_3 : ajoutez 35 (−6°) et 44 (0°) : la pointe dépasse puis se stabilise.

## Tutoriel 4 — Les arcs (10 min)
Lisez la trajectoire de la pointe (chemins de mouvement / motion paths de l'interface) : une courbe douce.

## Tutoriel 5 — Régler (15 min)
Ajustez retards et amplitudes jusqu'à ce que la cascade se lise ; contrôlez dans le Graph Editor que les extrêmes sont décalés.

## Vérifier
```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch07_06_overlap_starter_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch07_06.py" -- --exercise overlap --debug
```

Remarque d'honnêteté : la solution est générée par script (`keyframe_insert` de la rotation X des pose bones) ; les chemins de mouvement (motion paths) et les panneaux cités n'ont pas été relus dans l'interface 5.3. La courbe d'angle et la trajectoire (numpy) ont été regardées : cascade de quatre courbes, dépassement de la pointe, arc.

## Variante de contrôle

Retardez un seul élément secondaire de deux images. Comparez le mouvement principal à celui de l’accessoire. **Preuve** Le mouvement de base reste identique et le retard crée une suite lisible sans faire perdre le point d’arrivée.
