# CH02.05 — Exercices

## Exercice 1 — Facile : trois arêtes ⏱ 10 min
Trois cubes de 20 cm (échelle 1) : (a) sans bevel ; (b) Bevel modificateur 2 mm, 2 segments,
Angle ; (c) Bevel 1 cm, 1 segment. Rendu `F12` sous la lumière studio : décrivez en une phrase ce
que chaque arête fait de la lumière.

## Exercice 2 — Moyen : bevel ciblé ⏱ 20 min
Une boîte à outils 50 × 25 × 25 cm : arrondissez seulement les 4 arêtes du couvercle (Bevel Weight
+ Bevel « Weight » 3 cm, 5 segments), tout le reste en Bevel « Angle » 2 mm. Ajoutez une poignée
(tore aplati ou cylindre courbé) jointe à l'objet.

## Exercice 3 — Difficile : le boîtier (SANS procédure) ⏱ 35 min
Coins arrondis par poids, écran en creux, 3 boutons, arêtes fines en Harden Normals.
Validation : `--exercise device --render`.

### Grille d'auto-évaluation (sur 20)
| Critère | 0 | 1 | 2 |
|---|---|---|---|
| Échelle d'objet à 1, dimensions réelles | non | — | oui |
| Bevel Weight sur les bonnes arêtes seulement | non | partiel | oui |
| Bevel Weight + Bevel Angle empilés | non | un seul | les deux |
| Arrondis réguliers (pas de pincement) | non | partiel | oui |
| Harden Normals + Shade Smooth : faces propres | non | partiel | oui |
| Écran en creux net | non | partiel | oui |
| Boutons alignés, de taille cohérente | non | partiel | oui |
| Hiérarchie : grandes surfaces calmes, détails groupés | non | moyenne | oui |
| Modificateurs non appliqués | non | — | oui |
| Temps < 35 min | > 60 | 35–60 | < 35 |
**≥ 14/20** : acquis.

## Défis
- **Défi 1 :** grille d'aération : Inset *Individual* sur une série de faces d'une bande découpée
  par Loop Cut, puis Extrude vers l'intérieur.
- **Défi 2 :** reproduisez la recette sur un objet réel de votre bureau (souris, chargeur…) en
  respectant ses cotes mesurées.

## Mini-projet — Le talkie-walkie ⏱ 2 h
6 × 3,5 × 15 cm : coque à coins arrondis, antenne (cylindre + bevel), haut-parleur (grille), écran,
boutons, molette (Screw ou cylindre crénelé). Deux bevels empilés, Harden Normals. Rendu en
gros plan. Collection `PROPS` (projet P2).
