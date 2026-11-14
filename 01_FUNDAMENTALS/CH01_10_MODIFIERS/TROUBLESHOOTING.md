# CH01.10 — Dépannage

| Symptôme | Cause | Solution |
|---|---|---|
| Mirror : le reflet est loin ou superposé | L'origine n'est pas sur le plan de symétrie | Placer l'origine au centre de symétrie (CH01.07), ou *Mirror Object* |
| Mirror : couture/trou au centre | Sommets du centre non fusionnés | Cocher *Merge* (et *Clipping* pendant l'édition) |
| Array : copies espacées bizarrement | Échelle non appliquée ou mélange Relative/Constant | Appliquer l'échelle ; n'utiliser qu'un type d'offset |
| Bevel trop gros ou irrégulier | Échelle non appliquée ; *Amount* en mètres | `Ctrl+A` → Scale ; réduire *Amount* |
| Bevel n'affecte pas certaines arêtes | *Limit Method = Angle* (30° par défaut) | Baisser l'angle ou *Limit Method = None* |
| Solidify : épaisseur vers l'intérieur au lieu de l'extérieur | *Offset* (−1 par défaut) / normales | *Offset* = 1 ou 0 ; recalculer les normales (`Shift+N`) |
| Viewport très lent | *Levels Viewport* trop élevé | 0 ou 1 au viewport, plus au rendu (CH00.03) |
| Le modificateur ne s'affiche pas au rendu | Icône appareil photo du modificateur désactivée | Réactiver |
