# CH07.12 — Tutoriels pas à pas

Ouvrez `STARTER_FILES/ch07_12_camera_starter.blend`. Sauvegardez sous `ch07_12_camera_starter_<prenom>_v001.blend`.

## Tutoriel 1 — Le travelling (15 min)
Caméra `CAM_Main` : à l’image 1, entrez (0, −8, 1,6) dans *N → Item → Location*. Survolez le champ et pressez `I`. À l’image 72, entrez (0, −4, 1,6) et insérez une seconde clé de la même façon. Vérifiez l’interpolation dans le Graph Editor.

## Tutoriel 2 — Le suivi (10 min)
Caméra sélectionnée : propriétés de contraintes d'objet (Object Constraints) > Add Object Constraint > Track To ; Target EMP_Subject ; Track Axis −Z ; Up Axis Y.

## Tutoriel 3 — Le tremblé (15 min)
Graph Editor : courbe X Location de la caméra : modificateur Noise ; Scale 8 ; Strength 0,1 ; Phase 1. Courbe Z Location : Noise, Scale 8, Strength 0,1, Phase 5. Rien sur Y.

## Tutoriel 4 — Regarder (10 min)
Vue caméra (pavé numérique 0) : lisez le plan (Espace) : le sujet reste au centre, la caméra respire.

## Tutoriel 5 — Vérifier (10 min)
Lancez le correcteur : trajet, vitesses, visée, tremblé, roulis.

## Vérifier
```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch07_12_camera_starter_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch07_12.py" -- --exercise camera --debug
```

Remarque d'honnêteté : la solution est générée par script (`keyframe_insert`, contrainte `TRACK_TO`, modificateurs `NOISE`) ; les menus (Object Constraints, onglet des modificateurs) et la touche 0 du pavé numérique n'ont pas été rejoués dans l'interface 5.3. Le croquis (numpy) a été regardé : trajectoire verticale en vue de dessus avec les rayons vers le sujet, courbes de tremblé distinctes pour X et Z. Le contenu du plan (un point qui traverse) est volontairement minimal.

## Variante de contrôle

Comparez un mouvement de caméra à deux trajectoires avec le même cadre final. Faites une lecture à vitesse nominale et observez les repères du décor. **Preuve** La vitesse et le cadrage accompagnent l’action au lieu de masquer sa lecture.
