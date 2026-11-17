# CH05.08 — Dépannage

| Symptôme | Cause | Solution |
|---|---|---|
| Bâtiment enterré à moitié | Pas de translation hauteur ÷ 2 | Transform z = hauteur ÷ 2 |
| Fenêtres invisibles | y = 0 | y = −Depth ÷ 2 |
| Fenêtres aux bords des travées | Vertices X = Bays + 1 | Vertices X = Bays, Size X = (Bays − 1) × Bay Width |
| Nombre de fenêtres inchangé | Grid en dur | Brancher Bays et Floors |
| Hauteur inchangée | Constante dans le corps | Floors × Floor Height |
| Façade de travers | Rotation oubliée | Rotation X 90° |
| Fenêtres sous le sol | Translation z manquante | Size Y ÷ 2 + 0,55 × Floor Height |
| Bâtiment hors cadre | Caméra trop proche | Reculer |
