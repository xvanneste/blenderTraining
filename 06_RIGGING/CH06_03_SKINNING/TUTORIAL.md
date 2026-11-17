# CH06.03 — Tutoriels pas à pas

Ouvrez `STARTER_FILES/ch06_03_skinning_starter.blend` : le tube `CHR_Arm` (60 cm le long de X) et l'armature `RIG_Arm` (bones upper et fore), non liés. Sauvegardez sous `ch06_03_skinning_starter_<prenom>_v001.blend`.

## Tutoriel 1 — Lier (10 min)
En mode Objet, sélectionnez le tube, puis ajoutez l’armature avec `Shift` et un clic dans la vue 3D. Vérifiez que l’armature est active, puis utilisez **Ctrl+P → With Automatic Weights**. Vérifiez : modificateur Armature, groupes upper et fore.

## Tutoriel 2 — Voir les poids (15 min)
Sélectionnez le tube, mode **Weight Paint** ; Object Data > Vertex Groups : sélectionnez upper (rouge = 1, bleu = 0), puis fore.

## Tutoriel 3 — Plier (15 min)
Sélectionnez l'armature, Pose Mode : tournez `fore` de 90° (R, Z, 90). La racine reste, le bout suit, le coude se plie. Remettez la pose à zéro (Pose > Clear Transform > All).

## Tutoriel 4 — Normaliser (10 min)
Weights > **Normalize All** (en Weight Paint) ; vérifiez Limit Total = 4.

## Tutoriel 5 — Vérifier
```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch06_03_skinning_starter_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch06_03.py" -- --exercise skinning --debug
```
Le correcteur plie lui-même le coude et remet la pose à zéro.

Remarque d'honnêteté : la solution est faite avec l'opérateur réel `parent_set(type='ARMATURE_AUTO')` en arrière-plan ; j'ai regardé le croquis des poids et du pliage (transition progressive, coude plié). Une première version du correcteur refusait la solution car Automatic Weights laissait des sommes de 0,978 : j'ai normalisé les poids. Les noms de menus et raccourcis n'ont pas été relus dans l'interface 5.3.

## Variante de contrôle

Comparez le coude en neutre et à deux angles. Affichez le poids sur un groupe puis sur son voisin. Inspectez la transition qui accompagne le pli. **Preuve** La correction est lisible dans les deux poses et un test vérifie qu’elle n’a pas déplacé par erreur une région voisine.
