# CH00.03 — Dépannage

| Symptôme | Cause probable | Solution |
|---|---|---|
| `Ctrl+L` → *Link Object Data* ne fait rien | L'objet actif n'est pas celui dont on veut copier les données, ou un seul objet sélectionné | Sélectionner tous les objets, `Ctrl`+clic sur la référence **en dernier** (elle devient active) |
| *Copy to Selected* grisé | Les autres objets n'ont pas de modificateur du même nom | Ajouter le modificateur partout : menu déroulant du modificateur (˅) → *Copy to Selected* (opérateur « Copy Modifier to Selected »), ou `Ctrl+L` → *Copy Modifiers* |
| Le rendu GPU échoue « out of memory » | Scène trop lourde pour la VRAM | Optimiser (leviers §6), réduire les textures, rendre en CPU |
| Le viewport rame alors que le GPU est peu utilisé | Modificateurs/animation calculés par le CPU | Baisser *Levels Viewport*, Simplify viewport, masquer les collections inutiles |
| Les statistiques ne s'affichent pas | Option non cochée | Overlays → Statistics, ou Preferences → Interface → Status Bar → Scene Statistics |
| Affichage corrompu après mise à jour de pilote | Problème de backend | Tester `blender_startup_opengl.cmd` ; changer *Display Graphics → Backend* |
| Les anciens maillages restent dans le fichier | Données orphelines pas encore purgées | Enregistrer puis rouvrir, ou *File → Clean Up → Purge Unused Data* |
| L'estimation de faces ne baisse pas avec Simplify | *Simplify* décoché dans le titre du panneau, ou réglage *Viewport* modifié au lieu de *Render* | Cocher la case du panneau ; régler le sous-panneau *Render* |
