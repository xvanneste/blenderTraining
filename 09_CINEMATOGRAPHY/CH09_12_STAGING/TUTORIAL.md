# CH09.12 — Tutoriels pas à pas

Ouvrez `STARTER_FILES/ch09_12_staging_starter.blend`. Sauvegardez sous `ch09_12_staging_starter_<prenom>_v001.blend`.

## Tutoriel 1 — Voir (10 min)
Allez à l'image 36, vue de dessus (Numpad 7) : A, B et C sont presque alignés.

## Tutoriel 2 — Corriger le blocking (20 min)
À l’image 36, réglez X et Y de A sur (−2 ; −1,5), de B sur (2 ; 0,5) et de C sur (0 ; 3). Pour chaque objet, survolez le champ *Location* et pressez `I`. Gardez la coordonnée verticale du starter. Comparez la séparation des silhouettes via la caméra avant et après le déplacement.

## Tutoriel 3 — Corriger le raccord (15 min)
Pour A, supprimez la clé de l'image 37 (ou remettez-la à (−2, −1,5)) ; la tasse : supprimez sa clé de l'image 37 et remettez-la à (0,3, 0, 0,8) à l'image 36 et 72.

## Tutoriel 4 — Mesurer (10 min)
Lancez le correcteur.

## Vérifier
```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch09_12_staging_starter_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch09_12.py" -- --exercise staging --debug
```

Remarque d'honnêteté : le correcteur évalue la géométrie (positions image par image, rendu Workbench à l'image 36) ; les valeurs (solution : aire 7 m², angle minimal 39°, étagement 4,5 m, vitesse maximale 0,09 m/image ; départ : aire 0,3 m², saut 2,55 m) sont calculées par le script de génération ; les libellés de l'interface (insérer une clé avec I, vue de dessus Numpad 7) sont ceux de la keymap par défaut mais n'ont pas été regardés dans l'interface ; la collision est un contre-exemple ajouté après coup pour tester le contrôle de distance minimale. Vue de dessus regardée.

## Variante de contrôle

Placez une ligne de regard et une cible au-dessus d’un storyboard de trois poses. Vérifiez, dans le layout, la lisibilité de la main et du regard aux mêmes images. **Preuve** Deux cadres montrent où une occultation a été résolue et quelle intention elle révèle.
