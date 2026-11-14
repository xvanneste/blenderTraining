# CH01.06 — Dépannage

| Symptôme | Cause | Solution |
|---|---|---|
| « Cannot apply to a multi user » | Données partagées (`Alt+D`) | Rendre unique d'abord, ou utiliser l'option proposée par Blender |
| Après *Apply Scale*, l'objet change de taille | Il avait un parent avec une échelle, ou on a appliqué sur le mauvais objet | `Ctrl+Z` ; vérifier la hiérarchie (CH01.08) |
| L'objet s'aimante partout, déplacements saccadés | Snapping resté actif | `Shift+Tab` |
| Le snapping vise la mauvaise surface | mauvais *Snap Target*, ou *Snap Base* = Center | Régler *Snap Target* / *Snap Base* ; contraindre l'axe |
| L'objet se colle mais traverse la surface | *Snap Base = Center* : c'est le centre qui se colle | *Snap Base = Closest* |
| `G X X` ne prend pas l'axe local | L'orientation courante est déjà *Local* (la 2ᵉ pression donne alors Global) | Regarder l'en-tête (« along local X ») ; menu `,` → Global |
| Bevel irrégulier | Échelle non appliquée | `Ctrl+A` → Scale |
