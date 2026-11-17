# CH03.05 — Dépannage

| Symptôme | Cause | Solution |
|---|---|---|
| Boolean *Exact* : le buste disparaît (0 sommet) | Cas où le solveur Exact échoue (mesuré ici sur un maillage pourtant fermé) | Essayez le solveur **Manifold**, ou Float ; vérifiez le nombre de sommets avant d'appliquer ; gardez une copie |
| Le buste est décalé de plusieurs cm après Join | Le Join garde l'origine du premier objet sélectionné actif | Objet > Set Origin > Origin to 3D Cursor (curseur en 0,0,0), ou appliquez la transformation |
| « Hauteur de tête » hors plage | Buste pas à l'échelle réelle | Menton → couronne ≈ 23 cm : mesurez avec la règle du guide `GP_Guide` |
| « Yeux à mi-hauteur » refusé | Yeux au tiers supérieur (erreur classique) | Descendez les yeux : ligne rouge du guide à 50 % |
| Yeux « introuvables » | Objets pas nommés `EYE_L` / `EYE_R` | Renommez les deux sphères exactement ainsi |
| Yeux « non symétriques » | Écart latéral ou hauteur > 3 mm | Mêmes z ; x opposés (copiez avec Mirror) |
| Nez en saillie insuffisante | Nez trop plat | Clay Strips (C) sur le plan du nez, Inflate/Deflate (I) ; Pinch (P) pour l'arête |
| Symétrie < 90 % | Tête décalée ou rotation | Mirror X actif ; Object > Apply > Rotation & Scale ; recentrez sur x = 0 |
| « Plis secondaires » refusés | Plis trop peu profonds (< 0,5 mm sous la surface lissée) ou maillage trop lâche | Draw Sharp / Crease Sharp plus appuyés ; ou densifiez (Voxel 2–3 mm) |
| « Grain » refusé | Surface lisse | Multires > Subdivide, Sculpt Level supérieur, brosse fine ; ou Voxel Size plus petit |
| Le grain « bave » hors du visage | Bruit appliqué en zone nette | Atténuez progressivement sur les bords (c'est ce que fait la solution) |
| Plis détruits en retouchant la forme | Mauvais ordre de travail | Primaire → secondaire → tertiaire ; copie avant chaque palier |
| Lissage qui rétrécit la tête | Smooth trop fort, trop de passes | Force faible, raccords seulement ; Shift+clic = Smooth temporaire |
| Fichier énorme / lent | Densité excessive | Gardez le niveau Multires bas pour la forme, le haut pour le grain seulement |
| Brosse « Crease » introuvable | Elle ne s'appelle pas ainsi en 5.3 | Crease Sharp ou Crease Polish (Shift+C) dans le shelf de brosses |
| Socle étroit refusé (< 200 cm²) | Coupe au bas d'un ellipsoïde arrondi | Coupez là où la poitrine est déjà large |
