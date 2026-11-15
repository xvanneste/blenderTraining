# CH02.09 — Exercices

## Exercice 1 — Facile : lire une densité ⏱ 10 min
Ajoutez Monkey, appliquez une Subdivision de niveau 3 : nombre de faces ? Comparez avec la cage
d'origine (500 faces). À partir de quel niveau de détail la cage suffit-elle avec une *normal map* ?

## Exercice 2 — Moyen : le masque (retopologie manuelle) ⏱ 45 min
Sur le Monkey subdivisé (niveau 3, appliqué, objet « sculpture »), retopologisez **la moitié du
visage** en Poly Build + Face Project + Mirror (Clip) : boucle autour de l'œil, boucle autour de la
bouche, puis remplissage. Objectif : < 600 faces, 100 % quads.

## Exercice 3 — Difficile : le rocher (SANS procédure) ⏱ 20 min
Cage légère en quads, écart moyen < 2 cm, couverture ≥ 95 %. Validation : `--exercise retopo --render`.

### Grille d'auto-évaluation (sur 20)
| Critère | 0 | 1 | 2 |
|---|---|---|---|
| Sculpture intacte | non | — | oui |
| Densité adaptée (100–3 000 faces) | non | limite | oui |
| Quads ≥ 90 % | non | partiel | oui |
| Cage qui enveloppe avant Shrinkwrap | non | — | oui |
| Écart moyen < 2 cm | non | — | oui |
| Couverture ≥ 95 % | non | 80–95 % | oui |
| Cage fermée | non | — | oui |
| Overlay Retopology utilisé | non | — | oui |
| Sculpture masquée au rendu | non | — | oui |
| Temps < 20 min | > 35 | 20–35 | < 20 |
**≥ 14/20** : acquis.

## Défis
- **Défi 1 :** remplacez *Nearest Surface Point* par *Project* (avec *Negative* et *Positive*
  cochés) : différences visibles sur les creux du rocher ?
- **Défi 2 :** densifiez la cage uniquement sur une arête vive du rocher (Loop Cut) et observez la
  précision gagnée.

## Mini-projet — Retopologie de la créature ⏱ 2 h
Appliquez Skin + Subdivision de votre créature de CH02.08 (sur une copie), puis retopologisez-la
manuellement : boucles aux articulations (épaules, hanches, cou), < 3 000 faces, Mirror. Conservez
les deux versions dans `PROJECTS/`.
