# CH07.13 — Dépannage

| Symptôme | Cause | Solution |
|---|---|---|
| La caisse ne bouge pas comme prévu | Une action reste active | Push Down ou action active vide |
| La répétition ne se voit pas | Repeat = 1 ou plage trop courte | Repeat 2 et End = 49 |
| La rotation arrive d'un coup | Pas de Blend In | Blend In 6 |
| Les strips ne se placent pas | Chevauchement sur une piste | Une piste par strip qui se chevauche |
| La rotation est trop rapide | Échelle 0,5 | Échelle 1 |
| Le strip anime autre chose | Mauvais slot | Slot de l'objet |
| Une action disparaît à l'enregistrement | Aucun utilisateur | Utilisateur fictif ou strip |
| Mauvais ordre des pistes | Piste Spin sous Move | Move en bas, Spin au-dessus |
