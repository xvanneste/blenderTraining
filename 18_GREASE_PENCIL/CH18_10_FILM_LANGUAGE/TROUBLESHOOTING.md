# CH18.10 — Dépannage

| Symptôme | Cause | Solution |
|---|---|---|
| Le correcteur dit « ? » pour une caméra | Cadrage entre deux valeurs, ou personnage hors cadre | Lire la hauteur de coupe affichée ; ajuster la caméra |
| PM refusé alors que A est entier | A trop petit (< 55 %) ou tête coupée | Rapprocher la caméra ; vérifier la tête |
| Naviguer ne déplace pas la caméra | Camera to View non activé | `N` → View → View Lock → Camera to View |
| La vue n'est pas celle de ma caméra | Autre caméra active | `Ctrl+Num 0` sur la caméra sélectionnée |
| Très gros plan : caméra « dans » la tête | Clip Start trop grand ou caméra trop proche | Camera → Clip Start 0,01 ; reculer légèrement |
| 180° refusé | Une caméra de l'autre côté de la ligne A–B | Placer les deux caméras du même côté (ici y < 0) |
| Planche refusée | Dessin trop petit ou dans un seul cadre | Remplir les 8 cadres |
