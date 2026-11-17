# CH11.10 — Tutoriels pas à pas

Ouvrez `STARTER_FILES/ch11_10_consistency_starter.blend`. Sauvegardez sous `ch11_10_consistency_starter_<prenom>_v001.blend`.

## Tutoriel 1 — Voir (5 min)
Le cube est blanc et propre sur une plaque brune et granuleuse.

## Tutoriel 2 — Exposition (10 min)
Nœud Exposure entre Render Layers et Alpha Over : −2.

## Tutoriel 3 — Couleur et grain (15 min)
Nœud Color Balance (Lift/Gamma/Gain) : couleur de Gain (1,3 ; 1,0 ; 0,6). Render > Sampling : 2 échantillons.

## Tutoriel 4 — Mesurer (10 min)
Lancez le correcteur : exposition, dominante, grain.

## Vérifier
```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch11_10_consistency_starter_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch11_10.py" -- --exercise consistency --debug
```

Remarque d'honnêteté : les trois critères sont mesurés sur le dessus d'un cube gris et un patch de sol de la plaque, en valeurs AFFICHÉES ; je n'ai pas trouvé de nœud de grain de pellicule dans la liste des nœuds du compositeur 5.3 : le grain du cube vient du bruit de Cycles (peu d'échantillons, sans débruitage), ce qui n'est pas un grain de film ; une première version mesurait les « noirs » d'une face noire du cube : elle ne discriminait rien (l'encodage sRGB relève les noirs à 0,2) et a été remplacée par le grain ; le calibrage de l'exposition (−2 EV) tient à la compression sRGB de la mesure ; les menus de création des nœuds n'ont pas été regardés ; la plaque est générée (grain gaussien de 0,015, mesuré 0,011).

## Variante de contrôle

Utilisez une planche de deux plans adjacents avec les mêmes témoins. Apportez une correction globale, puis une correction locale si nécessaire. **Preuve** La coupe devient moins visible tout en préservant le changement narratif réellement voulu.
