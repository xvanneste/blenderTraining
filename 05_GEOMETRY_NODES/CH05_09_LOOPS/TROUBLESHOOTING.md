# CH05.09 — Dépannage

| Symptôme | Cause | Solution |
|---|---|---|
| Une seule marche | Join sans l'état précédent | Repeat Input [Geometry] → Join |
| Toujours 16 marches | Iterations en dur | Steps → Iterations |
| Marches empilées sur l'axe | Pas de translation x avant la rotation | Deux Transform, translation d'abord |
| Marches à plat | Montée absente | z = 0,05 + Iteration × Rise |
| Blender lent | Trop d'itérations | Borner Steps |
| Spirale à l'envers | Angle négatif ou sens de rotation | Signe de l'angle |
| Zone non reconnue | Input et Output non appariés | `pair_with_output` / zone créée par le menu |
| Géométrie perdue entre itérations | Élément d'état manquant | Déclarer l'item de la zone |
