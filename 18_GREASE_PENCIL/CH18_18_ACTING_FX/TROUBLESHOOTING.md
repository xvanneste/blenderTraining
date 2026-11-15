# CH18.18 — Dépannage

| Symptôme | Cause | Solution |
|---|---|---|
| La fumée reste jusqu'à la fin | Pas de clé vide après l'effet | Shift+I sans dessiner après le dernier dessin |
| Le personnage réagit avant l'éclair | Clé de réaction trop tôt | Réaction 1 à 6 images APRÈS le début de l'effet |
| Surprise peu lisible | Tenue trop courte | Tenez la pose 12 à 30 images |
| Le personnage paraît figé pendant la tenue | Dessin strictement fixe | Clignement ou moving hold |
| La caméra ne revient pas au cadrage | Dernière clé différente de la première | Remettez Location (0, −10, 0) et I |
| Tremblement trop « mou » | Interpolation Bézier lissée | Graph Editor : T > Linear ou Constant sur les clés du tremblement |
| Le tremblement décale le décor « pour toujours » | Clés manquantes après la secousse | Clé de repos après la dernière secousse |
| L'éclair passe derrière le personnage | Ordre des calques | Calque USER_FX au-dessus dans la liste |
