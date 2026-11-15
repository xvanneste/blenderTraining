# CH02.11 — Exercices

## Exercice 1 — Facile : où couper ? ⏱ 10 min
Sur papier ou en commentaire : proposez les coutures d'un cube (patron en croix), d'un cône, d'une
sphère (UV Sphere), d'un tore. Vérifiez ensuite dans Blender avec Mark Seam + Unwrap et le damier.

## Exercice 2 — Moyen : le tabouret de CH02.02 ⏱ 25 min
Dépliez votre tabouret : coutures sous l'assise et à l'arrière des pieds, Unwrap, *Average Islands
Scale*, Pack Islands. Damier régulier, pas d'île superposée.

## Exercice 3 — Difficile : caisse et boîte (SANS procédure) ⏱ 15 min
Validation : `--exercise uv --render`.

### Grille d'auto-évaluation (sur 20)
| Critère | 0 | 1 | 2 |
|---|---|---|---|
| Méthode adaptée à chaque objet | non | partiel | oui |
| Coutures cachées (dessous, arrière) | non | partiel | oui |
| 3 îles pour la boîte | non | — | oui |
| Damier carré (pas d'étirement) | non | partiel | oui |
| Pas d'îles superposées | non | — | oui |
| UV dans 0–1, Pack Islands | non | — | oui |
| Marges entre îles | non | — | oui |
| Densité de texels comparée | non | — | oui |
| Workspace UV Editing utilisé | non | — | oui |
| Temps < 15 min | > 30 | 15–30 | < 15 |
**≥ 14/20** : acquis.

## Défis
- **Défi 1 :** UV Sphere : comparez Unwrap (couture méridienne) et Sphere Projection ; où est
  l'étirement ?
- **Défi 2 :** route sinueuse (plan découpé) : *Follow Active Quads* pour un marquage continu.

## Mini-projet — Déplier trois props ⏱ 1 h
Trois props de votre collection `PROPS` (CH02.02–CH02.08) : dépliage propre, densité de texels
uniforme entre eux (Average Islands Scale sur les trois), damier contrôlé. Préparation de la phase 4.
