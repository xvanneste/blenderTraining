# CH02.02 — Dépannage

| Symptôme | Cause | Solution |
|---|---|---|
| Loop Cut ne propose aucune coupe | Anneau interrompu par un triangle ou un n-gon | Réparer la topologie (CH02.01) ; découper au Knife (CH02.03) |
| Les coupes ne sont pas symétriques | Coupe glissée à la souris | Clic droit après le clic gauche (coupe centrée), puis `S X` chiffré |
| Les pieds partent de travers | Extrusion non contrainte | `E` puis `Z` puis valeur ; vue de face pour vérifier |
| Les 4 coins s'extrudent en un seul bloc | Faces voisines sélectionnées | Ne sélectionner que les carrés d'angle (non voisins) |
| Bridge : « Select at least two edge loops » | Sélection incorrecte | Deux faces (ou deux boucles) avec le même nombre de sommets |
| Traverse vrillée | Sommets mal appariés | Panneau de l'opération → **Twist** |
| Faces internes après Bridge | Faces non supprimées (boucles d'arêtes sans faces) | Sélectionner les faces (Bridge Faces les supprime) ; *Select All by Trait → Interior Faces* |
| Bevel déforme tout l'objet | Échelle d'objet non appliquée | Object Mode, `Ctrl+A` → *Scale* ; puis refaire le Bevel |
| Bevel « explose » | Largeur trop grande | Réduire *Width* ; activer *Clamp Overlap* |
| Creux du dessus en biais | Inset avec *Depth* au lieu d'Extrude | `I` (Depth 0) puis `E` vers l'intérieur |
