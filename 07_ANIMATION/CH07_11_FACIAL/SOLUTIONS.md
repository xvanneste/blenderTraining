# CH07.11 — Solutions

<!-- QUIZ_ANSWERS_START -->
## Réponses du quiz

| Q | Réponse | Explication |
|---|---|---|
| Q1 | **a** — La forme de bouche associée à un groupe de phonèmes | Plusieurs phonèmes partagent la même forme : on anime des visèmes, pas des lettres. |
| Q2 | **a** — Bouche fermée | Les lèvres se joignent : mâchoire à 0° dans l'exercice. |
| Q3 | **a** — Une image avant | Le son est perçu comme synchrone quand l'image précède légèrement ; le correcteur vérifie aux images f − 1 et f. |
| Q4 | — | Peu de formes suffisent (fermée, ouverte, arrondie, étirée) ; animer chaque lettre produit une bouche qui papillonne. |
| Q5 | — | Une forme tenue (images f − 1 et f) se lit mieux qu'une pose fugitive : l'œil la voit. |
| Q6 | **a** — Quelques images (ici 3 à 8) | Dans la solution : départ à l'image 20, 3 images au-dessus de 5 mm. |
| Q7 | **a** — La bouche saute d'une forme à l'autre | Saut de 12° de la mâchoire d'une image à l'autre (contre-exemple « popping »). |
| Q8 | — | Une bouche entrouverte (−4°) sur M : le spectateur ne lit pas la consonne ; M doit fermer les lèvres. |
| Q9 | — | Chacune a sa forme : A grande ouverture (−12°), O arrondie (−7°), E étirée avec sourire (−4° et 0,04 m). |
| Q10 | — | Un visage qui ne cligne jamais paraît mort ; le clignement ponctue le regard et marque les pensées. |
<!-- QUIZ_ANSWERS_END -->

## Exercices
`COMPLETED_EXAMPLES/ch07_11_lipsync_solution.blend` (+ `_reference.png`)

**Fabrication.** Générées par script (`build_ch07_11_files.py`, à partir de `ch06_09_facial_solution.blend`) : texte PHONEMES, clés de jaw, ctl_smile, ctl_blink, variantes. Score 35/35 ; starter : arrêt anticipé (pas d'animation). Courbes regardées.

## Contre-épreuve du correcteur (`COMPLETED_EXAMPLES/COUNTER_EXAMPLES/`)
| Fichier faux | Défaut | Tests qui le refusent |
|---|---|---|
| `…_late` | visèmes en retard de 3 images | visèmes ; variété ; clignement (décalé) |
| `…_mouth_open_on_m` | bouche entrouverte sur M (−4°) | visèmes (seul) |
| `…_no_variety` | mêmes ouvertures pour A, O, E | visèmes ; variété |
| `…_popping` | interpolation Constant (la bouche saute) | continuité (seul) |
| `…_no_blink` | aucun clignement | clignement (seul) |
| `…_slow_blink` | clignement de 17 images | clignement (seul) |
Aussi refusé : le starter.

## Limites
- Visage synthétique (sphère), pas de langue ni de dents ; piste de huit phonèmes fixe.
- Le contre-exemple « late » échoue aussi sur la variété et le clignement mesurés à des images décalées.
- Aucun son réel : on valide des poses, pas la synchronisation perçue.
