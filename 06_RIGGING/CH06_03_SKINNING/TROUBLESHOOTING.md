# CH06.03 — Dépannage

| Symptôme | Cause | Solution |
|---|---|---|
| Rien ne bouge | Pas de modificateur Armature | Ctrl+P avec poids, ou ajouter le modificateur |
| Une partie reste en arrière | Sommets sans poids | Assigner / Automatic Weights |
| La racine bouge | Poids de fore sur la racine ou groupes inversés | Vérifier les noms |
| Coude cassé | Poids binaires | Smooth/Blur au coude |
| Volume qui s'effondre | Somme ≠ 1 | Normalize All |
| Export qui change les poids | > 4 influences | Limit Total 4 |
| Groupe sans effet | Nom ≠ bone | Renommer comme le bone |
| Automatic Weights échoue | Maillage non manifold ou armature inactive | Armature active, maillage propre |
