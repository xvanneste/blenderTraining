# CH01.14 — Dépannage

| Symptôme | Cause | Solution |
|---|---|---|
| L'image a disparu après fermeture de la fenêtre | `F12` n'enregistre pas | `F11` rouvre le dernier rendu ; *Image → Save As* |
| Rendu noir | Voir CH00.01 (5 suspects) | Caméra, visibilité, lumières, monde, résolution |
| Rendu très bruité | Peu d'échantillons, débruitage désactivé, seuil trop élevé | Denoise ; seuil 0,01–0,02 ; plus d'échantillons |
| Rendu Cycles très lent | Device CPU, échantillons énormes (4096 par défaut), résolution 200 % | GPU Compute ; Max Samples raisonnable ; vérifier le % |
| Couleurs délavées ou trop contrastées | View Transform/Look | AgX + Look adapté ; Standard pour des couleurs d'interface |
| Le fichier PNG est introuvable | Chemin absolu `/tmp/` ou `//` mal compris | Chemin relatif `//renders/` ; *Save As* au bon endroit |
| `Ctrl+F12` écrase les images | Même chemin de sortie pour plusieurs essais | Changer le préfixe ou le dossier (`//renders/v002/`) |
| Le verre est noir en EEVEE | Réglages de ray tracing/transmission EEVEE | Cycles, ou phase 10 |
