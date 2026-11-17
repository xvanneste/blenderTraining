# CH05.06 — Dépannage

| Symptôme | Cause | Solution |
|---|---|---|
| Le paramètre ne change rien | Entrée non branchée ou valeur en dur | Relier la sortie de Group Input |
| Piliers qui flottent | Height branché à Depth seulement | Aussi à Translation z (÷ 2) |
| Valeur négative acceptée | Minimum absent | Régler Min dans l'interface |
| Outil illisible | Pas de panneaux ni de descriptions | Ajouter les deux |
| Modificateur sans champs | Arbre sans entrées | Créer les entrées de l'interface |
| TypeError en script sur `modifier[...]` | API 5.3 | `modifier.properties.inputs[id]["value"]` |
| Valeur assignée refusée | Affectation du groupe | Écrire dans `["value"]` |
| Identifiant inconnu | Nom ≠ identifiant | Lire `item.identifier` |
