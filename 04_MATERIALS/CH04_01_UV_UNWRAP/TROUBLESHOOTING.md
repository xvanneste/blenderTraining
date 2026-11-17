# CH04.01 — Dépannage

| Symptôme | Cause | Solution |
|---|---|---|
| Damier étiré en bandes | Surface dépliée sans seams adaptés, ou projection plane | Marquer les seams sur les arêtes vives, refaire Unwrap |
| « Étirement » refusé après Unwrap | Trop peu de seams (grande surface fermée) | Ajouter des seams ; essayer Conformal ou Minimum Stretch |
| Îlots superposés | Pas de packing | UV > Pack Islands |
| Carrés de tailles différentes | Échelles d'îlots inégales | UV > Average Islands Scale (avant le packing) |
| UV hors du carré | Échelle excessive | Pack Islands, ou mettre à l'échelle (S) autour de l'origine |
| Occupation < 50 % | Îlots trop petits après packing | Pack Islands avec marge plus petite ; réduire le nombre d'îlots |
| Un îlot « bave » sur le voisin | Marge trop faible | Margin ≈ 0,02 |
| « Seams » refusé | Aucune arête marquée | Edge > Mark Seam (Ctrl+E) |
| Le damier disparaît dans la vue | Mode d'affichage Solid | Passer en Material Preview |
| Unwrap n'agit pas | Rien de sélectionné | A dans l'éditeur UV / Edit Mode, avec Sync désactivé ou faces visibles |
