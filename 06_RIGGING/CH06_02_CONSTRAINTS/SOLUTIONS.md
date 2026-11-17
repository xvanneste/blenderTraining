# CH06.02 — Solutions

<!-- QUIZ_ANSWERS_START -->
## Réponses du quiz

| Q | Réponse | Explication |
|---|---|---|
| Q1 | **a** — Il oriente un axe de l'objet vers la cible par la rotation minimale | Le bone tourne pour que son axe choisi (Track Axis) pointe vers la cible, sans rotation parasite autour de cet axe. |
| Q2 | **b** — Y | L'axe local Y d'un bone est sa direction : Track Axis Y. |
| Q3 | **a** — Pose Mode, onglet Bone Constraints | Contraintes de bone : en Pose Mode (`pose.bones[n].constraints`) ; les contraintes d'objet sont dans un autre onglet. |
| Q4 | — | Leur contrainte est évaluée après le mouvement du parent : elle recalcule l'orientation vers la cible quelle que soit la rotation de la tête. |
| Q5 | **a** — La contrainte agit à moitié (mélange avec l'orientation sans contrainte) | L'influence mélange le résultat de la contrainte avec l'état avant elle : 0 = aucun effet, 1 = plein. |
| Q6 | **a** — De haut en bas | La première (en haut) s'applique d'abord : la limite doit être placée APRÈS le suivi. |
| Q7 | — | Le suivi s'applique après la limite et la défait : la tête dépasse le plafond (43° mesurés au lieu de 35°). |
| Q8 | — | Pour limiter la rotation par rapport au parent de la tête (le cou), indépendamment de l'orientation du personnage dans le monde. |
| Q9 | — | 22,5° (influence 0,5 × 45°) ; pour une cible à 86°, 35° : la limite plafonne (0,5 × 86 = 43 > 35). |
| Q10 | — | Un rig n'est correct que s'il réagit : tester une seule position laisserait passer un œil réglé à la main sans contrainte. |
<!-- QUIZ_ANSWERS_END -->

## Exercice 2
`COMPLETED_EXAMPLES/ch06_02_constraints_solution.blend` (+ `_reference.png`).

**Fabrication.** Générée par script (`build_ch06_02_files.py`) : six contraintes de bone. Score du correcteur 31/31 ; starter 8/31. Mesures : voir THEORY.md §4.
Croquis comparé : à T1 yeux et tête alignés ; à T2 la tête (jaune) a tourné de moitié et les yeux (orange) visent la cible (rouge) ; à T3 la tête plafonne et les yeux visent encore.

**Ce que le développement a appris** : le studio de la bibliothèque contenait déjà un EMP_Target ; ma cible devenait EMP_Target.001 et ni le correcteur ni les contraintes ne visaient le bon objet (31 → 11/31 sur la solution) : j'ai renommé celui du studio.

## Contre-épreuve du correcteur (`COMPLETED_EXAMPLES/COUNTER_EXAMPLES/`)
| Fichier faux | Défaut | Tests qui le refusent |
|---|---|---|
| `…_no_constraints` | aucune contrainte | contraintes, comportement (T2, T3) |
| `…_wrong_axis` | Track Axis X au lieu de Y | axe ; yeux à 90° dès T1 ; comportement |
| `…_head_full` | tête à Influence 1 | Influence de la tête ; rapport de rotation à T2 (0,78) |
| `…_no_limit` | sans Limit Rotation | Limit Rotation ; ordre ; plafond à T3 (43,1°) |
| `…_eye_no_target` | eye.R sans cible | eye.R ; erreur de visée à T1 (1,1°), T2 (24°), T3 (53°) |
| `…_order_swapped` | limite avant le suivi | Ordre ; plafond à T3 (43,1°) |
Aussi refusé : le starter.

## Limites
- Un rig, trois positions de cible ; pas de test de continuité.
- Seuls Damped Track, Track To et Limit Rotation sont reconnus.
