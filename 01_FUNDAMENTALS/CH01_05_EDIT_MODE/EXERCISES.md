# CH01.05 — Exercices

## Exercice 1 — Facile : sélections ⏱ 5 min
Sur `GEO_Practice` : (a) un sommet, (b) une boucle d'arêtes, (c) un anneau, (d) une rangée
de faces, (e) tout sauf la bordure (sélectionner tout, puis retirer la boucle de bordure
avec `Shift+Alt+LMB`… à tester).

## Exercice 2 — Moyen : le terrain ⏱ 10 min
Créez une grille 30×30 de 20 m (`Shift+A` → *Mesh → Grid*, panneau d'ajustement), puis 3
collines et 1 creux avec l'édition proportionnelle, de rayons différents.

## Exercice 3 — Difficile : la maison (SANS procédure) ⏱ 3 min
Transformez `GEO_House` en maison à toit à deux pans, faîtage parallèle à Y à 3 m de haut,
murs intacts. Bonus (non obligatoire) : colline sur `GEO_Practice`. Validez (`--exercise house`).
Barème (12 pts + 2 bonus) : présence 1 · faîtage 3 m 3 · centré 3 · orientation 2 · murs 2 ·
extrusion 1 · colline 2 (bonus).

## Défis
- **Défi 1 :** ajoutez une cheminée : sélectionnez une face du toit… (indice : `I` *Inset*
  sera vu en CH02.02 ; ici, découpez avec `Ctrl+R`… et observez les limites des outils
  de base).
- **Défi 2 :** faites un toit à **quatre** pans (toit en croupe) : quelle mise à l'échelle
  au lieu de `S X 0` ?

## Mini-projet — Le hameau ⏱ 25 min
Cinq maisons de proportions différentes (copies `Shift+D` modifiées en Edit Mode), sur un
terrain à collines, une caméra, un rendu. Grille : variété des formes 40 · propreté (pas de
faces cassées, sortie d'Edit Mode) 30 · rendu 30.

## Tests chronométrés
| Test | Cible |
|---|---|
| Maison (toit deux pans) depuis un cube | 30 s |
| Sélection d'une boucle et d'un anneau | 5 s |
| Colline proportionnelle | 15 s |
