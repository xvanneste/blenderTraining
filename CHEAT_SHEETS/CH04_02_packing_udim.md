# Fiche de révision — CH04.02 UDIM

Tuile = 1001 + ⌊u⌋ + 10·⌊v⌋ (1001, 1002… 1010, puis 1011). Un carré UV [0,1]² par tuile, une image par tuile (Image Texture > Source : UDIM Tiles ; API : TILED).
Workflow : groupes → Pack Islands par groupe → déplacer le groupe d'un bloc (G, X, 1) → image avec toutes les tuiles utilisées.
Pièges : îlot à cheval sur une frontière ; tuile absente de l'image ; chevauchement.
Mesures solution : tuiles 1001 (76 %) et 1002 (74 %), densité couvercle ≈ 1,5× corps. Correcteur : `--exercise udim [--debug]`.
