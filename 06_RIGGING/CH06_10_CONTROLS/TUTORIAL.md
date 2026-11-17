# CH06.10 — Tutoriels pas à pas

Ouvrez `STARTER_FILES/ch06_10_controls_starter.blend`. Sauvegardez sous `ch06_10_controls_starter_<prenom>_v001.blend`.

## Tutoriel 1 — Constater (5 min)
Pose Mode : tournez ctl_arm.L : DEF-arm.L suit. Le rig marche, mais tous les bones sont mêlés.

## Tutoriel 2 — Collections (15 min)
Armature properties > Bone Collections : créez Controls, Deform, Mechanism ; assignez les bones (sélectionner puis Assign) ; masquez *Deform* et *Mechanism* via leur contrôle de visibilité. En mode Pose, faites une rotation de contrôle. Les os masqués doivent continuer à déformer le personnage selon leurs réglages.

## Tutoriel 3 — Formes (30 min)
Créez deux objets en fil de fer (WGT_circle : anneau ; WGT_box : cube) dans une collection WIDGETS ; masquez cette collection. Pour chaque contrôleur : Bone properties > Viewport Display > Custom Shape > Custom Object.

## Tutoriel 4 — Couleurs (10 min)
Bone properties > Bone Color : root THEME09, ctl_spine THEME03, ctl_arm.L THEME04, ctl_arm.R THEME01.

## Tutoriel 5 — Verrous (10 min)
Bone properties > Transform : cadenas de Location et Scale pour ctl_arm.L et .R ; cadenas de Scale pour ctl_spine. Vérifiez que use_deform est décoché pour les contrôleurs (Bone properties > Deform).

## Tutoriel 6 — Vérifier
```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch06_10_controls_starter_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch06_10.py" -- --exercise controls --debug
```

Remarque d'honnêteté : les fichiers sont construits par script avec les propriétés de l'API 5.3 (collections de bones, couleurs, formes, verrous) et testés en arrière-plan ; le croquis (projection oblique) a été regardé. Les noms de panneaux et d'onglets du tutoriel n'ont pas été relus dans l'interface 5.3.

## Variante de contrôle

Sur une copie, montrez à une autre personne deux contrôleurs nommés, l’un actif et l’autre masqué dans sa collection. Qu’elle trouve le second avec la convention du rig. **Preuve** Elle reconnaît le rôle des contrôleurs sans modifier directement les éléments de déformation et les collections restent organisées au retour.
