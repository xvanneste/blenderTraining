# CH07.05 — Dépannage

| Symptôme | Cause | Solution |
|---|---|---|
| La balle flotte au contact | Poignées horizontales aux contacts | V > Vector aux clés de contact |
| La balle va à vitesse constante | Interpolation linéaire | Bezier + poignées |
| Les rebonds sont trop réguliers | Hauteurs ou durées égales | Décroissance ×0,5 et ×0,7 |
| La balle s'enfonce dans le sol | Contacts négatifs | Z = 0 aux contacts |
| La balle ne s'arrête pas | Dernière clé non nulle | Z = 0 aux images 62 et 72 |
| La balle paraît trop légère | Durées trop longues pour la hauteur | h = g·T²/8 |
| Le sommet est pointu | Poignées Vector au sommet | Auto Clamped au sommet |
| Trop de clés | Bake image par image | 7 clés suffisent |
