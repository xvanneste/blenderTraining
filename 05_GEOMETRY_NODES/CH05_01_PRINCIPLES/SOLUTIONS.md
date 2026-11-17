# CH05.01 — Solutions

<!-- QUIZ_ANSWERS_START -->
## Réponses du quiz

| Q | Réponse | Explication |
|---|---|---|
| Q1 | **b** — De la géométrie (maillage, courbes, instances…) | Les sockets de géométrie (en vert-turquoise) transportent la géométrie de nœud en nœud jusqu'au Group Output. |
| Q2 | **b** — Une valeur calculée pour chaque point, face ou arête au moment où un nœud la lit | Un champ (par exemple un bruit ou la position) est évalué en chaque élément de la géométrie qui le consomme. |
| Q3 | **b** — Grid | Le nœud Grid (GeometryNodeMeshGrid) crée un maillage plan : taille et nombre de sommets. |
| Q4 | — | Son vecteur d'entrée par défaut est la position du point ; Set Position l'évalue en chaque sommet, d'où un déplacement différent partout. |
| Q5 | — | Il déplace chaque point de la valeur du champ Offset (un vecteur) : ici (0, 0, (bruit − 0,5) × 2). |
| Q6 | **b** — La géométrie générée n'hérite pas des matériaux du maillage d'origine | Un arbre qui remplace la géométrie produit un maillage sans matériaux : on assigne le matériau dans l'arbre. |
| Q7 | **b** — Lisse l'ombrage des faces sans changer la forme | Il active l'ombrage lisse : le terrain paraît continu sans polygones supplémentaires. |
| Q8 | — | Nombre de sommets (2 500–20 000), emprise 10 × 10 m, écart-type et étendue de Z, part de faces lisses, présence de MAT_Terrain. |
| Q9 | — | Une amplitude démesurée (ici ×20, étendue de 8 m) casse l'échelle du décor ; le correcteur exige 0,2–2,5 m d'étendue de Z. |
| Q10 | — | Avec le Spreadsheet (valeurs par élément) et le nœud Viewer (visualisation dans la vue 3D) ; l'arbre doit rester évalué. |
<!-- QUIZ_ANSWERS_END -->

## Exercice 2
`COMPLETED_EXAMPLES/ch05_01_principles_solution.blend` (+ `_reference.png`).

**Fabrication.** Générée par script (`build_ch05_01_files.py`) : arbre `GN_Terrain` créé par l'API (`GeometryNodeTree`, nœuds Grid, Set Position, Noise Texture, Math, Combine XYZ, Set Shade Smooth, Set Material, Group Output) ; objet `GEO_Terrain` surélevé de 0,8 m. Score du correcteur 34/34 ; starter 8/34.
Mesures évaluées : 10 000 sommets, emprise 10 × 10 m, écart-type de Z 0,139 m, étendue 0,84 m, 100 % lisse, MAT_Terrain.
Rendu regardé : un relief doux continu, deux vues cohérentes. Deux défauts corrigés avant validation : surface blanche (Set Material manquant) et terrain à moitié sous le sol.

## Contre-épreuve du correcteur (`COMPLETED_EXAMPLES/COUNTER_EXAMPLES/`)
| Fichier faux | Défaut | Tests qui le refusent |
|---|---|---|
| `…_flat` | Offset non alimenté (terrain plat) | champ Offset ; écart-type et étendue de Z (même défaut) |
| `…_no_smooth` | sans Set Shade Smooth | Set Shade Smooth ; part de faces lisses (même défaut) |
| `…_no_material` | sans Set Material | Set Material ; matériau évalué (même défaut) |
| `…_coarse` | Grid 8 × 8 | Grid ≥ 50 × 50 ; nombre de sommets évalués (même défaut) |
| `…_huge_amp` | amplitude 20 (étendue 8,4 m) | Étendue de Z (seul) |
| `…_orphan` | un nœud Cube inutilisé | Aucun nœud orphelin (seul) |
Aussi refusé : le starter.

## Limites
- Contrôle du graphe et de mesures évaluées ; aucune appréciation esthétique.
- Un seul modificateur Nodes est lu (le premier).
