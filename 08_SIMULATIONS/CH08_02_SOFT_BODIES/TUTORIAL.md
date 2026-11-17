# CH08.02 — Tutoriels pas à pas

Ouvrez `STARTER_FILES/ch08_02_softbody_starter.blend`. Sauvegardez sous `ch08_02_softbody_starter_<prenom>_v001.blend`.

## Tutoriel 1 — Activer (5 min)
GEO_Plate : propriétés Physics > Soft Body.

## Tutoriel 2 — Le goal (15 min)
Soft Body Goal : coché ; Vertex Group : « pin » ; Default 1,0 ; Min 0 ; Max 1.

## Tutoriel 3 — Les arêtes (10 min)
Soft Body Edges : coché ; Pull 0,9 ; Push 0,9 ; Bending 1,0 ; Object > Mass 1 kg.

## Tutoriel 4 — Lire (10 min)
Lisez depuis l’image 1 et comparez la position des sommets du groupe `pin` à celle du bord libre. Les premiers doivent rester ancrés. Si toute la plaque tombe, vérifiez le groupe du *Goal* avant de modifier la rigidité. Lancez le correcteur à partir du fichier enregistré.

## Vérifier
```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch08_02_softbody_starter_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch08_02.py" -- --exercise softbody --debug
```

Remarque d'honnêteté : la solution est générée par script (modificateur `SOFT_BODY`, propriétés `settings.*`) et simulée par le correcteur en arrière-plan ; les noms de panneaux (Physics > Soft Body, Soft Body Goal, Soft Body Edges) n'ont pas été relus dans l'interface 5.3. Résultat à connaître : avec Goal Default à 0 la plaque tombait entièrement en arrière-plan alors que Default 1 avec des poids 0 explicites fonctionnait ; ce comportement n'a pas été expliqué. Le profil (numpy) a été regardé : plaque horizontale, balancement, plaque pendue.

## Variante de contrôle

Sur une copie, comparez deux valeurs de maintien du goal et choisissez une zone qui doit rester attachée. Rejouez depuis le début après modification. **Preuve** La séparation entre zones attachée et déformée se voit au même instant des deux calculs.
