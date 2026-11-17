# CH06.10 — Solutions

<!-- QUIZ_ANSWERS_START -->
## Réponses du quiz

| Q | Réponse | Explication |
|---|---|---|
| Q1 | **b** — Les bones DEF- | Seuls les DEF- ont use_deform ; les contrôleurs et le mécanisme ne déforment pas. |
| Q2 | **b** — L'animateur n'a jamais à les toucher ; moins de bruit à l'écran | Les masquer évite les erreurs et allège la vue. |
| Q3 | **b** — Par Copy Transforms (World → World) | Chaque DEF- copie la transformation de son contrôleur. |
| Q4 | — | Il pourrait peser sur le maillage (poids automatiques) et le déformer en double ; la séparation contrôle/déformation garde le rig propre et réutilisable. |
| Q5 | — | Que tourner ctl_arm.L de 30° fait tourner DEF-arm.L de 30° sans toucher au bras droit, et que tourner ctl_spine de 20° entraîne les deux bras. |
| Q6 | **b** — Dans une collection masquée | Les formes personnalisées sont des objets ordinaires : on les range dans une collection masquée (WIDGETS). |
| Q7 | **b** — L'animateur ne peut que le tourner : aucun geste interdit | Les verrous empêchent des erreurs de manipulation (déplacer ou étirer un bras par accident). |
| Q8 | — | Pour repérer le côté d'un coup d'œil, en particulier en pose de profil ou avec des contrôleurs qui se superposent. |
| Q9 | — | ctl_arm.L/.R : Location et Scale verrouillés (rotation seule) ; ctl_spine : Scale verrouillé. |
| Q10 | — | Parce que ranger des bones, changer des formes ou des verrous peut casser un lien ; le contre-exemple « broken_link » est vert sur toute la structure mais le bras ne suit plus. |
<!-- QUIZ_ANSWERS_END -->

## Exercice 2
`COMPLETED_EXAMPLES/ch06_10_controls_solution.blend` (+ `_reference.png`).

**Fabrication.** Générée par script (`build_ch06_10_files.py`) : armature de 8 bones, Copy Transforms, collections, formes (WIDGETS masquée), palettes, verrous. Score 40/40 ; starter 17/40.
Croquis regardé : anneaux rouge et bleu (côtés), cube jaune (colonne), anneau violet (racine), bones DEF en gris.

## Contre-épreuve du correcteur (`COMPLETED_EXAMPLES/COUNTER_EXAMPLES/`)
| Fichier faux | Défaut | Tests qui le refusent |
|---|---|---|
| `…_no_collections` | bones sans collection | collections ; visibilité (seuls) |
| `…_not_hidden` | Deform et Mechanism visibles | visibilité (seule) |
| `…_no_shapes` | aucune forme personnalisée | formes personnalisées (seul) |
| `…_no_colors` | couleurs par défaut | couleurs (seul) |
| `…_no_locks` | aucun verrou | verrous (seul) |
| `…_broken_link` | DEF- sans Copy Transforms | comportement : 0° au lieu de 30° et 20° (seul) |
| `…_deform_flags` | use_deform actif sur les contrôleurs | use_deform (seul) |
Aussi refusé : le starter.

## Limites
- Rig de 8 bones, pas de sélecteur d'interface ; les verrous sont vérifiés comme propriétés (ils protègent l'interface, pas les scripts).
- Les couleurs sont vérifiées par palette, pas par teinte.
