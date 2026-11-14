# CH18.01 — Dépannage

| Symptôme | Cause | Solution |
|---|---|---|
| Rien ne se dessine | Pas en Draw Mode, ou objet GP non actif | Sélectionner GP_Practice, `Ctrl+Tab` → Draw Mode |
| Le trait apparaît ailleurs (en profondeur) | Placement des traits (*Stroke Placement*) sur une surface ou le curseur loin | En-tête : *Placement* → **Origin**, *Drawing Plane* → **Front (X-Z)** ; vue caméra `Num 0` |
| « Layer is locked » | Le calque actif est GUIDE | Activer un calque USER_ |
| Le trait est tremblé | Stabilisation faible, geste du poignet | Geste d'épaule ; *Stroke → Stabilize Stroke* (options de la brosse) ; `Shift`+glisser pour lisser |
| Trait trop épais/fin | Rayon de la brosse | `[` / `]` ou `F` |
| Pas de variation d'épaisseur | Souris, ou pression désactivée | Tablette + icône de pression (CH00.04) |
| La forme n'est pas remplie | Matériau sans *Fill*, ou contour non fermé | `U` → MAT_GP_Light/Shadow ; fermer le contour ; outil *Fill* |
| Le correcteur trouve 0 trait | Dessin fait sur le mauvais calque | Vérifier le calque actif avant de dessiner ; déplacer des traits : Edit Mode, *Move to Layer* (`M`) |
