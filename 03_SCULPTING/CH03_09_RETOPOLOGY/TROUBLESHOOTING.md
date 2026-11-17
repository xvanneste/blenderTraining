# CH03.09 — Dépannage

| Symptôme | Cause | Solution |
|---|---|---|
| Quads énormes qui s'étirent sur le côté de la tête | Sommets qui ne touchent pas le sculpt (restés sur le plan de départ) | Supprimer les faces hors visage avant le Shrinkwrap ; vérifier l'axe/direction |
| Shrinkwrap n'a aucun effet | Mauvaise cible ou mauvais axe/direction | Wrap Method Project, Y coché, Positive coché (le visage regarde −Y), cible `SCULPT_Bust` |
| Maillage « dans » le sculpt (invisible par endroits) | Offset trop faible | Offset ≈ 0,002 m |
| « Trous aux bons endroits » refusé | Ouvertures absentes ou décalées | Supprimer les faces du centre des anneaux, aux yeux et à la bouche |
| Îlots de faces au milieu des yeux | On a supprimé l'anneau, pas le centre | Supprimer les faces d'origine de la région insétée |
| « Tout en quads » refusé | Triangles ou n-gones | Faces by Sides ≠ 4 ; Tris to Quads ; refaire proprement |
| Topologie irrégulière (valence) | Trop de pôles | Refaire les raccords autour des yeux/bouche |
| Normales retournées | Faces dans le mauvais sens | Mesh > Normals > Recalculate Outside |
| Trop de faces (> 2 500) | Subdivision | Retirer des subdivisions : une retopo doit rester légère |
| Densité non resserrée | Anneaux de même taille que la grille | Inset plus serré (≈ 3 mm) autour des yeux et de la bouche |
| Visage non couvert | Maillage trop petit | Couvrir front, nez, joues, bouche, menton |
