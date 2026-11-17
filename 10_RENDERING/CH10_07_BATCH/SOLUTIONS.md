# CH10.07 — Solutions

<!-- QUIZ_ANSWERS_START -->
## Réponses du quiz

| Q | Réponse | Explication |
|---|---|---|
| Q1 | **a** — Lance Blender en arrière-plan, sans interface | Indispensable sur une machine sans écran. |
| Q2 | **a** — Rend les images 9 à 16 en animation | « -a » lance le rendu de l'animation avec la plage réglée avant. |
| Q3 | **a** — Les arguments s'exécutent dans l'ordre : -a lancé trop tôt ignore -s/-e | Mesuré : « -a -s 1 -e 2 » rend les 6 images ; « -s 1 -e 2 -a » en rend 2. |
| Q4 | — | Le numéro d'image sur 4 chiffres (shot_0001.png). |
| Q5 | — | Pour savoir quelle commande a produit quelle image et détecter une commande qui rend hors de sa plage. |
| Q6 | **a** — À ce qu'une machine ne rende pas une image déjà prise par une autre | Réglages relus dans l'API : RenderSettings.use_overwrite et use_placeholder. |
| Q7 | **a** — 25 (l'image 8 est comptée deux fois) | Contre-exemple overlap : couverture fausse. |
| Q8 | — | Une ligne de commande qui exécute du code arbitraire n'est pas sûre à lancer : la liste blanche (-b -o -F -s -e -a -x -t) garantit que le correcteur n'exécute que du rendu. |
| Q9 | — | C'est le gestionnaire de ferme de la Blender Foundation : il distribue des tâches de rendu à des workers. Je ne l'ai ni installé ni testé ici : le chapitre se limite à la base (commandes). |
| Q10 | — | Une machine, Workbench 64 × 36 : le correcteur ne mesure ni l'équilibrage des morceaux selon le coût réel, ni les erreurs réseau, ni une vraie ferme. |
<!-- QUIZ_ANSWERS_END -->

## Exercices
`COMPLETED_EXAMPLES/ch10_07_batch_solution.blend` (+ `_reference.png`)

**Fabrication.** Générées par script (`build_ch10_07_files.py`) : cube animé, texte BATCH, variantes ; mesures par exécution réelle des commandes. Score 39/39 ; starter 13/39. Images de la solution regardées.

## Contre-épreuve du correcteur (`COMPLETED_EXAMPLES/COUNTER_EXAMPLES/`)
| Fichier faux | Défaut | Tests qui le refusent |
|---|---|---|
| `…_wrong_order` | « -a » avant « -s » : le morceau rend toute la scène | images hors plage |
| `…_gap` | l'image 17 manque | couverture |
| `…_overlap` | l'image 8 rendue deux fois (plages 1–8 et 8–16) | couverture |
| `…_one_chunk` | une seule commande pour 24 images | nombre de commandes |
| `…_no_placeholders` | Overwrite activé, Placeholders désactivé | réglages de ferme |
| `…_forbidden_flag` | option --python-expr (hors liste blanche) | plan refusé : rien n'est exécuté |
Aussi refusé : le starter.

## Limites
- Une machine.
- Flamenco non testé.
- Équilibrage non mesuré.
