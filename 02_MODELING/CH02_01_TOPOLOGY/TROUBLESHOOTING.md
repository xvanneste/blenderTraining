# CH02.01 — Dépannage

| Symptôme | Cause | Solution |
|---|---|---|
| *Grid Fill* refuse (« Select two edge loops » ou erreur) | Contour non entièrement sélectionné, ou nombre de sommets impair | `Alt+clic` sur la boucle complète ; un contour à nombre pair de sommets se remplit mieux |
| *Triangles to Quads* laisse des triangles | Triangles sans voisin compatible (pôles) ou angles au-delà des seuils | Normal aux pôles ; sinon augmenter *Max Face Angle* / *Max Shape Angle* dans le panneau de l'opération |
| *By Distance* ne fusionne rien | Distance de fusion trop petite ou rien de sélectionné | `A` d'abord ; augmenter *Merge Distance* dans le panneau de l'opération |
| Ombrage taché après réparation | Normales incohérentes | `Shift+N` (Recalculate Outside) — détaillé en CH02.04 |
| *Non Manifold* ne sélectionne rien | Pas en mode sommet/arête | Passer en mode sommet (`1`) ou arête (`2`) |
| Le diagnostic des pôles est refusé | Valeur mal comptée, ou ligne modifiée | Gardez exactement `POLES = nombre` ; recomptez en fil de fer |
| Statistics n'apparaît pas | Overlay désactivé | Viewport Overlays → Statistics |
