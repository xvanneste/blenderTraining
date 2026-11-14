# CH01.04 — Dépannage

| Symptôme | Cause | Solution |
|---|---|---|
| Modifier un objet en modifie d'autres | Données partagées (`Alt+D` ou `Ctrl+L`) | Make Single User avant de modifier |
| `Ctrl+J` : l'objet joint a la mauvaise origine/position | L'objet actif n'était pas le bon | Annuler, refaire en cliquant la référence en dernier |
| Après jointure, les morceaux ont une échelle bizarre | Échelles non appliquées différentes | Normal : la géométrie est convertie dans l'espace de l'objet actif ; appliquer l'échelle avant (CH01.06) |
| `P` ne propose rien | Pas en Edit Mode, ou rien sélectionné | `Tab`, `A`, puis `P` |
| Un matériau a disparu après enregistrement | 0 utilisateur (orphelin) | Bouclier Fake User avant d'enregistrer |
| Le nombre d'utilisateurs n'apparaît pas | Données utilisées une seule fois (pas de nombre affiché) | Normal |
