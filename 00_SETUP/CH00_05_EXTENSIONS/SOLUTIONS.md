# CH00.05 — Solutions

<!-- QUIZ_ANSWERS_START -->
## Réponses du quiz

| Q | Réponse | Explication |
|---|---|---|
| Q1 | **b** — blender_manifest.toml | Le manifeste TOML décrit identité, version, licence, permissions. |
| Q2 | **b** — Node Wrangler | Node Wrangler. |
| Q3 | — | extensions.blender.org |
| Q4 | — | Ces formats sont intégrés au cœur (C++) de Blender. |
| Q5 | **b** — Non, il faut autoriser l'accès en ligne | Allow Online Access doit être accepté (ou --online-mode). |
| Q6 | — | Source/auteur, licence, permissions déclarées, compatibilité de version, contenu du paquet (code). |
| Q7 | — | Preferences > Get Extensions (ou Add-ons) > menu ˅ > Install from Disk, ou glisser-déposer le .zip dans Blender. |
| Q8 | — | Un .blend peut contenir du code (drivers, scripts) ; il ne doit s'exécuter que si le fichier est de confiance. |
| Q9 | — | blender -c extension validate <dossier> |
| Q10 | **b** — Compatible GPL | Compatible GPL (ex. GPL-3.0-or-later). |
<!-- QUIZ_ANSWERS_END -->

## Leçon 1
- **Moyen :** *Add-ons* → recherche « BVH » → *Import-Export: BioVision Motion Capture (BVH)* ;
  servira en phase 7 (motion capture).
- **Difficile :** OBJ, USD, Alembic, STL, PLY sont implémentés en C++ dans le cœur de
  Blender : toujours disponibles dans *File → Import/Export*, sans add-on à activer.

## Exercice 3 — procédure type
1. Sauvegarder `%APPDATA%\Blender Foundation\Blender\5.3` (zip).
2. Lancer `blender --factory-startup` : si Blender démarre, le problème vient de la configuration.
3. Lancer `blender -b --python bcma_extensions_report.py` pour lister ce qui est activé
   (ou lire `config\userpref.blend` via l'interface si elle démarre).
4. Démarrer normalement ; si l'interface s'ouvre, désactiver les extensions récentes une par
   une (*Get Extensions → Installed*), redémarrer après chacune.
5. Si l'interface ne s'ouvre pas : déplacer temporairement le dossier
   `%APPDATA%\Blender Foundation\Blender\5.3\extensions\user_default\<id_extension>` hors du
   dossier, relancer.
6. Signaler le problème au développeur (version de Blender, de l'extension, message d'erreur
   de la console).

## Défi 1 (piste)
Ajouter une classe `BCMA_OT_unprefix_names` qui retire `PREFIX[ob.type]` en tête du nom, la
déclarer dans `CLASSES` et ajouter `col.operator(...)` dans le panneau.
