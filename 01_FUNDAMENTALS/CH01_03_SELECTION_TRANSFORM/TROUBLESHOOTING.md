# CH01.03 — Dépannage

| Symptôme | Cause | Solution |
|---|---|---|
| Impossible de sélectionner la silhouette TGT | Volontaire : *Disable Selection* activé | Normal (Outliner : icône flèche) |
| `G` déplace l'objet bizarrement vite ou lentement | Distance de l'objet à la vue | Zoomer/cadrer avant ; `Shift` pour la précision |
| La saisie numérique ne marche pas | Pavé numérique en mode navigation / Emulate Numpad | Taper les chiffres **pendant** la transformation (après `G`) ; avec Emulate Numpad, la rangée du haut fonctionne aussi pendant une transformation |
| L'objet est parti « dans le décor » | Transformation validée par erreur | `Ctrl+Z`, ou `Alt+G/R/S` |
| Une rotation de 90 donne un angle étrange | Unités en radians dans un champ de script, ou rotation sur le mauvais axe | Vérifier l'axe dans l'en-tête ; les champs de l'interface sont en degrés |
| Le lasso ne marche pas | Sélection au clic droit (keymap différente) ou outil actif particulier | Avec la sélection au clic gauche : `Ctrl+RMB` glissé |
| Le correcteur trouve un écart alors que « ça a l'air bon » | Valeur approchée à la souris | Saisir les valeurs exactes |
