# CH18.16 — Solutions

<!-- QUIZ_ANSWERS_START -->
## Réponses du quiz

| Q | Réponse | Explication |
|---|---|---|
| Q1 | **b** — 12 dessins par seconde | Un dessin toutes les 2 images. |
| Q2 | — | Pose à pose : clés d'abord puis intervalles (contrôle) ; straight ahead : dessins dans l'ordre (spontané, mais dérive). |
| Q3 | **b** — R | Keyframe Type (R). |
| Q4 | — | Voir les dessins voisins en transparence pour régler arcs et espacement. |
| Q5 | — | Timing : la durée (nombre d'images) d'une action ; espacement : la distance entre dessins successifs, qui donne vitesse et ralentis. |
| Q6 | **b** — Au sommet | La balle ralentit en montant et repart lentement : ralenti au sommet. |
| Q7 | — | Écrasée au contact ; étirée juste avant et juste après, dans le sens du mouvement ; ronde au sommet. |
| Q8 | **b** — s'élargir d'environ 33 % | Volume constant : 0,75 × 1,33 ≈ 1. |
| Q9 | — | Chaque rebond monte à une fraction (≈ 60 %) du précédent et dure moins longtemps. |
| Q10 | — | Espacement trop régulier ou trop serré près du sol : il faut accélérer la chute (dessins écartés en bas). |
<!-- QUIZ_ANSWERS_END -->

## Exercice 1
`COMPLETED_EXAMPLES/ch18_16_keys_solution.blend` : 8 poses — sommet de départ (image 1), contacts
13, 32, 46, 57 (Keyframe), sommets 22, 39, 52 (Extreme). Hauteurs mesurées : 4,00 → 2,39 → 1,44 →
0,86 m (×0,6). Écrasement au contact : largeur/hauteur ≈ 1,74 au premier, moins ensuite.

## Exercice 2
`COMPLETED_EXAMPLES/ch18_16_bounce_solution.blend` (+ `_reference.png`) : 32 dessins en deux,
gravité constante (12 images de chute), étirement dans les 2 images autour des contacts, volume
exact (rayon_x × rayon_z = R²), intervalles en Breakdown. Mesures du correcteur : écart moyen 1,81
image, ralenti haut/bas 0,36.
Contre-épreuve : mêmes dessins, mais intervalles replacés à espacement LINÉAIRE entre les poses →
refusé (« vitesse haut / bas = 1,11 »).

## Exercice 3 (indications)
Bowling : chute rapide, rebond < 10 % de la hauteur, squash ≈ 0. Ping-pong : restitution ≈ 0,8,
rebonds courts et nombreux, squash faible. Baudruche : gravité faible (chute sur 30 images et plus),
squash fort, arcs larges et lents.
