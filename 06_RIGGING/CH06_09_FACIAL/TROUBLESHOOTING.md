# CH06.09 — Dépannage

| Symptôme | Cause | Solution |
|---|---|---|
| La mâchoire casse la forme | Poids binaires | Dégradé head → jaw |
| Rien ne bouge à l'ouverture | Pas de poids sur jaw | Assigner le groupe jaw |
| Le sourire bouge les yeux | Key sans groupe de zone | Vertex Group du key |
| Amplitude trop faible | Poids non normalisés, driver mal calibré | Poids 1 au centre, x / 0.05 |
| La glissière sort du cadre | Pas de Limit Location | Contrainte Local Space |
| Valeur du key > 1 | Curseur non borné | Slider Max 1 |
| Driver violet | Variable invalide | Objet, bone, X Location, Local Space |
| La mâchoire tourne dans le mauvais sens | Axe/signe | Essayer −15° puis +15° autour de X |
