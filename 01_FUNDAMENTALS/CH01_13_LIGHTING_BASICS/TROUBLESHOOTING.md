# CH01.13 — Dépannage

| Symptôme | Cause | Solution |
|---|---|---|
| Rien ne change en ajoutant une lumière | Mode Solid | `Z` → Rendered |
| L'Area n'éclaire pas le sujet | Elle regarde ailleurs (une Area n'éclaire que devant elle, vers son −Z local) | Contrainte Track To ou rotation vers le sujet |
| Image toute blanche | Puissance trop forte, lumière trop proche (inverse du carré) | Baisser la puissance ou éloigner |
| Ombres très dures et crénelées | Source minuscule (Radius/Size ~0) | Agrandir la source |
| Couleur de lumière ignorée | *Temperature* cochée : la couleur devient une teinte (Tint) | Régler la température, ou décocher |
| La rim n'apparaît pas | Mal placée (pas assez derrière/au-dessus) ou cône du spot trop étroit | Monter et reculer, élargir *Spot Size* |
| Un disque lumineux apparaît dans l'image | La source (Area/Spot) est visible par la caméra | *Object → Visibility → Ray Visibility → Camera* décoché (CH00.01) |
