# CH02.01 — Exercices

## Exercice 1 — Facile : lire une topologie ⏱ 10 min
Ajoutez : Cube, UV Sphere, Ico Sphere, Cylinder, Torus, Monkey. Pour chacun, notez (Statistics +
*Faces by Sides*) le nombre de faces, de triangles, de quads et de n-gons. Lequel est 100 % quads ?

## Exercice 2 — Moyen : déplacer un pôle ⏱ 20 min
Sur une grille 7 × 7 (*Add → Mesh → Grid*, X et Y Subdivisions = 7 : une face au centre), insérez une face (`I`) au centre puis extrudez-la : repérez les 8 pôles
créés aux coins de l'inset (4 à l'extérieur, 4 à l'intérieur). Avec *Vertex Slide* (`Shift+V`) et *Dissolve*, déplacez un pôle vers un
endroit plat. Comparez le résultat avec et sans modificateur Subdivision Surface (`Ctrl+2`).

## Exercice 3 — Difficile : la clinique (SANS procédure) ⏱ 25 min
Réparez les 4 patients et posez le diagnostic des pôles. Validation : `--exercise clinic --render`.

### Grille d'auto-évaluation (sur 20)
| Critère | 0 | 1 | 2 |
|---|---|---|---|
| Défaut de chaque patient identifié AVANT réparation | < 3 | 3–4 | 5 |
| Outil de sélection adapté (Faces by Sides, Non Manifold) | non | partiel | oui |
| N-gon remplacé, contour intact | non | contour modifié | oui |
| Triangles regroupés (≥ 80 % quads) | non | partiel | oui |
| Doublons fusionnés, surface fermée | non | partiel | oui |
| Trou bouché sans arête non-manifold | non | partiel | oui |
| Pôles comptés juste | non | ±2 | exact |
| Explication : pourquoi un pôle sur une articulation pose problème | non | floue | claire |
| Statistics utilisées pour vérifier | non | — | oui |
| Temps < 25 min | > 40 | 25–40 | < 25 |
**≥ 14/20** : acquis.

## Défis
- **Défi 1 :** importez (File → Import) un modèle OBJ libre (CC0) téléchargé **par vous** ;
  diagnostiquez-le avec la méthode du chapitre et rédigez 5 lignes de rapport.
- **Défi 2 :** activez l'overlay **Mesh Analysis** sur un modèle, type *Distortion* : à quoi
  correspondent les zones colorées ?

## Mini-projet — Fiche de validation d'un asset ⏱ 45 min
Rédigez la checklist que vous appliquerez à tous vos assets (phase 2 et suivantes) : 10 points
vérifiables dans Blender (quads, n-gons, doublons, non-manifold, échelle, origine, nommage, normales,
transformations appliquées, densité). Enregistrez-la dans `PROJECTS/checklist_asset.md` : elle
servira au projet P2.
