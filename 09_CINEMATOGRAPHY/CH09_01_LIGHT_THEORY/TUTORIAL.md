# CH09.01 — Tutoriels pas à pas

Ouvrez `STARTER_FILES/ch09_01_light_starter.blend`. Sauvegardez sous `ch09_01_light_starter_<prenom>_v001.blend`.

## Tutoriel 1 — Reculer (10 min)
LIGHT_Key > Object Properties > Transform : Location Z = 3.

## Tutoriel 2 — Compenser (15 min)
Light Properties > Power : 100 W (10 × 9 = 90, un peu plus pour la couleur chaude). Rendu (F12) : comparez avec la référence.

## Tutoriel 3 — Adoucir et réchauffer (10 min)
Radius 0,5 m ; Color (1 ; 0,85 ; 0,65).

## Tutoriel 4 — Le correcteur (10 min)
Lancez-le : il rend deux images et affiche exposition, rapport rouge / bleu et pénombre.

## Vérifier
```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch09_01_light_starter_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch09_01.py" -- --exercise light --debug
```

Remarque d'honnêteté : les deux rendus du correcteur sont faits avec Cycles CPU (64 échantillons) : un léger bruit existe (le seuil de ± 20 % l'absorbe) ; les valeurs de référence (0,119) sont mesurées avec ce moteur et pourraient légèrement varier avec une autre version ; les libellés des panneaux (Power, Radius, Color) ont été relus dans `properties_data_light.py` ; la température de couleur n'est pas testée. Profils d'ombre (numpy) regardés : bord progressif (orange) contre bord net (bleu).

## Variante de contrôle

Placez une petite source à 1 m puis à 2 m. Comparez les valeurs mesurées sur la même cible, caméra et exposition fixes. La loi de l’inverse du carré sert de repère pour une source assimilable à un point. Une grande source proche et les rebonds s’écartent de ce modèle. **Preuve** Deux mesures et les conditions du test.
