# CH10.07 — Dépannage

| Symptôme | Cause | Solution |
|---|---|---|
| Toutes les images rendues par une seule machine | -a avant -s/-e | -a en dernier |
| Image manquante | Trou entre deux plages | Plages contiguës |
| Image rendue deux fois | Recouvrement | Plages disjointes |
| Rien dans le dossier | -o manquant ou chemin faux | Ajouter -o |
| Plan refusé | Option hors liste blanche | Utiliser -b -o -F -s -e -a |
| Images écrasées | Overwrite activé | Le désactiver |
| Deux machines rendent la même image | Placeholders désactivé | Les activer |
| {BLEND} non reconnu | Fichier mal nommé | Mettre {BLEND} juste après -b |
