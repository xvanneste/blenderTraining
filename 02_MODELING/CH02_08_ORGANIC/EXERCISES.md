# CH02.08 — Exercices

## Exercice 1 — Facile : blocking en 10 minutes ⏱ 10 min
Avec uniquement des sphères, cylindres et cubes mis à l'échelle, bloquez un personnage de 1,75 m
(tête, cage thoracique, bassin, membres — proportions de CH18.03). Jugez la silhouette en vue
caméra, objet par objet en noir (*Viewport Shading → Flat*, couleur unie).

## Exercice 2 — Moyen : le champignon (box modeling) ⏱ 30 min
Cube + Subdivision (`Ctrl+2`) : chapeau par extrusion et mise à l'échelle des faces du haut, pied
par extrusion vers le bas, lamelles par Inset sous le chapeau. *To Sphere* (`Shift+Alt+S`) pour
arrondir le chapeau, édition proportionnelle (`O`) pour une asymétrie naturelle. 100 % quads.

## Exercice 3 — Difficile : l'arbre (SANS procédure) ⏱ 25 min
Squelette (≥ 10 sommets, ≥ 2 embranchements, ≥ 1,5 m), Skin puis Subdivision, rayons de la base
aux pointes (rapport ≥ 2,5). Validation : `--exercise tree --render`.

### Grille d'auto-évaluation (sur 20)
| Critère | 0 | 1 | 2 |
|---|---|---|---|
| Squelette sans faces, bien connecté | non | partiel | oui |
| Embranchements naturels (pas de croix parfaite) | non | partiel | oui |
| Branches courbées (plusieurs segments) | non | quelques | toutes |
| Racines | non | — | oui |
| Rayons dégressifs | non | irréguliers | oui |
| Skin au-dessus de Subdivision | non | — | oui |
| Branch Smoothing réglé | non | — | oui |
| Silhouette lisible en vue de face | non | moyenne | oui |
| Asymétrie maîtrisée | non | — | oui |
| Temps < 25 min | > 40 | 25–40 | < 25 |
**≥ 14/20** : acquis.

## Défis
- **Défi 1 :** *Skin Armature Create* (bouton du modificateur Skin, ou `F3`) : générez l'armature
  de l'arbre et pliez une branche en Pose Mode (aperçu de la phase 6).
- **Défi 2 :** une pieuvre stylisée : corps par Skin, 8 tentacules effilés, symétrie X du Skin.

## Mini-projet — La créature ⏱ 2 h
Une créature simple (quadrupède ou serpent à bras) par Skin : blocking, squelette, rayons,
Subdivision. Rendu de face et de profil. Elle servira de base de sculpture en phase 3.
