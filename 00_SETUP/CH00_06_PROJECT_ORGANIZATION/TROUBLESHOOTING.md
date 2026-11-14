# CH00.06 — Dépannage

| Symptôme | Cause | Solution |
|---|---|---|
| Texture rose/magenta | Fichier image introuvable | *File → External Data → Find Missing Files* ; puis *Make Paths Relative* |
| *Make Paths Relative* sans effet | Fichier jamais enregistré (pas de dossier de référence) ou image sur un autre disque que le `.blend` | Enregistrer d'abord ; garder images et `.blend` sur le même disque |
| Le renommage ajoute `.001` | Le nom existe déjà (dans ce fichier, même pour une donnée cachée ou orpheline) | Chercher le doublon dans l'Outliner (mode *Blender File*) ; purger les orphelins |
| Le dossier `.blender_project` est invisible | Dossier caché (commence par un point) | Explorateur : afficher les éléments masqués |
| Le menu *Project* n'apparaît pas | Aucun projet ouvert | *File → Project → Open…* ou *New…* |
| Le correcteur signale « fichier » | Nom de fichier non conforme | minuscules, sans espace, `_v001.blend` |
| `bcma_create_project.py` refuse le nom | Majuscules, espaces ou tirets | minuscules, chiffres, `_` |
