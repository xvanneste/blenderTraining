# CH06.04 — Dépannage

| Symptôme | Cause | Solution |
|---|---|---|
| Le bras reste droit | Chaîne parfaitement droite (singularité) | Pré-fléchir de quelques degrés |
| Le coude plie du mauvais côté | Pole Angle | Essayer 0, 90, −90, 180 |
| Le coude tourne autour de l'axe | Pas de pôle | Ajouter le Pole Target |
| Le bras s'étire | ik_stretch > 0 | 0 |
| Le bout n'atteint pas la cible | Chain Length trop court | 2 |
| Impossible de revenir en FK | Pas de driver | Driver sur l'influence |
| Le driver n'agit pas | Chemin de propriété faux | `pose.bones["switch"]["ik_fk"]` |
| Le bone cible se déforme | Cible dans la chaîne | Contrôleurs hors de la chaîne |
