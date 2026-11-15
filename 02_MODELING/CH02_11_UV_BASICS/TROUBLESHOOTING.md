# CH02.11 — Dépannage

| Symptôme | Cause | Solution |
|---|---|---|
| Objet d'une seule couleur avec la texture | Pas de carte UV | Edit Mode, `A`, `U` → Unwrap / Smart UV Project |
| Damier étiré | Coutures insuffisantes ou mal placées | Ajouter des coutures ; Unwrap Conformal/Minimum Stretch |
| Damier de tailles différentes | Densité de texels incohérente | Average Islands Scale, puis Pack Islands |
| Deux zones montrent le même motif | Îles superposées | Re-déplier ; Pack Islands |
| UV hors du carré 0–1 | Projection mise à l'échelle | Pack Islands |
| Unwrap donne des îles bizarres | Échelle d'objet non appliquée | `Ctrl+A` → Scale, puis Unwrap |
| Couture visible face caméra | Couture mal placée | La déplacer à l'arrière ou dans un angle |
| L'UV Editor est vide | Rien de sélectionné en 3D | `A` en Edit Mode, ou synchronisation de sélection |
