# CH11.08 — Tutoriels pas à pas

Ouvrez `STARTER_FILES/ch11_08_tracking_starter.blend` (le dossier `ch11_08_clip/` doit rester à côté). Sauvegardez sous `ch11_08_tracking_starter_<prenom>_v001.blend` dans le même dossier.

## Tutoriel 1 — Voir (5 min)
Espace de travail Motion Tracking (ou éditeur Movie Clip) : le clip de 40 images ; points blancs sur fond noir.

## Tutoriel 2 — La caméra (5 min)
Tracking > Camera : Sensor Width 36 mm puis Focal Length 35 mm.

## Tutoriel 3 — Détecter, suivre, résoudre (20 min)
Image 1 : Detect Features. Sélectionnez les pistes, Track Markers vers l'avant sur toute la séquence. Solve Camera Motion.

## Tutoriel 4 — Mesurer (10 min)
Lancez le correcteur : pistes, erreur, reproduction.

## Vérifier
```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch11_08_tracking_starter_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch11_08.py" -- --exercise tracking --debug
```

Remarque d'honnêteté : les opérateurs `clip.detect_features`, `clip.track_markers` et `clip.solve_camera` ne s'exécutent en arrière-plan que dans un éditeur de clip : le script change temporairement le type d'une zone de l'écran en CLIP_EDITOR (override de contexte) ; cela a fonctionné ici (28 pistes détectées, suivi de 40 images, erreur 0,75 px) ; le chemin d'un clip modifié dans une session non enregistrée vide le clip (256 × 256) : les statistiques sont lues avant ce changement ; le plan est une synthèse parfaite (48 sphères blanches, caméra en translation) : un vrai plan est plus difficile ; les libellés des panneaux Tracking > Camera, Detect Features, Track Markers et Solve Camera Motion n'ont pas été relus dans bl_ui ni regardés dans l'interface ; la focale 100 mm est « résolue » sans erreur (0,75 px) : seule la vérification de la focale la refuse ; Set Floor/Origin et la scène de suivi (Setup Tracking Scene) ne sont pas évalués.

## Variante de contrôle

Recherchez un point qui glisse ou disparaît. Comparez la trajectoire à un repère du décor et prévisualisez un objet simple dans le plan. **Preuve** Le suivi reste crédible sur les images de part et d’autre de l’événement où il se dégrade.
