# CH09.01 — Dépannage

| Symptôme | Cause | Solution |
|---|---|---|
| Le rendu est plus clair que prévu | Monde non noir | Background noir |
| Disque lumineux dans l'image | Lampe visible à la caméra | Ray Visibility : Camera décoché |
| Exposition 10 fois trop faible | Puissance non compensée | × 9 pour 3 fois plus loin |
| Ombre dure | Radius 0 | 0,5 |
| Image trop rouge | Couleur trop saturée | Moins de rouge |
| Mesure instable | Peu d'échantillons | Moyenne sur 8 × 8 pixels |
| Valeurs plafonnées à 1 | PNG ou vue Filmic/AgX | EXR linéaire, vue Standard |
| Pénombre non détectée | Lampe dans le plan du cube | Lampe au-dessus du cube |
