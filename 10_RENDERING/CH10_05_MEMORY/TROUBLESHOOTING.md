# CH10.05 — Dépannage

| Symptôme | Cause | Solution |
|---|---|---|
| Rochers disparus | Source visible ou instances manquantes | Exclure la collection source, 200 instances |
| Trop de maillages | Un maillage par rocher | Link Object Data |
| Trop de triangles | Subdivision au niveau 2 sur 200 objets | Instances ou niveau 0 |
| Texture trop lourde | Pas de limite | Simplify > Texture Limit 1024 |
| Limite sans effet | Simplify désactivé | Cocher la case de l'en-tête |
| Compte des rochers faux | Noms ne commençant pas par Rock | Garder Rock_* |
| Matériau perdu | Maillage partagé sans matériau | Matériau sur le maillage |
| Correcteur lent | Trop de modificateurs | Instances |
