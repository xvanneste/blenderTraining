# CH02.12 — Exercices

## Exercice 1 — Facile : la checklist d'un personnage ⏱ 10 min
Pour un personnage de 1,75 m : listez 8 vérifications avant de le confier au rigging (échelle,
transformations, origine, orientation, pose, boucles d'articulation, pôles, symétrie). Ajoutez-les à
`PROJECTS/checklist_asset.md`.

## Exercice 2 — Moyen : genou et cheville ⏱ 25 min
Une jambe (cylindre de 90 cm, cuisse + mollet + pied extrudé) : 3 boucles au genou, 3 à la cheville,
armature à 3 os. Pliez le genou à 120° et la cheville à 30° : pas d'écrasement visible.

## Exercice 3 — Difficile : le coude (SANS procédure) ⏱ 10 min
Validation : `--exercise arm --render` (volume conservé ≥ 95 % à 90°).

### Grille d'auto-évaluation (sur 20)
| Critère | 0 | 1 | 2 |
|---|---|---|---|
| Problème constaté avant correction | non | — | oui |
| ≥ 3 boucles ajoutées au coude | non | 1–2 | ≥ 3 |
| Boucles resserrées vers le pli | non | partiel | oui |
| Anneaux continus (quads) | non | — | oui |
| Volume ≥ 95 % | non | — | oui |
| Aucune géométrie inutile ailleurs | non | partiel | oui |
| Échelle 1, dimensions réelles | non | — | oui |
| Enregistré en pose de repos | non | — | oui |
| Test de pliage fait dans Blender | non | — | oui |
| Temps < 10 min | > 20 | 10–20 | < 10 |
**≥ 14/20** : acquis.

## Défis
- **Défi 1 :** pliez à 140° : à partir de quel angle faut-il des boucles supplémentaires ?
- **Défi 2 :** ajoutez une boucle « de muscle » (biceps) et observez le volume à l'intérieur du pli.

## Mini-projet — La main ⏱ 2 h
Main simplifiée (paume + 5 doigts à 3 phalanges) en box modeling : 3 boucles par articulation de
doigt, armature de test, poing fermé sans écrasement. Base du rig de la phase 6.
