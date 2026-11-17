# CH04.03 — Dépannage

| Symptôme | Cause | Solution |
|---|---|---|
| Le métal est noir | Environnement noir ou Base Color sombre | Monde clair ; Base Color du métal ≥ 0,5 de luminance |
| « Metallic proche de 0 ou de 1 » refusé | Valeur intermédiaire | 0 ou 1 ; mélanger avec un masque sinon |
| Le verre est opaque | Transmission Weight 0 | Mettre 1 |
| Le verre est invisible dans Solid | Mode d'affichage | Material Preview ou rendu |
| La cire est plastique | Subsurface Weight 0 | ≥ 0,2 et rayon R > B |
| « Quatre matériaux distincts » refusé | Un matériau partagé | Matériau dédié (bouton de duplication) par sphère |
| Albedo > 0,9 | Blanc pur | Descendre vers 0,8 |
| Rendu très sombre | Pas d'éclairage / monde noir | Monde ≥ 0,3 ou lampe |
