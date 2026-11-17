# CH04.03 — Solutions

<!-- QUIZ_ANSWERS_START -->
## Réponses du quiz

| Q | Réponse | Explication |
|---|---|---|
| Q1 | **c** — Proche de 1 | Un matériau est métallique ou non : Metallic vaut 0 ou 1 ; l'intermédiaire ne sert qu'aux transitions (rouille, peinture écaillée). |
| Q2 | **b** — La couleur de la réflexion | Un métal n'a pas de diffus : Base Color est la teinte de sa réflexion (or ≈ 1 ; 0,77 ; 0,34). |
| Q3 | **b** — Un miroir qui ne réfléchit presque rien : faux | Les métaux réfléchissent 60–100 % : la Base Color d'un métal n'est jamais sombre (le correcteur exige une luminance ≥ 0,5). |
| Q4 | — | Un diélectrique réel absorbe et réfléchit : la neige fraîche ≈ 0,9, le charbon ≈ 0,02–0,04. Les extrêmes donnent un rendu irréaliste et cassent l'éclairage. |
| Q5 | — | Elle étale le reflet : 0 = miroir net, 1 = reflet très diffus. Un caoutchouc mat est autour de 0,7–0,8, un métal poli de 0,1–0,4. |
| Q6 | **b** — Transmission Weight | Transmission Weight = 1 laisse passer la lumière (réfractée selon l'IOR). |
| Q7 | **b** — ≈ 1,45–1,55 | Le verre courant est entre 1,45 et 1,55 ; le correcteur accepte 1,3–1,7. |
| Q8 | — | La lumière pénètre et ressort ailleurs ; le rouge diffuse plus loin que le bleu : le rayon par canal (R, V, B) donne la teinte chaude des ombres douces d'une cire ou d'une peau. |
| Q9 | — | Le correcteur exige quatre matériaux distincts : chaque sphère a son MAT_ ; partager un matériau modifie tous les objets à la fois. |
| Q10 | — | Un métal reflète son environnement : sur un fond noir il paraît noir. Un monde clair (ici gris-bleu) est nécessaire pour qu'il ait quelque chose à refléter. |
<!-- QUIZ_ANSWERS_END -->

## Exercice 2
`COMPLETED_EXAMPLES/ch04_03_pbr_solution.blend` (+ `_reference.png`).

**Fabrication.** Générée par script (`build_ch04_03_files.py`) : quatre sphères, quatre matériaux dont les valeurs sont celles du tableau de THEORY.md §3, monde gris-bleu (0,30 ; 0,33 ; 0,38) pour que le métal ait un reflet, deux caméras.
Score du correcteur : 37/37. Starter : 22/37 (valeurs par défaut).

## Contre-épreuve du correcteur (`COMPLETED_EXAMPLES/COUNTER_EXAMPLES/`)
| Fichier faux | Défaut | Test qui le refuse |
|---|---|---|
| `…_metal_dark` | métal à Base Color 0,05 | Metal : Base Color claire (seul test en échec) |
| `…_mixed_metal` | caoutchouc à Metallic 0,5 | Rubber : Metallic et « Metallic proche de 0 ou 1 » (même défaut, deux tests) |
| `…_glass_opaque` | verre à Transmission 0 | Glass : Transmission (seul test en échec) |
| `…_white_wax` | cire à Base Color 1 | albedo de la cire et « aucun diélectrique blanc pur » (même défaut, deux tests) |
| `…_shared_material` | un seul matériau sur les 4 sphères | « Quatre matériaux distincts » + les valeurs des autres sphères |
Aussi refusé : le starter (valeurs par défaut).

## Limites
- Plages de valeurs, pas d'évaluation esthétique : toujours regarder le rendu.
- Le contre-exemple « matériau partagé » échoue forcément sur plusieurs tests, puisque les trois autres sphères reçoivent les valeurs du métal.
- Seul le premier Principled BSDF du matériau est lu ; un matériau à textures branchées n'est pas évalué.
