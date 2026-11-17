# CH07.07 — Tutoriels pas à pas

Ouvrez `STARTER_FILES/ch07_07_posing_starter.blend`. Sauvegardez sous `ch07_07_posing_starter_<prenom>_v001.blend`.

## Tutoriel 1 — Les hanches (15 min)
Pose Mode : sélectionnez `hips`, tournez-le de +8° autour de l'axe Y (R puis Y puis 8). Les cuisses suivent : sélectionnez `thigh.L` et `thigh.R` et tournez chacune de −8° autour de Y pour garder les jambes verticales.

## Tutoriel 2 — Les épaules et la colonne (20 min)
`spine` −4° autour de Y ; `chest` −14° ; `neck` −4° ; `head` −4° : les épaules basculent à l'opposé des hanches, la colonne se courbe.

## Tutoriel 3 — Les jambes (15 min)
`shin.L` : +28° autour de X (genou fléchi, pied vers l'arrière) : jambe libre. La jambe droite reste tendue.

## Tutoriel 4 — Les bras (20 min)
`upper_arm.L` +35° autour de Y, `fore.L` +25° ; `upper_arm.R` +40°, `fore.R` −30° : bras dégagés du corps.

## Tutoriel 5 — Juger la silhouette (10 min)
Vue de face, mode d'affichage Solid avec éclairage Flat et couleur unique (réglages d'ombrage de la vue 3D) : la pose doit se lire en aplat.

## Vérifier
```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch07_07_posing_starter_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch07_07.py" -- --exercise posing --debug
```

Remarque d'honnêteté : la pose de la solution est calculée par script (rotations monde autour du point d'attache de chaque bone) ; les gestes R > Y > valeur du tutoriel sont ceux de la vue 3D mais n'ont pas été rejoués dans l'interface 5.3, et les réglages d'ombrage Flat / couleur unique n'ont pas été relus dans l'interface. Le signe des rotations dépend de l'axe monde choisi : vérifiez le résultat à l'œil et dans la sortie du correcteur. Les silhouettes de la solution ont été regardées (rendu Workbench réel) : épaules et hanches inclinées en sens opposés, bras dégagés.

## Variante de contrôle

Faites une miniature en silhouette pour deux poses au même cadre. Notez centre de masse, appui et direction du regard. **Preuve** Le geste se comprend sans les détails du visage et la pose reste crédible depuis une deuxième vue.
