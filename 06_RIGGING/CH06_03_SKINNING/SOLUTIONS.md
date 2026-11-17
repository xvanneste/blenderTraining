# CH06.03 — Solutions

<!-- QUIZ_ANSWERS_START -->
## Réponses du quiz

| Q | Réponse | Explication |
|---|---|---|
| Q1 | **a** — Les poids : l'influence du bone du même nom sur chaque sommet | Le groupe « upper » donne, pour chaque sommet, l'influence du bone upper ; le modificateur Armature l'utilise. |
| Q2 | **a** — Ctrl+P > With Automatic Weights | Parent With Automatic Weights (`parent_set(type='ARMATURE_AUTO')`) : maillage sélectionné, armature active. |
| Q3 | **c** — 1 | La somme vaut 1 : les influences se répartissent 100 %. |
| Q4 | — | Les moteurs temps réel et le skinning GPU n'acceptent que 4 influences ; au-delà, les poids sont tronqués ou renormalisés (Weights > Limit Total). |
| Q5 | — | Le modificateur Armature associe un groupe à un bone par le nom : un groupe sans bone ne déforme rien (les groupes « extra » du contre-exemple). |
| Q6 | **b** — Une cassure : arêtes étirées jusqu'à ×4,3 au coude | Une coupure nette des poids déchire la surface ; la transition doit être progressive. |
| Q7 | **b** — Les poids semblent corrects à l'œil mais seul le mouvement montre les défauts (racine qui bouge, coude déchiré) | Le correcteur plie de 90° et mesure déplacement de la racine, solidarité du bout et allongement des arêtes. |
| Q8 | — | Les noms des groupes upper et fore sont inversés : la racine suit l'avant-bras et inversement (430 mm d'erreur) bien que les poids existent. |
| Q9 | — | La somme mesurée valait 0,978 par endroits : Weights > Normalize All (`vertex_group_normalize_all`) ramène la somme à 1. |
| Q10 | — | Weight Paint : brosse Smooth/Blur sur la zone du coude pour étaler la transition entre upper et fore, puis Normalize All. |
<!-- QUIZ_ANSWERS_END -->

## Exercice 2
`COMPLETED_EXAMPLES/ch06_03_skinning_solution.blend` (+ `_reference.png`).

**Fabrication.** Générée par script (`build_ch06_03_files.py`) avec l'opérateur réel `parent_set(type='ARMATURE_AUTO')` puis `vertex_group_normalize_all`. Score du correcteur 34/34 ; starter 18/34.
Mesures : 0 sommet non pesé ; somme 1,00 ; 2 influences au plus ; racine 0,0 mm ; bout 0,0 mm ; étirement ×1,71.
Croquis regardé : poids rouge → bleu avec une transition étroite au coude ; pliage de 90° propre.

## Contre-épreuve du correcteur (`COMPLETED_EXAMPLES/COUNTER_EXAMPLES/`)
| Fichier faux | Défaut | Tests qui le refusent |
|---|---|---|
| `…_unweighted` | 64 sommets du bout sans poids | Sommets sans poids ; bout solidaire ; coude (×16,8) |
| `…_unnormalized` | poids divisés par 2 (somme 0,5) | Poids normalisés (seul) |
| `…_rigid` | poids binaires au coude | Coude lisse : ×4,30 (seul) |
| `…_swapped` | noms des groupes upper/fore inversés | Racine immobile ; bout solidaire |
| `…_too_many` | trois groupes « extra » à 0,01 (5 influences) | Groupes sans bone ; normalisation ; 5 influences |
| `…_no_modifier` | modificateur Armature supprimé | Modificateur Armature ; bout solidaire |
Aussi refusé : le starter.

## Limites
- Un seul pliage de 90° autour de Z ; deux bones.
- Le coude « lisse » est jugé par l'allongement d'arête, pas par le volume.
