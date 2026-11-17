# CH05.04 — Dépannage

| Symptôme | Cause | Solution |
|---|---|---|
| Aucun point | Masque à 0 partout ou sortie non reliée | Vérifier Density Factor ; Spreadsheet |
| Arbres partout | Density Factor non relié | Masque → Density Factor |
| Arbres collés | Méthode Random | Poisson Disk |
| Peu d'arbres | Density Max trop bas | 3 par m² |
| Arbres penchés | Rotation non transmise ou sol incliné | Distribute [Rotation] → Rotation |
| Mauvais côté | Comparaison inversée | Greater Than |
| Socket introuvable en script | Sockets dépendant de la méthode | Tester `'Nom' in node.inputs` |
| Résultat différent | Seed changé | Fixer le Seed |
