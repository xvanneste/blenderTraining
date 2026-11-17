# CH05.02 — Solutions

<!-- QUIZ_ANSWERS_START -->
## Réponses du quiz

| Q | Réponse | Explication |
|---|---|---|
| Q1 | **b** — Join Geometry | Join Geometry fusionne les géométries reçues en une seule sortie (les pièces restent des composantes séparées). |
| Q2 | **b** — Transform avec Translation z = 1,5 | Transform reçoit une géométrie et applique Translation, Rotation, Scale. |
| Q3 | **b** — Au milieu de sa hauteur, sur l'origine | Le Cylinder est centré sur l'origine : un fût de 2,6 m s'étend de −1,3 à +1,3 ; Translation z = 1,5 le place de 0,2 à 2,8. |
| Q4 | — | Fût, base, chapiteau et anneau sont quatre pièces fermées qui ne partagent pas de sommets : Join Geometry les met dans un seul maillage sans les souder. |
| Q5 | — | 2,6 m : de z = 0,2 (sommet de la base) à z = 2,8 (dessous du chapiteau). |
| Q6 | **a** — Il extrude la section le long de la courbe pour produire un maillage | La courbe est le chemin, le profil la section : un cercle de 5 cm le long d'un cercle de 33 cm donne un tore. |
| Q7 | **b** — Un objet posé doit reposer sur le sol : les dimensions sont réelles | Les décors (CH05.07, CH05.08) placent les objets sur le sol à z = 0. |
| Q8 | — | Une pièce décalée en X ou Y (chapiteau de +0,2 m) : l'emprise dépasse 1,0 m et le centre sort de l'axe Z. |
| Q9 | — | Il laisserait un trou entre la base et le chapiteau : le correcteur mesure la hauteur de la composante cylindrique (≥ 2,4 m). |
| Q10 | — | Les dimensions deviennent des paramètres : hauteur, rayon, résolution se changent sans rien refaire, et l'arbre se réutilise (CH05.06). |
<!-- QUIZ_ANSWERS_END -->

## Exercice 2
`COMPLETED_EXAMPLES/ch05_02_procedural_solution.blend` (+ `_reference.png`).

**Fabrication.** Générée par script (`build_ch05_02_files.py`) : arbre `GN_Column` créé par l'API. Score du correcteur 41/41 ; starter 14/41.
Mesures évaluées : 4 pièces, hauteur 3,00 m, z min 0,000, emprise 0,90 × 0,90 m, centre (0 ; 0), fût de 2,6 m, 0 arête non manifold, MAT_Column, 100 % lisse.
Rendu regardé : colonne complète (base, fût, anneau, chapiteau), deux vues ; la première caméra coupait le haut de la colonne (corrigée).

## Contre-épreuve du correcteur (`COMPLETED_EXAMPLES/COUNTER_EXAMPLES/`)
| Fichier faux | Défaut | Tests qui le refusent |
|---|---|---|
| `…_no_join` | fût seul, sans Join ni autres pièces | Cube, Curve to Mesh, Transform, Join, pièces, hauteur, pieds, emprise (une seule pièce non assemblée) |
| `…_no_ring` | sans anneau (Curve to Mesh) | Curve to Mesh ; nombre de pièces (même défaut) |
| `…_floating` | colonne relevée de 0,3 m | Pieds sur z = 0 (seul) |
| `…_short` | fût de 1 m (trou entre base et chapiteau) | Fût de ≥ 2,4 m (seul) |
| `…_off_center` | chapiteau décalé de 0,2 m en X | Emprise ; centrage (même défaut) |
Aussi refusé : le starter.
Le contre-exemple « fût trop court » passait 38/38 avant l'ajout du contrôle de la hauteur du fût : sa hauteur totale (3,0 m) était inchangée par la base et le chapiteau fixes.

## Limites
- Mesures de dimensions et de graphe ; aucune appréciation esthétique.
- Les pièces ne sont pas soudées : le maillage n'est pas un volume unique.
