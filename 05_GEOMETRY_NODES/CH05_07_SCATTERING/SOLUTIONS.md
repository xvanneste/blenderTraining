# CH05.07 — Solutions

<!-- QUIZ_ANSWERS_START -->
## Réponses du quiz

| Q | Réponse | Explication |
|---|---|---|
| Q1 | **a** — Avec la composante Z de la normale (Normal Z) : 1 = plat, 0 = vertical | Pour une normale unitaire, Normal Z = cos(angle de pente). |
| Q2 | **b** — Une pente ≤ Max Slope équivaut à Normal Z ≥ cos(Max Slope) | Math : Radians → Cosine → Greater Than avec Normal Z → Density Factor (0 ou 1). |
| Q3 | **a** — Sur le terrain déplacé fourni à Distribute | La normale doit être celle du terrain après Set Position : on distribue sur le terrain déplacé. |
| Q4 | — | Pour vérifier que les arbres sont posés sur le terrain (points issus de Distribute) et pas translatés ; 0,003 m mesurés dans la solution. |
| Q5 | — | Qu'en réduisant la pente maximale à 10°, le nombre d'arbres baisse (123 au lieu de 187) et qu'aucun arbre n'est sur une pente supérieure à 13°. |
| Q6 | **b** — Geometry to Instance | Geometry to Instance reçoit plusieurs géométries (multi-entrée) et les range comme instances numérotées. |
| Q7 | **a** — Il choisit l'une des instances de l'entrée Instance selon Instance Index (champ) pour chaque point | Avec Pick Instance activé, Instance Index (ici Random Value entier 0–2) choisit la variante de chaque arbre. |
| Q8 | — | Contrairement au Cylinder (centré), le Cone du nœud a sa base à z = 0 (mesuré : z de 0 à Depth) : un Transform de Depth ÷ 2 le ferait flotter (contre-exemple « floating »). |
| Q9 | — | Que Seed est branché à Distribute : avec Seed 7, ≤ 20 % des arbres coïncident avec ceux du réglage par défaut (1 % mesuré) ; sans branchement, 100 % coïncident. |
| Q10 | — | Multiplier le masque de pente par un second masque (distance au centre > rayon de la clairière) avant Density Factor. |
<!-- QUIZ_ANSWERS_END -->

## Exercice 2
`COMPLETED_EXAMPLES/ch05_07_scattering_solution.blend` (+ `_reference.png`).

**Fabrication.** Générée par script (`build_ch05_07_files.py`). Score du correcteur 39/39 ; starter 3/7 (interface absente : arrêt anticipé).
Mesures : voir THEORY.md §5 (187 arbres par défaut ; Seed 7 → 200 dont 1 % identiques ; Density 0,25 → 108 ; Max Slope 10 → 123).
Rendu regardé : forêt de cônes de trois tailles sur un terrain vallonné, posés sur la surface ; cadrage élargi.

**Ce que le développement a appris** : (1) le nœud Cone a sa base à z = 0 : ma première version translatait les cônes de Depth ÷ 2 et les faisait flotter ; le contre-exemple « floating » passait d'abord 36/36 jusqu'à l'ajout de la mesure de la base ; (2) `bound_box` d'un objet d'instance n'est pas la géométrie de la variante choisie : lire les sommets de `inst.object.data` ; (3) un masque de pente inactif passe tous les tests de défaut (le terrain n'est jamais plus raide que 20°) : seul le test « Max Slope 10 » le détecte.

## Contre-épreuve du correcteur (`COMPLETED_EXAMPLES/COUNTER_EXAMPLES/`)
| Fichier faux | Défaut | Test qui le refuse (et lui seul) |
|---|---|---|
| `…_no_slope` | masque de pente non branché | Max Slope 10 (187 arbres, pente max 20,2°) |
| `…_no_variation` | une seule variante d'arbre | Variantes d'arbres (1) |
| `…_seed_unused` | Seed exposé mais non branché | Seed 7 (100 % identiques) |
| `…_no_scale` | Scale non alimenté | Échelles variées (0,000) |
| `…_floating` | cônes relevés de 0,5 m (arbres flottants) | Base des arbres (0,60 m) |
Aussi refusé : le starter.

## Limites
- Les seuils (33°, 30–70 %, 80 %) sont calibrés sur la graine et le terrain de l'exercice.
- Pas d'évaluation esthétique ; pas de test de collision entre houppiers.
