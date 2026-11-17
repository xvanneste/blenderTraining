# CH04.02 — Solutions

<!-- QUIZ_ANSWERS_START -->
## Réponses du quiz

| Q | Réponse | Explication |
|---|---|---|
| Q1 | **b** — Un carré UV [0,1]² avec sa propre image | Chaque tuile a sa propre texture ; l'objet les utilise toutes. |
| Q2 | **b** — 1002 | Numéro = 1001 + ⌊u⌋ + 10·⌊v⌋ : ici 1001 + 1 = 1002. |
| Q3 | **b** — 1011 | 1001 + 0 + 10 = 1011. |
| Q4 | — | Pack Islands remplit le carré [0,1]² avec les îlots sélectionnés ; on obtient ainsi un groupe qui occupe bien sa tuile, qu'on translate ensuite d'une unité (G, X, 1). |
| Q5 | — | Une partie de l'îlot lit une image et l'autre une autre : coupure visible sur le modèle, et les outils de peinture et de baking sont perdus. |
| Q6 | **b** — UDIM Tiles | Image Texture > Source : UDIM Tiles (en API : source = TILED). |
| Q7 | — | La tuile manquante s'affiche en magenta ou noir ; le correcteur exige que l'image possède toutes les tuiles utilisées. |
| Q8 | — | Choix de production : plus de résolution sur le couvercle (ici 1,5×) ; l'important est qu'elle soit uniforme DANS une tuile et que la différence soit voulue. |
| Q9 | — | 76 % pour la tuile 1001 et 74 % pour la tuile 1002 (le correcteur exige ≥ 40 %). |
| Q10 | — | Quand une seule texture dépasse la mémoire ou la taille voulue, ou quand différents artistes peignent différentes parties (corps, visage, vêtements) sur des tuiles séparées. |
<!-- QUIZ_ANSWERS_END -->

## Exercice 2
`COMPLETED_EXAMPLES/ch04_02_udim_solution.blend` (+ `_reference.png` ; `_uv_layout.png`).

**Fabrication.** Générée par script (`build_ch04_02_files.py`), qui réutilise la géométrie et les opérateurs de CH04.01 : dépliage global (seams, Unwrap, Average Islands Scale), puis `uv.pack_islands` PAR GROUPE
(index de matériau 0 : corps + sangles ; 1 : couvercle) et translation de +1 en U du couvercle. Image `UDIM_Grid` (tuiles 1001 et 1002, motif UV Grid).

Mesures du correcteur : tuiles [1001, 1002], 0 îlot à cheval, image [1001, 1002]. Tuile 1001 : étirement 1,00, densité 0,00, chevauchement 0 %, occupation 76 %. Tuile 1002 : étirement 1,00, densité 0,001, chevauchement 0 %, occupation 74 %.
Densité du couvercle ≈ 1,5× celle du corps (longueur 3D / UV : 2,375 et 1,566). Score 33/33. Starter : une seule tuile → 21/24.

## Contre-épreuve du correcteur (`COMPLETED_EXAMPLES/COUNTER_EXAMPLES/`)
| Fichier faux | Défaut | Test qui le refuse (et lui seul) |
|---|---|---|
| `…_straddle` | un îlot du corps centré sur u = 1 | 1 îlot à cheval |
| `…_single_tile` | tout en 1001 | tuiles utilisées ([1001]) |
| `…_missing_tile` | l'image n'a que la tuile 1001 | tuile 1002 absente de l'image |
| `…_overlap_tile` | deux îlots du corps superposés | chevauchement dans la tuile 1001 (86 %) |
Aussi refusé : le starter.

**Ce que le développement a appris** :
1. l'index de matériau « couvercle » assigné par l'ORDRE des faces était faux (le `bisect` réordonne) : le couvercle apparaissait éparpillé en lamelles dans l'éditeur UV ; on l'assigne par géométrie (sommets sur le cylindre) ;
2. deux contre-exemples étaient mal construits : « à cheval » ne chevauchait aucune frontière (il passait 33/33) et « chevauchement » débordait sur une tuile 1012 ; refaits (centrage sur u = 1 ; superposition de deux îlots du corps) ;
3. les tuiles créées par `img.tiles.new` ont une taille nulle jusqu'à leur premier usage (générées paresseusement) : sans effet au rendu.

## Limites
- Le correcteur ne juge pas la répartition des parties entre tuiles ni la résolution des images.
- Il détecte les tuiles en rangée v = 0 et au-delà (formule générale), mais l'image doit en posséder les numéros exacts.
- La mesure de chevauchement est rastérisée (1024² par tuile).
