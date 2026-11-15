# CH02.08 — Dépannage

| Symptôme | Cause | Solution |
|---|---|---|
| Le Skin ne produit rien | Le maillage contient des faces, ou aucun arête | Squelette d'arêtes uniquement (E sur des sommets) |
| Volumes bizarres, torsions | Sommets superposés, arêtes en double | `M` → By Distance |
| `Ctrl+A` ouvre le menu Apply | Object Mode | Passer en Edit Mode (`Tab`) : Ctrl+A = Skin Resize |
| Embranchement « boursouflé » | Rayons trop grands au nœud | Réduire le rayon du sommet de jonction ; Branch Smoothing |
| Forme carrée | Pas de Subdivision, ou au-dessus du Skin | Skin puis Subdivision Surface |
| Branche plate | Rayon X ≠ Y involontaire | `Ctrl+A` puis contrainte, ou Skin Radii Equalize (`F3`) |
| Objet trop lourd | Subdivision Levels trop haut | Levels 1, Render 2 |
