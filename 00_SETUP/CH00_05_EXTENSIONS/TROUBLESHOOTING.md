# CH00.05 — Dépannage

| Symptôme | Cause probable | Solution |
|---|---|---|
| *Get Extensions* vide, message sur l'accès en ligne | Accès en ligne refusé (défaut) | *Allow Online Access*, ou installer depuis le disque |
| « Missing manifest » à l'installation | Le `.zip` est un ancien add-on (sans `blender_manifest.toml`) | Onglet *Add-ons* → ˅ → *Install from Disk* gère aussi les anciens add-ons ; vérifier la compatibilité |
| L'extension s'installe mais rien n'apparaît | Elle ajoute ses outils ailleurs (menu, sidebar, éditeur précis) | Lire sa documentation ; chercher avec `F3` (recherche de menus) |
| Erreur rouge au démarrage après mise à jour de Blender | Extension incompatible avec 5.3 | Désactiver/mettre à jour l'extension ; `--factory-startup` pour diagnostiquer |
| `validate` échoue : « id » invalide | Majuscules, tirets ou espaces dans `id` | Minuscules, chiffres, `_` uniquement |
| Un `.blend` affiche « Auto-run disabled » | Le fichier contient des scripts (drivers Python…) bloqués par sécurité | Ne les autoriser (*Allow Execution*) que pour un fichier de confiance |
