# CH05.04 — Solutions

<!-- QUIZ_ANSWERS_START -->
## Réponses du quiz

| Q | Réponse | Explication |
|---|---|---|
| Q1 | **b** — Il crée des points sur les faces d'un maillage | Il sort un nuage de points (avec Normal et Rotation) à instancier ensuite avec Instance on Points. |
| Q2 | **b** — Poisson Disk | Poisson Disk écarte les points d'au moins Distance Min ; Random les tire sans contrainte (des paquets se forment). |
| Q3 | **a** — Distance Min, Density Max, Density Factor, Seed | En mode Random, Distance Min et Density Factor disparaissent et Density règle le nombre. |
| Q4 | — | Chaque point reçoit une orientation alignée sur la normale de la face : les instances suivent la surface (ici un sol plat : verticales). |
| Q5 | — | Changer le tirage aléatoire : même densité, répartition différente, sans autre changement. |
| Q6 | **a** — Density Factor = (Position X > 0) | Le facteur de densité vaut 1 ou 0 selon la position : aucun point là où il vaut 0. |
| Q7 | **b** — ≈ 0,50 m | 0,503 m : le Poisson Disk respecte Distance Min = 0,5 (0,024 m seulement en méthode Random). |
| Q8 | — | Une tolérance évite d'être trop strict pour les points proches de x = 0 ; dans la solution, 100 % sont du bon côté. |
| Q9 | — | Environ 7 arbres sur la moitié du sol (au lieu de 73) : trop clairsemé pour un bois ; le correcteur exige 40–400. |
| Q10 | — | Multiplier le masque par un champ de bruit ou de distance au centre : Density Factor décroît vers 0 dans la clairière (CH05.07). |
<!-- QUIZ_ANSWERS_END -->

## Exercice 2
`COMPLETED_EXAMPLES/ch05_04_distribution_solution.blend` (+ `_reference.png`).

**Fabrication.** Générée par script (`build_ch05_04_files.py`). Score du correcteur 34/34 ; starter 5/34.
Mesures : 73 arbres ; 100 % sur x > 0 ; distance minimale 0,503 m ; tous dans le sol ; MAT_Tree.
Rendu regardé : arbres sur la moitié droite du sol, répartis régulièrement sans contact (vue de face et vue du dessus) ; le cadrage de la vue du dessus a été élargi.

**Ce que le développement a appris** : (1) les entrées de Distribute Points on Faces changent avec la méthode : en Random, « Distance Min » et « Density Factor » n'existent pas (accès par clé → erreur) ; (2) une première lecture de la distance minimale donnait 0,00 / 1 / 2 : `KDTree.find_n` renvoie (position, indice, distance) et la distance est le 3ᵉ élément.

## Contre-épreuve du correcteur (`COMPLETED_EXAMPLES/COUNTER_EXAMPLES/`)
| Fichier faux | Défaut | Tests qui le refusent |
|---|---|---|
| `…_no_mask` | Density Factor non alimenté (arbres partout) | Density Factor ; proportion du bon côté (50 %) |
| `…_random_method` | méthode Random (arbres collés) | Méthode ; Density Factor absent ; distance minimale 0,02 m |
| `…_sparse` | Density Max 0,1 (7 arbres) | Nombre d'instances (seul) |
| `…_wrong_side` | masque inversé (x < 0) | Proportion du bon côté : 0 % (seul) |
| `…_orphan` | un nœud Cube inutilisé | Aucun nœud orphelin (seul) |
Aussi refusé : le starter.

## Limites
- Nombre, côté et distance minimale ; aucune appréciation de la composition.
- La graine est fixe (Seed 0) : les nombres exacts changent avec un autre Seed (73 à Seed 0).
