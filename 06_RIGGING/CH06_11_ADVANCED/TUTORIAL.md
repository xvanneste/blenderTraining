# CH06.11 — Tutoriels pas à pas

## Volet A — Bendy bones

Ouvrez `STARTER_FILES/ch06_11_bendy_starter.blend` (tube sur un bone rigide). Sauvegardez sous `ch06_11_bendy_starter_<prenom>_v001.blend`.

### Tutoriel 1 — Segments (10 min)
Bone properties > Bendy Bones : Segments = 8.

### Tutoriel 2 — Courber (10 min)
Pose Mode, bone spine : Bendy Bones > Curve In X = 0,3 et Curve Out X = 0,3 : le tube se courbe en arche. Comparez de profil au même cadrage et revenez à zéro après l’essai. Les segments du B-Bone servent à distribuer la déformation. Inspectez le tube pour vérifier l’effet sur le maillage.

### Tutoriel 3 — Vérifier le volet A
```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch06_11_bendy_starter_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch06_11.py" -- --exercise bendy --debug
```

## Volet B — Bibliothèque et override

Copiez `STARTER_FILES/ch06_11_shot_starter.blend` sous `STARTER_FILES/ch06_11_shot_starter_<prenom>_v001.blend` : le plan doit rester dans le MÊME dossier que `ch06_11_rig_library.blend`.

### Tutoriel 4 — Lier (10 min)
File > Link : ch06_11_rig_library.blend > Collection > COL_Rig ; vérifiez que Relative Path est coché. Ajoutez la collection liée à la scène.

### Tutoriel 5 — Override (10 min)
Sélectionnez la collection liée / l'objet RIG_Lib ; Object > Library Override > Make > Selected & Content (l'override éditable). L'objet RIG_Lib devient local (icône d'override).

### Tutoriel 6 — Placer et poser (20 min)
Déplacez RIG_Lib de 2 m en X. Pose Mode, bone arm : tournez-le de 30° autour de Z et insérez un keyframe de rotation à l'image 1 (une Action est créée).

### Tutoriel 7 — Enregistrer et vérifier le volet B
Enregistrez le plan (le chemin reste relatif), puis :
```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch06_11_shot_starter_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch06_11.py" -- --exercise override --debug
```

Remarque d'honnêteté : les fichiers sont construits par script avec les opérateurs et propriétés de l'API 5.3 (Segments, Curve In/Out X, `libraries.load`, `override_hierarchy_create`, keyframe) ; le croquis du volet A a été regardé. Les noms de menus (File > Link, Object > Library Override > Make) et les raccourcis du tutoriel n'ont pas été relus dans l'interface 5.3 ; c'est aussi le cas de l'ordre exact des panneaux. La pose par Action est une contrainte mesurée en arrière-plan : dans l'interface, une pose saisie à la main peut se comporter autrement.

## Variante de contrôle

Comparez une déformation Bend avec trois poses de contrôle, puis rouvrez un plan avec l’override de travail. Identifiez laquelle des deux couches vous modifiez. **Preuve** La pose locale est retrouvée après réouverture et le rapport indique la version de bibliothèque.
