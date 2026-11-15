# CH02.12 — Solutions

<!-- QUIZ_ANSWERS_START -->
## Réponses du quiz

| Q | Réponse | Explication |
|---|---|---|
| Q1 | — | Les sommets entre deux os sont interpolés ; avec trop peu de sommets au pli, l'interpolation écrase la forme et le volume diminue. |
| Q2 | **b** — 87,5 % | 87,5 % ; 97,5 % avec 4 boucles serrées au coude. |
| Q3 | — | Non : il faut de la géométrie là où ça plie ; 40 segments réguliers ne font guère mieux que 4 boucles bien placées, pour un coût bien supérieur. |
| Q4 | **b** — 3 | 3 minimum, resserrées vers le pli ; plus pour les grandes amplitudes. |
| Q5 | — | Un triangle ou un n-gon interrompt l'anneau : Loop Cut devient impossible et la déformation irrégulière. |
| Q6 | — | Sur une zone de pli ou d'articulation. |
| Q7 | — | Des boucles concentriques autour de chaque ouverture. |
| Q8 | — | Échelle réelle, Ctrl+A All Transforms, origine aux pieds, face à −Y, A-pose ou T-pose, symétrie sur X. |
| Q9 | **b** — efface la rotation des os sélectionnés | Clear Rotation : retour à la pose de repos. |
| Q10 | — | Non avec Loop Cut : les poids sont interpolés automatiquement sur la nouvelle boucle. |
<!-- QUIZ_ANSWERS_END -->

## Exercice 1
Échelle réelle ; `Ctrl+A` → All Transforms (échelle 1, rotation 0) ; origine aux pieds ; personnage
face à −Y ; A-pose ou T-pose ; 3 boucles minimum par articulation ; pôles hors des plis ; symétrie
sur X (sommets centraux à x = 0).

## Exercice 3
Référence : `COMPLETED_EXAMPLES/ch02_12_arm_solution.blend` ; rendus `ch02_12_arm_bent_starter.png`
(avant) et `ch02_12_arm_bent_solution.png` (après), coude plié à 90°. Boucles ajoutées à z = 0,24 /
0,27 / 0,33 / 0,36. Volume conservé mesuré par le correcteur : **97,5 %** (87,5 % au départ ; 98,4 %
avec 40 segments réguliers, beaucoup plus lourd).
