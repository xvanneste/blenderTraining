# CH05.02 — Dépannage

| Symptôme | Cause | Solution |
|---|---|---|
| Fût à moitié sous le sol | Primitive centrée, pas de Transform | Translation z = 1,5 |
| Une seule pièce visible | Join non branché | Relier chaque Transform à Join |
| Anneau absent | Profile Curve non relié | Petit cercle → Profile Curve |
| Colonne décentrée | Translation X/Y non nulle | Remettre 0 |
| Surface noire/blanche | Set Material manquant | Ajouter Set Material |
| Facettes | Set Shade Smooth manquant | L'ajouter |
| Chevauchements | Pièces non soudées | Normal ; Merge by Distance si besoin |
| Arbre illisible | Nœuds en désordre | Frames, alignement, noms |
