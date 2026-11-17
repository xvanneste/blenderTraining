# CH06.02 — Dépannage

| Symptôme | Cause | Solution |
|---|---|---|
| Les yeux ne bougent pas | Pas de Target ou contrainte invalide (rouge) | Choisir EMP_Target |
| Les yeux visent de côté | Track Axis faux | Y (direction du bone) |
| La tête dépasse la limite | Limite avant le suivi | Placer la limite en dessous |
| La limite ne fait rien | Mauvais espace ou axe | Limit Z, Owner Space Local |
| La tête suit entièrement | Influence 1 | 0,5 |
| Cible introuvable | Doublon de nom (EMP_Target.001) | Vérifier le nom exact |
| Contrainte impossible à ajouter | Edit Mode | Pose Mode |
| Rig qui tremble | Cible sur le bone lui-même | Cible externe |
