# CH03.04 — Solutions

<!-- QUIZ_ANSWERS_START -->
## Réponses du quiz

| Q | Réponse | Explication |
|---|---|---|
| Q1 | **c** — Le cercle | Carré = stabilité, triangle = danger/dynamisme. |
| Q2 | — | Utiliser trois tailles bien distinctes pour créer du contraste ; des tailles égales s'annulent. |
| Q3 | — | Par la silhouette (ombre chinoise), de face et de profil. |
| Q4 | — | Non : c'est choisir et exagérer ce qui sert une intention, et supprimer le reste. |
| Q5 | **b** — Negative | Object Data > Active Element > Negative. |
| Q6 | — | Leur rayon est un rayon d'influence : la taille visible dépend des voisins et du seuil ; elles se règlent à l'œil. |
| Q7 | — | Mesh > Bisect avec Clear Inner et Fill, ou Boolean Difference avec un grand cube. |
| Q8 | **b** — Boolean (Difference) | Puis remesh pour adoucir. |
| Q9 | — | Clay Strips pour poser des plans, Scrape/Fill pour aplatir, Pinch pour affirmer les arêtes ; peu de Smooth. |
| Q10 | — | À la fin, volontairement (mèche, sourire en coin), sans nuire à la lisibilité. |
<!-- QUIZ_ANSWERS_END -->

## Exercice 2
`COMPLETED_EXAMPLES/ch03_04_bust_solution.blend` (+ `_reference.png` : face, 3/4, profil).
Construction (script `build_ch03_04_files.py`) : 10 ellipsoïdes qui se chevauchent (poitrine, cou, tête,
crâne, nez, arcades, menton, oreilles, mèche) → Join → Voxel Remesh 5 mm → orbites creusées par deux
Boolean Difference (solveur Exact) → Voxel Remesh → Bisect au ras du bas avec remplissage.
Mesures du correcteur : 1 volume fermé, 24 144 faces, hauteur 0,45 m, socle 714 cm², cou 12,2 cm
(tête 28,6, épaules 41,8), tête 75 % de la hauteur, contraste ×1,46, nez +4,3 cm, symétrie 100 %.
Note honnête : un premier essai en métaballes (rayons pris pour des dimensions) a donné des volumes
séparés et une « capsule » d'un mètre ; la solution a été refaite en ellipsoïdes, plus prévisibles.
Contre-épreuve : un œuf lisse sur socle → refusé (pas de cou, pas de stylisation, pas de nez).
Le correcteur a dû être renforcé : la première version acceptait l'œuf comme « stylisé ».
