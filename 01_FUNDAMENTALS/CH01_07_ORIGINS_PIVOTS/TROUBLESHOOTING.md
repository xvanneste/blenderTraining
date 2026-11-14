# CH01.07 — Dépannage

| Symptôme | Cause | Solution |
|---|---|---|
| *Set Origin* déplace l'objet | On a utilisé *Geometry to Origin* | `Ctrl+Z`, utiliser *Origin to 3D Cursor* |
| Le curseur n'est pas où je pensais | `Shift+RMB` sur une surface / dans le vide | `Shift+S` → *Cursor to Selected* ; vérifier dans `N` → View → 3D Cursor |
| Les nouveaux objets apparaissent loin | Le curseur a été déplacé | `Shift+S` → *Cursor to World Origin* (ou `Shift+C`) |
| Tout tourne bizarrement autour d'un point lointain | Pivot resté sur *3D Cursor* | `.` → *Median Point* |
| Les objets tournent chacun sur eux-mêmes | Pivot = *Individual Origins* | `.` → pivot voulu |
| `G` déplace l'origine au lieu de l'objet | *Affect Only → Origins* resté coché | Options → décocher |
| En Edit Mode, *Cursor to Selected* va au mauvais endroit | Sélection incomplète (1 sommet au lieu de 2) | Vérifier la sélection avec X-Ray |
