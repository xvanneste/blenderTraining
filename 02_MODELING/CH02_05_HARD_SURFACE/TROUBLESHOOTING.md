# CH02.05 — Dépannage

| Symptôme | Cause | Solution |
|---|---|---|
| Biseaux plus larges sur un axe | Échelle d'objet ≠ 1 | `Ctrl+A` → Scale |
| Le Bevel « Weight » ne fait rien | Aucun poids posé, ou poids sur d'autres arêtes | *Edge → Edge Bevel Weight* = 1 ; overlay **Bevel** pour vérifier |
| Tout est arrondi | Limit Method = None | Limit Method : Weight (coins) ou Angle (le reste) |
| Arrondis qui se chevauchent, géométrie folle | Width trop grand | Réduire Width ; *Clamp Overlap* coché |
| Taches sur les grandes faces | Normales moyennées | Harden Normals (+ Shade Smooth) ou Weighted Normal |
| Harden Normals sans effet | Objet en Shade Flat | *Object → Shade Smooth* |
| Les boutons se biseautent bizarrement | Le bevel Angle s'applique aussi à eux | Normal ; ajuster Width, ou garder les boutons en objets séparés |
| Écran qui « bave » sur les côtés | Inset trop large, puis bevel | Inset plus petit ; vérifier en fil de fer |
