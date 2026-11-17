# CH07.13 — Tutoriels pas à pas

Ouvrez `STARTER_FILES/ch07_13_nla_starter.blend`. Sauvegardez sous `ch07_13_nla_starter_<prenom>_v001.blend`.

## Tutoriel 1 — Pousser Slide (10 min)
Éditeur Nonlinear Animation : GEO_Crate sélectionnée ; Push Down sur « Slide » : une piste apparaît, l'action active disparaît. Renommez la piste « Move ».

## Tutoriel 2 — Répéter (10 min)
Sélectionnez le strip « Slide » (panneau latéral > Strip) : Repeat = 2. Le strip couvre les images 1 à 49.

## Tutoriel 3 — La piste Spin (15 min)
Ajoutez une piste (Add Tracks), nommez-la « Spin » ; ajoutez le strip de l'action « Spin » (Add Action Strip) ; placez-le à l'image 13 (Frame Start 13 : le strip couvre 13 à 37).

## Tutoriel 4 — Le fondu (5 min)
Strip « Spin » : Blend In = 6.

## Tutoriel 5 — La plage (5 min)
Timeline : End = 49. Lisez l'animation : la caisse glisse deux fois ; la rotation s'ajoute à partir de l'image 13.

## Vérifier
```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch07_13_nla_starter_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch07_13.py" -- --exercise nla --debug
```

Remarque d'honnêteté : les fichiers sont générés par script (`animation_data.nla_tracks.new()`, `strips.new`, `repeat`, `blend_in` ; le slot est assigné automatiquement à la création du strip) ; les noms des boutons de l'éditeur NLA (Push Down, Add Tracks, Add Action Strip) et des champs (Repeat, Blend In, Frame Start) n'ont pas été relus dans l'interface 5.3. Le croquis (numpy) est une représentation schématique de l'éditeur NLA : strip répété avec séparateur, strip en fondu.

## Variante de contrôle

Comparez une Action active et la même action dans un strip NLA. Déplacez le strip en conservant les clés de l’action, puis choisissez deux degrés d’influence. **Preuve** L’action source est retrouvée et le résultat dans la timeline correspond au montage des strips.
