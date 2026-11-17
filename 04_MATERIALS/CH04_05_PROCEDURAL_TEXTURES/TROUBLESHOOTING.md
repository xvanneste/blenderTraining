# CH04.05 — Dépannage

| Symptôme | Cause | Solution |
|---|---|---|
| Briques étirées | Échelle d'objet non uniforme | Appliquer l'échelle (Ctrl+A) ou construire à la taille réelle |
| Mur uniforme | Brick non reliée à Base Color | Color → Base Color |
| Joints alignés | Offset 0 | 0,5 |
| Joints plats | Bump non alimenté | Fac → Height ; Bump → Normal |
| Joints saillants | Le masque de mortier est utilisé comme hauteur directe | Activer Invert sur le nœud Bump |
| Moirage | Scale trop grand | 3–12 |
| Briques toutes identiques | Color1 = Color2 | Deux couleurs voisines |
| Motif de côté en traînées | Coordonnées Object projetées | Normal pour un mur plat ; Box Mapping en CH04.08 |
| Rendu très clair | Couleurs trop claires | Albedo de briques 0,1–0,4 |
