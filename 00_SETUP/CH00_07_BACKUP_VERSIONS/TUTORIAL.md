# CH00.07 — Tutoriels pas à pas

## Tutoriel 1 — Versions incrémentales
1. *File → New → General*, enregistrez sous `PROJECTS\essai_versions_v001.blend`.
2. Déplacez le cube, `Ctrl+Alt+S`.
   ✅ Le titre de la fenêtre affiche `essai_versions_v002.blend`. Les deux fichiers existent.
3. Encore une modification, `Ctrl+Alt+S` → `v003`.

## Tutoriel 2 — Lire une sauvegarde de secours

1. Créez une scène d’essai, enregistrez v001, puis déplacez le cube. Dans les préférences **Save & Load → Blend Files**, repérez si Auto-Save est activé et notez son délai.
2. Laissez cette scène ouverte sans lancer de rendu. Après le délai, ouvrez **File → Recover → Auto Save**. Choisissez le fichier récent de l’exercice. Ne forcez pas la fermeture d’une session de travail pour provoquer une panne.
3. Vérifiez la position du cube. Si le fichier est plus ancien, l’intervalle ou une action en cours a retardé l’écriture. Enregistrez la scène relue dans un nouveau .blend v002.
4. **Comparer les mécanismes**. Le .blend1 est une ancienne version du fichier lorsqu’elle a été conservée par Save Versions. Auto Save est une copie de secours périodique. Last Session correspond à la dernière session enregistrée à la fermeture normale.

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
  --python-exit-code 1 --python "SCRIPTS\validate_ch00_07.py" -- --exercise recover
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
1. Dans la scène par défaut, donnez au cube trois dimensions différentes et un matériau nommé. Sélectionnez-le. *File → Export → glTF 2.0* →
   `PROJECTS\essai_export.glb` (cochez *Selected Objects* dans *Include*).
2. *File → New → General*, supprimez le cube, *File → Import → glTF 2.0* → le `.glb`.
   ✅ Comparez les dimensions et le matériau. En mode Solid, réglez le type de couleur sur Material ou utilisez Material Preview pour juger la couleur.
3. Recommencez avec **USD** (*File → Export → Universal Scene Description*) et **OBJ** ;
   comparez la taille, les dimensions et les données conservées. La portabilité d’une scène se vérifie dans le logiciel destinataire.

## Contrôles du cas d’échange 5.3

Le [script d’aller-retour](SCRIPTS/verifier_echanges.py) exporte une boîte de 0,8 × 1,2 × 1,8 m et la réimporte dans une scène vide. Il compare les dimensions dans le repère monde. Une rotation locale à l’import peut permuter les axes du maillage local tout en restituant correctement la boîte dans la scène.

| Format | Preuve exécutée dans Blender 5.3 |
|---|---|
| GLB, USD et FBX | Dimensions monde et nom du matériau conservés sur cette boîte. |
| OBJ | Même contrôle avec le MTL à côté de l’OBJ. |
| Alembic | Dimensions monde conservées sur une image. Gardez le fichier de cache disponible si Blender le référence. |

Ces essais portent sur une boîte statique. Pour un transfert de personnage ou de plan, contrôlez aussi animation, unités, axes, textures et lecture dans l’application destinataire. [Exemple de personnage GLB animé](../../02_MODELING/PARCOURS_PRATIQUE/projet-humain.md)
