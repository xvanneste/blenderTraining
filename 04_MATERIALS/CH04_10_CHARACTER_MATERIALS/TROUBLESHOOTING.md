# CH04.10 — Dépannage

| Symptôme | Cause | Solution |
|---|---|---|
| Peau en plastique | Subsurface Weight 0 | 1 ; Radius (1 ; 0,2 ; 0,1) |
| Peau grise | Rayon uniforme | Rayon R > V > B |
| Peau aveuglante | Scale trop grand | 0,05 pour un objet d'1 m |
| Œil mort | Coat 0 | Coat Weight 1, Roughness 0,02 |
| Iris décentré | Mapping / orientation de l'œil | Tourner Mapping ou l'objet |
| Cheveux plastiques | Principled BSDF | Principled Hair BSDF |
| Bruit au rendu | Peu d'échantillons | Augmenter ; débruitage |
| Tissu en papier | Sheen 0 | Sheen Weight ≥ 0,3 |
