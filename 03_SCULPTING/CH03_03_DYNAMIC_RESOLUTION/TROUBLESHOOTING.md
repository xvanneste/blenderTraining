# CH03.03 — Dépannage

| Symptôme | Cause | Solution |
|---|---|---|
| Plusieurs morceaux après le remesh | Masses qui ne se chevauchent pas | Ponts (cou, abdomen, épaules) qui pénètrent les voisins |
| Objet énorme, millions de faces | Sol ou autre objet joint par erreur | Alt+A avant la sélection ; Ctrl+Z |
| Remesh déformé | Échelle non appliquée | Ctrl+A > Rotation & Scale avant |
| Doigts / détails disparus | Voxel trop gros | Voxel Size plus petit (ou détails après) |
| Blender très lent | Voxel trop petit | Augmentez Voxel Size ; Multires Viewport plus bas |
| Masque / couleurs perdus au remesh | Attributs non conservés | Preserve Attributes dans le panneau Remesh |
| UV détruites | Remesh / DynTopo reconstruisent la topologie | Multires sur une base retopologisée |
| Multires : pics à l'Unsubdivide | Base trop irrégulière | Retopologie propre d'abord (CH03.09) |
| DynTopo grisé | Objet avec Multires ou attributs incompatibles | Appliquez/supprimez le Multires sur une copie |
