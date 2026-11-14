# Fiche de révision — CH00.08 Pipeline

Préproduction (scénario, design, storyboard, animatique, listes) → Production (assets :
modélisation → surfaçage → rigging ; plans : layout → animation → FX → lighting → rendu) →
Postproduction (compositing, montage, son, étalonnage, livraison).

- Plus tôt = moins cher. Animatique avant toute 3D.
- Asset = réutilisé (lié). Plan = unique (`sqNNN_shNNNN`).
- 24 i/s : 1 s = 24 images ; 2 s = 48 ; 3 s = 72.
- Valeurs : EWS · WS · FS · MS · MCU · CU · ECU · OTS · POV · INSERT.
- Shot list : `sequence;shot;duration_frames;shot_size;camera_move;description;characters;assets;status`
- Vérifier : `python SCRIPTS/bcma_shotlist_check.py fichier.csv --target-seconds 30`
