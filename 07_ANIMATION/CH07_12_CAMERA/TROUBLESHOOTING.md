# CH07.12 — Dépannage

| Symptôme | Cause | Solution |
|---|---|---|
| Le sujet sort du cadre | Pas de suivi | Track To vers le sujet |
| La caméra démarre brusquement | Interpolation linéaire | Bezier |
| La caméra tremble trop | Strength trop fort | 0,1 |
| L'horizon penche | Damped Track ou roulis | Track To, Up Y |
| La caméra bouge en diagonale | Même phase de bruit | Phases différentes |
| Le travelling est saccadé | Noise sur Y | Supprimer le bruit sur Y |
| La visée est fausse | Axe de visée mal choisi | −Z, Up Y |
| Rien ne bouge en vue caméra | Caméra non active | Scène > Camera = CAM_Main |
