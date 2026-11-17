# Fiche de révision — CH03.05 Sculpture réaliste

Tête adulte ≈ 23 cm (menton → couronne) · largeur/hauteur ≈ 0,6–0,75 · **yeux à mi-hauteur** · écart des
yeux ≈ 6,4 cm · pointe du nez au 1ᵉʳ tiers depuis le menton, saillie ≈ 3 cm · trois tiers du visage égaux.
Ordre : **primaire** (masses, plans) → **secondaire** (plis, sillons, poches) → **tertiaire** (rides fines, pores).
Transitions : Smooth (S ; Shift+clic temporaire) sur les raccords, pas sur les masses.
Brosses 5.3 : Clay Strips C · Smooth S · Scrape/Fill Shift+T · Pinch/Magnify P · Inflate/Deflate I · Crease Polish
Shift+C · Draw Sharp et Crease Sharp (shelf). Ctrl = inverser. Voxel Remesh Ctrl+R, taille du voxel R.
Densité = finesse : 2,5 mm → plis, pas pores ; Multires/Voxel plus fin pour le grain, **copie avant**.
Yeux : sphères `EYE_L` / `EYE_R` ≈ 2,5 cm dans des orbites (Boolean Difference ; si Exact donne vide → Manifold).
Correcteur : `--exercise bust --render [--debug]`.
