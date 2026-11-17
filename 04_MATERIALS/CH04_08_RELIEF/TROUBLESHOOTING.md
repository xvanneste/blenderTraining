# CH04.08 — Dépannage

| Symptôme | Cause | Solution |
|---|---|---|
| La silhouette reste plate | Méthode Bump Only | Settings > Displacement : Displacement Only / and Bump |
| Rien ne bouge | Plan non subdivisé | Subdivision Surface adaptative ou Render ≥ 6 |
| Relief énorme | Scale trop grand | 0,02–0,3 m ici |
| Relief uniforme | Height non reliée | Noise [Fac] → Height |
| Toute la surface monte | Midlevel 0 | 0,5 pour un Height centré sur 0,5 |
| Rien en EEVEE | Méthode non prise en charge | Cycles |
| Relief invisible au rendu | Soleil de face | Lumière rasante |
| Rendu très long | Subdivision trop forte | Adaptive Subdivision, edge length plus grande |
