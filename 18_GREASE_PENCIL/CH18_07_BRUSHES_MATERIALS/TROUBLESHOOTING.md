# CH18.07 — Dépannage

| Symptôme | Cause | Solution |
|---|---|---|
| L'outil Fill remplit tout l'écran | Forme non fermée (fuite) | `Ctrl+Z` ; fermer le trait, guide `Alt+glisser`, ou Gap Closure |
| L'outil Fill ne fait rien | Layer Mode exclut le calque des contours | Layer Mode : *Visible* (ou *Layer Above* si l'encrage est au-dessus) |
| Liseré blanc entre aplat et trait | Aplat calé exactement sur le bord | Dilate/Contract : 1–2 px ; Precision plus haute |
| L'aplat recouvre l'encrage | Calque de couleur au-dessus du calque d'encre | Faire glisser le calque COLOR sous LINE |
| Je ne trouve pas la case « Fill » du matériau | Elle n'existe plus en 5.3 | Le remplissage est choisi par trait : Stroke Mode *Fill/Both*, outil Fill, ou *Set Stroke Type* |
| Le trait est trop pâle | Strength faible ou calque à opacité basse | Strength = 1 ; opacité du calque |
| Pas de variation d'épaisseur | Pas de tablette, ou pression désactivée | Icône de pression à côté de Size ; à la souris, utiliser plusieurs pinceaux |
| Les couleurs sont plus sombres au rendu | Calque éclairé (*Use Lights*) sans lampe dans la scène | Décocher **Lights** sous la liste des calques (panneau Layers, à côté de Blend Mode et Opacity) ou éclairer la scène |
| Mauvaise couleur | Mauvais matériau actif | `U` avant de dessiner ; pipette (Eyedropper) |
