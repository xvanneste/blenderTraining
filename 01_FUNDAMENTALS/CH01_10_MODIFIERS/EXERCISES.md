# CH01.10 — Exercices

## Exercice 1 — Facile : l'escalier ⏱ 5 min
Une marche (cube 1 × 0,3 × 0,18 m, échelle appliquée) + Array : 12 marches qui montent
(Relative Offset X 0, Y 1, Z 1).

## Exercice 2 — Moyen : la chaise symétrique ⏱ 15 min
Modélisez la moitié d'une chaise (assise, un pied avant, un pied arrière, demi-dossier) avec
des cubes joints, puis Mirror + Bevel + (Subdivision faible). La pile doit rester non appliquée.

## Exercice 3 — Difficile : le petit pont (SANS procédure) ⏱ 8 min
Les 4 consignes du `README_EXERCICE`, validez (`--exercise bridge --render`).
Barème (15 pts) : objets 1 · Array 10 2 · longueur 1 · non appliqué 1 · Mirror 2 · Bevel 2 ·
ordre 3 · épaisseur 1 · subdivision 1 · rendu 1.

## Défis
- **Défi 1 :** escalier en colimaçon : Array + *Object Offset* vers un Empty tourné de 20° et
  monté de 0,18 m.
- **Défi 2 :** chaîne : un tore aplati, Array avec Object Offset tourné de 90° sur X.

## Mini-projet — La passerelle ⏱ 30 min
Une passerelle complète (tablier, rambardes, piliers biseautés, lampadaires en Array) en
n'utilisant que des primitives et des modificateurs. Rendu `F12`. Grille : pile non
destructive 40 · ordre correct 20 · rendu 20 · nommage 20.

## Tests chronométrés
| Test | Cible |
|---|---|
| Array de 10 avec espacement | 15 s |
| Mirror + Bevel + Subdivision dans le bon ordre | 30 s |
| Copier une pile de modificateurs sur 5 objets (`Ctrl+L` → Copy Modifiers) | 10 s |
