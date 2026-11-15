# CH18.08 — Dépannage

| Symptôme | Cause | Solution |
|---|---|---|
| Le masque ne masque rien | Œil du calque masque fermé (constaté 5.3), ou *Use Masks* non coché | Ouvrir l'œil, mettre l'opacité du masque à 0 ; cocher la case du sous-panneau Masks |
| Le calque masque est visible par-dessus le dessin | Opacité du masque > 0 | Opacity = 0 |
| Le modificateur agit sur tout le dessin | Influence non réglée | Influence → Layer : nom du calque |
| Le Build ne montre rien à l'image 1 | Normal : le tracé commence | Avancer dans la timeline ; régler *Delay*, *Length* |
| Le dessin a disparu après Apply | Modificateur appliqué (destructif) | `Ctrl+Z` ; ne pas appliquer ; garder les versions `_v00X` |
| L'ombre recouvre en gris opaque | Blend Mode Regular | Blend Mode Multiply, opacité 0,5–0,7 |
| En déplaçant les nuages, tout bouge | Objet déplacé au lieu du calque | Annuler ; Layers → Transform → Translation |
| Viewport lent | Trop de modificateurs/effets actifs à l'affichage | Désactiver l'icône écran pendant le dessin |
