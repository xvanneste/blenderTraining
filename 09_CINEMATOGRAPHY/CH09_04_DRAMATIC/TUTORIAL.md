# CH09.04 — Tutoriels pas à pas

Ouvrez `STARTER_FILES/ch09_04_dramatic_starter.blend`. Sauvegardez sous `ch09_04_dramatic_starter_<prenom>_v001.blend`.

## Tutoriel 1 — LOWKEY (20 min)
Choisissez la scène LOWKEY. LOW_Key : Power 70 W, Color orange (1 ; 0,65 ; 0,35). LOW_Fill : Power 0,5 W. LOW_Rim : Power 250 W, Color (0,35 ; 0,75 ; 1).

## Tutoriel 2 — HIGHKEY (10 min)
Choisissez la scène HIGHKEY. HIGH_Key 250 W, HIGH_Fill 150 W, HIGH_Rim 100 W (couleurs blanches).

## Tutoriel 3 — Comparer (10 min)
Rendez chaque scène (F12) et comparez à la planche de référence.

## Tutoriel 4 — Mesurer (10 min)
Lancez le correcteur : il rend les deux scènes et affiche ratio, luminance moyenne, contre-jour et écart de teinte.

## Vérifier
```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch09_04_dramatic_starter_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch09_04.py" -- --exercise dramatic --debug
```

Remarque d'honnêteté : les rendus du correcteur utilisent Cycles CPU (48 échantillons) : un léger bruit existe, les seuils l'absorbent ; les valeurs sont celles de cette sphère grise : un autre sujet donnerait d'autres luminances ; « high_too_contrasty » échoue aussi sur la luminance (réduire la Fill assombrit) ; le sélecteur de scène et les libellés Scene Properties n'ont pas été relus dans l'interface 5.3 ; les deux rendus de contrôle (numpy) ont été regardés.

## Variante de contrôle

Notez une intention de scène en un verbe. Composez la version Low Key puis High Key avec le même décor. Comparez le point focal en petit, puis les valeurs des ombres. **Preuve** Le contraste sert deux lectures distinctes et le personnage reste identifiable dans les deux cadres.
