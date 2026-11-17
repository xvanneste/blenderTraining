# CH09.02 — Tutoriels pas à pas

Ouvrez `STARTER_FILES/ch09_02_three_point_starter.blend`. Sauvegardez sous `ch09_02_three_point_starter_<prenom>_v001.blend`.

## Tutoriel 1 — La Key (10 min)
Sélectionnez LIGHT_Key > Light Properties > Power 250 W.

## Tutoriel 2 — La Fill (10 min)
LIGHT_Fill > Power 35 W : l'ombre reste lisible.

## Tutoriel 3 — La Rim (10 min)
LIGHT_Rim > Power 300 W. Rendu (F12) : le bord haut se détache.

## Tutoriel 4 — Mesurer (10 min)
Lancez le correcteur : il affiche le ratio et la contribution de la Fill et de la Rim.

## Vérifier
```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch09_02_three_point_starter_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch09_02.py" -- --exercise three_point --debug
```

Remarque d'honnêteté : les rendus du correcteur utilisent Cycles CPU (48 échantillons) : un léger bruit existe, les seuils l'absorbent ; les positions des lampes sont fixées par le fichier de départ (seules les puissances changent) ; la première position de la Rim (0, 3, 3) était inefficace (mesuré) et a été remplacée ; les libellés (Power, Light Properties) viennent de `properties_data_light.py` ; les trois rendus de contrôle (numpy) ont été regardés.

## Variante de contrôle

Rendez la Key seule, puis la Key avec Fill, puis avec Rim. Prenez les mêmes zones de mesure, et comparez l’ombre, la transition et la séparation du fond. **Preuve** Les différences peuvent être associées à une seule lampe ajoutée à chaque étape.
