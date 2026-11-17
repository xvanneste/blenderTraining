# CH08.10 — Dépannage

| Symptôme | Cause | Solution |
|---|---|---|
| Pas de dossier blendcache | Fichier non enregistré | Enregistrer puis cuire |
| Cache perdu après renommage | Nom du .blend changé | Copier le dossier blendcache |
| Bake n'a que 30 images | Plage de la scène trop courte | Scène 1–60 |
| Positions différentes selon l'ordre | Pas de cache | Bake |
| Nombre de particules changé | Réglage modifié après la cuisson | Supprimer le cache et recuire |
| `ptcache.bake` refuse en script | Pas de point_cache dans le contexte | temp_override(point_cache=pc) |
| Gros dossier | Beaucoup de particules | Nettoyer les anciens caches |
| Le correcteur voit 0 fichier | Fichier ouvert depuis une copie | Ouvrir depuis le dossier d'origine |
