# CH01.05 — Dépannage

| Symptôme | Cause | Solution |
|---|---|---|
| Tout bouge en même temps que la sélection | Édition proportionnelle restée active | `O` pour la désactiver |
| L'extrusion part dans une direction bizarre | `E` extrude le long de la normale moyenne ; après `E`, un axe tapé change la contrainte | `Échap` puis `Ctrl+Z` ; refaire `E` et taper juste la valeur |
| Une extrusion annulée par `Échap` laisse une géométrie en double | `Échap` annule le **déplacement**, pas la création | `Ctrl+Z` (ou `M` → *By Distance*) |
| `B` ne sélectionne pas les sommets de derrière | X-Ray désactivé | `Alt+Z` |
| Le correcteur ne voit pas mes modifications | Fichier enregistré en Edit Mode | `Tab` puis enregistrer |
| `1/2/3` changent la vue | Emulate Numpad actif | Icônes de l'en-tête |
| Faces noires ou inversées après édition | Normales inversées (CH02.04) | `Shift+N` (*Recalculate Outside*) en Edit Mode |
