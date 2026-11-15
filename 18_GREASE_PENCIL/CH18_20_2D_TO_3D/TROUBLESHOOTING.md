# CH18.20 — Dépannage

| Symptôme | Cause | Solution |
|---|---|---|
| Le personnage glisse entre deux plans | Interpolation Bézier | Clés en Constant (T) |
| « Caméras modifiées » | Une caméra déplacée pendant le blocking | Ctrl+Z ; verrouillez la sélection des caméras |
| Le board ne suit pas la caméra | GP non parenté | Object Properties > Relations > Parent = caméra |
| Board d'un autre plan visible | Tous les boards affichés | H sur les autres boards |
| Board caché par le personnage | Board placé trop loin de la caméra | Rapprochez-le (Z local −0,5) |
| Les boards apparaissent au rendu | Rendu non désactivé | Outliner : Disable in Renders |
| Le mannequin flotte ou s'enfonce | Z ≠ 0 | G puis X ou Y (axes au sol) ; Z = 0 |
| Une clé atterrit à la mauvaise image | Tête de lecture pas sur le marqueur | Flèches haut/bas pour sauter au marqueur |
