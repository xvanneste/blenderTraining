# CH05.03 — Instances

**Phase :** 5 — Geometry Nodes  
**Niveau :** intermédiaire  
**Durée estimée :** 5 h  
**Version :** Blender 5.3.0

## Introduction

Une instance est une copie d'une même géométrie placée en un point : elle ne duplique pas les sommets, d'où des milliers de copies à bas coût. Ce chapitre disperse 441 piquets sur une grille avec Instance on Points, en variant la rotation et l'échelle de chacun par des Random Value. Le correcteur énumère les instances réellement évaluées (nombre, emprise, échelles, orientations, base à z = 0, matériau) et vérifie que l'arbre n'a pas réalisé les instances.

## Prérequis

- CH05.01–02.

## Objectifs pédagogiques

À la fin du chapitre, vous saurez :
1. Distinguer instance et copie réalisée.
2. Utiliser Instance on Points (Points, Instance, Rotation, Scale).
3. Varier chaque instance avec Random Value.
4. Savoir quand réaliser les instances, et pourquoi l'éviter ici.

## Compétences évaluées

| Code | Compétence | Validée par |
|---|---|---|
| C05.03.a | Disperser des instances | Exercice 2 (correcteur) + rendu regardé |

## Plan du chapitre

| Leçon | Titre | Durée |
|---|---|---|
| L1 | Instance on Points | 2 h 30 |
| L2 | Variation, coût et Realize Instances | 2 h 30 |

## Parcours conseillé

1. Lire [LESSON.md](LESSON.md) leçon par leçon ; chaque leçon renvoie vers [THEORY.md](THEORY.md) (comprendre) et [TUTORIAL.md](TUTORIAL.md) (reproduire).
2. Faire les exercices de [EXERCISES.md](EXERCISES.md) dans l'ordre : facile → moyen → difficile.
3. Répondre au [QUIZ.md](QUIZ.md), puis corriger avec [SOLUTIONS.md](SOLUTIONS.md).
4. En cas de blocage : [TROUBLESHOOTING.md](TROUBLESHOOTING.md). Sources : [RESOURCES.md](RESOURCES.md).
5. Mettre à jour [PROGRESS.md](../../PROGRESS.md).

## Fichiers du chapitre

| Fichier | Rôle |
|---|---|
| `STARTER_FILES/ch05_03_instances_starter.blend` | Arbre avec le seul piquet |
| `COMPLETED_EXAMPLES/ch05_03_instances_solution.blend` | 441 piquets instanciés |
| `COMPLETED_EXAMPLES/ch05_03_instances_reference.png` | Deux vues |
| `COMPLETED_EXAMPLES/COUNTER_EXAMPLES/` | Fichiers FAUX volontaires (réalisé, sans aléa, enfoncé, trop clairsemé, trop dense, sans matériau) |
| `SCRIPTS/validate_ch05_03.py` | Correcteur (instances) |

## Correcteur automatique

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch05_03_instances_starter_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch05_03.py" -- --exercise instances --render
```

## Livrables attendus

1. Champ d'instances validé.
2. Auto-évaluation ≥ 7/10.

## Critères pour passer au chapitre suivant

- Quiz ≥ 8/10.
- Exercice 2 validé.

➡️ Chapitre suivant : [CH05.04 — Distribution](../CH05_04_DISTRIBUTION/README.md)
