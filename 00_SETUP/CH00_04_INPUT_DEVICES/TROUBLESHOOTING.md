# CH00.04 — Dépannage

| Symptôme | Cause probable | Solution |
|---|---|---|
| Pas de variation de pression | Pilote absent, mauvaise *Tablet API*, pression désactivée sur la brush | Installer le pilote officiel ; essayer *Windows Ink* puis *Wintab* ; activer l'icône de pression de *Radius*/*Strength* |
| Le stylet « clique » au lieu de dessiner (Windows) | Gestes Windows Ink (appui long = clic droit) | Désactiver les options Windows Ink dans le pilote de la tablette, ou passer en *Wintab* |
| Les chiffres changent de vue en Edit Mode au lieu du mode de sélection | *Emulate Numpad* actif | Icônes de l'en-tête, ou désactiver l'émulation |
| `Alt`+clic ne fait pas orbiter | *Emulate 3 Button Mouse* inactif, ou `Alt`+clic intercepté par un logiciel (capture d'écran, pilote) | Activer l'émulation ; vérifier les logiciels en arrière-plan ; changer le modificateur en *OS-Key* |
| Le zoom molette est inversé | Préférence personnelle | *Navigation → Zoom → Invert Zoom Direction* |
| Le curseur saute aux bords pendant un déplacement | *Continuous Grab* (normal : le curseur « boucle » pour des déplacements infinis) | Laisser actif ; le désactiver seulement si votre tablette en mode absolu se comporte mal |
| La souris 3D n'est pas reconnue | Pilote du fabricant absent | Installer le pilote ; vérifier *Input → NDOF* |
