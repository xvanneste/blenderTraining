# CH18.07 — Exercices

## Exercice 1 — Facile : traits de contrôle ⏱ 10 min
Avec **Ink Pen** : 10 lignes droites parallèles d'un seul geste, 10 cercles fermés, 10 traits
fin → épais → fin. Objectif : un geste continu, sans repasser.

## Exercice 2 — Moyen : la palette d'un personnage ⏱ 20 min
Créez 6 matériaux nommés pour un personnage : `MAT_GP_Skin`, `MAT_GP_SkinShadow`, `MAT_GP_Hair`,
`MAT_GP_Cloth`, `MAT_GP_ClothShadow`, `MAT_GP_Line`. Peignez un rond de chaque couleur. Changez
ensuite la couleur de `MAT_GP_Cloth` : tous les aplats associés changent.

## Exercice 3 — Difficile : la feuille complète (SANS procédure) ⏱ 40 min
3 bandes × 5 traits avec trois pinceaux différents ; au moins 4 matériaux de couleur ; au moins
8 zones remplies du dessin guide, sans liseré blanc ni débordement.
Validation : `--exercise brushes --render`.

### Grille d'auto-évaluation (sur 20)
| Critère | 0 | 1 | 2 |
|---|---|---|---|
| Trois pinceaux nettement différents | non | 2 | 3 |
| Traits continus (pas de repassage) | non | partiel | oui |
| Variation de pression visible (Ink Pen) | non | faible | nette |
| Matériaux nommés MAT_GP_… | non | partiel | oui |
| Une couleur = un matériau | non | partiel | oui |
| ≥ 8 zones remplies | < 5 | 5–7 | ≥ 8 |
| Aucun débordement | non | 1–2 | aucun |
| Aucun liseré blanc (Dilate) | non | quelques | aucun |
| Aplats sous l'encrage (ordre des calques) | non | — | oui |
| Propreté générale | confus | correct | net |
**≥ 14/20** : acquis.

## Défis
- **Défi 1 :** dessinez une forme **ouverte** (cercle avec une brèche de 1 cm) et réussissez à la
  remplir avec **Gap Closure** sans dessiner de guide.
- **Défi 2 :** matériau `MAT_GP_Dots` avec *Line Type : Dots* : tracez un pointillé de chemin.

## Mini-projet — Personnage encré et mis en couleur ⏱ 1 h 30
Reprenez votre personnage de CH18.04 : SKETCH (Pencil) → LINE (Ink Pen, formes fermées) → COLOR
(Fill, sous LINE) → SHADE (aplats d'ombre). Palette de 6 matériaux au moins. Export : rendu F12
dans `PORTFOLIO/drawing/ch18_07_personnage_couleur.png`.
