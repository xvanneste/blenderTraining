# CH12.01 — Tutoriels pas à pas

Ouvrez `STARTER_FILES/ch12_01_vse_starter.blend`. Sauvegardez sous `ch12_01_vse_starter_<prenom>_v001.blend`.

## Tutoriel 1 — Voir (5 min)
Espace de travail Video Editing : quatre strips sur le canal 1 avec des trous.

## Tutoriel 2 — Durées (10 min)
Raccourcissez B_green à 30 images, C_blue à 18, D_yellow à 24 (poignées de strip).

## Tutoriel 3 — Bout à bout (10 min)
Déplacez B, C, D pour qu'ils commencent à 25, 55, 73 ; Frame End 96.

## Tutoriel 4 — Mesurer (10 min)
Lancez le correcteur : durées, débuts, rendu aux quatre images.

## Vérifier
```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch12_01_vse_starter_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch12_01.py" -- --exercise vse --debug
```

Remarque d'honnêteté : l'API 5.3 des strips (`sequence_editor.strips.new_effect(type='COLOR', …)`, `frame_final_start`, `frame_final_duration`, `channel`, `mute`) a été vérifiée par exécution ; le menu Add > Color du Sequencer a été relu dans `bl_ui/space_sequencer.py` ; les libellés des panneaux de propriétés du strip (Time, Channel, Final Duration) et les raccourcis de coupe n'ont pas été relus ni regardés dans l'interface ; la couleur du rendu est mesurée en Workbench avec la vue Standard (avec AgX par défaut le rouge ne rendait pas (1, 0, 0)) ; proxies, ripple, vidéos et sons ne sont pas évalués.

## Variante de contrôle

Placez trois clips courts, puis vérifiez les bornes d’un enchaînement image par image. Comparez le temps lu et la durée d’après les bornes. **Preuve** La dernière image du clip précédent et la première du suivant s’enchaînent sans trou involontaire.
