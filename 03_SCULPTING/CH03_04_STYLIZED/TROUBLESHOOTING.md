# CH03.04 — Dépannage

| Symptôme | Cause | Solution |
|---|---|---|
| Plusieurs morceaux | Masses qui ne se chevauchent pas | Enfoncez-les les unes dans les autres, remesh |
| Socle ouvert | Bisect sans Fill | Refaites avec Fill coché, ou Boolean avec un cube |
| Boolean sans effet / trous | Maillage non fermé, ou sphère qui ne traverse pas | Remesh avant ; solveur Exact ; sphère bien enfoncée |
| « Cou marqué » refusé | Tête posée sur les épaules sans rétrécissement | Un cou nettement plus fin que tête et épaules |
| Stylisation refusée | Proportions trop « réalistes » et égales | Exagérez une taille (grosse tête, épaules massives) |
| Nez non détecté | Nez trop plat, ou visage tourné vers +Y | Visage vers −Y ; accentuez le nez |
| Métaballes qui ne fusionnent pas | Éléments trop éloignés / rayons trop petits | Rapprochez-les, augmentez Radius ou Stiffness |
| Métaballes énormes | Rayon d'influence ≠ taille visible | Réglez à l'œil, Resolution plus fine |
| Rendu tout gris, peu lisible | Matériau et lumière plats | Studio : lumière clé latérale, matériau mat clair |
