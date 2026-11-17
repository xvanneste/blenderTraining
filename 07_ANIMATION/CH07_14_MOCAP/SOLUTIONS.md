# CH07.14 — Solutions

<!-- QUIZ_ANSWERS_START -->
## Réponses du quiz

| Q | Réponse | Explication |
|---|---|---|
| Q1 | **a** — Une hiérarchie de joints et une suite de poses par image | Squelette (HIERARCHY) puis valeurs de canaux par image (MOTION). |
| Q2 | **a** — Elle contient du bruit, des glitches et trop de clés | Bruit de 1° et glitches de 9° dans l'exercice. |
| Q3 | **a** — Une par image (96) | 15 courbes de 96 clés. |
| Q4 | — | Une valeur aberrante isolée (mauvaise lecture d'un marqueur) : ici +9° aux images 21, 48 et 72 ; un lissage seul la répartit sur ses voisines au lieu de la supprimer. |
| Q5 | — | Pour comparer, recommencer et ne jamais perdre la capture d'origine ; le correcteur s'en sert de référence. |
| Q6 | **a** — Retirer les glitches, lisser, décimer | Décimer d'abord garderait les glitches comme des clés. |
| Q7 | **a** — Perdre l'amplitude du mouvement | σ = 6 images : amplitude conservée à 28 % seulement. |
| Q8 | — | Pour garder 28 à 32 clés au lieu de 96 sur les courbes importantes : le mouvement reste éditable à la main. |
| Q9 | — | Les clés restantes sont espacées : en Linear la courbe est anguleuse, en Bezier elle reste lisse (fidélité similaire, aspect meilleur). |
| Q10 | — | La réduire à quelques clés (ici ≤ 32 clés au plus, souvent 2) : il n'y a pas de mouvement utile. |
<!-- QUIZ_ANSWERS_END -->

## Exercices
`COMPLETED_EXAMPLES/ch07_14_mocap_solution.blend` (+ `_reference.png`)

**Fabrication.** Générées par script (`build_ch07_14_files.py`) : écriture du BVH (graine 7, bruit gaussien, trois glitches), import par `bpy.ops.import_anim.bvh`, copie `MOCAP_RAW`, nettoyage en script (médiane 5, gaussien σ = 1,2, Ramer-Douglas-Peucker), variantes. Score 38/38 ; starter 10/38. Courbe regardée.

## Contre-épreuve du correcteur (`COMPLETED_EXAMPLES/COUNTER_EXAMPLES/`)
| Fichier faux | Défaut | Tests qui le refusent |
|---|---|---|
| `…_not_cleaned` | action brute non modifiée | bruit ; forme ; glitches ; clés ; interpolation |
| `…_over_smoothed` | lissage trop fort (σ = 6 images) | forme conservée ; glitches (amplitude perdue) |
| `…_kept_spikes` | lissage léger sans suppression des glitches | forme ; glitches ; clés |
| `…_too_many_keys` | lissé mais 96 clés conservées | clés décimées (seul) |
| `…_linear_keys` | décimé mais clés linéaires | interpolation (seul) |
| `…_raw_modified` | la copie brute a été nettoyée aussi | MOCAP_RAW intacte ; mesures comparées à une référence altérée |
Aussi refusé : le starter.

## Limites
- BVH synthétique de quatre joints ; pas de retargeting sur un rig complet.
- La solution est calculée, pas obtenue par les opérateurs du Graph Editor ; un nettoyage manuel a un résultat différent (tolérances de 8 % de fidélité et 38 clés).
- Le contre-exemple « raw_modified » échoue aussi sur les mesures comparées (référence altérée).
