# CH09.10 — Tutoriels pas à pas

Ouvrez `STARTER_FILES/ch09_10_movements_starter.blend`. Sauvegardez sous `ch09_10_movements_starter_<prenom>_v001.blend`.

## Tutoriel 1 — Voir (10 min)
Sélectionnez chaque caméra et regardez à travers (View > Cameras > Set Active Object as Camera) : dans CAM_CLOSE, le bleu est à gauche.

## Tutoriel 2 — Corriger la ligne (5 min)
CAM_CLOSE : Location (0, −4, 0,9), Rotation (90°, 0, 0).

## Tutoriel 3 — Repères et travelling (20 min)
Timeline : image 1, sélectionnez CAM_WIDE, M puis Marker > Bind Camera to Markers ; idem pour CAM_MED à l'image 25 et CAM_CLOSE à l'image 49. CAM_MED : Location Y = −8 à l'image 25, I sur Y ; −6 à l'image 48, I ; puis interpolation Linear.

## Tutoriel 4 — Mesurer (10 min)
Contrôlez les images 24, 25, 48 et 49 en vue caméra. Les changements de caméra doivent coïncider avec les repères, et le sujet doit grandir entre 25 et 48. Comparez le côté occupé par le bleu au raccord. Lancez ensuite le correcteur pour confronter vos observations aux mesures.

## Vérifier
```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch09_10_movements_starter_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch09_10.py" -- --exercise movements --debug
```

Remarque d'honnêteté : le rendu de contrôle est du Workbench plat segmenté par couleur ; les mesures (27 %, 58 %, 82 %, travelling 58 % → 78 %) sont mesurées sur cette scène. Le libellé « Bind Camera to Markers » a été relu par l'API et le menu dans `bl_ui/space_time.py` ; la touche M est celle de la keymap par défaut ; les chemins de menu View > Cameras et le choix de l'interpolation linéaire à l'écran n'ont pas été vérifiés dans l'interface 5.3 (la solution est écrite par script). Planches regardées.

## Variante de contrôle

Comparez début, milieu et fin du mouvement. Notez l’orientation et la taille d’un repère dans le décor. **Preuve** Un tableau des trois images localise la perte de cadrage et la correction maintient le sujet dans la zone voulue.
