# CH07.01 — Les 12 principes

**Phase :** 7 — Animation 3D  
**Niveau :** intermédiaire  
**Durée estimée :** 6 h  
**Version :** Blender 5.3.0

## Introduction

Les douze principes de l'animation (formulés par les animateurs des studios Disney) sont la grammaire de tout mouvement crédible : squash & stretch, anticipation, mise en scène, pose à pose, chevauchement, ralentis, arcs, action secondaire, timing, exagération, volume du dessin, attrait. Ce chapitre les présente tous, puis en met deux à l'épreuve sur une balle qui saute : l'ÉCRASEMENT-ÉTIREMENT (à volume constant) et l'ANTICIPATION. Le correcteur lit l'animation image par image : contact au sol, volume, anticipation, étirement, sommet neutre, repos final.

## Prérequis

- CH01 (interface, objets), notions de keyframes (CH07.02 les approfondit).

## Objectifs pédagogiques

À la fin du chapitre, vous saurez :
1. Nommer et reconnaître les 12 principes.
2. Écraser et étirer à volume constant.
3. Placer une anticipation avant un mouvement.
4. Choisir le pivot pour qu'un volume se déforme depuis le sol.

## Compétences évaluées

| Code | Compétence | Validée par |
|---|---|---|
| C07.01.a | Identifier les principes | Quiz + exercice 2 (correcteur) |

## Plan du chapitre

| Leçon | Titre | Durée |
|---|---|---|
| L1 | Les douze principes | 3 h |
| L2 | La balle qui saute : squash, stretch, anticipation | 3 h |

## Parcours conseillé

1. Lire [LESSON.md](LESSON.md) leçon par leçon ; chaque leçon renvoie vers [THEORY.md](THEORY.md) (comprendre) et [TUTORIAL.md](TUTORIAL.md) (reproduire).
2. Faire les exercices de [EXERCISES.md](EXERCISES.md) dans l'ordre : facile → moyen → difficile.
3. Répondre au [QUIZ.md](QUIZ.md), puis corriger avec [SOLUTIONS.md](SOLUTIONS.md).
4. En cas de blocage : [TROUBLESHOOTING.md](TROUBLESHOOTING.md). Sources : [RESOURCES.md](RESOURCES.md).
5. Mettre à jour [PROGRESS.md](../../PROGRESS.md).

## Fichiers du chapitre

| Fichier | Rôle |
|---|---|
| `STARTER_FILES/ch07_01_principles_starter.blend` | Balle qui saute (position animée), sans déformation |
| `COMPLETED_EXAMPLES/ch07_01_principles_solution.blend` | Balle avec anticipation, étirement et écrasement |
| `COMPLETED_EXAMPLES/ch07_01_principles_reference.png` | Neuf images du saut en silhouette (orange : écrasée, vert : étirée) |
| `COMPLETED_EXAMPLES/COUNTER_EXAMPLES/` | Fichiers FAUX volontaires (sans déformation, sans anticipation, sans étirement, volume cassé, pivot au centre, sans repos final) |
| `SCRIPTS/validate_ch07_01.py` | Correcteur (principles) |

## Correcteur automatique

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch07_01_principles_starter_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch07_01.py" -- --exercise principles
```

## Livrables attendus

1. Saut de balle validé.
2. Fiche des 12 principes (une phrase chacun).
3. Auto-évaluation ≥ 7/10.

## Critères pour passer au chapitre suivant

- Quiz ≥ 8/10.
- Exercice 2 validé.

➡️ Chapitre suivant : [CH07.02 — Keyframes et timeline](../CH07_02_KEYFRAMES/README.md)
