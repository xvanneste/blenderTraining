# CH07.15 — Scène dialoguée

**Phase :** 7 — Animation 3D  
**Niveau :** expert  
**Durée estimée :** 10 h  
**Version :** Blender 5.3.0

## Introduction

Une scène dialoguée se construit par étapes : le BLOCKING (les poses clés qui racontent la scène, en interpolation Constant pour juger les poses sans les mouvements), le SPLINING (on passe en courbes lisses et on ajoute des breakdowns), puis le POLISH (overlap, détails). Ce chapitre applique la méthode au regard d'un personnage dans une conversation à trois (A à gauche, B à droite, la caméra) : sept poses, trois breakdowns, des maintiens qui restent plats et des marqueurs qui jalonnent la scène. Le correcteur lit les deux actions (BLOCK et FINAL) et l'animation évaluée.

## Prérequis

- CH07.02–07.04 (clés, courbes), CH07.07 (posing), CH07.10 (acting).

## Objectifs pédagogiques

À la fin du chapitre, vous saurez :
1. Construire un blocking en poses clés (Constant).
2. Passer en splining sans perdre les poses.
3. Ajouter des breakdowns et garder les maintiens plats.
4. Baliser une scène par des marqueurs.

## Compétences évaluées

| Code | Compétence | Validée par |
|---|---|---|
| C07.15.a | Scène dialoguée | Exercice 2 (correcteur) + courbes de la solution |

## Plan du chapitre

| Leçon | Titre | Durée |
|---|---|---|
| L1 | Le blocking | 5 h |
| L2 | Splining et polish | 5 h |

## Parcours conseillé

1. Lire [LESSON.md](LESSON.md) leçon par leçon ; chaque leçon renvoie vers [THEORY.md](THEORY.md) (comprendre) et [TUTORIAL.md](TUTORIAL.md) (reproduire).
2. Faire les exercices de [EXERCISES.md](EXERCISES.md) dans l'ordre : facile → moyen → difficile.
3. Répondre au [QUIZ.md](QUIZ.md), puis corriger avec [SOLUTIONS.md](SOLUTIONS.md).
4. En cas de blocage : [TROUBLESHOOTING.md](TROUBLESHOOTING.md). Sources : [RESOURCES.md](RESOURCES.md).
5. Mettre à jour [PROGRESS.md](../../PROGRESS.md).

## Fichiers du chapitre

| Fichier | Rôle |
|---|---|
| `STARTER_FILES/ch07_15_dialogue_starter.blend` | Tête GEO_Head avec l'action BLOCK active (7 poses en Constant), sans FINAL ni marqueurs |
| `COMPLETED_EXAMPLES/ch07_15_dialogue_solution.blend` | BLOCK intacte, FINAL active (Bezier, 3 breakdowns), marqueurs beat_1 à beat_7 |
| `COMPLETED_EXAMPLES/ch07_15_dialogue_reference.png` | Blocking en escalier (gris) et splining (orange) : poses en blanc, breakdowns en vert |
| `COMPLETED_EXAMPLES/COUNTER_EXAMPLES/` | Fichiers FAUX volontaires (reste en Constant, sans breakdowns, pose modifiée, maintien cassé, sans marqueurs, mauvaise action active) |
| `SCRIPTS/validate_ch07_15.py` | Correcteur |

## Correcteur automatique

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch07_15_dialogue_starter_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch07_15.py" -- --exercise dialogue
```

## Livrables attendus

1. Scène en blocking puis splining validée.
2. Auto-évaluation ≥ 7/10.

## Critères pour passer au chapitre suivant

- Quiz ≥ 8/10.
- Exercice 2 validé.

➡️ Chapitre suivant : [Projet P7 — Scène animée](../PROJECT_P7/README.md)
