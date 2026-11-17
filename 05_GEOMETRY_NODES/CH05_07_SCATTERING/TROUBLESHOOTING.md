# CH05.07 — Dépannage

| Symptôme | Cause | Solution |
|---|---|---|
| Arbres sur des pentes raides | Masque absent ou inversé | Normal Z > cos(Max Slope) → Density Factor |
| Arbres qui flottent | Translation inutile | Le Cone a sa base à z = 0 |
| Tous les arbres identiques | Pick Instance décoché ou Index constant | Random Value entier → Instance Index |
| Changer Seed ne fait rien | Seed non branché | Seed → Distribute [Seed] |
| Peu d'arbres | Density basse ou masque trop strict | Density 0,5 ; Max Slope 30 |
| Arbres hors du terrain | Distribute sur le plan d'entrée | Distribuer sur le terrain déplacé |
| Matériau absent | Set Material manquant | Sur les arbres ET le terrain |
| Lenteur | Trop d'instances | Réduire la densité |
