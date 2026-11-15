# CH02.13 — Dépannage

| Symptôme | Cause | Solution |
|---|---|---|
| Catalogues perdus à la réouverture | Fichier non enregistré, ou `blender_assets.cats.txt` non copié avec le .blend | Enregistrer ; copier le .cats.txt avec la bibliothèque |
| L'asset n'apparaît pas dans un autre fichier | Bibliothèque non déclarée | Preferences → Asset Libraries → + |
| L'asset glissé est vide ou mal placé | Origine éloignée de la géométrie | Origine au sol avant de marquer |
| Impossible de modifier un asset lié | Normal (Link) | Modifier le fichier source ; ou Append ; ou Library Override |
| Matériaux dupliqués (.001) | Plusieurs Append | Append (Reuse Data) |
| Aperçu noir | Objet hors du cadre de l'aperçu ou très petit | Generate Preview à nouveau ; aperçu personnalisé |
| Le correcteur ne trouve pas les catalogues | Fichier vérifié dans un autre dossier que son .cats.txt | Vérifier le fichier dans son propre dossier |
