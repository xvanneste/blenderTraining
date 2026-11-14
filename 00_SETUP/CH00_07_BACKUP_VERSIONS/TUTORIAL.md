# CH00.07 — Tutoriels pas à pas

## Tutoriel 1 — Versions incrémentales
1. *File → New → General*, enregistrez sous `PROJECTS\essai_versions_v001.blend`.
2. Déplacez le cube, `Ctrl+Alt+S`.
   ✅ Le titre de la fenêtre affiche `essai_versions_v002.blend`. Les deux fichiers existent.
3. Encore une modification, `Ctrl+Alt+S` → `v003`.

## Tutoriel 2 — Récupérer après un plantage
1. Modifiez la scène sans enregistrer, attendez au moins le délai d'Auto Save (2 min).
2. Simulez un plantage : Gestionnaire des tâches → *Blender* → *Fin de tâche*.
3. Relancez Blender → *File → Recover → Auto Save…* → choisissez le fichier le plus récent.
   ✅ Vos modifications (jusqu'à la dernière auto-sauvegarde) sont là. Enregistrez-les en
   nouvelle version immédiatement.
4. Variante : quittez Blender normalement **sans enregistrer** (en refusant la sauvegarde) ;
   relancez → *File → Recover → Last Session*.

## Tutoriel 3 — Récupérer via le .blend1 (exercice guidé)
1. Ouvrez `STARTER_FILES\ch00_07_recovery\ch00_07_hero_scene_v001.blend` : le personnage
   `GEO_Hero` a disparu ; `Ctrl+Z` n'y peut rien.
2. Fermez ce fichier. Dans l'explorateur Windows, à côté, se trouve
   `ch00_07_hero_scene_v001.blend1`.
3. **Méthode sûre** : copiez le `.blend1` dans votre dossier de travail et renommez la copie
   `ch00_07_hero_scene_v002.blend` (confirmez le changement d'extension).
4. Ouvrez-la : `GEO_Hero` est là. Enregistrez (`Ctrl+S`).
   ✅ Validez :
```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "<dossier>\ch00_07_hero_scene_v002.blend" `
  --python "SCRIPTS\validate_ch00_07.py" --python-exit-code 1 -- --exercise recover
```

## Tutoriel 4 — Sauvegarde 3-2-1 de l'académie
```powershell
python "SCRIPTS\bcma_backup.py" --source "G:\_formation\blender\BLENDER_CINEMA_MASTER_ACADEMY\PROJECTS" --dest "F:\Backups\BCMA" --keep 10
```
(Adaptez `F:\Backups\BCMA` à un **autre disque** que celui du projet ; le chemin du script est
relatif à la racine de l'académie.)
✅ `archive vérifiée : …\PROJECTS_AAAA-MM-JJ_HHMMSS.zip`.
Ajoutez une copie hors site (cloud ou disque gardé ailleurs) une fois par semaine.
`--dry-run` liste ce qui serait sauvegardé sans rien écrire.

## Tutoriel 5 — Planifier la sauvegarde (Windows)
1. Menu Démarrer → *Planificateur de tâches* → *Créer une tâche de base…*
2. Déclencheur : quotidien, 20 h. Action : *Démarrer un programme* :
   - Programme : `C:\Python314\python.exe` (votre Python, cf. rapport système)
   - Arguments : `"G:\…\SCRIPTS\bcma_backup.py" --source "G:\…\PROJECTS" --dest "F:\Backups\BCMA" --keep 14`
3. Testez avec *Exécuter* et vérifiez la présence de l'archive.

## Tutoriel 6 — Exporter et réimporter (formats)
1. Scène par défaut, sélectionnez le cube. *File → Export → glTF 2.0* →
   `PROJECTS\essai_export.glb` (cochez *Selected Objects* dans *Include*).
2. *File → New → General*, supprimez le cube, *File → Import → glTF 2.0* → le `.glb`.
   ✅ Le cube revient, avec son matériau.
3. Recommencez avec **USD** (*File → Export → Universal Scene Description*) et **OBJ** ;
   comparez la taille des fichiers et ce qui est conservé.
