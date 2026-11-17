# CH07.04 — Dépannage

| Symptôme | Cause | Solution |
|---|---|---|
| Le pendule est robotique | Interpolation linéaire | T > Bezier, V > Auto Clamped |
| La courbe dépasse | Poignées libres | Auto Clamped |
| Le pendule s'arrête après une période | Pas de Cycles | Ajouter Cycles |
| La répétition est invisible | Plage de scène trop courte | End = 48 ou plus |
| Le pendule saute | Noise trop fort | Strength 0,06 |
| Le bruit n'apparaît pas | Modificateur sur la mauvaise courbe | Le mettre sur Z Location |
| Les clés ont changé | Édition des clés | Annuler (Ctrl+Z) |
| Courbe plate | Aucune clé de variation | Vérifier les clés |
