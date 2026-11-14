# CH01.08 — Dépannage

| Symptôme | Cause | Solution |
|---|---|---|
| L'icône appareil photo n'apparaît pas dans l'Outliner | Colonne masquée | Filtre (entonnoir) → Restriction Toggles |
| Un objet a disparu de la vue | Œil (`H`), écran, collection exclue, vue locale | `Alt+H` ; vérifier les icônes et la case de la collection ; `Num /` |
| Un objet apparaît dans deux collections | Lié avec `Shift+M` ou `Ctrl`+glisser | `RMB` dans l'Outliner → *Unlink* depuis la collection en trop |
| `Ctrl+P` : l'enfant saute ailleurs | Parent déjà transformé et option inadaptée ; ou l'enfant avait un autre parent | `Ctrl+Z` puis *Object (Keep Transform)* |
| `Alt+P` → *Clear Parent* déplace l'objet | Normal : il revient à sa transformation locale | *Clear and Keep Transformation* |
| Le parent et l'enfant sont inversés | Mauvais objet actif | Le parent doit être sélectionné **en dernier** |
| Collection invisible au rendu mais objets visibles | Objets aussi liés à une autre collection rendue | Vérifier les collections de l'objet (Properties → Object → Collections) |
