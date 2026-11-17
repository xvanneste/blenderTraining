# CH07.04 — Solutions

<!-- QUIZ_ANSWERS_START -->
## Réponses du quiz

| Q | Réponse | Explication |
|---|---|---|
| Q1 | **a** — La valeur d'une propriété en fonction du temps | Une courbe par propriété animée ; la pente est la vitesse. |
| Q2 | **a** — La vitesse de changement de la valeur | Pente nulle = valeur constante à cet instant ; pente forte = changement rapide. |
| Q3 | **a** — V | V : types de poignée (Auto Clamped...) ; T : interpolation. |
| Q4 | — | Elles aplatissent la courbe à l'extrémité : vitesse quasi nulle (0,31 °/image mesurés) et pas de dépassement ; le pendule ralentit en haut et accélère au milieu. |
| Q5 | — | 5 °/image, constante ; la solution en Bezier atteint 7,5 °/image au milieu. |
| Q6 | **a** — Répète la courbe avant et après ses clés | Cycles répète l'aller-retour : 30° à l'image 37, −30° à 49, 30° à 61. |
| Q7 | **a** — Ajoute une variation pseudo-aléatoire lisse à la valeur | Strength règle l'amplitude, Scale la durée des ondulations (en images). |
| Q8 | — | Il se règle en deux nombres, reste modifiable et ne gonfle pas l'action. |
| Q9 | — | Avec Strength 0,5, Z varie de 20 cm crête à crête : le pendule saute au lieu de frémir. |
| Q10 | — | Pour lire deux aller-retours : un par les clés, un par le modificateur Cycles. |
<!-- QUIZ_ANSWERS_END -->

## Exercices
`COMPLETED_EXAMPLES/ch07_04_graph_solution.blend` (+ `_reference.png`)

**Fabrication.** Générées par script (`build_ch07_04_files.py`) : clés de rotation et de position, interpolation et poignées, modificateurs CYCLES et NOISE. Score 33/33 ; starter 11/33. Croquis regardé : trois arches identiques, frémissement vert discret.

## Contre-épreuve du correcteur (`COMPLETED_EXAMPLES/COUNTER_EXAMPLES/`)
| Fichier faux | Défaut | Tests qui le refusent |
|---|---|---|
| `…_linear` | interpolation linéaire | ralentis (seul) |
| `…_constant` | interpolation constante | ralentis (seul) |
| `…_no_cycles` | pas de modificateur Cycles | Cycles (seul) |
| `…_no_noise` | pas de modificateur Noise | Noise ; frémissement |
| `…_noise_too_strong` | Strength 0,5 | Noise (valeur) ; frémissement |
| `…_wrong_keys` | amplitude ±45° au lieu de ±30° | clés ; dépassement ; répétition |
Aussi refusé : le starter.

## Limites
- Un objet, deux courbes ; Generator, Envelope et Limits ne sont pas testés.
- Les poignées sont automatiques : l'édition manuelle des poignées n'est pas vérifiée.
- Le correcteur ne juge pas l'esthétique du balancement.
