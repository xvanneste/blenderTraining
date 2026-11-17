# CH07.02 — Tutoriels pas à pas

Ouvrez `STARTER_FILES/ch07_02_keyframes_starter.blend`. Sauvegardez sous `ch07_02_keyframes_starter_<prenom>_v001.blend`.

## Tutoriel 1 — La timeline (10 min)
Timeline : Start 1, End 72 ; propriétés de sortie : Frame Rate 24 ; image courante 1.

## Tutoriel 2 — La position (20 min)
Dans *N → Item → Location*, réglez X à 4 à l’image 24. Survolez *Location* et pressez `I`. Insérez une autre clé avec la même valeur à l’image 48, puis une clé à X = 0 à l’image 72. La clé de 1 existe déjà. Dans le Graph Editor, vérifiez que le canal X a quatre clés et qu’aucune courbe de rotation ou d’échelle n’a été créée par ces gestes.

[Manuel Blender 5.3 de l’insertion des clés](https://docs.blender.org/manual/en/5.3/animation/keyframes/editing.html)

## Tutoriel 3 — La rotation (20 min)
Image 24 : rotation Z = 0, I (Rotation). Image 48 : rotation Z = 90°, I. Image 72 : 90°, I.

## Tutoriel 4 — L'interpolation (10 min)
Dope Sheet : sélectionnez les clés de rotation, T > Linear.

## Tutoriel 5 — Les marqueurs (10 min)
Image 24 : M dans la timeline, F2 pour nommer « arrive ». Image 48 : « turn_end ».

## Vérifier
```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch07_02_keyframes_starter_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch07_02.py" -- --exercise keyframes --debug
```

Remarque d'honnêteté : la solution est générée par script (`keyframe_insert`, interpolation `LINEAR`) ; les touches I, T, M et F2 sont celles de la keymap par défaut (vérifiées dans `blender_default.py`) ; l'option exacte du menu d'insertion et les libellés des panneaux n'ont pas été relus dans l'interface 5.3. Le croquis (courbes numpy) a été regardé : maintien de X de l'image 24 à 48, rotation en ligne droite.

## Variante de contrôle

Fixez deux positions puis déplacez la deuxième clé de 12 images à 24 i/s. Rejouez la timeline et vérifiez l’ordre des événements. **Preuve** Les deux positions sont inchangées et l’arrivée est décalée d’une demi-seconde.
