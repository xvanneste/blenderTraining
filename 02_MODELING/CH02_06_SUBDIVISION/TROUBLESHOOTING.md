# CH02.06 — Dépannage

| Symptôme | Cause | Solution |
|---|---|---|
| Tout devient une boule | Cage sans boucles de maintien | Loop Cuts près des arêtes, ou crease |
| Bosse ou pincement après subdivision | Triangle, n-gon, ou pôle mal placé | Repasser la cage en quads (CH02.01) |
| Le crease ne fait rien | *Use Creases* décoché dans le modificateur | Cocher Use Creases |
| Arête trop vive (non réaliste) | Crease = 1 | 0,7–0,9, ou boucles de maintien |
| Viewport très lent | Levels trop élevés | Levels Viewport 0–1 ; Simplify → Max Subdivision |
| Le cube flotte au-dessus du sol après subdivision | La subdivision rétrécit la forme | Normal sans boucles ; boucles près du bas |
| Loop Cut dans le mauvais sens | Arête survolée parallèle à la coupe voulue | Survoler une arête perpendiculaire à la coupe |
| Après Apply, impossible de revenir | Modificateur appliqué | `Ctrl+Z` ; ne pas appliquer (travailler sur la cage) |
