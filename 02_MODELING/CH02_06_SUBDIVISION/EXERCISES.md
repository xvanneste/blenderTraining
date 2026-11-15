# CH02.06 — Exercices

## Exercice 1 — Facile : la distance fait l'arrondi ⏱ 10 min
Trois cubes subdivisés (`Ctrl+2`) avec une boucle de maintien près de chaque arête, à 20 cm, 8 cm et
2 cm des bords (cubes de 80 cm). Rendu : classez les arrondis et énoncez la règle.

## Exercice 2 — Moyen : crease ou boucles ? ⏱ 20 min
Modélisez deux fois une savonnette (galet aplati avec un dessus plat et un rebord net) : une fois
avec crease, une fois avec boucles de maintien. Comparez nombre de faces de la cage, netteté,
facilité de modification. Laquelle exporteriez-vous vers un autre logiciel ?

## Exercice 3 — Difficile : les trois cubes (SANS procédure) ⏱ 25 min
Validation : `--exercise subdiv --render`.

### Grille d'auto-évaluation (sur 20)
| Critère | 0 | 1 | 2 |
|---|---|---|---|
| Boucles de maintien dans les 3 directions | non | 1–2 | 3 |
| Distance des boucles régulière | non | approx. | oui |
| Forme cubique (remplissage ≥ 0,9) | non | — | oui |
| Crease seulement où il faut | non | partiel | oui |
| Dessous resté arrondi | non | — | oui |
| Levels Viewport ≤ 1, Render ≥ 3 | non | un des deux | oui |
| Cage en quads, sans n-gon | non | partiel | oui |
| Modificateurs non appliqués | non | — | oui |
| Explication crease vs boucles | non | floue | claire |
| Temps < 25 min | > 40 | 25–40 | < 25 |
**≥ 14/20** : acquis.

## Défis
- **Défi 1 :** sur un cylindre subdivisé, obtenez un couvercle plat sans n-gon (Inset puis Grid
  Fill ou « quad cap »).
- **Défi 2 :** faites un trou rond propre dans une plaque subdivisée (cercle dans une grille de
  quads, boucles de maintien autour).

## Mini-projet — La souris d'ordinateur ⏱ 2 h
Cage de 12 × 6 × 4 cm à partir d'un cube, boutons séparés par une rainure (boucles de maintien),
molette, câble. Subdivision Levels 1 / Render 3. Cage 100 % quads. Collection `PROPS` (projet P2).
