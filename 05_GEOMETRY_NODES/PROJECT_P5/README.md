# Projet de phase P5 — « Un outil procédural paramétrable » (ville ou forêt)

**Phase :** 5 — Geometry Nodes · **Durée estimée :** 20 à 30 h · **Évalue :** C05.01 → C05.10

## Brief
Concevez un **outil Geometry Nodes** qui génère une **ville** ou une **forêt** (ou un autre décor de votre choix) à partir de quelques paramètres : une **graine** (`Seed`),
une **densité** (`Density`), un **style** (`Style`) et au moins deux paramètres propres à votre outil (taille, pente, hauteur…). L'outil est **léger** (instances), **borné**,
**publié comme asset** dans un catalogue, et montré par une **planche** de trois réglages différents. Il servira à construire les décors du court-métrage (phases 9 et 15).

## Livrables
1. `PROJECTS/p5_tool/p5_tool_<prenom>_v0NN.blend` : l'objet `GEO_City` (ou `GEO_Forest`) avec un modificateur Geometry Nodes ; l'arbre est un **asset** (description, auteur, licence, ≥ 2 tags, catalogue).
2. `PROJECTS/p5_tool/blender_assets.cats.txt` : le fichier de catalogues (même dossier que le .blend).
3. `PROJECTS/p5_tool/renders/p5_turnaround.png` : trois réglages côte à côte, ≥ 1 600 px de large.
4. `PORTFOLIO/p5/` : l'arbre en capture, les trois réglages commentés, 10 lignes (choix, difficultés, budget).

## Contraintes techniques (vérifiées par `validate_p5.py`, qui RÈGLE les paramètres de votre outil)
1. **Interface** : `Seed` (Integer, min ≥ 0), `Density` (Float, 0–1), `Style` (Integer, 0 à ≥ 2) + **au moins deux autres entrées** ; chaque entrée a une description ; bornes finies (≤ 1 000), défauts dans les bornes.
2. **Arbre** : **pas de Realize Instances** ; la géométrie d'entrée est **conservée** (Join Geometry) ; ≤ 60 nœuds ; arbre utilisable comme **modificateur**.
3. **Comportement** (mesuré sur les instances évaluées) : par défaut 20 à 5 000 instances ; **Seed + 1** → au plus 50 % d'instances identiques ; **Density 0,3 → 0,9** → au moins 1,8 fois plus d'instances ;
   **Style 0 → 2** → des géométries de hauteurs différentes ; emprise ≤ 500 m ; **budget** : ≤ 20 000 instances quand tous les paramètres (sauf Seed et Style) sont à leur maximum.
4. **Publication** : l'arbre est marqué comme asset ; description, auteur, licence, ≥ 2 tags ; catalogue présent dans `blender_assets.cats.txt`.
5. **Planche** non noire et contrastée.

## Vérification
```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "PROJECTS\p5_tool\p5_tool_<prenom>_v001.blend" `
  --python-exit-code 1 --python "05_GEOMETRY_NODES\PROJECT_P5\validate_p5.py" -- --debug
```
Le correcteur est testé par `python 05_GEOMETRY_NODES/PROJECT_P5/test_p5.py` (référence acceptée ; neuf variantes fausses refusées).

## Référence
`REFERENCE/p5_tool_reference.blend` (+ `blender_assets.cats.txt`, `renders/p5_turnaround.png`) : outil « Mini-ville » produit par `build_p5_reference.py` : parcelles (Lots × Lots, Lot Size), sélection par Random Value
(Density, Seed), trois bâtiments (immeuble 8 × 8 × 12, tour 5 × 5 × 28, barre 14 × 5 × 8) choisis par Style, échelle verticale aléatoire, instances conservées. Validée 67/67.
**Limites honnêtes** : bâtiments réduits à des boîtes grises, pas de routes ni de parcs, composition au hasard ; une seule échelle de ville. Les mesures du correcteur ne jugent pas l'urbanisme.
Un piège rencontré : une entrée multiple de **Geometry to Instance** est lue en sens **inverse** de l'ordre de création des liens (l'indice 0 était la dernière géométrie reliée) ; vérifiez avec le correcteur (Style 0 → 2).
Ne copiez pas la référence : concevez votre propre outil.

## Grille d'évaluation (sur 100)
| Critère | Points | Comment l'évaluer |
|---|---|---|
| Contraintes techniques (score du correcteur) | 30 | Score ramené sur 30 |
| Qualité du résultat (crédibilité du décor, variété des styles) | 20 | Les trois réglages de la planche |
| Contrôle artistique (paramètres utiles, plages sensées, défauts agréables) | 15 | Essai de l'outil |
| Optimisation (instances, budgets, bornes) | 10 | Spreadsheet, nombre d'instances |
| Lisibilité de l'arbre (frames, noms, groupes) | 10 | Capture de l'arbre |
| Publication (asset, catalogue, descriptions, usage depuis un autre fichier) | 10 | Asset Browser |
| Documentation (fiche d'utilisation, 10 lignes) | 5 | PORTFOLIO |
**Phase 5 validée si ≥ 70/100** et tous les quiz de la phase ≥ 80 %.

## Conseils de méthode
1. Fixez d'abord l'interface (nom, type, bornes), puis construisez l'arbre autour.
2. Testez chaque paramètre isolément : changez-le et regardez le Spreadsheet.
3. Gardez les instances ; réalisez seulement ce qui doit l'être.
4. Publiez tôt (dès que l'outil marche) et améliorez en gardant le même nom d'asset.
5. Comparez trois graines : si elles se ressemblent trop, augmentez la variation.
