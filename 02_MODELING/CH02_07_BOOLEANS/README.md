# CH02.07 — Booléens et non destructif

**Phase :** 2 — Modélisation professionnelle  
**Niveau :** intermédiaire  
**Durée estimée :** 2 h 15  
**Version :** Blender 5.3.0

## Introduction

Percer, découper, fusionner des volumes sans jamais perdre la possibilité de revenir en arrière : c'est le travail non destructif avec le modificateur Boolean. Ce chapitre apprend à ranger les cutters dans une collection, à les rendre invisibles au rendu, à ordonner la pile de modificateurs (Boolean puis Bevel) et à juger quand une topologie booléenne est acceptable.

## Prérequis

- CH02.05 (Bevel modificateur)
- CH01.08 (collections, parentage).

## Objectifs pédagogiques

À la fin du chapitre, vous saurez :
1. Utiliser Boolean (Difference, Union, Intersect) et choisir un solver.
2. Organiser des cutters en collection, invisibles au rendu.
3. Ordonner la pile de modificateurs.
4. Savoir quand appliquer et quand retopologiser.

## Compétences évaluées

| Code | Compétence | Validée par |
|---|---|---|
| C02.07.a | Workflow non destructif | Exercice 3 (correcteur + grille) |

## Plan du chapitre

| Leçon | Titre | Durée |
|---|---|---|
| L1 | Le modificateur Boolean | 45 min |
| L2 | Organisation non destructive | 45 min |
| L3 | Ordre de la pile et topologie | 45 min |

## Parcours conseillé

1. Lire [LESSON.md](LESSON.md) leçon par leçon ; chaque leçon renvoie vers [THEORY.md](THEORY.md) (comprendre) et [TUTORIAL.md](TUTORIAL.md) (reproduire).
2. Faire les exercices de [EXERCISES.md](EXERCISES.md) dans l'ordre : facile → moyen → difficile.
3. Répondre au [QUIZ.md](QUIZ.md), puis corriger avec [SOLUTIONS.md](SOLUTIONS.md).
4. En cas de blocage : [TROUBLESHOOTING.md](TROUBLESHOOTING.md). Sources : [RESOURCES.md](RESOURCES.md).
5. Mettre à jour [PROGRESS.md](../../PROGRESS.md).

## Fichiers du chapitre

| Fichier | Rôle |
|---|---|
| `STARTER_FILES/ch02_07_plate_starter.blend` | Platine 60 × 40 × 3 cm |
| `COMPLETED_EXAMPLES/ch02_07_plate_solution.blend` | Platine percée non destructive |
| `COMPLETED_EXAMPLES/ch02_07_plate_reference.png` | Rendu de référence |
| `COMPLETED_EXAMPLES/ch02_07_plate_moved.png` | Même fichier, cutter déplacé |
| `SCRIPTS/validate_ch02_07.py` | Correcteur (cutters, pile, trous traversants par Euler) |

## Correcteur automatique

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch02_07_plate_<prenom>_v001.blend" `
  --python "SCRIPTS\validate_ch02_07.py" --python-exit-code 1 -- --exercise plate --render
```

## Livrables attendus

1. Platine validée.
2. Auto-évaluation ≥ 14/20.
3. Mini-projet : la grille d'aération.

## Critères pour passer au chapitre suivant

- Quiz ≥ 8/10.
- Platine validée.
- Auto-évaluation ≥ 14/20.

➡️ Chapitre suivant : [CH02.08 — Modélisation organique](../CH02_08_ORGANIC/README.md)
