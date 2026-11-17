# CH04.03 — Exercices

## Exercice 1 — Facile : classer ⏱ 15 min
Pour chacun : métal ou diélectrique, rugosité faible ou forte ? Cuivre brossé, plastique de jouet, miroir, béton, eau. (Réponses : métal rugueux moyen ; diélectrique lisse ; métal très lisse ; diélectrique rugueux ; diélectrique très lisse avec transmission.)

## Exercice 2 — Moyen : quatre matériaux ⏱ 2 h
Partez du starter et réglez MAT_Metal, MAT_Rubber, MAT_Glass, MAT_Wax. Validation : `--exercise pbr --render`.

## Exercice 3 — Difficile : variantes ⏱ 2 h
Remplacez l'or par un cuivre (Base Color ≈ 0,95 ; 0,64 ; 0,54) et ajoutez une peinture de voiture : Metallic 0, Base Color rouge, Coat Weight 1. Le correcteur doit rester vert sur les quatre sphères d'origine.

### Grille d'auto-évaluation (sur 10)
| Critère | 0 | 1 | 2 |
|---|---|---|---|
| Métal : Metallic 1, Base Color claire | non | partiel | oui |
| Diélectriques : albedo ni 0 ni 1, Metallic 0 | non | partiel | oui |
| Verre : Transmission 1, IOR plausible | non | partiel | oui |
| Cire : Subsurface avec rayon coloré | non | partiel | oui |
| Rendu regardé et commenté | non | partiel | oui |
**≥ 7/10** : acquis.

## Défis
- **Défi 1 :** un matériau « métal rouillé » : zones Metallic 1 et zones Metallic 0 (masque en CH04.04).
- **Défi 2 :** comparez EEVEE et Cycles sur le verre.

## Mini-projet
Une planche de cinq matériaux d'un accessoire de votre court-métrage avec la fiche de valeurs.
