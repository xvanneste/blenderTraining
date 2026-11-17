# CH07.08 — Solutions

<!-- QUIZ_ANSWERS_START -->
## Réponses du quiz

| Q | Réponse | Explication |
|---|---|---|
| Q1 | **a** — Contact, descente, passage, montée | Contact (talon), descente (le corps s'abaisse), passage (la jambe libre passe), montée (la jambe d'appui pousse). |
| Q2 | **a** — Au contact | 0,899 m au contact, 0,950 m au passage dans la solution. |
| Q3 | **a** — Un demi-cycle (12 images) | À l'image 13 la jambe gauche est où était la droite à l'image 1. |
| Q4 | — | On anime un seul cycle qui boucle ; le sol défile (ou le personnage est déplacé séparément) : plus simple à corriger et réutilisable (CH07.13). |
| Q5 | — | Pour l'équilibre : quand la jambe gauche avance, le bras droit avance ; le bras gauche recule. |
| Q6 | **a** — Le pied d'appui avance ou recule par rapport au sol | Le sol défile à la vitesse du pas : le pied d'appui doit reculer à 0,05 m par image, à vitesse constante. |
| Q7 | **a** — Pour que la boucle n'ait pas de saut | Sans cela la jambe saute à chaque cycle (contre-exemple « no_loop » : 158 mm d'écart). |
| Q8 | — | Une courbe Bezier ralentit près des clés : le pied glisse. En Linear, l'écart à la droite tombe à 0,6 mm (contre 15 à 18 mm en Bezier avec neuf clés). |
| Q9 | — | Les pieds ne se lèvent pas : ils restent au sol 24 images sur 24 ; la marche devient un traînement de pieds. |
| Q10 | — | Mesurer : écart de la boucle, pas, images au sol, levée du pied, vitesse d'appui, rebond des hanches, bras opposés (le correcteur). |
<!-- QUIZ_ANSWERS_END -->

## Exercices
`COMPLETED_EXAMPLES/ch07_08_walk_solution.blend` (+ `_reference.png`)

**Fabrication.** Générées par script (`build_ch07_08_files.py`) : IK analytique à deux segments dans le plan Y–Z (genou vers l'avant), une clé par image sur 25 images, hanches par √(0,90² − y²), bras opposés. Score 42/42 ; starter : arrêt anticipé (pas d'animation). Une version à neuf clés fabriquée à part est aussi acceptée (42/42).

## Contre-épreuve du correcteur (`COMPLETED_EXAMPLES/COUNTER_EXAMPLES/`)
| Fichier faux | Défaut | Tests qui le refusent |
|---|---|---|
| `…_no_loop` | cycle de 26 images dans une plage de 25 (l'image 25 ≠ l'image 1) | boucle et demi-cycle (seul) |
| `…_uneven_stance` | le pied d'appui accélère (u²) | glissement (seul) |
| `…_no_bob` | hanches à hauteur constante | hanches (seul) |
| `…_same_side_arm` | bras en phase avec la jambe du même côté | bras (seul) |
| `…_shuffle` | pas de levée du pied (traînement) | sol ; glissement |
| `…_short_stride` | pas de 0,20 m au lieu de 0,60 m | pas ; glissement ; hanches |
Aussi refusé : le starter.

## Limites
- Mannequin FK, marche sur place, mesures de profil seulement.
- Le contre-exemple « short_stride » échoue aussi sur le glissement et les hanches ; « shuffle » aussi sur le glissement (les mesures sont liées).
- Le correcteur ne juge pas le style de la marche.
