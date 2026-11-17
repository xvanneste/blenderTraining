# CH06.11 — Dépannage

| Symptôme | Cause | Solution |
|---|---|---|
| Le tube ne se courbe pas | Segments = 1, modificateur absent, use_deform décoché | Segments ≥ 6 ; modificateur Armature ; Deform |
| La courbe est anguleuse | Peu de segments | Augmenter Segments |
| Le rig lié ne bouge pas | Lien nu (non éditable) | Library Override > Make |
| Pose perdue à la réouverture | Pas d'Action | Keyframe de la pose |
| Bibliothèque introuvable | Chemin absolu ou dossier déplacé | Chemin relatif ; File > External Data > Make Paths Relative ; déplacer les deux fichiers ensemble |
| Overrides « système » | Création non éditable | Make > Selected & Content |
| Copie locale au lieu d'un lien | Append | Utiliser Link |
| La bibliothèque a été modifiée par erreur | Ouverte et enregistrée | La restaurer ; ne la modifier que dans son propre fichier |
