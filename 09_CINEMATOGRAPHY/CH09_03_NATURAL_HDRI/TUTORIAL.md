# CH09.03 — Tutoriels pas à pas

Ouvrez `STARTER_FILES/ch09_03_natural_hdri_starter.blend`. Sauvegardez sous `ch09_03_natural_hdri_starter_<prenom>_v001.blend`.

## Tutoriel 1 — Voir le monde (10 min)
Passez dans l'espace de travail Shading ; dans le Shader Editor choisissez Shader Type : World. Repérez Environment Texture et Mapping.

## Tutoriel 2 — Tourner (10 min)
Mapping > Rotation Z : 180°. Rendu (F12) : l'ombre part vers la droite.

## Tutoriel 3 — Exposer (10 min)
Background > Strength : 1. Comparez avec 0,3 et 3.

## Tutoriel 4 — Mesurer (10 min)
Lancez le correcteur : direction de l'ombre, exposition, teinte de l'ombre.

## Vérifier
```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch09_03_natural_hdri_starter_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch09_03.py" -- --exercise hdri --debug
```

Remarque d'honnêteté : la HDRI est SYNTHÉTIQUE (générée par numpy, pas une photo) ; le correcteur rend avec Cycles CPU (64 échantillons) et mesure la direction de l'ombre à ± 20° ; la longueur de l'ombre n'est pas contrôlée (2,56 m mesurés pour 2,75 m attendus) ; le chemin Shading > Shader Editor > World n'a pas été relu dans l'interface 5.3 (libellés des nœuds vérifiés par l'API) ; le sens de rotation (180° pour un soleil à gauche) est empirique, mesuré par rendu. Vue du dessus (numpy) regardée : ombre à droite (solution), en haut (90°).

## Variante de contrôle

Tournez l’environnement sans déplacer la caméra. Dans la sphère brillante, repérez le déplacement d’un reflet. Dans la version diffuse, comparez l’orientation de l’ombre. **Preuve** Deux mécanismes observés au même instant, avec rotation et intensité indiquées.
