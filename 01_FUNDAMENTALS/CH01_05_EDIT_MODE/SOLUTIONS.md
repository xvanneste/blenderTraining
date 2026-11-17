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
En mode Édition, pressez `3` pour sélectionner la face du haut, puis `E`, `1`, `Entrée`.
Alignez le faîtage sur X avec `S`, `X`, `0`, `Entrée`. Passez en sélection de sommets (`1`)
sans étendre la sélection et fusionnez les paires superposées avec `M → By Distance`.
Sélectionnez tout, recalculez les normales avec `Shift+N`, puis revenez en mode Objet.
Le [corrigé](COMPLETED_EXAMPLES/ch01_05_house_solution.blend) possède 10 sommets et 9 faces.
Le [contre-exemple](COMPLETED_EXAMPLES/COUNTER_EXAMPLES/ch01_05_house_degenerate_roof.blend)
montre le résultat avant la fusion. Le contrôle de topologie le refuse.

## Défi 2
Pour un toit en croupe, gardez `S X 0`, puis appliquez `S Y 0.4` sur le faîtage avant la
fusion. Il devient plus court que la maison. Vérifiez de dessus que ses deux extrémités
sont en retrait des murs et orbitez pour compter quatre pans inclinés.

## Exercice 1 (e)
`A`, puis `Shift+Alt+LMB` sur une arête de bordure retire la boucle de bordure de la
sélection (`Shift` = ajouter/retirer, `Alt` = boucle).
