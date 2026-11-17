# CH04.06 — Dépannage

| Symptôme | Cause | Solution |
|---|---|---|
| La peinture a disparu à la réouverture | Image non empaquetée | Image > Pack, puis enregistrer |
| Rien ne se peint | Pas en Texture Paint, ou image absente du matériau | Mode Texture Paint ; vérifier T_Can sur Base Color |
| Peinture à deux endroits | UV qui se chevauchent | Refaire les UV (CH04.01) |
| Traits étirés près du bord | Vue rasante | Tourner la vue ; rester à ≤ 53° de la normale |
| Couleur plus claire que prévue | Couleur saisie en linéaire (script) | Convertir sRGB → linéaire |
| « Peinture hors des îlots » | Peinture dans le vide de l'image | Peindre sur l'objet |
| Bavure sur l'îlot voisin | Marge UV trop petite | Augmenter la marge au packing |
| Une seule couleur détectée | Une famille < 5 % des pixels peints | Peindre assez de la seconde couleur |
