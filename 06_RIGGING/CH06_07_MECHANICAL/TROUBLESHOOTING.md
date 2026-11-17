# CH06.07 — Dépannage

| Symptôme | Cause | Solution |
|---|---|---|
| La roue ne tourne pas | Rotation Mode en Quaternion ou driver en erreur | Rotation Mode XYZ Euler ; corriger l'expression |
| Driver en rouge/violet | Variable invalide | Objet, bone et espace de la variable |
| La roue vrille | Mauvais axe | Rotation Y (axe du bone) |
| La roue glisse | Rayon faux | d / rayon |
| Les roues restent sur place | Non enfants de root | Parent = root |
| Le vérin ne suit pas | Pas de Damped Track | Contrainte et cible |
| La benne traverse le châssis | Pas de limite | Limit Rotation X |
| Contrainte sans effet | Influence 0 ou cible vide | Vérifier Target et Bone |
