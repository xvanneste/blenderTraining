# CH07.15 — Tutoriels pas à pas

Ouvrez `STARTER_FILES/ch07_15_dialogue_starter.blend` (BLOCK active). Sauvegardez sous `ch07_15_dialogue_starter_<prenom>_v001.blend`.

## Tutoriel 1 — Lire le blocking (10 min)
Lisez l'animation (Espace) : le regard saute de pose en pose. Dope Sheet : 7 clés en Constant.

## Tutoriel 2 — Dupliquer (10 min)
Éditeur d'action : dupliquez « BLOCK » ; renommez la copie « FINAL » ; assurez-vous que FINAL est l'action de GEO_Head (BLOCK en utilisateur fictif).

## Tutoriel 3 — Splining (15 min)
Dope Sheet (action FINAL) : toutes les clés : T > Bezier ; Graph Editor : V > Auto Clamped.

## Tutoriel 4 — Breakdowns (15 min)
Image 7 : lacet +22°, clé ; image 31 : +5°, clé ; image 55 : −12°, clé. Pas de clé dans les maintiens.

## Tutoriel 5 — Marqueurs (10 min)
Timeline : M aux images 1, 13, 25, 37, 49, 61, 73 ; F2 pour nommer beat_1 à beat_7.

## Vérifier
```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch07_15_dialogue_starter_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch07_15.py" -- --exercise dialogue --debug
```

Remarque d'honnêteté : les fichiers sont générés par script (clés, interpolation, poignées, marqueurs) ; les touches T, V, M et F2 sont celles de la keymap par défaut (vérifiées dans `blender_default.py`) ; le bouton de duplication de l'éditeur d'action et la gestion de l'utilisateur fictif n'ont pas été relus dans l'interface 5.3. Le croquis (numpy) a été regardé : escalier gris du blocking, courbe orange du splining, maintiens plats. Ce chapitre ne mesure pas le polish.

## Variante de contrôle

Comparez une lecture en blocking Constant à une lecture lissée de la même scène. Identifiez un passage où le lissage adoucit trop le choix du personnage. **Preuve** Le blocking reste dans une action conservée et votre ajustement maintient une articulation lisible entre les poses.
