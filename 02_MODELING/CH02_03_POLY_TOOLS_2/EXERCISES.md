# CH02.03 — Exercices

## Exercice 1 — Facile : une fenêtre au Knife ⏱ 15 min
Sur un mur (cube 4 × 0,2 × 2,5 m, échelle appliquée), découpez au Knife un rectangle de fenêtre
1 × 1,2 m sur la face avant (vue de face, `X`/`Z` pour contraindre), puis `I` + `E` vers l'intérieur
pour l'embrasure. Vérifiez qu'il n'y a pas de n-gon autour de la fenêtre (*Faces by Sides*) ; sinon,
reliez les sommets avec `J`.

## Exercice 2 — Moyen : un verre à pied ⏱ 25 min
Dessinez un profil de verre à pied (sommets en vue de face, `E` pour prolonger, premier sommet sur
l'axe), Spin 360° 32 pas, `A`, `M` → *By Distance*, *Shade Smooth*. Ajoutez une épaisseur au bol avec
le modificateur *Solidify* (aperçu de CH02.07).

## Exercice 3 — Difficile : l'atelier (SANS procédure) ⏱ 30 min
Les 6 postes du starter. Validation : `--exercise atelier --render`.

### Grille d'auto-évaluation (sur 20)
| Critère | 0 | 1 | 2 |
|---|---|---|---|
| Bisect à la cote exacte, coupe bouchée | non | approx. | oui |
| Limited Dissolve sans déformation | non | — | oui |
| Spin complet, sans couture | non | partiel | oui |
| Doublons de l'axe fusionnés | non | — | oui |
| Pyramide centrée | non | décentrée | oui |
| Ressort non destructif (modificateur) | non | appliqué | oui |
| Diagonale Knife d'un coin à l'autre | non | approx. | oui |
| Bonnes touches du Knife (Shift, Ctrl, C) | non | partiel | oui |
| Vérifications après chaque coupe | non | parfois | toujours |
| Temps < 30 min | > 45 | 30–45 | < 30 |
**≥ 14/20** : acquis.

## Défis
- **Défi 1 :** escalier en colimaçon : une marche (pavé décalé de l'axe) + modificateur Screw
  (*Angle* 360°, *Screw* 3 m, *Iterations* 1, *Steps* 16).
- **Défi 2 :** coupez une pomme (UV Sphere déformée) en deux avec Bisect *Fill* et observez la
  face de coupe ; recommencez avec *Clear Inner*.

## Mini-projet — Lampe de chevet tournée ⏱ 1 h
Pied et abat-jour par Spin (profils dessinés), câble par Screw ou courbe, interrupteur au Knife +
Inset. Dimensions réelles (hauteur 45 cm). Collection `PROPS` (projet P2).
