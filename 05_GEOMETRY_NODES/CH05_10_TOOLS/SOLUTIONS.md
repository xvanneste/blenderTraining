# CH05.10 — Solutions

<!-- QUIZ_ANSWERS_START -->
## Réponses du quiz

| Q | Réponse | Explication |
|---|---|---|
| Q1 | **b** — Le nombre de sommets de la géométrie instanciée multiplié par le nombre d'instances, surtout si elles sont réalisées | 64 côtés × 2 000 instances réalisées = 252 504 triangles ; 8 côtés instanciés = 14 triangles partagés. |
| Q2 | **b** — Il les convertit en géométrie propre : chaque copie a ses sommets | On ne réalise que si la suite exige une géométrie réelle (booléen, export, déformation par copie). |
| Q3 | **b** — Pour qu'un utilisateur ne puisse pas demander 400 001 instances par erreur (mesuré avec 1 000) | Une borne est une protection : 5/m² × 400 m² ≈ 2 000 instances. |
| Q4 | — | Garder des instances ; réduire la géométrie instanciée ; borner les paramètres coûteux ; éviter les nœuds évalués inutilement ; réutiliser des attributs plutôt que recalculer. |
| Q5 | — | Dans un script en arrière-plan le temps mesuré est trompeur (évaluation paresseuse et mise en cache : 0,001 s même pour 400 001 instances) ; le nombre de sommets, d'instances et de triangles est reproductible. |
| Q6 | **a** — is_modifier (option Modifier de l'arbre) | `node_group.is_modifier` : l'arbre apparaît dans le menu Add Modifier > Geometry Nodes ; `is_tool` est une autre option (outils d'édition). |
| Q7 | **b** — La recevoir et la conserver (Join Geometry), en y ajoutant son résultat | Sinon le maillage de l'objet disparaît quand on applique l'outil (contre-exemple « ignores_input » : 0 sommet de base). |
| Q8 | — | Description, auteur, licence, au moins 2 tags et un catalogue présent dans blender_assets.cats.txt. |
| Q9 | — | Blender écrit les catalogues dans blender_assets.cats.txt, à côté du .blend de la bibliothèque : les assets y font référence par un identifiant (UUID). |
| Q10 | — | Dans l'Asset Browser (catalogue « Tools/Scatter ») si le dossier est une bibliothèque déclarée ; en glissant l'asset sur l'objet ou via le menu des modificateurs. |
<!-- QUIZ_ANSWERS_END -->

## Exercice 2
`COMPLETED_EXAMPLES/ch05_10_tools_solution.blend` (+ `blender_assets.cats.txt`, `_reference.png`).

**Fabrication.** Générée par script (`build_ch05_10_files.py`) : arbre allégé (cône de 8 côtés, instances conservées, Density 0,05–5, défaut 0,5), `is_modifier = True`, `asset_mark()` avec description, auteur, licence, tags « scatter » et « instances », `catalog_id` = identifiant du catalogue « Tools/Scatter ». Score du correcteur 43/43 ; starter 16/44.
Mesures : voir THEORY.md §2. Rendu regardé : des cônes verts dispersés sur la grille, deux vues cohérentes.

## Contre-épreuve du correcteur (`COMPLETED_EXAMPLES/COUNTER_EXAMPLES/`, avec leur propre `blender_assets.cats.txt`)
| Fichier faux | Défaut | Tests qui le refusent |
|---|---|---|
| `…_heavy_cone` | cône de 64 côtés (65 sommets) | Sommets par instance ; triangles à Density max (252 504) |
| `…_realized` | Realize Instances présent | Pas de Realize Instances ; plus d'instances (mesures : conséquences) |
| `…_unbounded` | Density max 1000 | Borne de Density ; budget à Density max (400 001 instances) |
| `…_not_asset` | arbre non marqué comme asset | Asset ; métadonnées ; catalogue (même défaut) |
| `…_no_catalog` | catalogue vide | Catalogue (seul) |
| `…_not_modifier` | is_modifier = False | is_modifier (seul) |
| `…_ignores_input` | Join sans la géométrie d'entrée | Entrée conservée ; grille de base absente (même défaut) |
Aussi refusé : le starter.

## Limites
- Budgets de géométrie, pas de chronométrage ; pas de test d'affichage dans l'Asset Browser.
- Le matériau de l'arbre (MAT_Cone) vit dans le fichier ; un asset réutilisable doit l'embarquer ou le recréer.
