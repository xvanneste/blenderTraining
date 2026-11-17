# CH07.03 — Tutoriels pas à pas

Ouvrez `STARTER_FILES/ch07_03_dopesheet_starter.blend`. Sauvegardez sous `ch07_03_dopesheet_starter_<prenom>_v001.blend`.

## Tutoriel 1 — Lire (10 min)
Éditeur Dope Sheet : repérez les trois losanges de « Slide » aux images 1, 13, 25.

## Tutoriel 2 — Retimer (15 min)
Placez la tête de lecture à l’image 1. Elle sert de pivot à la mise à l’échelle temporelle du Dope Sheet. Sélectionnez uniquement les clés de *Slide*. Faites `S`, `2`, `Entrée` et vérifiez les images 1, 25 et 49. Si la première clé a bougé, annulez et vérifiez l’image courante.

## Tutoriel 3 — Dupliquer l'action (15 min)
Sélectionnez GEO_CrateB ; dans l'éditeur d'action, assignez une nouvelle action en dupliquant « Slide » (bouton de duplication), renommez-la « Slide_Late » ; vérifiez que le slot est bien assigné à B.

## Tutoriel 4 — Décaler (10 min)
Dans l'action « Slide_Late », sélectionnez toutes les clés, G puis 24 puis Entrée : les clés tombent aux images 25, 49, 73.

## Tutoriel 5 — La plage (5 min)
Timeline : End = 73.

## Vérifier
```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch07_03_dopesheet_starter_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch07_03.py" -- --exercise dopesheet --debug
```

Remarque d'honnêteté : les fichiers sont générés par script (`keyframe_insert`, `action_slot`) ; les touches S, G et T sont celles de la keymap par défaut ; les boutons et libellés exacts de l'éditeur d'action (duplication, slots) n'ont pas été relus dans l'interface 5.3. Le croquis du Dope Sheet (numpy) a été regardé : trois lignes, losanges aux bonnes images.

## Variante de contrôle

Comptez les images avant et après avoir rapproché un groupe de clés dans le Dope Sheet. Sur une copie d’action, faites le même changement sur un seul canal et comparez avec le Graph Editor. **Preuve** Les clés de détail gardent la relation temporelle voulue et vous pouvez expliquer ce qui a été retimé.
