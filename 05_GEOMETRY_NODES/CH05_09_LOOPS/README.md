# CH05.09 — Boucles et simulation

**Phase :** 5 — Geometry Nodes  
**Niveau :** avancé  
**Durée estimée :** 5 h  
**Version :** Blender 5.3.0

## Introduction

Certaines constructions dépendent de l'étape précédente : un escalier en colimaçon, une fractale, une croissance. La zone de répétition (Repeat Zone) exécute un groupe de nœuds plusieurs fois en passant l'état d'une itération à la suivante. Ce chapitre construit un escalier en colimaçon marche par marche, avec quatre paramètres (nombre de marches, angle, hauteur, rayon). Le correcteur règle l'outil sur deux configurations et mesure les marches : nombre, contremarche, angle entre marches, rayon. Les zones Simulation et For Each sont présentées dans le cours mais ne sont pas évaluées par le correcteur.

## Prérequis

- CH05.06.

## Objectifs pédagogiques

À la fin du chapitre, vous saurez :
1. Construire une Repeat Zone : Iterations, état, Iteration.
2. Accumuler la géométrie d'une itération à l'autre avec Join Geometry.
3. Utiliser le numéro d'itération pour placer chaque élément.
4. Situer les zones Simulation et For Each Element par rapport à Repeat.

## Compétences évaluées

| Code | Compétence | Validée par |
|---|---|---|
| C05.09.a | Utiliser une zone | Exercice 2 (correcteur) + rendu des deux réglages |

## Plan du chapitre

| Leçon | Titre | Durée |
|---|---|---|
| L1 | La zone de répétition | 2 h 30 |
| L2 | Un escalier paramétrique ; Simulation et For Each | 2 h 30 |

## Parcours conseillé

1. Lire [LESSON.md](LESSON.md) leçon par leçon ; chaque leçon renvoie vers [THEORY.md](THEORY.md) (comprendre) et [TUTORIAL.md](TUTORIAL.md) (reproduire).
2. Faire les exercices de [EXERCISES.md](EXERCISES.md) dans l'ordre : facile → moyen → difficile.
3. Répondre au [QUIZ.md](QUIZ.md), puis corriger avec [SOLUTIONS.md](SOLUTIONS.md).
4. En cas de blocage : [TROUBLESHOOTING.md](TROUBLESHOOTING.md). Sources : [RESOURCES.md](RESOURCES.md).
5. Mettre à jour [PROGRESS.md](../../PROGRESS.md).

## Fichiers du chapitre

| Fichier | Rôle |
|---|---|
| `STARTER_FILES/ch05_09_loops_starter.blend` | Une seule marche, sans zone ni interface |
| `COMPLETED_EXAMPLES/ch05_09_loops_solution.blend` | Outil « Escalier en colimaçon » |
| `COMPLETED_EXAMPLES/ch05_09_loops_reference.png` | Deux réglages (bas : défaut ; haut : 30 marches, 15°, 0,12 m, rayon 2 m) |
| `COMPLETED_EXAMPLES/COUNTER_EXAMPLES/` | Fichiers FAUX volontaires (nombre d'itérations fixe, sans rotation, sans montée, sans accumulation, rayon codé en dur) |
| `SCRIPTS/validate_ch05_09.py` | Correcteur (loops) |

## Correcteur automatique

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch05_09_loops_starter_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch05_09.py" -- --exercise loops --render
```

## Livrables attendus

1. Escalier en colimaçon validé.
2. Auto-évaluation ≥ 7/10.

## Critères pour passer au chapitre suivant

- Quiz ≥ 8/10.
- Exercice 2 validé.

➡️ Chapitre suivant : [CH05.10 — Optimisation et outils](../CH05_10_TOOLS/README.md)
