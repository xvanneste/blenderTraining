# CH02.10 — Dépannage

| Symptôme | Cause | Solution |
|---|---|---|
| Ratio 0,2 mais « 32 % des faces » | Decimate compte en triangles | Lire Statistics → Triangles |
| La statue se déforme fortement | Ratio trop bas | Remonter ; Symmetry ; préserver la forme avec Collapse |
| Les LOD ne partagent pas le maillage | `Shift+D` (copie simple) au lieu de `Alt+D` | Object → Link/Transfer Data → Link Object Data (`Ctrl+L`) |
| Changer le ratio d'un LOD change tous les LOD | Impossible : modificateurs par objet | Vérifier que le bon objet est actif |
| By Distance ne fusionne rien | Rien de sélectionné | `A` puis `M` → By Distance |
| Delete Loose ne trouve rien | Éléments isolés déjà reliés | Vérifier avec *Select All by Trait → Loose Geometry* |
| Ombrage taché après Decimate | Triangles longs et normales lissées | Shade Auto Smooth ; ratio plus haut |
