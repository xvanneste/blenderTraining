# CH18.06 — Dépannage

| Symptôme | Cause | Solution |
|---|---|---|
| Au rendu F12, le dessin passe devant les objets qui devraient le cacher | Passe Z désactivée (comportement constaté en 5.2/5.3) | Properties → View Layer → Passes → Data → **Z** |
| Rien ne se dessine | Pas en Draw Mode, ou calque actif verrouillé/masqué | `Ctrl+Tab` → Draw Mode ; vérifier cadenas et œil du calque actif |
| Le trait apparaît loin ou de travers | Drawing Plane ≠ View, ou origine de l'objet ailleurs | En-tête : Drawing Plane = View ; vérifier l'origine de l'objet |
| Le dessin est à la mauvaise profondeur | Objet créé au curseur 3D mal placé | Object Mode, `G` `Y` + valeur ; ou Stroke Placement : 3D Cursor |
| Le nouvel objet n'est pas dans DRAWINGS | Une autre collection était active à la création | `M` → DRAWINGS ; cliquer la collection avant Add |
| Impossible de glisser un calque dans le groupe | Glissé hors de la ligne du groupe | Déposer le calque **sur** la ligne du groupe (surbrillance) |
| Le dessin disparaît en vue caméra | Hors du cadre ou derrière la caméra | `Num 0`, réduire la distance, vérifier Y |
| `Ctrl+Tab` ouvre un autre menu | Objet actif non GP | Cliquer d'abord l'objet GP dans l'Outliner |
