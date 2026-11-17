# CH13.02 — Dépannage

| Symptôme | À vérifier |
|---|---|
| Les deux caisses changent de couleur | Vérifiez `a.data == b.data`. Repartez de la copie de départ et dupliquez le maillage avant le changement. |
| La console reste à l’invite de continuation | Ajoutez une ligne vide pour terminer le bloc indenté. |
| L’ajout échoue ou modifie un maillage existant | Revenez en mode Objet et vérifiez `poll()` avant de recommencer. |
| La sphère apparaît deux fois dans l’Outliner | Elle est liée à plusieurs collections. Gardez son lien dans `COL_Props`, puis retirez les autres. |
| Le nom actif n’est pas celui attendu | L’ajout a rendu la sphère active. Rétablissez la sélection et l’objet actif sur B. |
