# CH03.09 — Exercices

## Exercice 1 — Facile : lire une topologie ⏱ 30 min
Sur `ch03_09_retopo_reference.png`, dessinez (papier ou Grease Pencil) les boucles autour d'un œil et de la bouche. Combien d'anneaux ? Où la densité est-elle la plus forte ?

## Exercice 2 — Moyen : la retopo du visage ⏱ 4 h
Partez du starter. `RETOPO_Face` : tout en quads, 300–2 500 faces, anneaux et ouvertures aux yeux et à la bouche, collé au sculpt, normales vers l'extérieur.
Validation : `--exercise retopo --render`.

## Exercice 3 — Difficile : le nez et les joues ⏱ 3 h
Ajoutez des boucles pour les ailes du nez et les plis naso-géniens (une boucle qui descend de l'aile du nez vers la commissure). Le maillage doit rester valide
(quads, valence 4 ≥ 80 %, budget).

### Grille d'auto-évaluation (sur 10)
| Critère | 0 | 1 | 2 |
|---|---|---|---|
| Tout en quads, normales cohérentes | non | partiel | oui |
| Anneaux autour des yeux et de la bouche, ouvertures | non | partiel | oui |
| Densité resserrée aux endroits utiles | non | partiel | oui |
| Peu de pôles, bien placés | non | partiel | oui |
| Épouse le sculpt (silhouette, nez, lèvres) | non | partiel | oui |
**≥ 7/10** : acquis.

## Défis
- **Défi 1 :** étendre la retopo aux oreilles et au cou, en gardant la topologie valide.
- **Défi 2 :** mesurer l'écart au sculpt face par face et repérer où le maillage s'en éloigne le plus.

## Mini-projet
La retopo du visage de votre personnage, avec une carte de ses boucles (dessin) et la fiche de mesures du correcteur.
