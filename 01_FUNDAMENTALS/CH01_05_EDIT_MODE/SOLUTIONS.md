# CH01.05 — Solutions

<!-- QUIZ_ANSWERS_START -->
## Réponses du quiz

| Q | Réponse | Explication |
|---|---|---|
| Q1 | **a** — Tab | Tab (Ctrl+Tab : menu des modes). |
| Q2 | — | 8 sommets, 12 arêtes, 6 faces. |
| Q3 | **b** — Des arêtes | 1 sommets, 2 arêtes, 3 faces. |
| Q4 | — | Pose Mode. |
| Q5 | **b** — Une boucle d'arêtes | Edge loop ; Ctrl+Alt+clic = anneau. |
| Q6 | — | Sans X-Ray, seuls les éléments visibles sont sélectionnés ; avec X-Ray, ceux de derrière aussi. |
| Q7 | — | Toute la partie connectée (linked) sous la souris. |
| Q8 | — | Ctrl + Num + (et Ctrl + Num - pour réduire). |
| Q9 | **b** — E | E. |
| Q10 | — | Met à l'échelle 0 sur X : tous les sommets sélectionnés s'alignent sur le même X (la face s'écrase en arête). |
| Q11 | — | Les modifications sont validées dans le maillage à la sortie du mode ; scripts, correcteurs et certains outils lisent le maillage validé. |
| Q12 | — | Avec la molette de la souris (après avoir activé O). |
<!-- QUIZ_ANSWERS_END -->

## Exercice 3
`Tab` → `3` → clic sur la face du haut → `E 1 Entrée` → `S X 0 Entrée` → `Tab`.
Fichier : `COMPLETED_EXAMPLES/ch01_05_house_solution.blend` (12 sommets : les 4 du haut
sont superposés deux à deux sur le faîtage — *Merge by Distance* (`M` → *By Distance*) les
fusionnerait en 10 sommets, ce qui est plus propre ; le correcteur accepte les deux).

## Défi 2
Toit en croupe : au lieu de `S X 0`, mettre à l'échelle la face extrudée sur X **et** Y
dans des proportions différentes, par ex. `S X 0` puis `S Y 0.4` → faîtage plus court que
la maison, quatre pans inclinés.

## Exercice 1 (e)
`A`, puis `Shift+Alt+LMB` sur une arête de bordure retire la boucle de bordure de la
sélection (`Shift` = ajouter/retirer, `Alt` = boucle).
