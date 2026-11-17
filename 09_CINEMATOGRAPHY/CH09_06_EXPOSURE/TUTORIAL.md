# CH09.06 — Tutoriels pas à pas

Ouvrez `STARTER_FILES/ch09_06_exposure_starter.blend`. Sauvegardez sous `ch09_06_exposure_starter_<prenom>_v001.blend`.

## Tutoriel 1 — Voir le problème (5 min)
Rendez (F12) : la sphère émissive est un disque blanc plat.

## Tutoriel 2 — La vue (5 min)
Properties > Render > Color Management > View Transform : AgX. Re-rendez : la sphère garde du détail.

## Tutoriel 3 — L'exposition (10 min)
Exposure : +0,5. Comparez avec −2,5 et +3.

## Tutoriel 4 — Mesurer (10 min)
Lancez le correcteur : brûlés, moyenne, contraste.

## Vérifier
```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch09_06_exposure_starter_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch09_06.py" -- --exercise exposure --debug
```

Remarque d'honnêteté : les listes de vues et de looks sont dynamiques (OCIO) et n'ont pas pu être énumérées en arrière-plan ; les noms utilisés (Standard, AgX, Filmic, Khronos PBR Neutral ; looks « AgX - Punchy », « AgX - High Contrast ») ont été acceptés par l'API ; le chemin de menu Properties > Render > Color Management n'a pas été relu dans l'interface 5.3 ; les seuils sont calibrés sur cette scène. Rendus et histogrammes (numpy) regardés.

## Variante de contrôle

Dans deux copies, augmentez de 1 stop l’exposition d’affichage puis changez la puissance d’une seule lumière. Gardez les autres paramètres constants. **Preuve** Vous distinguez une modification globale de la présentation de l’image d’un changement de la contribution de cette source.
