# CH02.07 — Dépannage

| Symptôme | Cause | Solution |
|---|---|---|
| Trou incomplet ou faces parasites | Cutter qui affleure une face (coplanaire) | Faire dépasser le cutter ; Solver Exact |
| Rien ne se passe | Cutter hors de la pièce, ou mauvaise collection | Vérifier positions et *Collection : CUTTERS* |
| Les cutters apparaissent au rendu | *Renders* encore coché | Visibility → Show In → Renders décoché |
| La pièce disparaît entièrement | Operation Intersect, ou cutter englobant | Difference ; cutter plus petit que la pièce |
| Bords des trous vifs | Bevel au-dessus du Boolean | Glisser le Bevel sous le Boolean |
| Bosses après subdivision | Topologie booléenne (n-gons, triangles) | Ne pas subdiviser après un booléen ; retopologiser (CH02.09) |
| Solver Manifold échoue | Cutter ou pièce non manifold | Réparer (CH02.01) ou repasser en Exact |
| Viewport lent avec beaucoup de cutters | Solver Exact coûteux | Display As Bounds ; Manifold si possible ; désactiver le Boolean au viewport pendant le travail |
