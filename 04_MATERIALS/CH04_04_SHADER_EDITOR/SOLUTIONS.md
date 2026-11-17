# CH04.04 — Solutions

<!-- QUIZ_ANSWERS_START -->
## Réponses du quiz

| Q | Réponse | Explication |
|---|---|---|
| Q1 | **b** — De gauche à droite : des entrées vers le Material Output | Les sorties (à droite d'un nœud) alimentent les entrées (à gauche) du nœud suivant ; le résultat final arrive au Material Output. |
| Q2 | **b** — Il déplace, tourne et met à l'échelle des coordonnées avant une texture | Mapping transforme le vecteur de coordonnées (Location, Rotation, Scale) transmis à la texture. |
| Q3 | **a** — Object | La sortie Object donne les coordonnées locales de l'objet : la texture le suit. |
| Q4 | — | Un nœud dont aucune sortie n'est reliée : il ne sert à rien, alourdit le graphe et trompe le lecteur ; on le supprime ou on le relie. |
| Q5 | — | Le facteur choisit entre A (facteur 0) et B (facteur 1) ; avec un facteur intermédiaire, le résultat est un mélange. |
| Q6 | **b** — Elle convertit une valeur 0–1 en couleur et durcit la transition entre zones | On resserre les deux stops pour passer de gradients mous à des plaques nettes (ici 0,45 et 0,62). |
| Q7 | **a** — Pour que le métal apparaisse là où il n'y a pas de rouille | La rouille n'est pas métallique : le même masque pilote la couleur et Metallic, donc ils restent cohérents. |
| Q8 | — | Elle convertit la plage utile du bruit (ici 0,3–0,7) en plage de rugosité voulue (0,25–0,85). |
| Q9 | — | Les taches deviennent minuscules : aspect « sel et poivre », sans zones lisibles ; le correcteur exige 2 à 30. |
| Q10 | — | Un graphe court est lisible et maintenable ; au-delà, regrouper en Frame ou Node Group (voir la suite). |
<!-- QUIZ_ANSWERS_END -->

## Exercice 2
`COMPLETED_EXAMPLES/ch04_04_nodes_solution.blend` (+ `_reference.png`).

**Fabrication.** Générée par script (`build_ch04_04_files.py`) : nœuds créés avec l'API (`nodes.new`, `links.new`), valeurs du tableau de THEORY.md §3. Score du correcteur 25/25 ; starter 7/25.
Rendu regardé : plaques de rouille orangée sur un acier gris clair, lisibles dans les deux vues. Une première version avait l'ordre A/B inversé (la rampe donnait du métal sur la rouille) : corrigé.

## Contre-épreuve du correcteur (`COMPLETED_EXAMPLES/COUNTER_EXAMPLES/`)
| Fichier faux | Défaut | Test qui le refuse |
|---|---|---|
| `…_orphan` | un Noise sans sortie utilisée | « Aucun nœud orphelin » (seul test en échec) |
| `…_const_metal` | Metallic constant à 1 | « Metallic piloté » (seul) |
| `…_no_mapping` | Mapping retiré | « Noise : coordonnées via Texture Coordinate → Mapping » (seul) |
| `…_no_output` | BSDF non relié à la sortie | « BSDF relié à Surface » et « orphelin » (même défaut) |
| `…_flat_ramp` | stops de même couleur | « Color Ramp : écart de luminance » (seul) |
| `…_huge_scale` | Noise Scale 400 | « Noise Scale » (seul) |
Aussi refusé : le starter.

## Limites
- Structure et valeurs, pas l'apparence ; le correcteur ne lit que le premier Noise relié à Base Color.
- Les groupes de nœuds (Node Groups) ne sont pas traversés.
