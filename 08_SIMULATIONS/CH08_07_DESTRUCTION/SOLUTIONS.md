# CH08.07 — Solutions

<!-- QUIZ_ANSWERS_START -->
## Réponses du quiz

| Q | Réponse | Explication |
|---|---|---|
| Q1 | **a** — Fixed | Fixed bloque tous les degrés de liberté. |
| Q2 | **a** — Breaking | Panneau Settings : Breaking et Threshold. |
| Q3 | **a** — La liaison résiste à un choc plus fort | Au-dessus du seuil la liaison saute. |
| Q4 | — | Pour que chaque brique tienne à tous ses voisins ; avec 38 liaisons, le mur reste une pièce unique tant qu'aucune ne saute. |
| Q5 | — | L'extension n'est pas fournie avec Blender 5.3 (extensions de base) : nous partons de pièces séparées, sans prétendre que Cell Fracture marche. |
| Q6 | **a** — 1 | Mesuré : seuil ≤ 2 : 12 à 13 liaisons cassées ; seuil ≥ 5 : 0. |
| Q7 | **a** — Distance entre voisines modifiée de plus de 10 cm | L'API ne marque pas la rupture (enabled reste vrai) : on mesure les positions. |
| Q8 | — | Le mur explose : les briques traversent le sol (mesuré : z jusqu'à −68 m avec 5 m/s et 10 sous-étapes) ; ralentir le boulet et monter les sous-étapes à 30. |
| Q9 | — | Un seuil de 20 : aucune liaison ne casse, le mur est poussé d'un bloc (5 m plus loin, à plat) : pas de destruction. |
| Q10 | — | Les simulations de corps rigides ne s'avancent qu'image par image depuis l'image 1 : le correcteur les rejoue de façon déterministe. |
<!-- QUIZ_ANSWERS_END -->

## Exercices
`COMPLETED_EXAMPLES/ch08_07_destruction_solution.blend` (+ `_reference.png`)

**Fabrication.** Générées par script (`build_ch08_07_files.py`) : sol, briques, boulet, 38 contraintes par l'opérateur Connect, variantes. Score 47/47 ; starter 35/47. Vue de dessus regardée.

## Contre-épreuve du correcteur (`COMPLETED_EXAMPLES/COUNTER_EXAMPLES/`)
| Fichier faux | Défaut | Tests qui le refusent |
|---|---|---|
| `…_no_breaking` | contraintes sans Breaking : le mur est poussé d'un bloc (0 liaison cassée) | contraintes cassables ; fracture |
| `…_high_threshold` | seuil de 20 : rien ne casse (0 liaison cassée) | contraintes cassables (seuil) ; fracture |
| `…_no_constraints` | aucune contrainte : les briques se dispersent séparément | contraintes ; contraintes cassables |
| `…_no_ground` | le sol n'est pas un corps rigide : tout tombe à l'infini | sol ; sous le sol ; distance |
Aussi refusé : le starter.

## Limites
- Cell Fracture non disponible dans la 5.3 de base.
- Rupture mesurée indirectement.
- Instabilité à haute vitesse non expliquée.
