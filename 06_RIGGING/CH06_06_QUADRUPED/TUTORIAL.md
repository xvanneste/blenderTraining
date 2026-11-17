# CH06.06 — Tutoriels pas à pas

Ouvrez `STARTER_FILES/ch06_06_quadruped_starter.blend` : la créature `CHR_Quad` (capsules) et `META_Quad` (méta-rig Basic Quadruped) trop grand (échelle 1,4) et décalé (0,3 m en X, 0,2 m en Z). Sauvegardez sous `ch06_06_quadruped_starter_<prenom>_v001.blend`.

## Tutoriel 1 — Ajuster (20 min)
Sélectionnez META_Quad : échelle 1, position (0, 0, 0) (Alt+S et Alt+G). Vérifiez en X-Ray : les os sont dans la créature.

## Tutoriel 2 — Générer (10 min)
Object Data > Rigify > **Generate Rig** ; renommez « rig » en RIG_Quad.

## Tutoriel 3 — Lier (20 min)
En mode Objet, sélectionnez `CHR_Quad`, puis ajoutez `RIG_Quad` et laissez-le actif. Après *With Automatic Weights*, vérifiez le modificateur Armature. En Weight Paint, limitez les influences de déformation à quatre avec *Limit Total*, puis utilisez *Normalize All* et vérifiez la flexion de chaque patte.

## Tutoriel 4 — Essayer (15 min)
Pose Mode : déplacez `root` ; levez `front_foot_ik.L` : la patte avant gauche se plie, les autres restent.

## Tutoriel 5 — Vérifier
```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch06_06_quadruped_starter_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch06_06.py" -- --exercise quadruped --debug
```

Remarque d'honnêteté : la créature est construite autour du méta-rig d'origine (elle l'épouse donc par construction) ; l'exercice porte sur la procédure et le contrôle, pas sur l'ajustement d'un méta-rig à une anatomie quelconque. Les opérateurs sont les vrais (méta-rig, `rigify_generate`, Automatic Weights). Le croquis de profil montre la patte avant gauche pliée par l'IK, les autres inchangées. Noms de menus et raccourcis non relus dans l'interface 5.3.

## Variante de contrôle

Comparez patte de soutien et patte qui se lève dans deux poses. Vérifiez l’orientation du pôle et le point d’appui sur le sol. **Preuve** Le pied de soutien reste stable et vous nommez la cible ou le réglage nécessaire pour corriger une rotation imprévue.
