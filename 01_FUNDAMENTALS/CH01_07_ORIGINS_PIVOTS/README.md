# CH01.07 — Origines, pivots, curseur 3D

**Phase :** 1 — Fondamentaux absolus  
**Niveau :** débutant  
**Durée estimée :** 1 h 30  
**Version :** Blender 5.3.0

## Introduction

Une porte dont l'origine est au milieu ne s'ouvrira jamais correctement : elle tournera sur elle-même comme une girouette. Ce chapitre explique l'origine d'un objet (le point autour duquel il tourne et se met à l'échelle), comment la déplacer sans bouger la géométrie, le curseur 3D comme outil de précision, et les points de pivot qui déterminent autour de quoi tourne une sélection. Exercice : une porte à accrocher à sa charnière et des boulons à faire tourner autour d'une roue.

## Prérequis

- CH01.05 (Edit Mode, sélection de sommets).
- CH01.06 (snapping).

## Objectifs pédagogiques

À la fin du chapitre, vous saurez :
1. Comprendre le rôle de l'origine et choisir son emplacement.
2. Déplacer l'origine (Set Origin, Affect Only Origins).
3. Placer et utiliser le curseur 3D (Shift+RMB, Shift+S).
4. Choisir le point de pivot adapté (Median, 3D Cursor, Individual Origins…).

## Compétences évaluées

| Code | Compétence | Validée par |
|---|---|---|
| C01.07.a | Contrôler origines, curseur et pivots | Exercice 3 (correcteur) |

## Plan du chapitre

| Leçon | Titre | Durée |
|---|---|---|
| L1 | Origines | 25 min |
| L2 | Curseur 3D | 20 min |
| L3 | Point de pivot | 25 min |

## Parcours conseillé

1. Lire [LESSON.md](LESSON.md) leçon par leçon ; chaque leçon renvoie vers [THEORY.md](THEORY.md) (comprendre) et [TUTORIAL.md](TUTORIAL.md) (reproduire).
2. Faire les exercices de [EXERCISES.md](EXERCISES.md) dans l'ordre : facile → moyen → difficile.
3. Répondre au [QUIZ.md](QUIZ.md), puis corriger avec [SOLUTIONS.md](SOLUTIONS.md).
4. En cas de blocage : [TROUBLESHOOTING.md](TROUBLESHOOTING.md). Sources : [RESOURCES.md](RESOURCES.md).
5. Mettre à jour [PROGRESS.md](../../PROGRESS.md).

## Fichiers du chapitre

| Fichier | Rôle |
|---|---|
| `STARTER_FILES/ch01_07_door_starter.blend` | Porte (origine au centre), roue et 3 boulons |
| `COMPLETED_EXAMPLES/ch01_07_door_solution.blend` | Porte sur charnière, ouverte ; boulons tournés autour de la roue |
| `SCRIPTS/validate_ch01_07.py` | Correcteur (15 points) |

## Correcteur automatique

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch01_07_door_<prenom>_v001.blend" `
  --python "SCRIPTS\validate_ch01_07.py" --python-exit-code 1 -- --exercise door
```

## Livrables attendus

1. ch01_07_door_<prenom>_v001.blend validé.
2. Mini-projet : trois mécanismes prêts à animer.

## Critères pour passer au chapitre suivant

- Quiz ≥ 8/10.
- Exercice difficile réussi sans tutoriel.
- Mini-projet ≥ 70/100.

➡️ Chapitre suivant : [CH01.08 — Collections et Outliner](../CH01_08_COLLECTIONS_OUTLINER/README.md)
