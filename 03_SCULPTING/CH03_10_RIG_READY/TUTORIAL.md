# CH03.10 — Tutoriels pas à pas

Ouvrez `STARTER_FILES/ch03_10_char_starter.blend` : un mannequin nommé `Mannequin.001`, volontairement sale. Sauvegardez sous
`ch03_10_char_<prenom>_v001.blend`.

## Tutoriel 1 — Diagnostiquer (15 min)
Sélectionnez le mannequin : Sidebar (N) > Item : *Scale* 0,01, *Rotation Z* 4°, *Location* ≠ 0 ; Object Data : nom `Mannequin.001`. Lancez le correcteur (tutoriel 6) :
il liste ce qui ne va pas.

## Tutoriel 2 — Remettre la rotation à zéro (5 min)
En mode Objet, sélectionnez le mannequin et pressez `Alt+R`. Vérifiez en vue de côté (`Numpad 3`) que les pieds pointent
vers −Y. Sur cette scène, les semelles sont déjà quasiment sur le plan du sol.

## Tutoriel 3 — Appliquer les transformations (5 min)
Sur le mannequin seul, en mode Objet, choisissez *Object → Apply → All Transforms*. L’emplacement et la rotation
affichent 0, l’échelle affiche 1. La géométrie garde sa position mondiale et l’origine passe à l’origine de la scène.
Cette opération s’effectue sur le maillage avant l’ajout d’une armature.

## Tutoriel 4 — Origine au sol, entre les pieds (10 min)
En vue de face, vérifiez que le point orange est entre les pieds et que les semelles longent Z = 0.
Sur le starter, le point inférieur est à environ 0,4 mm au-dessus du sol. Si vous utilisez une autre scène,
repositionnez le maillage en mode Édition selon l’écart que vous mesurez. Contrôlez de nouveau de face et de profil.

## Tutoriel 5 — Nommer et ranger (10 min)
F2 : `CHR_Hero_Body` ; données : *Object Data* > nom `ME_CHR_Hero_Body`. Nouvelle collection `CHR_Hero` (M > New Collection) et déplacez-y l'objet.
Aucun suffixe `.001`.

## Tutoriel 6 — Vérifier
```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch03_10_char_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch03_10.py" -- --exercise rigready --render
```
Ajoutez `--debug` pour les grandeurs brutes. Référence : `COMPLETED_EXAMPLES/ch03_10_char_reference.png`.

Remarque d'honnêteté : le mannequin est **généré par script** ; les étapes ci-dessus sont celles que le correcteur vérifie, mais elles n'ont pas été exécutées à la
souris. Le correcteur, lui, a été éprouvé (SOLUTIONS.md).

## Variante de contrôle

Avant de transmettre le maillage au rigging, vérifiez l’axe, l’échelle, les noms, la continuité et les normales. Faites un test de flexion simple au coude ou au genou et conservez une pose neutre. **Preuve** Le maillage rouvert conserve ses réglages et la comparaison de poses situe un défaut éventuel.
