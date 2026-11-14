# CH01.03 — Solutions

<!-- QUIZ_ANSWERS_START -->
## Réponses du quiz

| Q | Réponse | Explication |
|---|---|---|
| Q1 | — | Plusieurs objets peuvent être sélectionnés ; un seul est actif (le dernier cliqué, contour plus clair), il sert de référence et est affiché dans Properties. |
| Q2 | **b** — Alt+A | Alt+A (A = tout sélectionner, Ctrl+A = menu Apply, X = supprimer). |
| Q3 | **b** — C | C. |
| Q4 | — | Select > Select Pattern… avec GEO_Tree_*. |
| Q5 | — | Ctrl+I (Select > Invert). |
| Q6 | **b** — Déplace sur l'axe Z local de l'objet | Deuxième pression = axe local. |
| Q7 | — | R Y -30 Entrée. |
| Q8 | **b** — Tous les axes sauf Z | Exclusion d'axe : plan X-Y. |
| Q9 | — | Clic droit ou Échap. |
| Q10 | — | Alt+R. |
| Q11 | — | Avancer par pas réguliers (snapping incrémental). |
| Q12 | — | Saisir la valeur sur l'objet actif, puis clic droit sur le champ > Copy to Selected (ou glisser la valeur en maintenant Alt). |
<!-- QUIZ_ANSWERS_END -->

## Exercice 2
Méthode fiable : sélectionner les 30 cailloux (le caillou actif en dernier), sidebar `N` →
*Item* → taper `0` dans *Location Y* de l'objet actif, puis **clic droit sur le champ →
Copy to Selected** : la valeur est copiée sur toute la sélection. Idem pour *Z* = `0.12`.
(Variante : maintenir `Alt` pendant que l'on glisse la valeur d'un champ l'applique à tous les
objets sélectionnés.)
Piège instructif : `S Y 0 Entrée` en Object Mode rapproche les **positions** sur Y **et**
met l'échelle Y de chaque caillou à 0 : ils deviennent plats (*Scale Y = 0* dans la
sidebar). Pour n'agir que sur les positions : en-tête de la vue 3D → *Options* → *Transform
→ Affect Only → Locations* (vu en CH01.07), puis `S Y 0`.

## Exercice 3 — séquence de touches de référence
- A : `Alt+G`, `G X 2`, `G Y 2`, `G Z 0.5`.
- B : `Alt+G`, `G X 4`, `G Y 2`, `G Z 0.5`, `R X 90`.
- C : `Alt+G`, `G X 2`, `G Y 4`, `G Z 1`, `S Z 2`.
- D : `Alt+G`, `G X 4`, `G Y 4`, `G Z 0.3`, `R Z 45`, `S 0.5`.
(chaque commande terminée par `Entrée`). Fichier : `COMPLETED_EXAMPLES/ch01_03_puzzle_solution.blend`.

## Défi 2
Une rotation locale tourne autour des axes **de l'objet** (déjà tournés de 45° sur Z) ;
une rotation globale autour des axes du monde. Le résultat diffère dès que l'objet n'est
plus aligné sur le monde.
