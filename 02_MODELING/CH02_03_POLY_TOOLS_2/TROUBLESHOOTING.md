# CH02.03 — Dépannage

| Symptôme | Cause | Solution |
|---|---|---|
| Spin tourne autour du mauvais axe | Curseur 3D ailleurs | `Shift+C` (ou *Center* dans le panneau) avant Spin |
| Vase ombré bizarrement au fond | 24 sommets superposés sur l'axe | `A` puis `M` → *By Distance* |
| `M` → By Distance ne fusionne rien après Spin | Seule la dernière copie est sélectionnée | `A` d'abord |
| Spin à plat (un disque) | Mauvais axe (profil dessiné dans X-Y) | *Axis* (0,0,1) pour un profil dans X-Z ; ou redessiner en vue de face |
| Bisect coupe au mauvais endroit | Plane Point en coordonnées locales, échelle non appliquée | `Ctrl+A` → Scale ; régler *Plane Point* chiffré |
| Bisect laisse un trou | *Fill* non coché | Cocher *Fill* dans le panneau |
| Knife ne coupe pas les faces arrière | Test de profondeur | `C` (cut through) pendant la coupe, ou `Shift+K` sur une sélection |
| Coupe Knife qui crée des n-gons | Coupe s'arrêtant au milieu d'une face | Prolonger jusqu'à une arête ; `J` entre sommets |
| Limited Dissolve casse une surface courbe | *Max Angle* trop grand | Réduire à 1–5° ; réserver aux zones planes |
| Ressort aplati | *Screw* = 0 ou axe faux | *Screw* > 0, *Axis* Z |
