# Fiche de révision — CH03.09 Retopologie

Sculpt (75 000 faces) → maillage léger tout en **quads**, **boucles** concentriques autour des yeux et de la bouche (plus serrées), ouvertures aux yeux/bouche,
peu de **pôles** (valence ≠ 4), budget 300–2 500 faces.
Outils : **Poly Build** + Snap (Face Project), overlay **Retopology**, **Inset Faces**, **Loop Cut and Slide**, **Tris to Quads**, **Shrinkwrap** (Wrap Method Project,
Y, Positive, Offset 0,002 m) puis Apply.
Pièges : sommets non projetés → quads étirés ; `inset_region` renvoie l'anneau (le centre = les faces d'origine) ; paroi d'orbite inclinée.
Mesures de la solution : 404 faces, 100 % quads, 1,5 mm de l'écart moyen, 3/3 ouvertures, 70 % de densité, 96 % de valence 4.
Correcteur : `--exercise retopo [--debug]`.
