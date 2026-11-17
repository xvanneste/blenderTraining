# CH12.02 — Tutoriels pas à pas

Ouvrez `STARTER_FILES/ch12_02_editing_starter.blend`. Sauvegardez sous `ch12_02_editing_starter_<prenom>_v001.blend`.

## Tutoriel 1 — Durées (15 min)
Réglez SH1 30, SH2 24, SH3 18, SH4 12, SH5 12 images ; placez-les bout à bout sur le canal 1.

## Tutoriel 2 — La résolution (10 min)
Placez SH6 sur le canal 2, de l’image 85 à 112 incluses. Le recouvrement avec SH5 dure 12 images, de 85 à 96 incluses.

## Tutoriel 3 — Le fondu (10 min)
Sélectionnez SH5 puis SH6 et ajoutez *Add → Transition → Crossfade*. Placez la scène sur la plage 1–112. Vérifiez un début cyan, un milieu mélangé et une fin bleue. Si le sens du fondu est inversé, contrôlez l’ordre des deux entrées.

## Tutoriel 4 — Mesurer (10 min)
Lancez le correcteur : échelles, rythme, fondu, rendu.

## Vérifier
```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch12_02_editing_starter_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch12_02.py" -- --exercise editing --debug
```

Remarque d'honnêteté : l'API 5.3 de l'effet Crossfade (`strips.new_effect(type='CROSS', input1=…, input2=…)`, attributs `input_1`, `input_2`) a été vérifiée par exécution : au milieu du fondu le pixel central est le mélange à 50 % ; le menu Add > Transition > Crossfade et ses conditions (sélection de deux strips) n'ont pas été relus ni regardés dans l'interface ; les « plans » sont des couleurs : le correcteur ne juge ni l'axe, ni le regard, ni la continuité ; les échelles viennent du nom du strip ; la règle « durées non croissantes » est une convention d'exercice, pas une loi du montage.

## Variante de contrôle

Essayez deux coupes à 12 images d’écart, sans changer la durée totale. Faites regarder les deux variantes à quelqu’un et demandez à quel instant il comprend l’action. **Preuve** Le choix de montage cite un événement et une réaction observables.
