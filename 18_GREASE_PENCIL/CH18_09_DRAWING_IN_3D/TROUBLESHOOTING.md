# CH18.09 — Dépannage

| Symptôme | Cause | Solution |
|---|---|---|
| Le trait atterrit à la mauvaise distance | Stroke Placement sur Origin, curseur ignoré | Stroke Placement : 3D Cursor ; vérifier la position du curseur (`N` → View) |
| La route est « debout » au lieu d'être au sol | Drawing Plane resté sur View/Front | Drawing Plane : Top (X-Y), curseur à Z = 0 |
| Le dessin du fond paraît minuscule | Dessiné trop petit pour sa distance | Dessiner plus grand ; vérifier en vue caméra |
| Un trait de premier plan couvre tout l'écran | Trop près de la caméra | Reculer le curseur (Y ≈ −5 pour une caméra à −12) ou dessiner plus petit |
| Le sol (mesh) cache la route dessinée | Route exactement à Z = 0 | Curseur à Z = 0,02 ou Stroke Placement Surface avec Offset |
| Rendu : décor devant la 3D | Passe Z désactivée | View Layer → Passes → Data → Z |
| Couleurs ternes ou sombres | Calques éclairés par le soleil | Décocher *Lights* des calques |
| Grille du Canvas invisible | Overlay désactivé | Viewport Overlays → Canvas → Use Grid |
| L'image de référence a disparu à l'ouverture | Image non empaquetée, chemin cassé | File → External Data → Pack Resources ; ou relocaliser |
| Lecture saccadée | Remplissages et effets lourds | Render → Simplify → Grease Pencil → Playback Only |
