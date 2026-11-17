# CH08.04 — Dépannage

| Symptôme | Cause | Solution |
|---|---|---|
| Les particules traversent le sol | Pas de Collision | Ajouter Collision sur le sol |
| Les particules montent sans fin | Gravité nulle | Gravity 1 |
| Toutes naissent d'un coup | Frame End trop court | End 30 |
| Aucune particule visible | Rendu None | Normal en test : lire la simulation ou changer Render As |
| Pas de jet | Vitesse normale 0 | Normal 3 |
| Mauvais nombre | Number trop bas | 200 |
| Elles meurent trop tôt | Lifetime court | 60 |
| Simulation absente à l'image 100 | Image courante hors cache | Repartir de l'image 1 |
