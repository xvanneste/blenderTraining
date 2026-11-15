# CH18.21 — Dépannage

| Symptôme | Cause | Solution |
|---|---|---|
| `ModuleNotFoundError: bcma_shots` au Run Script | Fichier non enregistré dans STARTER_FILES | Enregistrez sous STARTER_FILES puis relancez |
| Le script ne crée rien | SHOTLIST mal formatée (moins de 6 champs) | `code;valeur;sujet;côté;durée_s;note` |
| « focale None » dans la console | Valeur impossible à obtenir depuis la position prévue | Vérifiez valeur/sujet ; changez la distance dans DIST |
| Deux caméras CAM_SH0030 / CAM_SH0030.001 | Code en double non corrigé | Corrigez SHOTLIST, relancez (le script nettoie) |
| Plans conformes refusés « image » | Durées modifiées après le lancement | Relancez le script après chaque correction |
| Journal refusé | Lignes commençant par « # » ou mots-clés absents | Écrivez outil / accepté / refusé ou corrigé |
| Les boards apparaissent au rendu | — | Ils sont exclus du rendu par le script (hide_render) ; vérifiez l'Outliner |
