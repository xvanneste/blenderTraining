# CH01.11 — Exercices

## Exercice 1 — Facile : cinq sphères, cinq matières ⏱ 10 min
Cinq sphères lissées : plastique rouge brillant, caoutchouc noir mat, or, verre, néon cyan.
Comparez en Material Preview et en Rendered.

## Exercice 2 — Moyen : variante sans casser l'original ⏱ 5 min
Deux cubes partagent `MAT_Wood`. Faites que l'un devienne plus foncé sans modifier l'autre.

## Exercice 3 — Difficile : la maison en couleurs (SANS procédure) ⏱ 8 min
Les 5 consignes du `README_EXERCICE`, validez (`--exercise colors --render`).
Barème (15 pts) : maison 1 · murs clairs 1 · murs en MAT_Wall 1 · toit 3 · toit rouge/rugueux 1 ·
porte 3 · gouttière métal 2 · lanterne émissive 2 · rendu 1.

## Défis
- **Défi 1 :** une fenêtre en verre : face séparée (ou petit cube aplati) avec *Transmission
  Weight* 1, *Roughness* 0 ; testez en Cycles (EEVEE nécessite des réglages de ray tracing, phase 10).
- **Défi 2 :** reproduisez trois objets de votre bureau (tasse, téléphone, crayon) uniquement
  en primitives et matériaux simples : quelle propriété fait le plus pour la crédibilité ?

## Mini-projet — Le village coloré ⏱ 30 min
Reprenez votre hameau (CH01.05) : 4 matériaux de toit, 3 de murs, portes, une lanterne par
maison. Rendu EEVEE. Grille : cohérence de palette 30 · bon usage Metallic/Roughness 30 ·
affectations propres 20 · nommage 20.

## Tests chronométrés
| Test | Cible |
|---|---|
| Créer un matériau nommé et l'assigner à 2 faces | 30 s |
| Matériau métal crédible | 15 s |
| Copier les matériaux sur 5 objets (`Ctrl+L`) | 10 s |
